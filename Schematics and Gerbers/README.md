# Schematics and Gerbers

Electronic design files of the system, made with KiCad.

| Folder | Board(s) |
| ------ | -------- |
| [`PCB sensor node`](PCB%20sensor%20node) | LoRaWAN sensor node (6-layer) |
| [`PCB pliers`](PCB%20pliers) | Inductive fruit gauge: sensing arm, second arm, target and spacer (2-layer) |

Each folder contains:

* the **KiCad project** (schematic + PCB layout), to view or modify the design;
* a **PDF schematic**, to read the design without KiCad;
* **Gerber production files**: Gerber/drill ZIP archives plus BOM and CPL (pick-and-place) files in JLCPCB format with LCSC part numbers, ready for a PCB assembly service.

The projects were saved with **KiCad 10**. Older versions cannot open them; use the PDF schematics instead.
