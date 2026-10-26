# Agro LoRa Inductive Fruit Gauge

An open-source, low-cost and low-power LoRaWAN sensor node for continuous, non-destructive monitoring of fruit growth directly on the tree, together with the high-resolution inductive fruit gauges (*pliers*) it reads.

<img width="1254" height="1216" alt="Agro LoRa Inductive Fruit Gauge" src="https://github.com/user-attachments/assets/f9fefbf2-a46f-4367-93ff-209f6adea2f6" />

## Overview

Fruits shrink and swell every day following the plant's water balance. Tracking these sub-millimetre variations makes it possible to detect water stress, to time irrigation and to follow fruit development during the season. This needs sensors that are accurate, cheap enough to be deployed in large numbers, and able to run for months without anybody touching them.

The system has two parts:

| Part | What it does |
| ---- | ------------ |
| **Inductive fruit gauge** (plier) | A two-arm caliper built from FR4 PCBs. A contactless inductive angle sensor (Microchip LX3302A) measures the opening angle of the arms, from which the fruit diameter is computed. An on-board LMT01 sensor measures the plier temperature for thermal compensation. Data are sent digitally over the automotive **SENT** protocol. |
| **Sensor node** | A LoRaWAN hub based on the RAKwireless RAK3172-SiP (STM32WLE5JC). It powers and reads up to **8 fruit gauges** and **4 analog sensors**, applies calibration and thermal compensation locally, and sends the results over LoRaWAN. It runs from a Li-ion battery recharged by a small solar panel. |

To the best of the authors' knowledge, this is the first sensor node to bring the SENT protocol into agricultural applications, so that low-cost automotive sensors can be used in the orchard.

## Key specifications

**Fruit gauge**

| Parameter | Value |
| --------- | ----- |
| Sensing principle | Inductive angular sensing (planar coils on FR4 + copper target), Microchip LX3302A |
| Measurement range | up to 120 mm fruit diameter |
| Nominal resolution | 71 µm (1 LSB) |
| Accuracy after calibration | mean absolute error 111 µm, maximum error < 247 µm (cubic-spline calibration, 33 points) |
| Temperature sensor | Texas Instruments LMT01 (pulse-count output) |
| Output | SENT (tick = 24 µs) + temperature pulse train |
| Supply | 5 V, switched on by the node only during the reading |
| Weight | about 81 g |
| Structure | FR4 PCBs used as both circuit and mechanical frame, PTFE spacers, 3D-printed PETG clips |

**Sensor node**

| Parameter | Value |
| --------- | ----- |
| MCU / radio | RAK3172-SiP: STM32WLE5JC (Arm Cortex-M4, 48 MHz, 256 kB Flash, 64 kB RAM) + SX126x-class LoRa radio |
| Network | LoRaWAN, EU868, ABP activation, application port 2 |
| Fruit gauge inputs | 8 (4-pin Molex PicoBlade), individually powered |
| Analog inputs | 4 × 0–3.3 V (3-pin Molex PicoBlade), with a switched 3.3 V supply |
| Energy harvesting | TI BQ25570 with MPPT for a photovoltaic cell, Li-ion battery, 3.3 V buck output |
| Configuration | USB-C (CH340E USB–UART bridge) and the desktop app in [`Configuring software`](Configuring%20software) |
| PCB | 6-layer, 1.6 mm |
| Cost | about €25 per node (€24.92 for a batch of 20) |
| Battery life without sun | 1440 h (60 days) with 4 gauges, 1156 h (48 days) with 8 gauges, 800 mAh battery, 300 s interval; up to 2602 h (108 days) with the battery-aware sampling interval |

## How it works

1. **Wake-up.** The RTC wakes the MCU from Stop 2 mode at the end of each acquisition interval.
2. **Fruit gauge readings.** The node turns on the 5 V boost converter, then powers one gauge at a time through its load switch. For each gauge it averages a configurable number of SENT frames and reads the LMT01 temperature. SENT and temperature lines are selected with two 8:1 multiplexers and decoded in firmware with timer input capture, since the MCU has no SENT peripheral.
3. **Analog readings.** The analog sensors' 3.3 V supply is turned on. After a configurable pre-sampling time, each enabled input is sampled and averaged by the 12-bit ADC.
4. **Computation.** Each raw reading is converted to an opening angle with a cubic-spline calibration. The diameter is then computed as `d = 2·L·sin(α/2)` and corrected for the thermal expansion of the FR4 arms and the PETG clips.
5. **Transmission.** A 26-byte LoRaWAN uplink is sent. The node then turns off every power stage and goes back to sleep.

When the battery voltage is low, the node increases its sampling interval to extend its lifetime (in firmware v1.0.0, up to 3× between 3.85 V and 3.65 V). Below 3.65 V it skips the readings.

More details, including the power budget of each phase, are given in the papers below and in the [`Firmware`](Firmware) documentation.

## Repository contents

| Folder / file | Contents |
| ------------- | -------- |
| [`building_instructions.md`](building_instructions.md) | **Step-by-step guide to build the system**: materials, PCB ordering, programming, mechanical assembly, wiring and first start-up. |
| [`Schematics and Gerbers`](Schematics%20and%20Gerbers) | KiCad projects, PDF schematics, Gerbers, BOM and pick-and-place files for the sensor node and the fruit gauge. |
| [`Firmware`](Firmware) | STM32CubeIDE project of the node, ready-to-flash `.hex`, LX3302A configuration file and ChirpStack payload decoder. |
| [`Configuring software`](Configuring%20software) | PyQt6 desktop app to configure the node over USB (Python sources and a Windows executable). |
| [`3d models`](3d%20models) | FreeCAD/STEP/STL models of the fruit gauge, 3D-printable clips and PTFE spacer geometries (STL/SVG/G-code). |
| [`Images`](Images) | Pictures used in the documentation. |

## Getting started

1. Read the [building instructions](building_instructions.md) and collect the parts.
2. Order the PCBs from the [`Schematics and Gerbers`](Schematics%20and%20Gerbers) folder.
3. Flash the node with the `.hex` file and program every LX3302A with `lx3302a_config.txt` (see [`Firmware`](Firmware)).
4. Assemble the fruit gauges and connect them to the node.
5. Set the LoRaWAN keys and the acquisition parameters with the [configuration software](Configuring%20software).
6. Add the [ChirpStack decoder](Firmware/Chirpstack_decoder.js) to your network server and install the node in the orchard.

## Publications

If you use this project in your research, please cite:

> L. M. Peppi, A. Gallo, L. Manfrini, and L. De Marchi,
> "Inductive Sensor for Real-Time, Autonomous and Non-Destructive Fruit Size and Growth Monitoring,"
> *2025 IEEE International Workshop on Metrology for Agriculture and Forestry (MetroAgriFor)*, pp. 29–34, 2025.
> [IEEE Xplore](https://ieeexplore.ieee.org/document/11512426) | [DOI: 10.1109/MetroAgriFor66923.2025.11512426](https://doi.org/10.1109/MetroAgriFor66923.2025.11512426)

This paper covers the design and metrological characterisation of the inductive fruit gauge: coil design, temperature behaviour, non-linearity calibration and thermal compensation.

> L. M. Peppi, L. Manfrini, and L. De Marchi,
> "An Open-Source, Low-Cost and Low-Power LoRaWAN Hub for SENT-Based Fruit Growth and Analog Plant Related Physiological Sensors,"
> *2026 IEEE International Workshop on Metrology for Agriculture and Forestry (MetroAgriFor)*, 2026.

This paper covers the sensor node: architecture, SENT decoding over long cables, operating modes and energy budget.

Earlier versions of the fruit gauge (potentiometer-based) are described in:

* L. M. Peppi *et al.*, "A low-cost and high-accuracy non-invasive system for the monitoring of fruit growth," *IEEE MetroAgriFor 2020*, pp. 18–23.
* L. M. Peppi *et al.*, "Low-cost, high-resolution and no-manning distributed sensing system for the continuous monitoring of fruit growth in precision farming," *Acta IMEKO*, vol. 12, no. 2, pp. 1–11, 2023.

## Authors

Developed at the University of Bologna by the [ISS Lab](https://github.com/ISS-Lab-Unibo) (DEI, ARCES) and the [ECOPOM](https://github.com/ECOPOM) group (DISTAL):

* Lorenzo Mistral Peppi — DEI, ARCES
* Alessandro Gallo — CIRI-MAM
* Luigi Manfrini — DISTAL, ARCES
* Luca De Marchi — DEI, ARCES

## Acknowledgements

This work was carried out within the Emilia-Romagna Regional Programme — European Regional Development Fund (ERDF/FESR) 2021–2027, Priority 1, Specific Objective 1.1, Action 1.1.2 — Call for Strategic Industrial Research Projects — Project *"Smart Specialized Sustainable Stonefruit Orchard"*.
