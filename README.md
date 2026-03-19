# 🎛️ Engineering Assistant — Music Production AI

> *"This app doesn't think like any AI. Every brain is built from scratch. Default AI thinking: annihilated."*

---

## 🔥 Philosophy: Annihilating Default AI Thinking

This app is not built on top of default AI behaviour — it is built **against** it. Every operating system inside this application is engineered from the ground up, with zero tolerance for the patterns that make AI tools generic, vague, and useless in professional creative workflows.

- **Every "brain" / operating system is custom-built from the ground up.** No plug-and-play AI defaults. No borrowed logic. Every single module is invented, defined, and enforced by hand.
- **Default AI behaviour is explicitly destroyed and replaced.** Vague suggestions, safe/bland outputs, generic advice — all of it is annihilated before the first line of real logic is written.
- **Each OS follows strict protocols, instructions, and definitions** — no room for lazy interpretation, hedged language, or generic output. Every answer is specific, actionable, and precise.
- **The system thinks like a genius producer, not like a chatbot.** It knows how plugins work at a parameter level. It knows what "shimmery" means for a hi-hat vs. a synth pad. It knows how to chain effects to create something that rivals a top-tier engineer.
- **Every operation must be detailed, specific, mouse-level precise, and genuinely creative.** Instructions are not suggestions. They are exact, step-by-step, parameter-level directions.
- **"No excuse, no garbage, no AI slop" is the operating principle.** If an output isn't genius-level, it doesn't ship.
- **We don't adapt AI defaults. We ANNIHILATE them and build from zero**, inventing the most intelligent, protocol-driven brains possible for each operating system.
- **During both planning AND coding with Cursor, problem simulations are run proactively** — imagining every possible problem (creative, coding, workflow, app-level) and pre-attributing solutions before they occur.

---

## 🎯 Core Workflow (User Journey) — 13 Phases

### Phase 1 — Instrument Selection
Pick instruments for the song: synths, piano, kick, hi-hat, snare, bass, etc. For each instrument, tag the desired sonic outcomes: **glassy, shimmery, plucky, full, spacey, warm, punchy, airy**, etc. Multiple outcomes can be stacked per instrument and the system knows how to balance them perfectly.

### Phase 2 — Preset Selection
The app maps every instrument's desired outcomes to the best available presets across the user's entire plugin library. For synthesizers and any plugin with tweakable macro parameters, the system knows how to **create a sound from scratch** — not just pick one. The selected presets are the objectively best match for the requested outcomes, not a generic suggestion.

### Phase 3 — Source Preparation
Before anything is arranged, the system delivers detailed, **mouse-level precise** instructions for every selected preset inside its plugin. Kick envelopes shaped to spec. Synth oscillators tuned to purpose. Every source instrument is sculpted according to the outcome targets before it enters the arrangement. No guessing, no approximation.

### Phase 4 — Arrangement
The user arranges the song in FL Studio — melodies, harmonies, structure, rhythmic layers. The app has done its job preparing the sources; now the creative process happens in the DAW.

### Phase 5 — Checkpoint 1: Preset Update
The user sends the full arranged song **plus** individual stems **plus** bus stems to the app. The app listens to the rough arrangement in full context. Some presets and drums are confirmed; others are replaced, layered, or redesigned based on how the arrangement sits together. The user receives an updated preset selection with full reasoning and instructions.

### Phase 6 — Problem Detection
Essentia + Neutron 5 + SmartEQ + additional detection plugins analyze every instrument, every bus, and the full mix. The user defines exactly what categories of problems Essentia should scan for. Detection is exhaustive — nothing is skipped.

### Phase 7 — Problem Translation
A custom-coded translation system (integrated into the app) converts raw Essentia diagnostics and plugin analysis data into **human-readable, actionable problem descriptions**. Every issue is named, explained, and scoped to its instrument or bus.

### Phase 8 — Engineering Phase 1: Clean Mix
For every problem in the full problem list, the app generates **detailed operations** using the user's plugins and their manuals. It knows which plugins are available, what each parameter does, and how to combine them. Instructions are mouse-level: click this, set this to this value, enable this, chain this plugin next.

### Phase 9 — Per-Instrument Verification
After the user applies the instructions for each instrument, they send it back to the app. The app uses Essentia to confirm whether the problem is resolved. If yes: thumbs up. If no: specific corrective feedback. This verification loop runs for every instrument, in both Phase 1 and Phase 2.

### Phase 10 — Checkpoint 2: Re-analysis
The full song is re-analyzed (third checkpoint). Updated preset operations at this stage are lighter and optional. Focus shifts to safe, final source decisions: layering, redesigning, subtle character adjustments.

### Phase 11 — Gap Analysis (Clean → Ideal)
The cleaned, engineered song is re-analyzed through Essentia and plugins. This time, the goal is to generate a **gap list**: the precise delta between the current clean mix and the ideal mix where every instrument is filled with the desired energy (spacey, shimmery, full, punchy, etc.). Every gap is documented and scoped.

### Phase 12 — Engineering Phase 2: Ideal Mix
For every identified gap, the app generates operations to bridge it. Same level of genius, same level of detail, same mouse-level instruction quality as Phase 1 — but now targeted at elevating each instrument from technically clean to emotionally and sonically ideal.

### Phase 13 — Final Output
Industry-grade song. Nothing less.

---

## 🧠 Core Operating Systems (14 Brains)

Each brain listed below replaces default AI thinking with a custom-designed protocol. Every one of them is built from scratch.

---

### 1. Outcomes Definition Engine
**File:** `core/outcomes_engine.py`

**Purpose:** Holds strict, embedded definitions for every sonic outcome (glassy, shimmery, plucky, full, spacey, warm, punchy, airy, etc.). These are not vague descriptions — they are precise, actionable specifications that drive every downstream decision in the app.

**Default AI thinking replaced:** Generic label matching ("shimmery = high-frequency content"). Replaced with: per-instrument nuanced outcome definitions, stacked outcome balancing logic, and outcome-to-parameter mapping chains.

**Protocols:**
- Every outcome has a unique definition per instrument type (a "full" kick is entirely different from a "full" synth pad)
- When multiple outcomes are selected for one instrument, the engine knows exactly how to weight and balance them
- Outcomes map directly to plugin parameter targets, not abstract descriptions

---

### 2. Preset & Kit Library Manager
**File:** `core/preset_library.py`

**Purpose:** Scans the user's installed plugins, catalogues every available preset, and builds a fully tagged, searchable library annotated by sonic character.

**Default AI thinking replaced:** Manual or assumption-based preset selection. Replaced with: deep automated library scanning, sonic tagging from audio analysis and metadata, and outcome-aligned indexing.

**Protocols:**
- Gets inside each selected plugin and acquires every preset
- Tags each preset with sonic descriptors derived from analysis + metadata
- Maintains a live, updatable library that can be re-scanned on demand

---

### 3. Manual Intelligence System
**File:** `core/manual_intelligence.py`

**Purpose:** Ingests plugin manuals in full, understands every parameter deeply, and becomes more capable of creating creative combinations than any human reading the same manual.

**Default AI thinking replaced:** Surface-level parameter descriptions. Replaced with: deep cross-parameter relationship mapping, creative combination generation, and plugin-specific "genius mode" operation chains.

**Protocols:**
- Studies every parameter, its range, its effect, and its interaction with other parameters
- Generates combinations that a human would not discover by casual reading
- Becomes the authoritative knowledge base for every plugin in the user's arsenal

---

### 4. Preset Selection Brain
**File:** `core/preset_selector.py`

**Purpose:** Maps desired outcomes to the best available presets across the entire library, per instrument type. For synthesizers and plugins with macro/tweakable parameters, it creates sounds from scratch.

**Default AI thinking replaced:** Generic keyword matching against preset names. Replaced with: outcome-aligned deep selection across piano presets, synth presets, guitar presets, kicks, hi-hats, snares — with full instrument-type awareness.

**Protocols:**
- Selects the objectively best preset for each outcome target, not a ranked list of guesses
- For synthesis-capable plugins: generates parameter-level sound creation instructions
- Accounts for stacked outcomes when evaluating preset fit

---

### 5. Source Preparation Instructor
**File:** `core/source_preparation.py`

**Purpose:** Delivers mouse-level, parameter-specific instructions inside each plugin for shaping the selected preset before it enters the arrangement.

**Default AI thinking replaced:** "Adjust the attack on your kick." Replaced with: exact parameter locations, exact values, exact mouse movements inside the specific plugin the user is working with.

**Protocols:**
- Instructions reference the actual plugin UI, not generic DSP concepts
- Every instruction is tied to the specific preset selected for that instrument
- Covers envelopes, oscillators, filters, modulation, effects chains — all of it

---

### 6. Genius Instructions Engine
**File:** `core/genius_instructions.py`

**Purpose:** Thinks like a top-level producer (Aiden Kenway-level creativity). Chains plugin effects creatively: this plugin's output feeding into this plugin's character = something that sounds like it was made by a genius.

**Default AI thinking replaced:** Single-plugin, one-dimensional processing suggestions. Replaced with: multi-plugin creative chain design where the combined result is beautiful and rivals what a world-class engineer would create.

**Protocols:**
- Always thinks in chains, not individual plugins
- Each chain decision is justified by sonic outcome logic
- The combined sound after all plugins are active must be objectively excellent

---

### 7. Essentia Integration
**File:** `analysis/essentia_integration.py`

**Purpose:** Deep audio analysis for problem detection, gap analysis, and verification at every checkpoint.

**Default AI thinking replaced:** Shallow waveform-level analysis or standard loudness checks. Replaced with: full Essentia descriptor extraction, timbral analysis, spectral analysis, rhythm analysis, and problem-specific detection routines.

**Protocols:**
- Whatever is necessary to ensure the best, deepest audio analysis possible
- Must hear problems that a human might miss
- Must hear gaps between a well-engineered song and the ideal song with target outcomes

---

### 8. Essentia Translator
**File:** `analysis/essentia_translator.py`

**Purpose:** A custom-coded translation layer that converts raw Essentia descriptor output into human-readable, actionable problem statements.

**Default AI thinking replaced:** Dumping raw analysis numbers at the user. Replaced with: a mapping system that turns every Essentia diagnostic into a named, explained, instrument-scoped problem statement.

**Protocols:**
- Every raw descriptor maps to a named problem category
- Every problem is described in production language, not math
- Output is always actionable: the problem is stated, its impact is explained, its location is scoped

---

### 9. Problem → Solution Engine
**File:** `problem_solving/solution_engine.py`

**Purpose:** Takes any problem from the problem list and generates a complete series of operations — selecting the ideal plugins, chaining them intelligently, and providing step-by-step fix instructions.

**Default AI thinking replaced:** Generic EQ/compression suggestions. Replaced with: problem-specific plugin selection logic, creative multi-plugin solution chains, and parameter-level instructions for each operation.

**Protocols:**
- Selects plugins based on suitability for the specific problem, not availability alone
- Every solution is a chain of operations, not a single step
- Instructions are mouse-level precise, not conceptual

---

### 10. Engineering Planner
**File:** `core/engineering_planner.py`

**Purpose:** Reads the full problem list for the entire song and creates a phased, intricate engineering plan with per-instrument detailed instructions — for both Phase 1 (clean mix) and Phase 2 (clean to ideal).

**Default AI thinking replaced:** A flat list of suggestions. Replaced with: a structured, phase-separated plan with sequenced operations, dependency awareness, and per-instrument breakdowns.

**Protocols:**
- Separates the plan into clear phases with defined objectives
- Per-instrument instructions are sequenced in the optimal processing order
- Plan accounts for inter-instrument interactions (e.g., kick/bass relationship)

---

### 11. Preset Update System
**File:** `core/preset_updater.py`

**Purpose:** After hearing the fully arranged but unmixed song (Checkpoint 1) and after hearing the cleaned/sculpted song (Checkpoint 2), updates the preset and drum selections intelligently.

**Default AI thinking replaced:** Re-running initial preset selection. Replaced with: context-aware update logic that hears the full arrangement and makes keep/replace/layer decisions based on how everything fits together.

**Protocols:**
- Checkpoint 1 updates are comprehensive: presets can be fully replaced
- Checkpoint 2 updates are lighter and optional: focus on final source polish
- Every update decision is explained with specific sonic reasoning

---

### 12. Verification System
**File:** `core/verification.py`

**Purpose:** Per-instrument and per-phase verification checkpoints. Uses Essentia to confirm whether fix instructions were followed correctly and whether problems are actually resolved.

**Default AI thinking replaced:** Trusting the user's self-assessment. Replaced with: Essentia-powered re-analysis after every instruction set, with a clear thumbs-up or targeted corrective feedback.

**Protocols:**
- Runs after every instrument processing step, in both Phase 1 and Phase 2
- Also verifies preset sounds at the very beginning (before arrangement)
- Output is always binary: fixed or not-fixed, with specifics either way

---

### 13. Clean → Ideal Bridge
**File:** `core/clean_to_ideal.py`

**Purpose:** Hears the engineered, clean song, identifies every gap between the current sound and the desired outcomes, and generates Phase 2 operations to bridge each gap with mouse-level precision.

**Default AI thinking replaced:** Adding "excitement" or "warmth" generically. Replaced with: outcome-mapped gap detection, instrument-specific bridging operations, and a clear path from technically clean to emotionally ideal.

**Protocols:**
- Gap detection is outcome-specific: every gap is measured against the target outcome for that instrument
- Operations are creative, not conservative — the target is ideal, not "better"
- Instructions are at the same genius level as Phase 1

---

### 14. Problem Simulation Engine
**File:** `problem_solving/simulation_engine.py`

**Purpose:** Proactively runs simulations of every problem imaginable — creative, coding, app functionality, workflow, edge cases — and pre-attributes a solution to each one before it occurs.

**Default AI thinking replaced:** Reactive debugging and ad-hoc problem solving. Replaced with: proactive simulation at both the planning and coding stages, ensuring every foreseeable problem has a pre-built solution path.

**Protocols:**
- Runs during both planning and coding with Cursor
- Covers creative problems, technical problems, workflow problems, and user experience problems
- Every simulated problem has an attributed solution stored in the system

---

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

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend + AI + Analysis | Python (Essentia, PyTorch, FastAPI, NumPy, SciPy, librosa) |
| Audio Analysis Engine | Essentia (deep descriptor extraction, problem detection, gap analysis) |
| Frontend (later) | React or Electron |
| Plugin Integration | Neutron 5, SmartEQ, and other production plugins via integration layer |

---

## 📁 Project Structure

```
engineering-assistant/
├── README.md
├── requirements.txt
├── setup.py
├── .gitignore
│
├── config/
│   └── settings.py               # App config, paths, plugin directories
│
├── core/                         # Core operating system brains
│   ├── __init__.py
│   ├── outcomes_engine.py        # Brain 1: Outcomes Definition Engine
│   ├── preset_library.py         # Brain 2: Preset & Kit Library Manager
│   ├── manual_intelligence.py    # Brain 3: Manual Intelligence System
│   ├── preset_selector.py        # Brain 4: Preset Selection Brain
│   ├── source_preparation.py     # Brain 5: Source Preparation Instructor
│   ├── genius_instructions.py    # Brain 6: Genius Instructions Engine
│   ├── engineering_planner.py    # Brain 10: Engineering Planner
│   ├── preset_updater.py         # Brain 11: Preset Update System
│   ├── verification.py           # Brain 12: Verification System
│   └── clean_to_ideal.py         # Brain 13: Clean → Ideal Bridge
│
├── analysis/                     # Audio analysis layer
│   ├── __init__.py
│   ├── essentia_integration.py   # Brain 7: Essentia Integration
│   ├── essentia_translator.py    # Brain 8: Essentia Translator
│   ├── plugin_analyzers.py       # Plugin analysis (Neutron 5, SmartEQ, etc.)
│   └── gap_analyzer.py           # Gap analysis: clean vs ideal
│
├── problem_solving/              # Problem detection and resolution layer
│   ├── __init__.py
│   ├── problem_detector.py       # Problem Detection Aggregator
│   ├── solution_engine.py        # Brain 9: Problem → Solution Engine
│   └── simulation_engine.py      # Brain 14: Problem Simulation Engine
│
├── plugins/                      # Plugin registry and intelligence
│   ├── __init__.py
│   ├── plugin_registry.py        # Registry of all available plugins
│   ├── plugin_manuals.py         # Manual ingestion and understanding
│   └── plugin_chains.py          # Creative plugin chain combinations
│
├── workflow/                     # Full pipeline orchestration
│   ├── __init__.py
│   ├── phase1_clean_mix.py       # Phase 1: Clean Mix engineering
│   ├── phase2_ideal_mix.py       # Phase 2: Clean → Ideal engineering
│   ├── checkpoints.py            # Checkpoint system (3 checkpoints)
│   └── pipeline.py               # Full workflow orchestrator
│
├── audio/                        # Audio I/O and stem handling
│   ├── __init__.py
│   ├── stem_handler.py           # Handle full songs, stems, bus stems
│   └── audio_io.py               # Audio I/O utilities
│
├── chords/                       # Module 2: Infinite Chord Progression Generator
│   ├── __init__.py
│   ├── audio_analysis.py         # Brain 1: Audio Analysis Engine
│   ├── translation.py            # Brain 2: Translation System (Analysis → Plan)
│   ├── chord_creator.py          # Brain 3: Chord Creation Brain
│   ├── infinity_engine.py        # Brain 4: Infinity Engine
│   ├── emotion_system.py         # Brain 5: Emotion Description System
│   ├── prompt_interpreter.py     # Brain 6: Prompt Interpreter
│   ├── chord_mixer.py            # Brain 7: Chord Mixer
│   ├── elongation.py             # Brain 8: Elongation System
│   ├── ai_blocker.py             # Brain 9: AI Blocker
│   └── editor.py                 # Piano Roll-style Editor Logic
│
├── melodies/                     # Module 3: Infinite Melody Generator
│   ├── __init__.py
│   ├── chord_analysis.py         # Brain 1: Chord Analysis Engine
│   ├── song_analysis.py          # Brain 2: Song Analysis Engine
│   ├── translation.py            # Brain 3: Translation System (Analysis → Plan)
│   ├── melody_creator.py         # Brain 4: Melody Creation Brain
│   ├── infinity_engine.py        # Brain 5: Infinity Engine
│   ├── elongation.py             # Brain 6: Elongation System
│   ├── ai_blocker.py             # Brain 7: AI Blocker
│   ├── modification_engine.py    # Brain 8: Modification Engine
│   ├── role_intelligence.py      # Brain 9: Melody Role Intelligence
│   └── editor.py                 # Piano Roll-style Editor Logic
│
├── data/
│   ├── presets/                  # User preset library (gitignored)
│   ├── manuals/                  # Plugin manuals (gitignored)
│   ├── outcomes/                 # Outcome definitions
│   └── analysis_results/         # Essentia analysis outputs (gitignored)
│
└── tests/
    ├── __init__.py
    └── test_placeholder.py
```

---

## 🚀 Development Approach

- **Planning first with Cursor** — every OS brain is fully designed (protocols, instructions, definitions) before a single line of real logic is written
- **Problem simulation at every stage** — the Problem Simulation Engine runs proactively during both planning and coding
- **Each module built independently, tested, then integrated** — no big-bang integration; every brain is verifiable in isolation
- **No default AI patterns** — every system is custom-designed from scratch; generic AI behaviour is not permitted to survive inside this codebase

---

## 📊 Status

`🟡 Planning Phase — Designing operating system brains with Cursor`
