# Sensor Node Building Instructions

This document describes the main steps required to manufacture, program, and mechanically assemble the Agro LoRa Inductive Fruit Gauge sensor node and the associated inductive fruit gauges.

The procedure is organised into four main stages:

1. Required materials and tools
2. Sensor node PCB programming
3. Inductive fruit gauge programming
4. Mechanical assembly of the fruit gauges

---

# 1. Required Materials and Tools

Before starting the assembly procedure, all the electronic, mechanical, and programming components listed in the following table should be available.

| Category            | Item                                  | Description / Part Number                                                                                                                                     | Quantity          |
| ------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| PCB                 | Assembled sensor node PCB             | PCB manufactured from the Gerber files available in [`Schematics and Gerbers/PCB sensor node`](Schematics%20and%20Gerbers/PCB%20sensor%20node)                | 1                 |
| PCB                 | Inductive fruit gauge PCB             | PCB manufactured from the Gerber files available in [`Schematics and Gerbers/PCB pliers`](Schematics%20and%20Gerbers/PCB%20pliers). 1X GERBER-Braccio, 1X GERBER-Piste, 1X GERBER-spacer, 1x GERBER-TargetGrande.                            | 1 set per fruit gauge |
| 3D printed part     | Fruit gripping elements               | `clippa acciaio armonico-Body_v.02.stl`, available in [`3d models/Grubber`](3d%20models/Grubber)                                                              | 2 per fruit gauge |
| Mechanical material | PTFE sheet                            | 1 mm thick PTFE (Teflon) sheet. The sheet must be machined according to the geometries provided in the [`Teflon disks`](3d%20models/Teflon%20disks) directory | 2 set per fruit gauge           |
| Mechanical hardware | M2 nut                                | M2 nut used for the fruit gauge mechanical assembly. RS Code 908-7637                                                                                                           | 3 per fruit gauge |
| Mechanical hardware | M2 screw                              | M2 × 8 mm screw used to connect the gripping elements to the fruit gauge structure + . RS code  560-271                                                                           | 3 per fruit gauge |
| Mechanical hardware | M3 locknut                            | M3 locknut used for the fruit gauge mechanical assembly. RS Code 521-917                                                                                                       | 3 per fruit gauge |
| Mechanical hardware | M3 screw                              | M3 × 25 mm screw. RS code  560-271                                                                           | 3 per fruit gauge |
| Mechanical hardware | Self-tapping screw                    | Required to fix harmonic steel to grippers. RS code  287-4014                                                                          | 2 per fruit gauge |
| Mechanical hardware | Spring                                | RS 751-770, 0.63 mm Diam., ext Diam. 7mm, length 35mm, maximum length 101.5mm, k = 0.16N/mm, initial force = 12.2N                                                                                                                                                  | 2 per fruit gauge |
| Mechanical hardware | harmonic steel wire                       |  Diam harmonic steel wire                                                                                                                                                  | 4 per fruit gauge |
| Mechanical hardware | **TO BE COMPLETED**                   | **Additional central joint hardware / bearing specifications to be added**                                                                                    | **TBD**           |
| Enclosure           | **ENCLOSURE PART NUMBER TO BE ADDED** | Weather-resistant enclosure for the sensor node electronics                                                                                                   | 1                 |
| Battery           | Battery                |                                                                                        | 1 per sensor node |
| Connector           | Fruit gauge connector                 | Connector used to connect each inductive fruit gauge to the sensor node                                                                                       | 1 per fruit gauge |
| Cable               | UNITRONIC® LiYY                       | LAPP 0028304 cable used to connect the inductive fruit gauges to the sensor node                                                                              | As required       |
| Programmer          | LXM9518                               | Microchip programmer for the LX3302A inductive position sensor interface IC                                                                                   | 1                 |
| MCU programmer      | ST-LINK or SEGGER programmer          | SWD-compatible programmer for programming the sensor node MCU                                                                                                 | 1                 |
| Software            | STM32CubeProgrammer                   | ST software used to program the sensor node MCU                                                                                                               | —                 |
| Software            | IPCE                                  | Microchip Integrated Programming and Calibration Environment used with the LXM9518 programmer                                                                 | —                 |

The UNITRONIC® LiYY LAPP 0028304 cable is used for the electrical connection between each fruit gauge and the sensor node. Its PVC-based cable construction is suitable for the proposed outdoor installation and is adopted to improve the robustness of the sensor interconnection against environmental exposure, including sunlight and the associated UV radiation.

> **Note:** The exact sensor node enclosure part number must be added before finalising this document.
---

# 2. PCB Manufacturing

The system requires different PCB designs:

* the main sensor node PCB;
* the inductive fruit gauge PCB.

The corresponding manufacturing files are provided in the [`Schematics and Gerbers`](Schematics%20and%20Gerbers) directory.

## 2.1 Sensor Node PCB

The sensor node PCB manufacturing files are available in:

[`Schematics and Gerbers/PCB sensor node`](Schematics%20and%20Gerbers/PCB%20sensor%20node)

The `Gerber production files` directory contains the files required for PCB manufacturing and assembly

The provided production package includes the Gerber files and the associated BOM and component placement information required by an external PCB assembly service. Remember the assembly for the GERBER-LoRa Pinze Sent PCB. Bill of Materials and placement files are available in the same folder.

## 2.2 Inductive Fruit Gauge PCB

The fruit gauge PCB manufacturing files are available in:

[`Schematics and Gerbers/PCB pliers`](Schematics%20and%20Gerbers/PCB%20pliers): 
1X GERBER-Braccio, 1X GERBER-Piste, 1X GERBER-spacer, 1x GERBER-TargetGrande

The corresponding Gerber production files must be used to manufacture the PCB forming the main structural and sensing elements of the inductive fruit gauge.

The PCB integrates the inductive sensing coils and the LX3302A-based acquisition electronics. Remember the assembly for the GERBER-Piste PCB. Bill of Materials and placement files are available in the same folder.

---

# 3. Sensor Node MCU Programming

The sensor node MCU must be programmed before the final assembly of the system.

The recommended programming procedure uses STM32CubeProgrammer and an SWD-compatible programmer, such as an ST-LINK or a SEGGER programming probe.

## 3.1 Required Software

Download and install STM32CubeProgrammer from the official STMicroelectronics website.

The precompiled firmware binary provided in the [`Firmware`](Firmware) directory is the recommended firmware image for reproducing the sensor node.

The complete firmware source code is also available in the repository. Advanced users may download the source code, configure the development environment, and compile the firmware independently.

However, **building the firmware from source is not recommended for standard sensor node reproduction**, since compiler versions, library dependencies, and project configuration may affect the resulting firmware behaviour.

For this reason, the provided precompiled firmware image should normally be used.

## 3.2 Connecting the Programmer

Connect the ST-LINK or SEGGER programmer to the sensor node programming interface.

The sensor node programming connector pinout is reported in the following table. **Pin 1 is identified on the PCB by a white dot printed next to the connector.**

| Pin | Signal       | Description                                                                                                                                                                                              |
| --- | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `VDD_TARGET` | Target voltage sensing input. Used by the programming probe to measure the target voltage. This connection is optional and can normally be left disconnected when the sensor node is powered separately. |
| 2   | `SWCLK`      | Serial Wire Debug clock line.                                                                                                                                                                            |
| 3   | `GND`        | Ground reference.                                                                                                                                                                                        |
| 4   | `SWDIO`      | Serial Wire Debug bidirectional data line.                                                                                                                                                               |
| 5   | `NRST`       | MCU hardware reset line.                                                                                                                                                                                 |
| 6   | `NC`         | Not connected.                                                                                                                                                                                           |

> **Note:** Pin 1 (`VDD_TARGET`) is marked on the sensor node PCB by a **white dot**, which can be used as a reference to determine the programming connector orientation.


### Programming connection

![Logo di esempio](img/programming_port.png)

*Figure X. Connection of the programming probe to the sensor node PCB.*

## 3.3 Programming with STM32CubeProgrammer

The following procedure can be used to program the sensor node:

1. Connect the programming probe to the sensor node PCB.
2. Connect the programmer to the computer.
3. Open STM32CubeProgrammer.
4. Select `ST-LINK` as the programming interface when using an ST-LINK probe.
5. Configure the SWD connection.
6. Press **Connect**.
7. Verify that the target MCU is correctly detected.
8. Open the firmware programming section.
9. Select the precompiled firmware file provided in the repository.
10. Verify the firmware start address according to the supplied firmware image.
11. Start the programming procedure.
12. Wait for the programming and verification process to complete.
13. Disconnect STM32CubeProgrammer.
14. Remove the programming probe from the sensor node.

### STM32CubeProgrammer — Step 1

<!-- INSERT IMAGE: STM32CubeProgrammer connection configuration -->

![STM32CubeProgrammer connection](Images/CUBEPROGRAMMER_STEP_1_PLACEHOLDER.png)

*Figure X. STM32CubeProgrammer connection configuration.*

### STM32CubeProgrammer — Step 2

<!-- INSERT IMAGE: Firmware file selection -->

![STM32CubeProgrammer firmware selection](Images/CUBEPROGRAMMER_STEP_2_PLACEHOLDER.png)

*Figure X. Selection of the precompiled sensor node firmware.*

### STM32CubeProgrammer — Step 3

<!-- INSERT IMAGE: Programming and verification -->

![STM32CubeProgrammer programming](Images/CUBEPROGRAMMER_STEP_3_PLACEHOLDER.png)

*Figure X. Firmware programming and verification.*

After programming, disconnect the programming probe and power-cycle the sensor node.

---

# 4. LX3302A Programming

Each inductive fruit gauge integrates a Microchip LX3302A inductive position sensor interface IC.

Before the fruit gauge can be used, the LX3302A must be programmed with the appropriate sensor configuration.

Programming is performed using the Microchip LXM9518 programmer and the Integrated Programming and Calibration Environment (IPCE).

The LXM9518 programmer is described on the Microchip website:

[LXM9518 Programmer](https://www.microchip.com/en-us/development-tool/lxm9518)

## 4.1 Required Equipment

The following components are required:

* one LXM9518 programmer;
* the Microchip IPCE software;
* the inductive fruit gauge PCB;
* the appropriate programming cable or adapter.

## 4.2 Connecting the Fruit Gauge

During programming, the programming connector must be manually held against the programming contacts available on the fruit gauge PCB.

The connector must remain correctly positioned and in electrical contact with the PCB for the entire programming procedure.

The required connector position is shown in the following figures.

### Programming connector position

<!-- INSERT IMAGE: Programming connector held against the fruit gauge -->

![LX3302A programming connector](Images/LX3302A_PROGRAMMING_CONNECTION_PLACEHOLDER.png)

*Figure X. Programming connector manually held against the fruit gauge programming interface.*

### Detail of the programming contacts

<!-- INSERT IMAGE: Detail of programming pads -->

![LX3302A programming pads](Images/LX3302A_PROGRAMMING_PADS_PLACEHOLDER.png)

*Figure X. Detail of the LX3302A programming contacts.*

> **Important:** The programming connector must be kept firmly in position by hand throughout the programming procedure. An intermittent electrical contact may interrupt communication with the LX3302A.

A dedicated pogo-pin programming fixture is currently under development. This fixture will simplify the programming procedure and provide a more repeatable electrical connection to the fruit gauge programming pads.

## 4.3 Programming with IPCE

Connect the LXM9518 programmer to the computer and start the Microchip IPCE software.

The recommended programming procedure is:

1. Connect the LXM9518 programmer to the computer.
2. Open IPCE.
3. Position the programming connector on the fruit gauge programming contacts.
4. Keep the connector firmly pressed against the PCB.
5. Verify that the LX3302A is detected by IPCE.
6. Load the LX3302A configuration provided with this repository.
7. Verify the programmed sensor parameters.
8. Start the EEPROM programming procedure.
9. Wait until the programming process has completed.
10. Verify the programmed configuration.
11. Remove the programming connector from the fruit gauge.

### IPCE — Device connection

<!-- INSERT IMAGE: IPCE device detection -->

![IPCE device connection](Images/IPCE_STEP_1_PLACEHOLDER.png)

*Figure X. LX3302A detection using the IPCE software.*

### IPCE — Configuration loading

<!-- INSERT IMAGE: IPCE configuration loading -->

![IPCE configuration loading](Images/IPCE_STEP_2_PLACEHOLDER.png)

*Figure X. Loading the LX3302A configuration.*

### IPCE — EEPROM programming

<!-- INSERT IMAGE: LX3302A EEPROM programming -->

![IPCE programming](Images/IPCE_STEP_3_PLACEHOLDER.png)

*Figure X. Programming the LX3302A internal configuration memory.*

The LXM9518 and IPCE are specifically intended for configuration and calibration of Microchip inductive position sensor ICs. The LX3302A stores its digital calibration and configuration parameters in non-volatile EEPROM.

---

# 5. Fruit Gauge Mechanical Assembly

After the PCB has been manufactured and the LX3302A programmed, the mechanical components of the fruit gauge can be assembled.

The mechanical design files are available in the [`3d models`](3d%20models) directory.

## 5.1 Manufacturing the PTFE Spacers

The fruit gauge uses PTFE spacers to reduce friction between the moving PCB elements and allow smooth relative rotation of the two arms.

A **1 mm thick PTFE sheet** must be machined according to the geometries provided in the [`Teflon disks`](3d%20models/Teflon%20disks) directory.

The following spacer geometries are provided:

* `Spessore_braccio.stl/.svg`;
* `Spessore_centrale.stl/.svg`.

The STL or SVG files define the required external geometry of the PTFE components and can be used as a dimensional reference for machining or cutting the 1 mm PTFE sheet.

Two units of each spacer geometry are required for the complete fruit gauge assembly.

### PTFE spacer geometry


![PTFE spacer geometry](img/spacers.png)

*Figure X. PTFE spacer geometries manufactured from a 1 mm thick PTFE sheet.*

## 5.2 Manufacturing the Fruit Gripping Elements

Two fruit gripping elements must be manufactured for each fruit gauge.

The printable STL file is available in the [`Grubber`](3d%20models/Grubber) directory:

`clippa acciaio armonico-Body_v.02.stl`

The corresponding editable FreeCAD source file is also provided.

The gripping elements should be 3D printed in PETG.

![CLIPPE geometry](img/Clippe.png)

Two identical components are required for each fruit gauge.

Each fruit gripping element must be equipped with two spring steel wires. The two wires must pass through the dedicated holes provided inside each gripper and be secured in position using a self-tapping screw.

After installation, the spring steel wires must be bent to form a suitable gripping profile, allowing them to gently engage with the fruit surface and keep the fruit gauge correctly positioned during the monitoring period.

If required, the portions of the spring steel wires that come into contact with the fruit can be covered with heat-shrink tubing. This can provide a softer contact surface and reduce direct contact between the metal wires and the fruit skin.

<!-- INSERT IMAGE: Spring steel wire installation and bending -->

![Spring steel wire installation](Images/GRIPPER_SPRING_WIRE_PLACEHOLDER.png)

*Figure X. Installation, fastening, and bending of the spring steel wires inside the fruit gripping element.*


## 5.3 Mechanical Assembly

The different components must be assembled according to the exploded view shown below.

### Fruit gauge exploded view

<!-- INSERT IMAGE: Complete exploded view -->

![Fruit gauge exploded view](img/exploded.png)

*Figure X. Exploded view of the inductive fruit gauge assembly.*

The recommended assembly sequence is as follows:

1. Prepare the two fruit gauge PCB arms.
2. Position the PTFE spacers according to the exploded view.
3. Align the central rotation interfaces of the two PCB arms.
4. Install the central mechanical joint components.
5. Assemble the two PCB arms while ensuring free relative rotation.
6. Install the two PETG fruit gripping elements.
7. Fix each gripping element using the M2 × 8 mm screws and M2 nuts.
8. Verify the alignment of the two fruit gripping elements.
9. Manually open and close the fruit gauge.
10. Verify that the two arms rotate smoothly and without significant mechanical interference.

The PTFE components must remain correctly positioned between the moving surfaces during assembly.

After tightening the mechanical fasteners, verify that the fruit gauge can move freely throughout its operating range.

Excessive tightening of the central joint may increase friction and negatively affect the detection of small fruit diameter variations.

---

# 6. Final Assembly

Once the fruit gauges and the sensor node have been programmed and mechanically assembled, the system can be interconnected.

Connect each inductive fruit gauge to the sensor node using the UNITRONIC® LiYY LAPP 0028304 cable and the selected connectors.

Verify the cable wiring and connector pinout before connecting the fruit gauge to the sensor node.

### Fruit gauge cable connection

<!-- INSERT IMAGE: Cable connection between fruit gauge and sensor node -->

![Fruit gauge cable connection](Images/FRUIT_GAUGE_CABLE_CONNECTION_PLACEHOLDER.png)

*Figure X. Connection between an inductive fruit gauge and the sensor node.*

Install the sensor node PCB inside the selected **ENCLOSURE PART NUMBER TO BE ADDED** enclosure.

After completing the assembly, verify:

* sensor node power-up;
* communication with each connected fruit gauge;
* valid SENT data acquisition;
* LoRa/LoRaWAN configuration;
* wireless data transmission.

The sensor node can then be configured using the dedicated software provided in the [`Configuring software`](Configuring%20software) directory.
