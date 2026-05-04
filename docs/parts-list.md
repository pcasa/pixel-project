# Project Pixel — Parts List

10 units. All prices USD, approximate as of mid-2025. Links are starting points — shop around.

---

## Per-Unit Bill of Materials

| # | Component | Part Name | Qty | Unit Price | 10-unit Total | Where to Buy |
|---|---|---|---|---|---|---|
| 1 | MCU + camera + mic | Seeed Studio XIAO ESP32-S3 Sense | 1 | $15 | $150 | seeedstudio.com, Amazon |
| 2 | Display | Seeed Studio Round Display for XIAO (1.28" GC9A01 + touch + RTC) | 1 | $10 | $100 | seeedstudio.com, Amazon |
| 3 | Audio DAC | Adafruit MAX98357A I2S Class D Mono Amp Breakout | 1 | $5 | $50 | adafruit.com, Amazon |
| 4 | Speaker | Waveshare 8Ω 2W Cavity Speaker (B) — 20×30mm, 2-pin PH1.25 | 1 | $3 | $30 | waveshare.com |
| 4a | Speaker connector | JST PH1.25 2-pin male+female pigtail set (20 pairs) | 1 pack | $1 | $8 | Amazon |
| 5 | Power | USB-C to USB-A cable, 1m | 1 | $4 | $40 | Amazon |
| 6 | Power | 5V 1A USB-A wall adapter | 1 | $5 | $50 | Amazon |
| 7 | Enclosure | 3D printed — PLA/PETG filament (~30g/unit) | 1 | $2 | $20 | (filament you own) |
| 8 | Misc | M2×6 screws (4/unit), rubber feet, short wires | 1 | $1 | $10 | Amazon, hardware store |

**Per-unit total: ~$46**
**10-unit hardware total: ~$458**

---

## Shopping Links (Seeed Studio Bundle)

Buy the XIAO ESP32-S3 Sense and Round Display together from Seeed for best price:
- **XIAO ESP32-S3 Sense**: https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html
- **Round Display for XIAO**: https://www.seeedstudio.com/Seeed-Studio-Round-Display-for-XIAO-p-5638.html

Seeed often has bundle discounts — check "Combos" section. Also available on Amazon (Prime shipping).

---

## Audio Circuit (MAX98357A → Speaker)

```
XIAO ESP32-S3                MAX98357A Breakout
─────────────────            ─────────────────
D8  (GPIO4 / BCLK)  ──────►  BCLK
D9  (GPIO6 / LRCK)  ──────►  LRC
D10 (GPIO7 / DIN)   ──────►  DIN
3.3V                ──────►  VIN
GND                 ──────►  GND

                    MAX98357A ──► Speaker (+) / (-)
```

**Note**: The XIAO ESP32-S3 Sense already has a PDM microphone built in (no external mic needed).
The MAX98357A adds the speaker output capability — the base OmniBot Pixel firmware only has mic input.
Speaker output (I2S TX) will require a firmware addition in Phase 4.

**Phase 1 note**: For Phase 1 testing, audio output plays through the Mac's speakers (browser dashboard).
The MAX98357A hardware integration is Phase 4.

---

## Enclosure Materials

| Item | Qty | Notes |
|---|---|---|
| PETG filament (any color) | 300g | ~30g per unit, some waste |
| Clear PETG or resin | 100g | Optional: clear diffuser layer over display |
| M2×6mm screws | 40 | 4 per unit |
| M2 brass heat inserts (optional) | 40 | 4 per unit — cleaner than threading plastic |
| Self-adhesive rubber feet | 40 | 4 per unit |

---

## Development Tools (One-Time)

| Item | Notes |
|---|---|
| USB-C to USB-A cable | For initial firmware flash (separate from unit cables) |
| PlatformIO (VS Code extension) | Free — for firmware build and flash |
| Soldering iron + solder | For MAX98357A breakout wiring |
| Helping hands / PCB holder | Makes wiring much easier |
| Digital multimeter | For continuity checks |

---

## API Keys (Per Recipient, Zero Hardware Cost)

Each recipient needs two free/low-cost API keys:

| Service | Key Type | Cost | Where |
|---|---|---|---|
| Anthropic (Claude) | Personal API key | ~$5 credit (months of use) | console.anthropic.com |
| Google Gemini | Personal API key | Free tier (15 RPM) | aistudio.google.com |

---

## Recommended Buying Order

1. **Week 1**: Order Seeed XIAO ESP32-S3 Sense × 10 + Round Display × 10 (may take 1–2 weeks to ship)
2. **Week 1**: Order MAX98357A breakouts × 10 + speakers × 10 (Amazon, fast shipping)
3. **Week 1**: Order USB-C cables × 10 + wall adapters × 10 (Amazon)
4. **Week 2**: Start enclosure design and first print once hardware arrives for sizing
5. **Week 3**: Order screws, rubber feet, heat inserts after finalizing enclosure design

---

## Where to Buy (Aggregated)

**Seeed Studio (seeedstudio.com)**: XIAO ESP32-S3 Sense, Round Display
**Adafruit (adafruit.com)**: MAX98357A breakout (most reliable supplier)
**Amazon**: Speakers, USB-C cables, wall adapters, screws, rubber feet
**DigiKey / Mouser**: If you need higher quantities or specific specs on passives
