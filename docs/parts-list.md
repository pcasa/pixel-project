# Project Pixel — Complete Parts List

All parts needed across all phases to complete 10 finished units.
Prices approximate as of May 2026. Order Phase 1 + Phase 4 parts together — no reason to do two separate orders.

---

## Quick Summary

| Phase | What | Est. Cost |
|---|---|---|
| Phase 1–3 | Core electronics (boards, power) | ~$400 |
| Phase 4 | Audio (amp, speaker, wiring) | ~$130 |
| Enclosure | Filament, hardware, adhesive | ~$60 |
| Dev tools | Soldering, testing | ~$80 |
| Spares | Insurance against accidents | ~$50 |
| Gift packaging | Boxes, welcome cards | ~$40 |
| **Total** | | **~$760** |

---

## Phase 1–3 — Core Electronics (Order Now)

These are the main boards. Order these immediately — Seeed ships from China and takes 1–2 weeks.

| # | Part | Qty | ~Price | Notes |
|---|---|---|---|---|
| 1 | Seeed Studio XIAO ESP32-S3 Sense — **Pre-Soldered** | 10 | $160 | Must be pre-soldered — plugs into display |
| 2 | Seeed Studio Round Display for XIAO (1.28") | 10 | $120 | GC9A01 display, touch, RTC |
| 3 | USB-C to USB-A cable, 1m | 10 | $40 | For recipients — always-on power |
| 4 | **5V 2A** USB-A wall adapter | 10 | $60 | ⚠️ Must be 2A — audio load peaks at ~1.3A |

**Phase 1–3 total: ~$380**

### USA — Where to Buy

| Part | Seeed Studio (direct, cheapest) | Amazon (faster) |
|---|---|---|
| XIAO ESP32-S3 Sense Pre-Soldered | [seeedstudio.com](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32S3-Sense-Pre-Soldered-p-6335.html) | [amazon.com](https://www.amazon.com/Seeed-Studio-ESP32S3-Sense-Pre-Soldered/dp/B0DRNW6KMG) |
| Round Display for XIAO | [seeedstudio.com](https://www.seeedstudio.com/1-28-Round-Touch-Display-for-Seeed-Studio-XIAO-ESP32.html) | [amazon.com](https://www.amazon.com/Seeed-Studio-Round-Display-XIAO/dp/B0CB5HHY77) |
| USB-C cables + adapters | — | Amazon (any brand) |

### Serbia — Where to Buy

Amazon frequently blocks electronics shipping to Serbia. AliExpress is reliable and ships worldwide.

| Part | AliExpress (recommended) | Seeed Studio Direct (fallback) |
|---|---|---|
| XIAO ESP32-S3 Sense Pre-Soldered | [aliexpress.com](https://www.aliexpress.com/i/1005005599130052.html) — confirm "pre-soldered" variant in listing | [seeedstudio.com](https://www.seeedstudio.com/Seeed-Studio-XIAO-ESP32S3-Sense-Pre-Soldered-p-6335.html) |
| Round Display for XIAO | [aliexpress.com](https://www.aliexpress.com/item/1005003022741453.html) | [seeedstudio.com](https://www.seeedstudio.com/1-28-Round-Touch-Display-for-Seeed-Studio-XIAO-ESP32.html) |
| USB-C cables + adapters | AliExpress (any listing) | — |

**AliExpress tips:** Filter by "Seeed Studio Official Store" for genuine boards. Expect 2–4 week delivery. AliExpress Buyer Protection covers non-delivery.

---

## Phase 4 — Audio Hardware (Order with Phase 1)

No reason to wait — order these at the same time to avoid a second shipping window.
**No soldering needed until Phase 4 assembly.**

| # | Part | Qty | ~Price | Notes |
|---|---|---|---|---|
| 5 | Adafruit MAX98357A I2S Class D Amp Breakout | 10 | $50 | I2S digital audio → speaker output |
| 6 | Waveshare 8Ω 2W Cavity Speaker (B) — 20×30mm | 10 | $30 | Built-in acoustic cavity, 2-pin PH1.25 connector |
| 7 | JST PH1.25 2-pin pigtail wire set (20+ pairs) | 1 pack | $8 | Connects speaker to amp output |
| 8 | Short jumper wires, 22–24 AWG, pre-cut (assorted pack) | 1 pack | $8 | 5–6 wires per unit for amp ↔ XIAO GPIO |
| 9 | Heat shrink tubing assortment, 2–4mm | 1 pack | $6 | Clean up the wiring joints |

**Phase 4 hardware total: ~$102**

| Part | Where to Buy |
|---|---|
| MAX98357A Amp | [adafruit.com](https://www.adafruit.com/product/3006) or Amazon |
| Waveshare Speaker (B) | [waveshare.com](https://www.waveshare.com/8ohm-2w-speaker-b.htm) |
| JST PH1.25 pigtails | Amazon — search "JST PH 1.25 2 pin pigtail" |
| Jumper wires | Amazon — search "22AWG pre-cut jumper wire kit" |
| Heat shrink | Amazon — any assortment pack |

**Audio wiring (Phase 4 reference):**
```
XIAO ESP32-S3           MAX98357A Amp
─────────────           ─────────────
GPIO pin (BCLK) ──────► BCLK
GPIO pin (LRC)  ──────► LRC
GPIO pin (DIN)  ──────► DIN
3.3V            ──────► VIN
GND             ──────► GND
                        OUT+ / OUT- ──► Speaker (via JST pigtail)
```

Exact GPIO pin assignments to be finalized in Phase 4 firmware work.

---

## Enclosure

STL and STEP files already purchased ($15) from the official Pixel Patreon build.
Free OnShape CAD for modifications: [onshape.com — Pixel CAD](https://cad.onshape.com/documents/36ef3639f0adcbd215c2da2e/w/06b991eb4c1f6f28b2fd677f/e/884c5e41b396d185bfcf0efe)

| # | Part | Qty | ~Price | Notes |
|---|---|---|---|---|
| 10 | PETG filament, any color | 500g | $15 | ~30g per unit + prototype waste |
| 11 | M2×6mm screws | 50 | $5 | ~4 per unit + extras |
| 12 | M2 brass heat inserts | 50 | $8 | Press into plastic for clean screw threads — much better than threading plastic directly |
| 13 | Self-adhesive rubber feet | 40+ | $5 | 4 per unit |
| 14 | Double-sided foam mounting tape | 1 roll | $5 | Securing MAX98357A breakout inside enclosure |

**Enclosure total: ~$38**

**Modifications to original design:**
- Remove LiPo battery bay (we're USB-C powered)
- Add USB-C cable exit at rear or bottom
- Add speaker grille opening (Phase 4)
- Add internal shelf for MAX98357A (Phase 4)

---

## Development Tools (Team — One-Time Purchase)

| # | Item | ~Price | Notes |
|---|---|---|---|
| 15 | Soldering iron (temp-controlled) | $30–50 | Needed for Phase 4 amp wiring. A Hakko FX-888D or TS100 are good. Don't use a cheap fixed-temp iron. |
| 16 | Lead-free solder, rosin core, 0.8mm | $10 | 60/40 or 63/37 |
| 17 | Helping hands / PCB holder | $10 | Essential for soldering small breakout boards |
| 18 | Digital multimeter | $15–25 | Continuity testing, voltage checks |
| 19 | USB-C **data** cable (for firmware flashing) | $0–10 | Many USB-C cables are charge-only — must support data. Test with `pio device list`. Each dev needs one. |
| 20 | Flush cutters | $8 | Trimming wire ends cleanly |

**Dev tools total: ~$75–115**

> PlatformIO (firmware IDE), Docker Desktop, and VS Code are all free downloads.

---

## Spares (Strongly Recommended)

Development will break something. Order these with the initial batch.

| # | Part | Qty | ~Price | Notes |
|---|---|---|---|---|
| 21 | XIAO ESP32-S3 Sense Pre-Soldered | 2 | $32 | One bad flash or drop and you'll be glad you have these |
| 22 | Round Display for XIAO | 1 | $12 | Display glass is fragile during enclosure prototyping |

**Spares total: ~$44**

---

## Gift Delivery (Phase 6)

| # | Item | Qty | ~Price | Notes |
|---|---|---|---|---|
| 23 | Welcome card printing | 10 | $15–25 | Designed in Phase 6 — Canva or local print shop |
| 24 | Small padded mailers (or rigid gift boxes) | 10 | $15 | For shipping units that aren't hand-delivered |

---

## Complete Order Checklist

### Order Now (Seeed + Amazon + Adafruit)
- [ ] XIAO ESP32-S3 Sense Pre-Soldered × 12 (10 units + 2 spares)
- [ ] Round Display for XIAO × 11 (10 units + 1 spare)
- [ ] MAX98357A I2S Amp × 10
- [ ] Waveshare 8Ω 2W Speaker × 10
- [ ] USB-C to USB-A cable × 10
- [ ] 5V **2A** wall adapter × 10
- [ ] JST PH1.25 2-pin pigtail pack
- [ ] 22AWG jumper wire pack
- [ ] Heat shrink assortment

### Order When Enclosure Design is Finalized
- [ ] PETG filament 500g
- [ ] M2×6mm screws (50 pack)
- [ ] M2 brass heat inserts (50 pack)
- [ ] Rubber feet (40 pack)
- [ ] Double-sided foam mounting tape

### Development Tools (If Not Already Owned)
- [ ] Temperature-controlled soldering iron
- [ ] Lead-free solder
- [ ] Helping hands
- [ ] Digital multimeter
- [ ] Flush cutters
- [ ] USB-C data cable per team member

### Phase 6 (When Ready to Ship)
- [ ] Welcome cards × 10 (printed after Phase 6 design)
- [ ] Padded mailers × 10

---

## API Keys (Per Recipient — Not Hardware)

| Service | Cost | Where |
|---|---|---|
| Anthropic (Claude) | ~$5 credit, lasts months | [console.anthropic.com](https://console.anthropic.com) |

No Gemini key needed — STT and TTS run locally on the Mac.
