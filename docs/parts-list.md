# Project Pixel — Parts List

Sourced directly from the official Pixel Tutorial BOM by Naz Louis.
Prices as listed in the original tutorial (May 2026).

---

## Per-Unit Bill of Materials

| # | Part | Qty | Unit Price | 10-unit Total | Notes |
|---|---|---|---|---|---|
| 1 | Seeed Studio XIAO ESP32-S3 Sense — **Pre-Soldered** | 10 | $14.99 | $149.90 | Must be pre-soldered — pins plug directly into display. **Buy Sense, not standard** — the Sense module includes a built-in PDM microphone (used for wake word + speech input). Non-Sense boards have no mic. The built-in camera is replaced by the external OV2640, but the mic is kept. |
| 2 | Seeed Studio Round Display for XIAO (1.28") | 10 | $18.00 | $180.00 | GC9A01, touch, RTC, JST battery connector |
| 3 | LiPo battery — DCH 523450, 3.7V **1000mAh**, JST | 10 | $11.99 | $119.90 | Exact model from original BOM |
| 4 | OV2640 Camera Module, 160° wide-angle, 2MP (Aideepen) — 2-pack | 10 | $19.99/2-pack | $99.95 | Replaces the XIAO's built-in camera. Sold in 2-packs — buy 1 pack per 2 units. |
| 5 | CR927 RTC battery (10-pack) | 1 pack | $5.99 | $5.99 | Keeps RTC running when unplugged — 1 pack covers all 10 units |
| 6 | USB-C to USB-C cable, 1m | 10 | ~$3 | ~$30 | Power — not in original BOM, added for our always-on USB-C design |

**Per-unit total: ~$68**
**10-unit total: ~$685**

> **No soldering required.** The XIAO's pre-soldered pins plug directly into the Round Display — snap together. Battery plugs into the JST socket on the Round Display. OV2640 connects via ribbon cable.

> **Spares recommended:** Order 2 extra XIAOs and 1 extra display — development will inevitably damage one.

---

## Where to Buy

### USA

**Order from Seeed Studio** (boards):

| Part | Seeed Studio | Amazon |
|---|---|---|
| XIAO ESP32-S3 Sense Pre-Soldered | [seeedstudio.com](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32S3-Sense-Pre-Soldered-p-6335.html) | [amazon.com](https://amzn.to/4tPeg00) |
| Round Display for XIAO | [seeedstudio.com](https://www.seeedstudio.com/1-28-Round-Touch-Display-for-Seeed-Studio-XIAO-ESP32.html) | [amazon.com](https://amzn.to/4tH215P) |

**Order from Amazon** (battery, camera, RTC):

| Part | Amazon Link |
|---|---|
| LiPo 3.7V 1000mAh (DCH 523450, JST) | [amazon.com](https://amzn.to/3QwjBLn) |
| OV2640 Camera Module 160° — 2-pack | [amazon.com — 2-pack](https://www.amazon.com/Camera-Aideepen-Wide-Angle-Megapixel-Support/dp/B09XXPX4SP) |
| CR927 RTC Battery 10-pack | [amazon.com](https://amzn.to/48vFAYO) |
| USB-C to USB-C cable | Amazon (any brand) |

> **Seeed tip:** Select the US warehouse at checkout for faster shipping.

---

### Serbia

AliExpress is the most reliable option — ships worldwide with buyer protection.

| Part | AliExpress | Seeed Studio Direct |
|---|---|---|
| XIAO ESP32-S3 Sense Pre-Soldered | [aliexpress.com](https://www.aliexpress.com/i/1005005599130052.html) — confirm "pre-soldered" variant | [seeedstudio.com](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32S3-Sense-Pre-Soldered-p-6335.html) |
| Round Display for XIAO | [aliexpress.com](https://www.aliexpress.com/item/1005003022741453.html) | [seeedstudio.com](https://www.seeedstudio.com/1-28-Round-Touch-Display-for-Seeed-Studio-XIAO-ESP32.html) |
| LiPo 3.7V 1000mAh JST | AliExpress — search "DCH 523450 3.7V 1000mAh JST" | — |
| OV2640 Camera 160° — 2-pack | [aliexpress.com — Taidacent OV2640 160° 24-pin](https://www.aliexpress.com/item/4001333887594.html) — Aideepen not on AliExpress; Taidacent is identical spec (160°, 2MP, 24-pin DVP). Buy 1 per 2 units. | — |
| CR927 RTC Battery | AliExpress (any listing) or local pharmacy | — |
| USB-C to USB-C cable | AliExpress (any listing) | — |

> **AliExpress tips:** Filter by "Seeed Studio Official Store" for genuine boards. Expect 2–4 week delivery.

---

## Enclosure

STL and STEP files purchased from the official Pixel Patreon build ($15).
Free OnShape CAD for modifications: [onshape.com — Pixel CAD](https://cad.onshape.com/documents/36ef3639f0adcbd215c2da2e/w/06b991eb4c1f6f28b2fd677f/e/884c5e41b396d185bfcf0efe)

**Team members print their own.** Serbia: STL files are in the repo — send to a local print shop or friend with a printer.

**Modifications needed vs original:**
- Add USB-C cable exit at rear or bottom (original was battery-only powered)

**Print settings:**
- Material: PETG
- Layer height: 0.2mm, infill 15% gyroid

---

## Development Tools

| Item | Notes |
|---|---|
| PlatformIO (VS Code extension) | Free — firmware build and flash |
| USB-C **data** cable | For flashing — must support data, not charge-only |

---

## API Keys (Per Recipient)

| Service | Cost | Where |
|---|---|---|
| **Anthropic (Claude)** | ~$5 credit, lasts months | [console.anthropic.com](https://console.anthropic.com) |

No Gemini key needed — STT and TTS run locally on the Mac.
