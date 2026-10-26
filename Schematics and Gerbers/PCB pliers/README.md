# Fruit Gauge (Pliers) PCBs

Design and production files of the inductive fruit gauge.

| Folder / file | Contents |
| ------------- | -------- |
| `Kicad project/` | KiCad 10 project `BraccioPisteMCU_stampa` (schematic + layout of all gauge boards) |
| `BraccioPisteMCU_stampa_schematic.pdf` | PDF schematic |
| `gerber production files/` | Gerbers, BOM and CPL of the four boards |

## Working principle

The gauge is a caliper with two arms joined at a pivot. A fruit held between the clips sets the opening angle α of the arms. The diameter is then:

```
d = 2 · L · sin(α / 2) − 2 · L_clip
```

where *L* is the arm length and *L_clip* the length of the PETG clips. Both lengths are corrected for thermal expansion using the on-board temperature sensor.

The angle is measured without any contact by an **inductive position sensor**. The sensing arm carries one transmitting coil and two receiving coils, printed on the PCB. The other arm carries a copper target. The TX coil, resonating at about 4.2 MHz, induces eddy currents in the target. The RX coils, laid out in phase opposition, pick up a signal whose envelope depends on the target position. The Microchip LX3302A drives the coils, demodulates the signal and outputs the position over **SENT**.

| Parameter | Value |
| --------- | ----- |
| Resolution | 71 µm (1 LSB, after averaging N = 40 at 2 kS/s) |
| Range | up to 120 mm |
| Accuracy (cubic-spline calibration, 33 points) | MAE 111 µm, max 247 µm |
| TX coils | L ≈ 2.06 / 2.47 µH, Q ≈ 17 / 15, tuned with 680 pF |
| Coil traces | 0.127 mm width, 0.15 mm clearance, inner radius 10 mm, outer diameter 28 mm |
| Target | 60° copper sector between Ø 9.8 mm and Ø 28 mm on both layers |

Temperature tests from −10 °C to 60 °C showed a drift of no more than 1 LSB for the IC and none measurable for the coils. The main thermal effect is the expansion of the arms and clips, which the node compensates for.

## Boards

| Board | Gerber | Description | Assembled |
| ----- | ------ | ----------- | --------- |
| **Piste** | `GERBER-Piste.zip` | Sensing arm: TX/RX coils, LX3302A, LMT01, MCP6541, cable and programming pads | **Yes** (`BOM-Piste.csv`, `CPL-Piste.csv`) |
| **Braccio** | `GERBER-Braccio.zip` | Second arm | No |
| **TargetGrande** | `GERBER-TargetGrande.zip` | Inductive target | No |
| **spacer** | `GERBER-spacer.zip` | FR4 spacer | No |

All boards are 2-layer FR4, 1.6 mm thick. The FR4 is also the structural material of the gauge.

## Schematic (Piste board)

| Ref | Part | Function |
| --- | ---- | -------- |
| IC1 | LX3302AQPW | Inductive sensor interface. IO1 = PWM, IO2 = SENT, IO3 = analog out, each with a 10 k pull-up to VIN |
| C4, C5 | 680 pF | TX LC tank capacitors |
| U1 | LMT01 | Temperature sensor with pulse-count current output |
| IC2 | MCP6541 | Comparator that turns the LMT01 current pulses (across a 10 k resistor) into logic pulses. Threshold 0.76 V, set by a 56k/10k divider from VIN |
| C1–C3, C6, C7 | | Decoupling |

Supply: VIN = 5 V from the node, switched on only during readings.

### Pads

| Group | Pad | Signal |
| ----- | --- | ------ |
| Cable to node | J3 | VIN (+5 V) |
| | J2 | GND |
| | J4 | SENT |
| | J5 | Temperature (LMT01 pulses) |
| LX3302A programming | J1 | VIN |
| | J9 | GND |
| | J8 | IO1 (PWM) |
| | J7 | IO2 (SENT) |
| | J6 | IO3 (analog) |

The LX3302A EEPROM is programmed with the Microchip LXM9518 and [`Firmware/lx3302a_config.txt`](../../Firmware/lx3302a_config.txt). See the [building instructions](../../building_instructions.md#4-lx3302a-programming).

## Manufacturing

Order one set of the four boards for each gauge. Only **Piste** needs assembly. The LMT01 has no LCSC code in the BOM and may have to be sourced and soldered separately.
