# Design Principles

Core decisions that shape how Pixel is built. These are not preferences or defaults — they are constraints. Any feature that violates these principles does not ship.

---

## 1. Human-in-the-Loop: Claude Drafts, Humans Execute

**The rule:** Claude can read anything. Claude can generate and draft anything. Claude cannot execute any action that affects the outside world without explicit human confirmation.

**Why:** Recipients include executives and board members. A mistakenly sent email, an accidentally created calendar event, or any external action taken on their behalf without their knowledge could have serious professional and legal consequences.

**What this means in practice:**

| Action Type | Claude can do it automatically? |
|---|---|
| Read Gmail / Calendar / Documents | Yes |
| Summarize, analyze, generate insights | Yes |
| Take meeting notes | Yes |
| Write a draft email | Yes — writes to `vault/pending/` |
| Send an email | No — requires explicit confirmation |
| Create or modify a calendar event | No — requires explicit confirmation |
| Post or reply anywhere externally | No — requires explicit confirmation |
| Delete anything | No — requires explicit confirmation |
| Forward anything | No — requires explicit confirmation |

**How confirmation works:**
1. Claude calls a "staged" tool (e.g. `draft_email`) — never a direct-send tool
2. The hub writes the action to `vault/pending/` and notifies the user
3. User confirms via voice ("yes, send it") or dashboard button
4. Only the confirmation handler calls the actual Gmail/Calendar API — Claude never touches it directly

**This is architectural, not a setting.** There is no configuration that bypasses this gate. The `send_email` tool definition in Claude's tool list never directly calls any external API — it only calls `stage_action()`. The actual execution path is unreachable by Claude.

**Ambiguity rule:** If it's unclear whether a user utterance is confirmation, it isn't. "That sounds good" is not confirmation. "Yes, send it" is.

---

## 2. Claude API and CLI Only — Not Claude.ai Desktop or Workspace

**The rule:** All Claude usage must go through the Claude API or Claude Code CLI. Claude.ai desktop and Claude.ai Workspace are not permitted for work involving org data.

**Why:** The org's BAA with Anthropic covers the **Claude API and Claude Code CLI only**. Claude.ai desktop and Claude.ai Workspace are consumer/commercial products that operate under different data handling terms and are explicitly not covered by the BAA. Any work data, PHI, email content, or calendar data processed through those surfaces is unprotected.

**What is covered:**
| Surface | BAA Covered | Use for work data |
|---|---|---|
| Claude API (Anthropic SDK) | ✅ Yes | Yes |
| Claude Code CLI | ✅ Yes | Yes |
| MCP servers (Gmail, Calendar, Drive) via API | ✅ Yes | Yes |
| Claude.ai desktop app | ❌ No | Never |
| Claude.ai Workspace | ❌ No | Never |

**For the hub:** All Claude calls go through the `anthropic` Python SDK (`claude_session.py`). No browser-based Claude surface is ever in the data path.

---

## 3. Audio Never Leaves the Mac

**The rule:** All speech-to-text and text-to-speech processing runs locally. No audio is sent to any cloud service.

**Why:** A BAA exists with Anthropic (Claude) but not with any audio processing service. Conversations may contain PHI, sensitive organizational information, or executive-level strategy. Audio processed by a third party without a BAA is a HIPAA violation.

**What this means:**
- STT: Whisper (local) or MLX-Audio (Apple Silicon) — no network call
- TTS: MLX-Audio or Kokoro-ONNX — no network call
- Only text reaches the network, only via Claude API (covered by BAA)
- Gemini API is not used for any purpose

**Recipients need exactly one API key: Claude.**

---

## 3. Persistent Storage via Vault Volume

**The rule:** All user data — notes, drafts, pending actions, persona files, skills — lives in a mounted Docker volume. Nothing important lives inside the container.

**Why:** Docker containers are ephemeral. If the container is rebuilt or updated, the volume persists. If a unit is replaced, the vault can be restored.

**Vault structure:**
```
~/pixel-vault/              ← Docker volume mount
├── persona/                ← SOUL.md, USER.md, MEMORY.md etc.
├── notes/                  ← Meeting notes, daily logs
├── emails/                 ← Email drafts
├── pending/                ← Staged actions awaiting confirmation
├── skills/
│   ├── default/            ← Template skills shipped with hub
│   └── company/            ← Company skills (git-managed, updatable)
└── .obsidian/              ← Obsidian config (auto-generated)
```

The vault is a valid Obsidian vault — the executive can open `~/pixel-vault/` in Obsidian on their Mac to browse all notes, drafts, and meeting summaries with Obsidian's full UI.

**Note:** Obsidian the app is not run inside Docker (it's a desktop app). Only the vault folder structure is used. Docker reads and writes markdown files; Obsidian reads the same files on the desktop.

---

## 4. Skills Are Version-Controlled

**The rule:** Company skills live in a private git repo and are pulled into the vault, not hardcoded.

**Why:** Skills need to evolve — new workflows, new templates, org changes. A git-based approach means updates propagate to all units on next restart, are version-controlled and auditable, and can be rolled back.

**Default skills** ship with the hub Docker image as a starting point.
**Company skills** are layered on top via `git pull` at startup.

---

## 5. omnibot/ Is Never Modified

**The rule:** The `omnibot/` directory is the upstream OmniBot source, cloned read-only. It is never edited.

**Why:** It is our reference. If we need to understand what the original code did, or pull in a future upstream fix, we need it intact. All our work lives in `hub/`, `firmware/`, and `tools/`.
