# Project Pixel — Parts List

Based on the original OmniBot Pixel build by Naz Louis.
Prices approximate as of May 2026.

---

## Per-Unit Bill of Materials

| # | Part | Qty | ~Price | Notes |
|---|---|---|---|---|
| 1 | Seeed Studio XIAO ESP32-S3 Sense — **Pre-Soldered** | 10 | $160 | Must be pre-soldered — pins plug directly into the display |
| 2 | Seeed Studio Round Display for XIAO (1.28") | 10 | $120 | GC9A01 display, touch controller, RTC |
| 3 | LiPo battery, 3.7V, JST 1.25mm 2-pin, ~400mAh | 10 | ~$50 | From original author's BOM — powers RTC and allows brief untethered use |
| 4 | USB-C to USB-A cable, 1m | 10 | $40 | Always-on desk power |
| 5 | 5V **2A** USB-A wall adapter | 10 | $60 | Must be 2A — 1A is insufficient under load |

**Per-unit total: ~$43**
**10-unit total: ~$430**

> **No soldering required.** The XIAO's pre-soldered pins plug directly into the Round Display's socket — snap together, done. The battery connects via the JST 1.25mm plug on the Round Display — no soldering.

> **Spares recommended:** Order 2 extra XIAOs and 1 extra display — development will inevitably damage one.

---

## Where to Buy

### USA

| Part | Seeed Studio (direct, cheapest) | Amazon (faster) |
|---|---|---|
| XIAO ESP32-S3 Sense Pre-Soldered | [seeedstudio.com](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32S3-Sense-Pre-Soldered-p-6335.html) | [amazon.com](https://www.amazon.com/Seeed-Studio-ESP32S3-Sense-Pre-Soldered/dp/B0DRNW6KMG) |
| Round Display for XIAO | [seeedstudio.com](https://www.seeedstudio.com/1-28-Round-Touch-Display-for-Seeed-Studio-XIAO-ESP32.html) | [amazon.com](https://www.amazon.com/Seeed-Studio-Round-Display-XIAO/dp/B0CB5HHY77) |
| LiPo battery (if using) | — | Amazon — search "3.7V LiPo JST 1.25 2 pin" |
| USB-C cables + 5V 2A adapters | — | Amazon (any brand) |

> **Seeed tip:** Select the US warehouse at checkout for faster shipping. CN warehouse is cheaper but 1–2 weeks.

### Serbia

AliExpress is the most reliable option — ships worldwide, free or low-cost from China.

| Part | AliExpress | Seeed Studio Direct |
|---|---|---|
| XIAO ESP32-S3 Sense Pre-Soldered | [aliexpress.com](https://www.aliexpress.com/i/1005005599130052.html) — confirm "pre-soldered" variant | [seeedstudio.com](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32S3-Sense-Pre-Soldered-p-6335.html) |
| Round Display for XIAO | [aliexpress.com](https://www.aliexpress.com/item/1005003022741453.html) | [seeedstudio.com](https://www.seeedstudio.com/1-28-Round-Touch-Display-for-Seeed-Studio-XIAO-ESP32.html) |
| LiPo battery (if using) | AliExpress — search "3.7V LiPo JST 1.25 2 pin 400mAh" | — |
| USB-C cables + adapters | AliExpress (any listing) | — |

> **AliExpress tips:** Filter by "Seeed Studio Official Store" for genuine boards. Expect 2–4 week delivery.

---

## Enclosure

STL and STEP files already purchased from the official Pixel Patreon ($15).
Free OnShape CAD for modifications: [onshape.com — Pixel CAD](https://cad.onshape.com/documents/36ef3639f0adcbd215c2da2e/w/06b991eb4c1f6f28b2fd677f/e/884c5e41b396d185bfcf0efe)

**Team members print their own** on their 3D printers.
**Serbia:** STL files will be shared from the repo — she can send to a local print shop or friend with a printer.

**Modifications needed vs original:**
- Add USB-C cable exit at rear or bottom (original used battery-only power)

**Print settings:**
- Material: PETG (better heat tolerance near USB-C than PLA)
- Layer height: 0.2mm, infill 15% gyroid

---

## Development Tools

| Item | Notes |
|---|---|
| PlatformIO (VS Code extension) | Free — firmware build and flash |
| USB-C **data** cable | For flashing — many cables are charge-only, confirm yours supports data |

---

## API Keys (Per Recipient)

| Service | Cost | Where |
|---|---|---|
| **Anthropic (Claude)** | ~$5 credit, lasts months | [console.anthropic.com](https://console.anthropic.com) |

No Gemini key needed — STT and TTS run locally on the Mac.

