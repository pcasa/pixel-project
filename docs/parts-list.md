# Project Pixel — Parts List

Based on the original OmniBot Pixel build by Naz Louis.
Prices approximate as of May 2026. Speaker and amp are not included in this phase — audio plays through the Mac's speakers via the browser dashboard.

---

## Per-Unit Bill of Materials

| # | Component | Part | Qty | ~Price |
|---|---|---|---|---|
| 1 | MCU + camera + mic | Seeed Studio XIAO ESP32-S3 Sense — **Pre-Soldered version** | 1 | $16 |
| 2 | Display | Seeed Studio Round Display for XIAO (1.28" GC9A01, touch, RTC) | 1 | $12 |
| 3 | Power | USB-C to USB-A cable, 1m | 1 | $4 |
| 4 | Power | 5V 1A USB-A wall adapter | 1 | $5 |
| 5 | Enclosure | 3D printed — PETG filament (~30g/unit) | 1 | ~$2 |
| 6 | Misc | M2×6 screws (4/unit), rubber feet | 1 | ~$1 |

**Per-unit total: ~$40**
**10-unit hardware total: ~$400**

> **No soldering required for this phase.** The XIAO's pre-soldered header pins plug directly into the Round Display's female socket — assembly is snap-together. The only soldering in the entire project is Phase 4 (speaker + amp wiring), which comes later.

---

## Where to Buy

### USA Team Members

| Component | Option 1 — Seeed Studio (direct) | Option 2 — Amazon (faster shipping) |
|---|---|---|
| **XIAO ESP32-S3 Sense (Pre-Soldered)** | [seeedstudio.com — Pre-Soldered](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32S3-Sense-Pre-Soldered-p-6335.html) | [amazon.com — Pre-Soldered](https://www.amazon.com/Seeed-Studio-ESP32S3-Sense-Pre-Soldered/dp/B0DRNW6KMG) |
| Round Display for XIAO | [seeedstudio.com](https://www.seeedstudio.com/1-28-Round-Touch-Display-for-Seeed-Studio-XIAO-ESP32.html) | [amazon.com](https://www.amazon.com/Seeed-Studio-Round-Display-XIAO/dp/B0CB5HHY77) |
| USB-C cable + adapter | — | Amazon (any brand) |

> **Do not buy the bundle** — the Amazon bundle listing does not specify pre-soldered and may ship the standard version. Buy the two items separately using the links above to guarantee you get the pre-soldered XIAO.

**Seeed tip:** The CN warehouse ships internationally and is cheapest. If you need faster, Seeed has a US warehouse — select it at checkout.

---

### Serbia (Jelena / international team member)

Amazon.de and Amazon.com are unreliable for electronics shipping to Serbia — items frequently show "cannot ship to your location." **AliExpress is the best option** — ships worldwide, reliable, often free or low-cost shipping from China.

| Component | AliExpress | Seeed Studio Direct |
|---|---|---|
| **XIAO ESP32-S3 Sense (Pre-Soldered)** | [aliexpress.com](https://www.aliexpress.com/i/1005005599130052.html) — search "XIAO ESP32S3 Sense pre-soldered" to confirm variant | [seeedstudio.com — Pre-Soldered](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32S3-Sense-Pre-Soldered-p-6335.html) ¹ |
| Round Display for XIAO | [aliexpress.com](https://www.aliexpress.com/item/1005003022741453.html) | [seeedstudio.com](https://www.seeedstudio.com/1-28-Round-Touch-Display-for-Seeed-Studio-XIAO-ESP32.html) ¹ |
| USB-C cable + adapter | AliExpress (any listing) | — |

¹ Seeed Studio ships from CN warehouse to most countries including Serbia. Expect 15–25 days. Verify Serbia is available at checkout before ordering.

**AliExpress tips for Serbia:**
- Filter by "Seeed Studio Official Store" for genuine parts
- Check seller rating (look for 95%+ positive feedback)
- AliExpress Buyer Protection covers non-delivery
- Expect 2–4 week delivery from CN

---

## Enclosure

STL and STEP files are already purchased from the official Pixel Patreon build ($15).
The original CAD is also free on OnShape if modifications are needed:
[onshape.com — Pixel CAD](https://cad.onshape.com/documents/36ef3639f0adcbd215c2da2e/w/06b991eb4c1f6f28b2fd677f/e/884c5e41b396d185bfcf0efe)

**Print settings (Bambu X1):**
- Material: PETG (better heat tolerance near USB-C than PLA)
- Layer height: 0.2mm
- Infill: 15% gyroid

**Modifications needed vs original design:**
- Remove LiPo battery bay (we use USB-C power)
- Add USB-C cable exit (rear or bottom)
- (Phase 4 only) Add speaker grille + MAX98357A mount

---

## API Keys (Per Recipient)

Each recipient needs one API key:

| Service | Cost | Where to get it |
|---|---|---|
| **Anthropic (Claude)** | ~$5 credit (lasts months) | [console.anthropic.com](https://console.anthropic.com) |

> Gemini key no longer needed — STT and TTS run locally on the Mac. See `docs/local-audio-recommendation.md`.

---

## Development Tools (One-Time, Team)

| Item | Notes |
|---|---|
| PlatformIO (VS Code extension) | Free — firmware build and flash |
| USB-C data cable | For flashing — confirm it's data-capable, not charge-only |

**Note on soldering:** None required for the current build. When Phase 4 (speaker + amp) is ready, you'll need a soldering iron for 5 wires between the MAX98357A breakout and the speaker/XIAO. That's covered in the Phase 4 guide.

---

## Buying Order

1. **Now**: Order XIAO ESP32-S3 Sense × 10 + Round Display × 10 — Seeed ships from China, allow 1–2 weeks
2. **Now**: Serbia team member orders via AliExpress at the same time — similar shipping window
3. **When hardware arrives**: Begin Phase 2 (captive portal) and prototype the enclosure
4. **Phase 4**: Order speaker + amp when ready for hardware assembly
