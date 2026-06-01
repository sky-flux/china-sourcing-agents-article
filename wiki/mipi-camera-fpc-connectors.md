---
title: "MIPI CSI/DSI Camera & Display FPC Connectors"
description: "MIPI CSI-2 and DSI FPC connectors from China: pin counts, ZIF types, lane configs, signal integrity limits, and non-standard Chinese pinout risks."
canonical_url: "https://china-sourcing-agents.com/wiki/mipi-camera-fpc-connectors/"
---

# MIPI CSI/DSI Camera & Display FPC Connectors

> **Read the full guide**: [https://china-sourcing-agents.com/wiki/mipi-camera-fpc-connectors/](https://china-sourcing-agents.com/wiki/mipi-camera-fpc-connectors/)

MIPI CSI-2 and DSI FPC connectors from China: pin counts, ZIF types, lane configs, signal integrity limits, and non-standard Chinese pinout risks.

---

MIPI CSI-2 and DSI connectors are the most signal-integrity-sensitive FPC connectors you will encounter in Chinese-sourced camera and display modules. The connector itself is a commodity ZIF part, but the FPC routed through it carries differential signals at 1.5 Gbps or higher per lane — and the combination of non-standard Chinese module pinouts, variable FPC lengths, and inconsistent connector quality makes this category one of the highest-risk in embedded product development. A connector that measures fine on a bench will produce systematic image corruption at 1.5 Gbps if the FPC impedance deviates by 15% from 100 Ω differential. MIPI FPC connectors are critical components in consumer electronics products from cameras to display modules; professional inspection at the PCBA stage catches ZIF actuator failures and non-standard pinouts before they propagate through a production run.

MIPI (Mobile Industry Processor Interface) defines two serial interfaces relevant to camera and display connections. CSI-2 (Camera Serial Interface 2) connects image sensors or camera modules to an application processor. DSI (Display Serial Interface) connects an application processor to a display panel or LCD module. Both use the same physical layer (MIPI D-PHY or, in newer designs, C-PHY), the same differential pair topology, and the same FPC connector families.

The connector itself is a ZIF (Zero Insertion Force) surface-mount FPC connector: a housing with a flip-lock or back-flip actuator that clamps the FPC flex cable when closed. The connector does not define the signal integrity — the FPC cable does. But the connector must make reliable electrical contact at each of the differential pairs, and it must not degrade signal quality through impedance discontinuity at the insertion point. Generic connectors with plating defects or contact geometry deviations can add enough impedance variation to cause link training failures at the PHY layer.

---

## What this covers

- Overview
- Key Specifications
- Main Variants
- Sourcing from China: What to Look For
- Common Issues

---

## Further reading

- [consumer electronics](https://china-sourcing-agents.com/industries/consumer-electronics/)
- [inspection](https://china-sourcing-agents.com/services/inspection/)
- [IoT modules](https://china-sourcing-agents.com/industries/iot-modules/)
- [FPC & FFC Connectors](https://china-sourcing-agents.com/wiki/fpc-ffc-connectors/)
- [Full guide on China Sourcing Agent](https://china-sourcing-agents.com/wiki/mipi-camera-fpc-connectors/)

