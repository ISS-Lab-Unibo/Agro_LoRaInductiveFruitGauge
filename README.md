# Agro_LoRaInductiveFruitGaug


A low-power wireless sensor node designed for high-resolution, non-destructive fruit growth monitoring and LoRa/LoRaWAN data transmission.
<img width="1254" height="1216" alt="immagine" src="https://github.com/user-attachments/assets/f9fefbf2-a46f-4367-93ff-209f6adea2f6" />

##Overview

The Agro LoRa Inductive Fruit Gauge is an autonomous sensor node developed for continuous and non-destructive fruit growth monitoring directly on the tree.

The system interfaces with up to eight inductive fruit gauges attached to the monitored fruits, periodically acquiring fruit diameter measurements and transmitting the collected data through a LoRa/LoRaWAN wireless communication interface.

The inductive sensing technology adopted by the fruit gauges provides a nominal diameter resolution of up to 71 µm over a 120 mm measurement range. Following the proposed non-linearity calibration procedure, the sensing system achieves a mean absolute diameter error of 111 µm and a maximum absolute diameter error below 247 µm.


The design and metrological characterization of the inductive fruit gauge are presented in:

> L. M. Peppi, A. Gallo, L. Manfrini, and L. De Marchi,
> “Inductive Sensor for Real-Time, Autonomous and Non-Destructive Fruit Size and Growth Monitoring,”
> *2025 IEEE International Workshop on Metrology for Agriculture and Forestry (MetroAgriFor)*, pp. 29–34, 2025.
> [IEEE Xplore](https://ieeexplore.ieee.org/document/11512426) | [DOI: 10.1109/MetroAgriFor66923.2025.11512426](https://doi.org/10.1109/MetroAgriFor66923.2025.11512426)

The high measurement resolution enables the detection of small fruit diameter variations associated with daily shrinkage and swelling cycles, making the system suitable for long-term fruit growth monitoring and plant water-status assessment in Precision Agriculture applications.

The repository contains all the hardware design files, embedded firmware, configuration software, and mechanical models required to reproduce and configure the proposed sensor node.

## Building the Sensor Node

Complete instructions for manufacturing, assembling, programming, and configuring the sensor node are provided in the dedicated building guide:

 **[Sensor Node Building Instructions](building_instructions.md)**

The guide describes the complete procedure required to reproduce the system, from PCB manufacturing and component assembly to firmware programming, fruit gauge assembly, and final node configuration.

## Repository Contents

The repository is organised into the following directories:

### [`3d models`](3d%20models)

Contains the mechanical design files required to manufacture the sensor node enclosure and the mechanical components of the fruit gauges.

The directory includes STL files for 3D printing and the corresponding editable CAD source files.

### [`Configuring software`](Configuring%20software)

Contains the software developed to configure and manage the sensor node.

The configuration software allows the main node parameters, sensor acquisition settings, and LoRa/LoRaWAN communication parameters to be configured before field deployment.

### [`Firmware`](Firmware)

Contains the embedded firmware of the sensor node.

The firmware implements fruit gauge acquisition, analog sensor acquisition, system power management, battery monitoring, and LoRa/LoRaWAN communication.

### [`Schematics and Gerbers`](Schematics%20and%20Gerbers)

Contains the electronic design and PCB manufacturing files.

The directory includes the electrical schematics and Gerber files required to manufacture the sensor node PCB.

### [`Images`](Images)

Contains photographs, diagrams, and graphical resources used throughout the repository documentation.

## Documentation

Each main directory contains dedicated `.md` documentation files describing the purpose of the provided files, their organisation, and the procedures required to use, manufacture, configure, or modify the corresponding system components.

Users are encouraged to refer to the documentation available in each directory before modifying the hardware, firmware, software, or mechanical components.

For the complete sensor node reproduction procedure, refer to the **[Sensor Node Building Instructions](building_instructions.md)**.

## How It Works

The sensor node periodically acquires measurements from the connected inductive fruit gauges. Each gauge estimates the fruit diameter by measuring the angular position between its two arms using a contactless inductive sensing technique.

The acquired SENT digital signals are decoded by the sensor node and converted into calibrated fruit diameter measurements. The collected data are subsequently processed and transmitted through the LoRa/LoRaWAN communication interface.

The low-power architecture of the node is designed to support autonomous and long-term field operation.

## System Composition

The complete system consists of:

* a low-power LoRa/LoRaWAN sensor node;
* up to eight high-resolution inductive fruit gauges;
* interfaces for additional analog sensors;
* an energy harvesting and battery power supply system;
* dedicated embedded firmware;
* sensor node configuration software;
* custom mechanical components and enclosures.

Detailed information about each subsystem is available in the corresponding repository directory.


