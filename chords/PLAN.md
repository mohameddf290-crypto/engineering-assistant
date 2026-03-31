> Source of truth extracted from the root README.md for easy reference by Cursor and other tools.

## 🎹 Module 2: Infinite Chord Progression Generator

Generates deep, professional, human-quality chord progressions — infinitely, from any input — tailored to the user's personal taste profile. Every progression is voiced with purpose, shaped with intentional harmonic rhythm, and screened by the AI Blocker before delivery. The system thinks like a genius producer: no clichés, no patterns recalled from training data, no generic extensions. It creates from a deliberate creation plan built by its 9 operating system brains working in concert.

### Input Methods

| # | Method | Description |
|---|--------|-------------|
| 1 | **Audio Input** | Drop a song or excerpt (no vocals, no drums) → app analyzes harmonic content → generates chord progressions inspired by it |
| 2 | **Emotion Selection** | Select one or multiple emotions/moods/vibes (e.g., nostalgia + excitement, power + melancholy) → generates chords embodying that exact emotional blend |
| 3 | **Prompt** | Write a text description → app reads it, maps to emotion combinations and sonic characteristics, generates chords |

### User Controls & Features

| Feature | Description |
|---------|-------------|
| Length | 4-bar or 8-bar progressions |
| Per-chord duration | Adjust the length of every individual chord |
| Key & Scale | Full key and scale selection |
| Piano roll editor | In-app piano roll-style editor (like FL Studio) — move, resize, and transpose chords |
| Keep + Generate Another | Keep the current progression and generate a new one alongside it |
| Discard + Regenerate | Discard the current result and regenerate entirely |
| Generate Similar | Generate a new progression with the same harmonic DNA |
| Generate Different | Generate a contrasting progression using different harmonic choices |
| Mix 2 Progressions | Intelligently blend any 2 generated progressions into one cohesive result |
| Elongate | Extend any progression by additional bars while maintaining harmonic coherence |
| Drag to FL Studio | Drag-and-drop MIDI export directly to FL Studio |

### Operating System Brains (Chords Module)

---

#### Chords Brain 1 — Audio Analysis Engine
**File:** `chords/audio_analysis.py`

**Purpose:** Best-in-class harmonic analysis of audio input (song/excerpt without vocals and drums). Extracts every piece of harmonic information needed — chord sequences, key, scale, harmonic rhythm, tension/resolution mapping, voice leading patterns, modulation markers — and sends it to the Translation System.

**Default AI thinking replaced:** Shallow key detection or BPM extraction. Replaced with: a full harmonic extraction pipeline that hears chord types, voicings, tension curves, and voice leading tendencies with professional-grade precision.

**Protocols:**
- Analysis is harmonic-first: chroma extraction, chord detection, key/scale identification, harmonic rhythm mapping
- Works only on clean harmonic sources (no vocals, no drums) — a prerequisite enforced before any analysis runs
- Output is a structured `HarmonicAnalysisResult` ready for direct consumption by the Translation System

---

#### Chords Brain 2 — Translation System
**File:** `chords/translation.py`

**Purpose:** Takes raw harmonic analysis data (or emotion descriptors, or a prompt mapping) and converts it into a structured `ChordCreationPlan` — the blueprint that the Chord Creation Brain uses to build every chord.

**Default AI thinking replaced:** Feeding raw audio features directly into generation with no interpretation layer. Replaced with: a deliberate musical intelligence step that reads analysis results and outputs a precise harmonic blueprint with chord quality palette, harmonic rhythm profile, tension strategy, and voice leading rules.

**Protocols:**
- Every analysis result becomes a creation plan — never a parameter dump passed blindly downstream
- The plan includes: target chord quality palette, harmonic rhythm blueprint, tension/resolution strategy, voice leading guidelines, complexity level
- Handles three input paths: from audio analysis, from emotion descriptors, from prompt interpretation

---

#### Chords Brain 3 — Chord Creation Brain
**File:** `chords/chord_creator.py`

**Purpose:** The core skill. Creates deep, professional, human-quality chord voicings from any creation plan. The user's personal taste profile is embedded in this brain's DNA — not as a post-processing filter but as a live constraint shaping every voicing decision.

**Default AI thinking replaced:** Pattern-matched progressions recalled from training data — the same I-V-vi-IV in a different key, the same generic jazz voicings. Replaced with: deliberate harmonic construction where every note in every voicing has a reason, every extension is chosen for harmonic meaning, and every progression is production-ready (full voicing data + MIDI notes).

**Protocols:**
- Every chord is voiced with purpose — no random extension stacking
- Taste profile influences generation without overriding musical coherence
- Output is always production-ready: chord names, full voicing data, and MIDI note data per chord

---

#### Chords Brain 4 — Infinity Engine
**File:** `chords/infinity_engine.py`

**Purpose:** Generates an infinite number of chord progressions from any input without ANY degradation in quality or professionalism. Covers similar regeneration, different regeneration, and every variation in between.

**Default AI thinking replaced:** Re-running the same generation with different random seeds. Replaced with: a structured variation space with explicit similarity axes, controlled variation operators, and a mandatory quality gate on every output.

**Protocols:**
- Similar regeneration: preserves harmonic DNA (key, scale, quality palette, harmonic rhythm) while varying specific chord choices
- Different regeneration: applies contrast operators across multiple dimensions simultaneously (root movement, chord quality, rhythm)
- Quality gate runs on every generation — a degraded result is never delivered

---

#### Chords Brain 5 — Emotion Description System
**File:** `chords/emotion_system.py`

**Purpose:** Contains deep, profound, accurate descriptions of simple and complex emotions — written without AI lenses, embedded directly in the brain. Creates chord progressions for any single emotion or any combination of multiple emotions.

**Default AI thinking replaced:** Mapping "sad = minor chords." Replaced with: a full emotion taxonomy where every emotion has an embedded harmonic descriptor: specific chord qualities, preferred extensions, voice leading tendencies, rhythm profiles, and tension levels. Blended emotions are resolved through a weighting system, never averaged.

**Protocols:**
- Every emotion has unique harmonic correlates — not generic major/minor assignments
- Complex blended emotions (nostalgia + power, melancholy + excitement) have dedicated resolution logic
- Conflict between incompatible emotions is resolved intelligently, never discarded

---

#### Chords Brain 6 — Prompt Interpreter
**File:** `chords/prompt_interpreter.py`

**Purpose:** Reads a text prompt, maps it to emotion combinations and sonic characteristics with full transparency, and feeds the result to the Chord Creation Brain via the Emotion Description System.

**Default AI thinking replaced:** Free-form text-to-chord generation with no intermediate mapping. Replaced with: a deliberate interpretation pipeline — extract emotional intent, map to the Emotion System explicitly, build a creation plan with a traceable path from prompt words to emotion labels to chord choices.

**Protocols:**
- Every prompt is interpreted for emotional content, genre context, energy level, and sonic character
- Interpretation maps explicitly to the Emotion Description System — no bypassing
- Every mapping is explainable: full trace from prompt to emotion labels to chord plan

---

#### Chords Brain 7 — Chord Mixer
**File:** `chords/chord_mixer.py`

**Purpose:** Takes any 2 generated chord progressions and intelligently blends them into a single cohesive progression. The result is musically superior to either input alone — not a naive interleave.

**Default AI thinking replaced:** Simple alternation or averaging of two progressions. Replaced with: compatibility analysis, pivot chord detection, key conflict resolution, and a blend that creates a unified musical identity from two sources.

**Protocols:**
- Both progressions are analysed for compatibility before any blending begins
- Key/scale conflicts are resolved through intelligent pivot chord detection
- The blended result must score above the quality gate threshold before delivery

---

#### Chords Brain 8 — Elongation System
**File:** `chords/elongation.py`

**Purpose:** Extends any chord progression by additional bars while maintaining harmonic coherence, quality, and the character of the original.

**Default AI thinking replaced:** Looping the progression or randomly appending chords. Replaced with: harmonic arc analysis followed by an intelligent continuation that respects the established key, scale, quality palette, and rhythmic feel.

**Protocols:**
- The original progression's harmonic arc is analysed before any extension is written
- Extension respects established key, scale, and harmonic rhythm
- Extended bars feel like a natural continuation — never an appended afterthought

---

#### Chords Brain 9 — AI Blocker
**File:** `chords/ai_blocker.py`

**Purpose:** A hard constraint system that actively screens every generated progression and rejects anything that resembles default AI output. Non-negotiable. Every generation passes through this gate.

**Default AI thinking replaced:** Unconstrained generation. Replaced with: explicit blacklists of AI chord patterns, cliché detectors, bland progression screeners, and a quality score threshold. Rejection is immediate and triggers regeneration — no flagged progression ever reaches the user.

**Protocols:**
- Blacklisted patterns include: I-V-vi-IV and all transpositions, monotone rhythmic grids, parallel-fifths stacking, aimless random extensions
- Every progression receives a quality score; below-threshold results are rejected
- Rejection triggers immediate regeneration from the Chord Creation Brain

---

#### Editor
**File:** `chords/editor.py`

Piano roll-style editor logic for the Chords module. Handles in-app editing of chord progressions: move, resize, and transpose chords in a piano roll interface (like FL Studio).

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
