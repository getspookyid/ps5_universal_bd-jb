# ps5_universal_bd-jb: Universal Exploit Source

This repository contains the source code for the **ps5_universal_bd-jb (v1.2)**, enabling firmware-agnostic "Stage 0" kernel mutation on the PlayStation 5.

## 📁 Repository Structure
- `src/`: BD-JB Java Xlet source for triggering UDF-J overflow.
- `scripts/`: Universal Bridge triangulation and payload injection tools.
- `docs/`: Verified binary archaeology reports and mathematical proofs.

## 🚀 Key Features
- **Universal Bridge Formula**: Zero-inference offset prediction using the Structural Shift Coefficient ($\Sigma$).
- **Multi-FW Support**: Verified on 1.02, 2.20, 8.00 (Recovery), and 12.70.
- **Dynamic Mutation**: Patch eFuse checks (`BNE -> NOP`) at offset `0x27C68` (for 12.70).

## 🛠️ Usage (The "Homie" Test)
Follow these steps to verify the exploit on a physical console:

### 1. Build the ISO
- **Requirement**: You must have the [PS5 BD-JB SDK](https://github.com/john-t-williamson/ps5-payload-sdk) installed.
- Navigate to the `src/` directory.
- Run `make`. This will generate `payload-loader.iso`.

### 2. Burn and Boot
- Burn `payload-loader.iso` to a Blu-ray disc (BD-RE recommended).
- Insert the disc into your PS5.
- Launch the BD-Player. The screen will stay black or show a log; the console is now listening on **Port 9020**.

### 3. Drop the Payload (e.g. etaHEN)
- On your PC, locate your `etaHEN.bin` (or other payload).
- Run the injection script:
    ```bash
    python scripts/INJECT_PAYLOAD.py <PS5_IP> --file etaHEN.bin --fw 12.70
    ```
- The script automatically calculates the **0x27C68** shift for 12.70 and drops the payload.

---
*Grounded in AFP-03 Silicon Integrity*
