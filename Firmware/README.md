# Firmware

This folder holds everything that runs on the hardware: the sensor node firmware, the LX3302A configuration for the fruit gauges and the payload decoder for the network server.

| File | Description |
| ---- | ----------- |
| `RAK3172_Ver_1.0.0_2026-06-02.hex` | Precompiled node firmware, v1.0.0. **Use this one to build a node.** |
| `STM32CubeIDE_Project/RAK3172_Ver_1.0.0_2026-06-02.zip` | Full STM32CubeIDE source project of the same version. |
| `lx3302a_config.txt` | EEPROM image for the LX3302A on each fruit gauge (32 × 16-bit words). |
| `Chirpstack_decoder.js` | Uplink decoder for ChirpStack. |

The file names follow the pattern `RAK3172_Ver_<version>_<build date>`.

## Flashing the node

Flash the `.hex` with STM32CubeProgrammer and an ST-LINK or J-Link through the SWD connector CN1. The full procedure and pinout are in [`building_instructions.md`](../building_instructions.md#3-sensor-node-firmware-programming).

## Programming the LX3302A

Write `lx3302a_config.txt` into each gauge's LX3302A with the Microchip LXM9518 programmer and the IPCE software. See [`building_instructions.md`](../building_instructions.md#4-lx3302a-programming).

## Firmware overview

Target: RAKwireless RAK3172-SiP (STM32WLE5JC, Cortex-M4 at 48 MHz, 256 kB Flash, 64 kB RAM), built on the STM32CubeWL LoRaWAN middleware.

| Setting | Value |
| ------- | ----- |
| LoRaWAN region | EU868 |
| Activation | ABP (keys set from the configuration software) |
| Application port | 2 |
| Data rate, ADR, TX interval | Set from the configuration software |
| SENT tick | 24 µs |
| Configuration UART | 115200 baud, through the on-board CH340E (USB-C) |
| Low-battery threshold | 3650 mV — below this, sensor readings are skipped |

### Operating modes

**Acquisition mode** runs a cycle every TX interval:

| # | Phase | What happens | Typical duration |
| - | ----- | ------------ | ---------------- |
| 1 | Start-up | RTC wakes the MCU from Stop 2 | 56 ms |
| 2 | Fruit gauge readings | 5 V boost on; each enabled gauge is powered on its own; SENT frames averaged; LMT01 temperature read | ≈ Σ (200 + 5.368 · ⌈samples/9⌉) ms |
| 3–4 | Analog readings | Analog supply on; for each enabled input, wait for the pre-sampling time, then average *R* samples | ≈ Σ (T_PS + 10.92 + 2.008 · R) ms |
| 5 | Computation | Spline calibration, thermal compensation, diameter | 25 ms |
| 6 | TX | 26-byte uplink | 1974 ms at DR0 |
| 7 | RX | LoRaWAN RX1/RX2 windows | 220 ms |
| 8 | Idle | All power stages off, Stop 2 | rest of the interval |

When the battery drops below 3.85 V (≈ 50 % charge), the firmware lengthens the TX interval by linear interpolation. The interval reaches 3× the configured value at 3.65 V (`MAX_VOLTAGE_THRESHOLD_BATTERY`, `MIN_VOLTAGE_THRESHOLD_BATTERY` and `FATTORE_MOLTIPLICATIVO_SAMPLING` in `Core/NodeConfig/LoRaNodeConfig.h`). The paper's 2602 h figure was measured with a factor of up to 5.

**Configuration mode** starts when the node is connected to the [configuration software](../Configuring%20software). The CH340E RTS line wakes the MCU, and the parameters can then be read and written over the serial link.

### Measured power consumption

N = 4 gauges, DR0, 10 SENT samples per gauge, 4 analog channels with 16 samples and 10 ms pre-sampling, 300 s interval, 4.03 V battery:

| Phase | Power [mW] | Energy [mJ] | Duration [s] |
| ----- | ---------- | ----------- | ------------ |
| 1 – Start | 39.15 | 2.193 | 0.056 |
| 2 – SENT readings | 126.4 | 156.832 | 1.241 |
| 3 – ADC pre-sampling | 40.6 | 1.623 | 0.040 |
| 4 – ADC readings | 42.96 | 7.733 | 0.180 |
| 5 – Computation | 18.3 | 0.457 | 0.025 |
| 6 – TX 26 B DR0 | 215 | 424.900 | 1.974 |
| 7 – RX | 22.1 | 4.865 | 0.220 |
| 8 – Idle | 0.00849 | 2.500 | 294.51 |

With an 800 mAh battery and no sun, this gives 1440 h (4 gauges) or 1156 h (8 gauges). With the battery-aware interval, it reaches 2602 h.

### Source code layout

| Path | Contents |
| ---- | -------- |
| `Core/` | Application, peripherals init, `NodeConfig/` (persistent node configuration) |
| `LoRaWan/App/` | LoRaWAN application (`lora_app.c/.h`: region, activation, payload) |
| `Drivers/tim2InputCapture/` | SENT and temperature decoding with TIM2 input capture |
| `Drivers/sel74hc151`, `Drivers/74hc151` | Gauge input multiplexers |
| `Drivers/TCA9634` | Driver for the TCA9534 I²C expander that switches the gauge power |
| `Drivers/TMUX1204`, `Drivers/ADC_if`, `Drivers/ADCGeneric` | Analog input multiplexer and ADC |
| `Drivers/BatterySensing` | Battery and RTC backup cell measurement |
| `Drivers/cubic_spline` | Cubic-spline non-linearity calibration |
| `Drivers/PinzeFunctions` | Gauge acquisition sequence, diameter computation, payload packing |
| `calibFiles/defaultPlierCalibData.h` | Default calibration table (raw SENT value → angle, 33 points) |

To build it, unzip the project, import it into STM32CubeIDE (*File → Import → Existing Projects into Workspace*) and build it. `RAK3172.ioc` is the STM32CubeMX configuration. `post_build_hex.py` generates the versioned `.hex` file after the build.

## Uplink payload

26 bytes, all fields `uint16` **little-endian**:

| Bytes | Field | Scaling (raw → value) |
| ----- | ----- | --------------------- |
| 0–15 | Fruit gauges 1–8 | raw / 100 |
| 16–23 | Analog inputs 1–4 | raw / 10 → mV |
| 24–25 | Battery voltage | raw / 10 → mV |

`Chirpstack_decoder.js` decodes this payload into the fields `pinza1`…`pinza8`, `analogico1`…`analogico4` and `battVoltage`.
