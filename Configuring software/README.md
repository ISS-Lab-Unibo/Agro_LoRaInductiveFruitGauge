# Configuring Software

`SetNodeParameter` is a desktop app (Python 3 + PyQt6) that configures the sensor node over its USB-C port. With it you can set the LoRaWAN parameters, the acquisition settings of every fruit gauge and analog input, and the RTC time, and you can run test readings before installing the node in the field.

## Folder contents

| Folder | Contents |
| ------ | -------- |
| `dist-windows-exe/` | Ready-to-run Windows executable (`SetNodeParameter.exe`) and the `ui/` folder it needs. No Python installation required. |
| `python files/` | Source code: `SetNodeParameter.py` (main app), `main_window.py` (generated UI), `Battery_Widget.py` (battery gauge widget), `ui/*.ui` (Qt Designer files), `*.qrc` / `risorse.py` / `immaginiLoghi.py` (embedded images). |

## Running it

### Windows executable

1. Download the whole `dist-windows-exe` folder. **Keep the `ui` folder next to the `.exe`.**
2. Run `SetNodeParameter.exe`.

### From source (Windows, Linux, macOS)

Requires Python ≥ 3.10.

```bash
pip install PyQt6 pyserial
```

```bash
cd "Configuring software/python files"
```

```bash
python SetNodeParameter.py
```

On Windows, the CH340 driver may need to be installed for the node's USB port to show up as a COM port.

## Using the software

1. Connect the node to the PC with a USB-C cable. The USB-to-UART bridge (CH340E) is powered from USB and wakes the MCU through its RTS line, which puts the node into **configuration mode**.
2. Press **Find Serial port**, choose the port, set the speed to **115200** and press **Serial Connect**.
3. Press **Read data** to load the current configuration: firmware version, LoRaWAN settings, RTC time, main battery and backup cell voltages.

### LoRaWAN parameters — *Change LoRa parameters*

The node uses **ABP** activation (EU868). Enter the values registered on your network server:

| Field | Size |
| ----- | ---- |
| Dev ADDR | 4 bytes |
| App. EUI | 8 bytes |
| Net. Session Key | 16 bytes |
| App. Session Key | 16 bytes |
| ADR Enable | on/off |
| DR | 0–5 |
| TX Interval | seconds between two acquisitions |

Use **Set time** to copy the PC time to the node RTC.

### Acquisition parameters — *Set node config.*

**Fruit gauges (8 channels):**

| Parameter | Description |
| --------- | ----------- |
| ON | Enables the channel |
| Samples | Number of SENT frames averaged per reading |
| Thermal compensation | Enables the thermal compensation for this gauge |
| Plier radius | Arm length *L* between the pivot and the clip fixing point |
| Clamp length | Length of the PETG clip, subtracted from the diameter |
| λ plier / λ clamp | Linear thermal expansion coefficients of the arm (FR4 ≈ 1.2·10⁻⁵ K⁻¹) and of the clip (PETG) |

**Analog inputs (4 channels):** enable, pre-sampling time (ms, settling time after the supply is switched on) and number of averaged samples.

The same window can trigger an **on-demand reading**. It shows, for each gauge, the raw value, the temperature and the computed diameter, and the voltage of each analog input. Use it to check the wiring before deployment.

Disconnect the USB cable when you are done. The node goes back to acquisition mode.

## Serial protocol (for developers)

The app talks to the firmware with a simple command/response protocol at 115200 baud. Before each command it sends a `0x00` byte and waits for the node to answer `0xAB`. Write commands are acknowledged with `0xAF`.

| Command | Direction | Payload |
| ------- | --------- | ------- |
| `0x01` | read | Firmware version (4 bytes) |
| `0x02` | read | LoRaWAN configuration (56 bytes: DR, DevAddr, AppEUI, NwkSKey, AppSKey, TX interval in ms, ADR) |
| `0x04` | read | Battery and backup cell voltages (2 × uint16, mV) |
| `0x05` | read | RTC timestamp (uint32, Unix time) |
| `0x10` / `0x11` | read / write | Fruit gauge parameters (8 × 20 bytes) |
| `0x12` / `0x13` | read / write | Analog input parameters (4 × 3 bytes) |
| `0x14` | read | Live readings (104 bytes: 8 raw + 8 temperatures + 8 diameters as float, 4 analog as uint16) |

See `SetNodeParameter.py` for the exact packing of each structure.

## Rebuilding the executable

The executable can be rebuilt with PyInstaller, for example:

```bash
pyinstaller --onefile --windowed SetNodeParameter.py
```

Then copy the `ui` folder next to the generated `.exe`.
