# Sensor Node PCB

Design and production files of the LoRaWAN sensor node, internally called *LoRa Pinze Sent*, V1.1.

| Folder / file | Contents |
| ------------- | -------- |
| `KiCad project/` | KiCad 10 project (`LoRa Pinze Sent.kicad_pro`), hierarchical schematic and 6-layer layout |
| `LoRa pinze Sent V1.1 schematic.pdf` | PDF schematic |
| `Gerber production files/` | `GERBER-LoRa Pinze Sent.zip`, `BOM-LoRa Pinze Sent.csv`, `CPL-LoRa Pinze Sent.csv` |

## Architecture

<!-- TODO: add the block diagram (Fig. 1 of the MetroAgriFor 2026 paper) to Images/ and reference it here. -->

| Block | Main parts | Function |
| ----- | ---------- | -------- |
| MCU + radio | RAK3172-SiP (STM32WLE5JC + SX126x) | Acquisition, processing, LoRaWAN. RF output on U.FL (J4) through a matching network |
| Energy harvesting | TI BQ25570, L4/L5 | MPPT solar charger for the Li-ion battery and 3.3 V buck output. Battery-OK thresholds ≈ 3.32 V / 3.60 V; the buck is turned off below the lower one to prevent deep discharge. Max. battery voltage ≈ 4.23 V |
| RTC backup | VL-1220 rechargeable coin cell (BT1), JP4 | Keeps the RTC (VBAT pin) running |
| Fruit gauge supply | TPS61322 (5 V boost), TPS22917 load switches (one per gauge, plus stage switches) | 5 V is generated only during readings, then switched to each gauge on its own |
| Gauge power control | TCA9534 I²C expander (address 0x20) | Drives the 8 per-gauge load switches. Its pins default to inputs at power-on, so all gauges start off |
| Gauge inputs | 2 × SN74HCS151 8:1 mux, 12k/22k dividers, BAV199 | One mux for the SENT lines, one for the temperature lines. The 5 V signals are divided down to ≈ 3.2 V and clamped |
| Analog inputs | TMUX1204 4:1 mux, TPS22917, BAV199, 10 Ω | 4 × 0–3.3 V inputs with a switched 3.3 V sensor supply |
| Battery sensing | TPS22917 + 200k/200k divider + RC filter | Divider connected only during the measurement (wait > 5 τ before sampling) |
| USB / configuration | USB-C (GT-USB-7055BB), USBLC6-2 ESD, CH340E, NCP115 LDO, TMUX1219 ×3 | USB-to-UART bridge powered from USB. The analog switches isolate the UART/RTS lines when USB is not connected, to avoid leakage |
| User interface | LED1 (PB11), LED2 (USB), USER button B1 (PA7), RESET button B2 | |

## Connectors

| Ref | Type | Pinout |
| --- | ---- | ------ |
| J9–J16 | Molex PicoBlade 53398-0471 (4-pin) — fruit gauges 1–8 | 1 GND · 2 Temperature · 3 SENT · 4 +5 V switched |
| J5–J8 | Molex PicoBlade 53398-0371 (3-pin) — analog inputs 4–1 | 1 +3.3 V switched · 2 Analog in · 3 GND |
| J2 | JST PH B2B-PH-K-S — battery | 1 +VBAT · 2 GND |
| J3 | 2-pin — solar panel | 1 +Solar · 2 GND |
| J17 | USB-C | Configuration (CH340E) |
| CN1 | 6-pin — SWD | 1 VDD · 2 SWCLK · 3 GND · 4 SWDIO · 5 NRST · 6 NC |
| J1 | 3-pin — debug UART | 1 RX (PA3) · 2 TX (PA2) · 3 GND |
| J4 | U.FL | LoRa antenna |

Channel mapping: gauge *n* (1–8) → J(8+*n*); analog input 1 → J8, 2 → J7, 3 → J6, 4 → J5.

## MCU pin assignment

| Pin | Net | Function |
| --- | --- | -------- |
| PB8 | `SENTInput` | SENT input (from SENT mux) |
| PB9 | `TempDgitalOutput` | LMT01 pulse input (from temperature mux) |
| PC0 / PC1 / PC2 | `CTRLA/B/C` | Gauge mux select |
| PA10 | `PinzeOn` | Gauge stage power enable |
| PB14 | `BoostOnPinze` | 5 V boost enable |
| PA11 / PA12 | `I2C1_SDA` / `I2C1_SCL` | TCA9534 expander |
| PB1 | `AnalogIN` | ADC input (from analog mux) |
| PA8 / PA9 | `AnSel0` / `AnSel1` | Analog mux select |
| PB2 | `AnalogPowerIN` | Analog sensor supply enable |
| PB12 | `VStorageReadActivate` | Battery divider enable |
| PB13 | `VStorageSensing` | Battery voltage ADC input |
| PA2 / PA3 | `USART2_TX` / `USART2_RX` | Configuration / debug UART |
| PA5 / PA6 | `CTS#` / `RTS#` | CH340E handshake (RTS wakes the MCU) |
| PA7 | `BlueButton` | USER button |
| PB11 | `indicatore` | Status LED |
| PA13 / PA14 | `SWDIO` / `SWCLK` | Debug |

## Schematic sheets

| Sheet | File |
| ----- | ---- |
| Top level (MCU, connectors, buttons, LEDs) | `LoRa Pinze Sent.kicad_sch` |
| Energy harvesting (BQ25570) | `untitled.kicad_sch` (`power_supply1`) |
| Battery sensing | `Avoir.kicad_sch` |
| Gauge supply and I²C expander | `AlimentazionePinze.kicad_sch` → `SwitchPowerPinze.kicad_sc.kicad_sch` (×8) |
| Gauge input muxes | `DigitalInputMux.kicad_sch` → `DigitalInput.kicad_sch` (×8) |
| Analog inputs | `InputAnalogico.kicad_sch` |
| USB–UART | `USB_Uart.kicad_sch` |
| Antenna and matching network | `antennas.kicad_sch` |

## Manufacturing

Upload `GERBER-LoRa Pinze Sent.zip` to the PCB manufacturer (6 layers, 1.6 mm), then use the BOM and CPL files for assembly. Through-hole and mechanical parts that the assembler does not mount (battery/solar/coin-cell connectors, headers) are soldered by hand.

About €25 per node for a batch of 20.
