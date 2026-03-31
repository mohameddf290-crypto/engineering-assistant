> Source of truth extracted from the root README.md for easy reference by Cursor and other tools.

## 🎵 Module 3: Infinite Melody Generator

Generates professional, strong, deep, simple-yet-catchy, human-quality melodies — infinitely, from any input. Works on top of any chord progression (from the Chords module or third-party). Generates melodies for every role — lead, counter-melody, ear candy, pad melody, bass line, arpeggio layer, and more — that **perfectly complement each other**. If any melody is modified, the complementary melodies adapt automatically through the Melody Role Intelligence brain.

### Input Methods

| # | Method | Description |
|---|--------|-------------|
| 1 | **From app chords** | Click a button after selecting chords in the Chords module → melody generated over those exact chords |
| 2 | **From any chords** | Feed any chord progression (third-party, imported, manually entered) → melody generated over it |
| 3 | **From audio** | Drop a song (no vocals, no drums) → app analyzes melodic DNA → generates a melody inspired by it |

### User Controls & Features

| Feature | Description |
|---------|-------------|
| Length | 4-bar or 8-bar melodies |
| Complexity gauge | Simple, Medium, Complex |
| Mode | Normal (pure melody) vs Hybrid (blend of chords and melody fused together) |
| Piano roll editing | Move notes across octaves, change pitch, adjust note length |
| Modify | Adjust steps, leaps, shape, and rhythm |
| Partial lock | Lock specific notes, regenerate the rest |
| Keep + Generate Another | Keep the current melody and generate a new one |
| Generate Similar / Different | Preserve or contrast melodic DNA on regeneration |
| Elongate | Extend any melody by additional notes or bars |
| Melody Roles | Lead, Counter-melody, Ear candy, Pad melody, Bass line, Arpeggio layer, and more |
| Multi-role generation | After selecting the main lead melody, generate complementary role-melodies that perfectly complement it |
| Adaptive complementarity | If any melody is modified, all complementary melodies adapt automatically |
| Drag to FL Studio | Drag-and-drop MIDI export directly to FL Studio |

### Operating System Brains (Melodies Module)

---

#### Melodies Brain 1 — Chord Analysis Engine
**File:** `melodies/chord_analysis.py`

**Purpose:** Analyzes any chord progression (from the Chords module or external) and extracts everything needed for melody generation: harmonic structure, note pools per chord, tension arc, resolution points, approach notes, and avoid notes.

**Default AI thinking replaced:** Using chord root notes as the melody or restricting melody to pentatonic scales. Replaced with: a full harmonic analysis that constructs per-chord note pools with priority weighting (chord tones > extensions > passing tones > approach notes) and maps the tension/resolution arc across the entire progression.

**Protocols:**
- Every chord is fully analysed: chord tones, available extensions, approach notes, avoid notes
- Note pool is constructed per-chord with priority weighting for use by the Melody Creation Brain
- Tension arc and resolution points are mapped for the entire progression before melody generation begins

---

#### Melodies Brain 2 — Song Analysis Engine
**File:** `melodies/song_analysis.py`

**Purpose:** Analyzes a full song (no vocals, no drums) and extracts melodic DNA: contour shape, rhythmic density, phrasing length, interval preferences, syncopation level, and emotional arc.

**Default AI thinking replaced:** Copying melodic fragments from the analyzed song. Replaced with: extracting melodic principles — the underlying shape, rhythmic tendencies, phrasing habits, and interval vocabulary — and using those as a blueprint for original creation.

**Protocols:**
- Analysis extracts melodic principles, never melodic content (no copying)
- Contour is mapped as a directional shape over time, not as pitch values
- Rhythmic DNA is extracted as onset density and syncopation patterns, not raw note durations

---

#### Melodies Brain 3 — Translation System
**File:** `melodies/translation.py`

**Purpose:** Converts chord analysis and/or song analysis into a structured `MelodyCreationPlan` ready for the Melody Creation Brain.

**Default AI thinking replaced:** Feeding analysis data directly into generation with no interpretation. Replaced with: a musical intelligence layer that reads analysis results and produces an actionable melody blueprint: note pool strategy, contour target, rhythmic framework, phrasing plan, and complexity level.

**Protocols:**
- Chord-input translation focuses on harmonic fit, tension navigation, and note pool usage
- Song-input translation focuses on melodic principle extraction and style-informed creation
- Both paths can combine when both inputs are provided simultaneously

---

#### Melodies Brain 4 — Melody Creation Brain
**File:** `melodies/melody_creator.py`

**Purpose:** The core skill. Creates professional, strong, deep, simple-yet-catchy, human-quality melodies from any creation plan. Creates both Normal (pure melodic line) and Hybrid (chord-melody blend) forms.

**Default AI thinking replaced:** Pattern-recalled melodic sequences. Replaced with: deliberate melodic construction — intentional contour shaping, specific rhythmic patterns, careful note selection from the harmonic note pool, human-quality phrasing. The user's taste profile shapes every decision without sacrificing musical coherence.

**Protocols:**
- Every melody is built note-by-note from the creation plan — no template recall
- Normal mode: pure melodic line. Hybrid mode: harmonic elements woven into the melody
- Output includes full note data: pitch (MIDI), duration, position, velocity, and role annotation

---

#### Melodies Brain 5 — Infinity Engine
**File:** `melodies/infinity_engine.py`

**Purpose:** Generates infinite melodies from any input without any quality degradation. Similar regeneration, different regeneration, and everything in between.

**Default AI thinking replaced:** Re-running the same generation with different seeds. Replaced with: a structured melodic variation space with controlled similarity/contrast operators and a mandatory quality gate on every output.

**Protocols:**
- Similar regeneration preserves melodic DNA (contour, rhythm) while varying specific note choices
- Different regeneration applies contrast operators across contour, rhythm, and note selection simultaneously
- Quality gate runs on every melody — degradation is never tolerated

---

#### Melodies Brain 6 — Elongation System
**File:** `melodies/elongation.py`

**Purpose:** Extends any melody by additional notes or bars while maintaining melodic coherence, quality, and the character of the original.

**Default AI thinking replaced:** Repeating the existing melody or appending random notes. Replaced with: melodic arc analysis followed by a harmonically and melodically intelligent continuation that uses the same interval vocabulary and rhythmic patterns as the source.

**Protocols:**
- The original melody's contour arc and phrasing structure are analysed before any extension
- Extension uses the established melodic vocabulary: interval choices, rhythmic patterns, phrasing length
- Extended section always closes with a proper phrase ending — never a hanging note

---

#### Melodies Brain 7 — AI Blocker
**File:** `melodies/ai_blocker.py`

**Purpose:** Hard constraint system blocking any output that resembles default AI melody generation. Non-negotiable. Every melody is screened.

**Default AI thinking replaced:** Unconstrained melody generation. Replaced with: explicit blacklists of AI melody patterns — stepwise scalic runs, bare pentatonic defaults, even-eighth-note rhythmic grids, emotional flatness, lack of dynamic phrasing. Rejection triggers immediate regeneration.

**Protocols:**
- Blacklisted patterns: monotone stepwise scalic runs, bare pentatonic patterns, even-8th-note rhythmic grid, zero dynamic shaping
- Every melody receives a quality score; below-threshold results are rejected immediately
- Rejection triggers regeneration — no flagged melody is ever delivered to the user

---

#### Melodies Brain 8 — Modification Engine
**File:** `melodies/modification_engine.py`

**Purpose:** Integrates any user modification — steps, leaps, shape, rhythm, individual note changes, complexity level — with zero difficulty. The modified melody remains professional and coherent regardless of what was changed.

**Default AI thinking replaced:** Simple note replacement or transposition with no harmonic awareness. Replaced with: a context-aware modification system that validates every change against harmonic coherence and re-runs the AI Blocker on every result.

**Protocols:**
- Every modification is validated for harmonic coherence before being applied
- Partial lock: specific notes can be locked while the rest are regenerated around them
- After any modification, the AI Blocker re-screens the result — the quality bar never drops

---

#### Melodies Brain 9 — Melody Role Intelligence
**File:** `melodies/role_intelligence.py`

**Purpose:** Has profound, embedded knowledge of every melody role. Generates melodies according to the selected role with role-specific constraints. Most critically: every role-melody perfectly complements every other, and if ANY melody is modified, the complementary melodies adapt automatically.

**Default AI thinking replaced:** Generic melody generation with a "role" label applied superficially. Replaced with: deep role-aware construction where every role has embedded harmonic, rhythmic, and registral constraints that guarantee perfect complementarity. The Complementarity Matrix defines the exact relationship between every pair of roles.

**Protocols:**
- Every role has embedded constraints: register range, rhythmic density, harmonic priority, note pool bias
- The Complementarity Matrix defines explicit relationships between every pair of melody roles
- When any melody is modified, all dependent role-melodies are re-evaluated and adapted automatically

---

#### Editor
**File:** `melodies/editor.py`

Piano roll-style editor logic for the Melodies module. Handles in-app editing of melodies: move notes across octaves, change pitch, and adjust note length in a piano roll interface.

---

## 🧠 Shared Philosophy (Chords & Melodies Modules)

Both modules are built on the same non-negotiable rules as the rest of the Engineering Assistant. No exceptions.

| Rule | Implementation |
|------|---------------|
| **Custom-built from zero** | No default AI patterns. Every brain is invented, protocol-driven, and enforced from scratch |
| **Own information database** | Each brain has its own embedded knowledge base — emotion taxonomy, role constraints, AI pattern blacklists, harmonic rules — not shared generic data |
| **Thinks like a genius producer** | Every decision made with the mindset of a professional human producer with deep musical knowledge |
| **Zero AI slop** | The AI Blocker is a hard gatekeeper in both modules — no flagged output ever reaches the user |
| **Taste profiles embedded** | The user's personal taste profile is embedded in the Chord Creation Brain and Melody Creation Brain — live constraint, not post-processing filter |
| **Every protocol designed with Cursor** | All emotion descriptions, harmonic rules, role constraints, and operating protocols are designed during development — never auto-generated |
