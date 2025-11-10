# LiDAR to RS232 Converter for TracMap (Raspberry Pi Pico)

This project uses a **Raspberry Pi Pico** to convert **RS485 data from a LiDAR sensor** into **RS232 format**, making it compatible with **TracMap systems**.  
An additional **TTL-to-RS232 converter board** is used to provide the final signal output.

---

## 📁 Project Overview

- **`main.py`** – Updated and optimized version of the original `lidar_pico.py`.  
  - Faster data processing  
  - Improved packet handling (reduces partial packets)  
- **`lidar_pico.py`** – Original version (kept for reference)  
- **Gerber (PCB design)** – Included in the provided ZIP archive  
- **Schematic** – Refer to this for pinout details  

---

## 🔌 Serial Communication

- **Standard rule:** RX → TX, TX → RX  
- **TracMap connection:** RX → RX, TX → TX  
  > Yes, this seems reversed—and no, we don’t know why either, but it works.  

---

## ⚡ Grounding

Two separate ground connections are used on the converter board:

1. **Power ground** – For power input  
2. **Signal ground** – Used as the serial communication reference  

👉 Always use the **ground from the TTL-to-RS232 converter** as the **reference ground** for serial connections.

---

## 🧠 Raspberry Pi Pico Setup

1. Flash **MicroPython** onto your Raspberry Pi Pico.  
2. Copy **`main.py`** (from this repository) directly onto the Pico.  
3. **Do not rename the file** – it must be called `main.py` to auto-run on power-up.  

---

## 🔋 Power Supply – Buck Converter Setup

> ⚠️ **Important:** Set up the buck converter **before** soldering or connecting it to the Pico.

1. Adjust output voltage to **5.12V DC** using a multimeter.  
2. Turn the **small adjustment screw counterclockwise (CCW)** until voltage drops to the desired level.  
   - Many converters ship from the factory set near full voltage (up to 40V).  
   - It can take **12–20 full turns** before voltage begins to decrease.  
3. Verify output voltage matches **5.12V** before powering the Pico.  
4. When testing, use the same input voltage as your aircraft system (e.g., **12V or 28V**) to confirm proper regulation.

---

## 🧵 LiDAR Wiring Notes (N.H. Reference)

Use **Ethernet Type B** wiring standard. Match the following wires between the Ethernet cable and LiDAR:

| Ethernet Wire | LiDAR Wire |
|----------------|-------------|
| Green          | Green       |
| Striped Blue   | Red         |
| Striped Yellow | White       |
| Yellow         | Black       |
| Blue           | Blue        |
| Brown          | Brown       |

---

## 🧩 Files Included

- `main.py` – Final running script  
- `lidar_pico.py` – Original version  
- `PCB_Gerber.zip` – PCB design files  
- `schematic.png/pdf` – Wiring and pinout reference  

---

## 🛠️ License

This project is open for modification and personal use.  
Please credit the original authors if redistributed or adapted.
