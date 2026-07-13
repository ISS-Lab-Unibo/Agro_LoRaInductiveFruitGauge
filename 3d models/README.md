# PLIERS PRODUCTION OVERVIEW and REQUIRED MATERIALS

This repository contains the design files, manufacturing files, and assembly references required for the gripper system and its integration with the pliers assembly.

## Folder Structure

### 1. `Grubber`
<img alt="immagine" src="https://github.com/ISS-Lab-Unibo/Agro_LoRaInductiveFruitGauge/blob/main/Images/Clippe.png" />
This folder contains:

* FreeCAD CAD files of the grubbers that must be attached to the pliers.
* Printable `.stl` files corresponding to the grubber components.

These files are intended for manufacturing and assembly of the gripping elements.

---

### 2. `Pliers cad files and renderings`

This folder is provided **for reference purposes only**.

It contains:

* STEP files of the various pliers subassemblies and components.
* A complete rendering of the assembled pliers.
* The full pliers assembly in both STEP and FreeCAD formats.

These files are supplied to facilitate understanding of the overall assembly and integration of the grubbers.

---

### 3. `Teflon Disks`

<img alt="immagine" src="https://github.com/ISS-Lab-Unibo/Agro_LoRaInductiveFruitGauge/blob/main/Images/Spacers.png" />

This folder contains:

* `.stl` files of the spacers/disks that must be manufactured in PTFE (Teflon).

These components are required during the assembly of the pliers.

---

# Manufactured Parts List 

| Item | Part Name | Manufacturing Process (3D Printing / Machining) | Material | Quantity | File name|
| ---- | --------- | ----------------------------------------------- | -------- | -------- | ----- |
|  1    | Grubbers          	| 3D printing          | PETG         | 2         |  clippa acciaio armonico-Body_v.02     |
|  2    |  Teflon spacer 1         | Machining           |  Teflon 1mm thicknes        |   2       |  Spessore_braccio.stl     |
|  3    |  Teflon spacer 2         | Machining           | Teflon 1mm thicknes         |  2        |  Spessore_centrale.stl     |

---

# Mechanical Hardware Bill of Materials (To Be Completed)

| Item | Description | Specification | Quantity | RS Code |
| ---- | ----------- | ------------- | -------- | ----- |
|  1    |   M2 bold          | 1) To connect the grubbers to the plier's structure 2) to fix one arm of the plier             |  3        |  560-271     |
|   2   |   M2 screw 8mm          |  To connect the grubbers to the plier's structure             |   2       |   908-7637    |
|   3   |  RS 751-770, 0.63 mm Diam., ext Diam. 7mm, length 35mm, maximum length 101.5mm, k = 0.16N/mm, initial force = 12.2N           |               |  2        |       |
|   4   |  M3 locknut           |               | 2         |       |
|   5   |  M5 screw          |               | 2         |       |
|   6   |  Self-tapping screw           |               | 2         |       |
---