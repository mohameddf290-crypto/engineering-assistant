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
