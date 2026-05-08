---
title: "I built a 11-language B2B site on Astro 6 + Cloudflare Workers — here's what surprised me"
published: true
description: "How I shipped china-sourcing-agents.com: fully static multilingual content, one dynamic edge endpoint, OG images with satori+resvg-wasm, and Pagefind search — with zero database."
tags: astro, cloudflare, webdev, javascript
cover_image: https://china-sourcing-agents.com/og.png?title=I%20built%20a%2011-language%20B2B%20site%20on%20Astro%206%20%2B%20Cloudflare%20Workers&description=Here%27s%20what%20surprised%20me
canonical_url: https://github.com/sky-flux/china-sourcing-agents-article/blob/main/devto/astro6-cloudflare-multilingual-sourcing-site.md
---

I recently shipped [china-sourcing-agents.com](https://china-sourcing-agents.com) — a B2B sourcing agency site for electronics and IoT hardware. It supports 11 languages, generates dynamic OG images at the edge, has full-text search with zero backend, and accepts leads through a form that emails me directly.

Total monthly infrastructure cost: **$0** (all within free tiers).

Here are the things that genuinely surprised me while building it.

---

## The stack

```
Astro 6          — framework
Cloudflare Pages — hosting (static assets + edge worker)
Tailwind CSS v4  — styling
MDX + Zod 4      — content collections
satori           — OG image text rendering
@resvg/resvg-wasm — SVG → PNG at the edge
Pagefind         — build-time full-text search index
Resend           — transactional email
Cloudflare Turnstile — bot protection
```

Almost entirely static. One dynamic endpoint: the RFQ (lead capture) form.

---

## Surprise #1: Astro 6 dev mode runs in workerd

This is the thing I was most skeptical about — and it's actually real.

Astro 6 (released March 2026) partnered with Cloudflare to run `astro dev` inside [workerd](https://github.com/cloudflare/workerd), the same JavaScript runtime as Cloudflare Workers. The practical consequence: if it works locally, it works in production. Edge runtime bugs in dev are gone.

Before this, I'd hit the classic problem: code that works in Node.js (`process.env`, `fs`, Node streams) silently breaks when deployed to Workers. Now the runtime is the same from the first `npm run dev`.

The config is minimal:

```js
// astro.config.mjs
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'server',
  adapter: cloudflare({ imageService: 'compile' }),
  // ...
});
```

---

## Surprise #2: 11 languages × 5 content types = one glob loader

The site supports en, de, fr, ja, ko, es, it, pt, nl, ru, pl. Each language has its own versions of guides, blog posts, case studies, services, and industries — ~250 MDX files total.

With Astro 6's Content Layer API, the entire multilingual structure is one collection definition per content type:

```ts
// src/content.config.ts
const guides = defineCollection({
  loader: glob({ pattern: '**/*.mdx', base: './src/content/guides' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date(),
    tags: z.array(z.string()),
  }),
});
```

The `en/how-to-source-from-china.mdx`, `de/how-to-source-from-china.mdx`, `ja/how-to-source-from-china.mdx` are all in the same `guides` collection. A helper function filters by language prefix:

```ts
export async function getLocalizedCollection(collection, locale) {
  const all = await getCollection(collection);
  return all
    .filter(entry => entry.id.startsWith(`${locale}/`))
    .map(entry => ({ ...entry, slug: entry.id.slice(locale.length + 1) }));
}
```

Strongly typed by Zod, available everywhere including server endpoints. No CMS, no database, no API calls — just files.

---

## Surprise #3: OG image generation at the edge is tricky, but solvable

Every page gets a dynamic OG image via `/og.png?title=...&description=...`. The endpoint runs on Cloudflare Workers using `satori` + `@resvg/resvg-wasm`.

The approach: satori converts a React-like element tree into an SVG where **all text is already rendered as `<path>` elements**. Then resvg-wasm converts that SVG to PNG. Since the text is paths, resvg never needs to look up a font — which matters because Cloudflare Workers has no system fonts.

```ts
// og.png.ts
const svg = await satori(element, { width: 1200, height: 630, fonts });
const resvg = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 } });
const png = resvg.render().asPng();
```

The font data (Geist Regular + SemiBold, ~25KB total as woff2) is fetched from the same Cloudflare CDN on first request and cached in the module scope — warm worker instances skip the fetch entirely.

**The thing that bit me**: the `.wasm` file. The 2.4MB resvg WASM binary can't be bundled into the Worker script — too large, and Vite's `.wasm` import handling is unreliable across different environments. The fix: serve `resvg.wasm` as a static asset from `public/`, and `fetch()` it at runtime.

```ts
// fetch-based WASM init — works in workerd, avoids bundling 2.4MB into the Worker
function ensureWasm(origin: string) {
  if (!wasmReady) {
    wasmReady = fetch(`${origin}/resvg.wasm`).then(r => initWasm(r));
  }
  return wasmReady;
}
```

A `prebuild` script in `package.json` keeps the WASM file in sync with the npm package version:

```json
"prebuild": "cp node_modules/@resvg/resvg-wasm/index_bg.wasm public/resvg.wasm"
```

---

## Surprise #4: SVG `stroke` silently fails in librsvg

While building the favicon, I ran into a fun one. I designed an IC chip icon (the logo mark for the site) using SVG `<line>` elements with `stroke="#E26B1F"`. In the browser: perfect. Rendered with ImageMagick (which uses librsvg): the lines disappeared completely, leaving just the `fill`-based dot.

This is a [known librsvg bug](https://gitlab.gnome.org/GNOME/librsvg/-/issues/) — stroke colors on `<line>` elements are silently dropped in certain rendering contexts.

The fix: replace every `stroke`-based element with `fill`-based rectangles:

```svg
<!-- Before: rendered invisible in librsvg -->
<line x1="5" y1="16" x2="13" y2="16" stroke="#E26B1F" stroke-width="2.5"/>

<!-- After: renders correctly everywhere -->
<rect x="5" y="14.75" width="8" height="2.5" fill="#E26B1F"/>
```

Rule I've adopted: **any SVG rendered outside the browser (OG images, favicons, server-side PNG generation) must use `fill` only, never `stroke`.**

---

## Surprise #5: Pagefind is genuinely good

Full-text search across all 11 languages, ~250 pages, with no backend and no Algolia bill.

Pagefind runs at build time, crawls the output HTML, and generates a binary index in `dist/client/pagefind/`. The client-side JS is ~15KB, loads the index lazily, and supports language-scoped queries.

```bash
npx pagefind --site dist/client
```

That's the entire integration. It works across all languages out of the box because it reads the `lang` attribute from each page's `<html>` tag.

The one sharp edge: Pagefind only indexes `prerender: true` pages (static HTML). Dynamic routes get no search entries. Fine for this use case — the RFQ form doesn't need to be searchable.

---

## Surprise #6: one dynamic endpoint, everything else static

The entire site is statically prerendered except for two endpoints:
- `POST /api/inquiries` — the RFQ form
- `GET /og.png` — dynamic OG images

With `output: 'server'`, every page needs an explicit `export const prerender = true`. I opted for a different approach: set each page's prerender flag explicitly and let `prerender = false` be the exception.

The RFQ endpoint is ~50 lines:

```ts
export const prerender = false;

export const POST: APIRoute = async ({ request, clientAddress }) => {
  const payload = InquirySchema.parse(await request.json());
  
  await verifyTurnstile(payload.turnstileToken, TURNSTILE_SECRET_KEY, clientAddress);
  
  const ref = crypto.randomUUID().slice(0, 8).toUpperCase();
  
  await Promise.allSettled([
    resend.emails.send({ /* sales notification */ }),
    resend.emails.send({ /* customer auto-reply */ }),
  ]);
  
  return Response.json({ ok: true, ref }, { status: 201 });
};
```

Three-layer spam protection: Zod schema validation (length limits, type checks), Cloudflare Turnstile (bot detection), honeypot hidden field. No database — leads go straight to email.

**Common mistake**: I initially had the RSS feed as `prerender = false`. It 500'd in production because `getCollection` can't run on the Workers runtime — the content store isn't available outside build time. Changed to `prerender = true`, fixed immediately.

```ts
// rss.xml.ts — must be prerendered; getCollection only works at build time
export const prerender = true;
```

---

## The result

- [china-sourcing-agents.com](https://china-sourcing-agents.com) — live site
- Lighthouse scores: Performance 97, SEO 100, Accessibility 96
- 11 languages, ~250 MDX content files
- First contentful paint < 0.8s (Cloudflare edge, static HTML)
- Monthly cost: $0

The Astro 6 + Cloudflare combination genuinely earns its reputation. The workerd dev parity alone saves hours of "works locally, breaks in prod" debugging. Pagefind is the unsung hero — full multilingual search with a single build command and zero ongoing cost.

---

Questions welcome in the comments.
