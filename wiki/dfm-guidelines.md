---
title: "DFM for PCB: Design for Manufacturability Reference"
description: "PCB DFM rules for China manufacturing: trace spacing, via sizing, component clearances, stencil aperture ratios, fiducials, and test point layout."
canonical_url: "https://china-sourcing-agents.com/wiki/dfm-guidelines/"
---

# DFM for PCB: Design for Manufacturability Reference

> **Read the full guide**: [https://china-sourcing-agents.com/wiki/dfm-guidelines/](https://china-sourcing-agents.com/wiki/dfm-guidelines/)

PCB DFM rules for China manufacturing: trace spacing, via sizing, component clearances, stencil aperture ratios, fiducials, and test point layout.

---

Design for Manufacturability (DFM) is the practice of designing PCBs so they can be assembled with high yield, low defect rates, and at the lowest possible cost. DFM problems caught before Gerber release cost nothing to fix. The same problems caught after tooling is made cost $500–5,000. Problems discovered during production cost the equivalent of the defective units plus rework time plus schedule delay. Most Chinese PCB assembly factories will run a free DFM check — but their check is for machine capability, not design quality. Your engineer must run DFM before sending files for multilayer PCBs or complex assemblies. A pre-production factory audit is also an opportunity to validate that the factory's equipment and process capability match your DFM rules, and proper sourcing ensures you only shortlist factories whose process specs align with your design requirements.

DFM covers three domains: PCB fabrication (what the board shop can make), SMT assembly (what the pick-and-place and reflow process can handle reliably), and test (what the test fixtures can reach). A board that passes fabrication DFM can still fail SMT DFM if pad geometries are wrong, and a board that passes both can fail test DFM if there are no accessible test points. The rules below focus on the most common violations seen in China PCBA production.

Standard trace/space 0.10/0.10 mm is achievable at almost every Chinese PCB factory. Below 0.10 mm, the pool of capable factories shrinks, yield drops, and per-board cost rises. For inner layers on impedance-controlled boards, trace width controls impedance — get the factory to calculate final trace width from their actual Dk and prepreg thickness before you finalize the design.

---

## What this covers

- Overview
- Key Parameters
- Fabrication DFM
- SMT Assembly DFM
- Test Point DFM
- Panelization DFM
- What to Specify When Ordering from China
- Common Issues

---

## Further reading

- [PCB assembly](https://china-sourcing-agents.com/industries/pcb-assembly/)
- [multilayer PCBs](https://china-sourcing-agents.com/products/multilayer-pcb/)
- [factory audit](https://china-sourcing-agents.com/services/factory-audit/)
- [sourcing](https://china-sourcing-agents.com/services/sourcing/)
- [Full guide on China Sourcing Agent](https://china-sourcing-agents.com/wiki/dfm-guidelines/)

