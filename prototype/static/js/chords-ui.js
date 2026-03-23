const chordsUI = {
    currentLength: 4,

    setLength(bars) {
        this.currentLength = bars;
        document.querySelectorAll('#len-4, #len-8').forEach(b => b.classList.remove('active'));
        const el = document.getElementById('len-' + bars);
        if (el) el.classList.add('active');
    },

    async generate() {
        const key = document.getElementById('key-select').value;
        const scale = document.getElementById('scale-select').value;
        const prompt = document.getElementById('chord-prompt').value;
        const emotions = app.state.selectedEmotions;

        try {
            app.showLoading(true);
            const result = await app.apiCall('/chords/generate', 'POST', {
                emotions, prompt, key, scale, length: this.currentLength
            });
            app.state.currentProgression = result;
            app.state.currentKey = key;
            app.state.currentScale = scale;
            this.displayProgression(result);
            pianoRoll.renderChords('chord-canvas', result.progression, this.currentLength);
            playback.loadData(result.progression, app.state.currentMelodies);
        } catch (e) {
            app.showError('Failed to generate chords: ' + e.message);
        } finally {
            app.showLoading(false);
        }
    },

    async regenerateSimilar() {
        if (!app.state.currentProgression) return app.showError('Generate first');
        try {
            const result = await app.apiCall('/chords/regenerate-similar', 'POST', {
                progression: app.state.currentProgression.progression,
                key: app.state.currentKey, scale: app.state.currentScale
            });
            app.state.currentProgression = result;
            this.displayProgression(result);
            pianoRoll.renderChords('chord-canvas', result.progression, this.currentLength);
            playback.loadData(result.progression, app.state.currentMelodies);
        } catch (e) {
            app.showError('Failed: ' + e.message);
        }
    },

    async regenerateDifferent() {
        if (!app.state.currentProgression) return app.showError('Generate first');
        try {
            const result = await app.apiCall('/chords/regenerate-different', 'POST', {
                progression: app.state.currentProgression.progression,
                key: app.state.currentKey, scale: app.state.currentScale
            });
            app.state.currentProgression = result;
            this.displayProgression(result);
            pianoRoll.renderChords('chord-canvas', result.progression, this.currentLength);
            playback.loadData(result.progression, app.state.currentMelodies);
        } catch (e) {
            app.showError('Failed: ' + e.message);
        }
    },

    keepProgression() {
        if (!app.state.currentProgression) return app.showError('Nothing to keep');
        const idx = app.state.keptProgressions.length;
        app.state.keptProgressions.push({ ...app.state.currentProgression, id: idx });
        this.renderKeptList();
    },

    renderKeptList() {
        const container = document.getElementById('kept-progressions');
        if (!container) return;
        container.innerHTML = '';
        app.state.keptProgressions.forEach((prog, i) => {
            const div = document.createElement('div');
            div.className = 'kept-item';
            const names = prog.progression.map(c => c.name).join(' - ');
            div.innerHTML = `<span class="kept-name">${names}</span>
                <button class="btn-small" onclick="chordsUI.loadKept(${i})">Load</button>
                <button class="btn-small" onclick="chordsUI.selectForMix(${i})">Select</button>`;
            container.appendChild(div);
        });
    },

    loadKept(idx) {
        app.state.currentProgression = app.state.keptProgressions[idx];
        this.displayProgression(app.state.currentProgression);
        pianoRoll.renderChords('chord-canvas', app.state.currentProgression.progression, this.currentLength);
    },

    _mixSelection: [],

    selectForMix(idx) {
        const i = this._mixSelection.indexOf(idx);
        if (i >= 0) this._mixSelection.splice(i, 1);
        else if (this._mixSelection.length < 2) this._mixSelection.push(idx);
        this.renderKeptList();
    },

    async mix() {
        if (this._mixSelection.length < 2) return app.showError('Select 2 progressions to mix');
        try {
            const a = app.state.keptProgressions[this._mixSelection[0]];
            const b = app.state.keptProgressions[this._mixSelection[1]];
            const result = await app.apiCall('/chords/mix', 'POST', {
                progression_a: a.progression, progression_b: b.progression
            });
            app.state.currentProgression = result;
            this.displayProgression(result);
            pianoRoll.renderChords('chord-canvas', result.progression, this.currentLength);
            playback.loadData(result.progression, app.state.currentMelodies);
        } catch (e) {
            app.showError('Mix failed: ' + e.message);
        }
    },

    async elongate() {
        if (!app.state.currentProgression) return app.showError('Generate first');
        try {
            const result = await app.apiCall('/chords/elongate', 'POST', {
                progression: app.state.currentProgression.progression,
                key: app.state.currentKey, scale: app.state.currentScale
            });
            app.state.currentProgression = result;
            this.displayProgression(result);
            pianoRoll.renderChords('chord-canvas', result.progression, result.progression.length);
            playback.loadData(result.progression, app.state.currentMelodies);
        } catch (e) {
            app.showError('Elongate failed: ' + e.message);
        }
    },

    displayProgression(data) {
        const container = document.getElementById('chord-display');
        if (!container) return;
        container.innerHTML = '';
        (data.progression || []).forEach(chord => {
            const div = document.createElement('div');
            div.className = 'chord-card';
            div.innerHTML = `<span class="chord-roman">${chord.roman_numeral || ''}</span>
                <span class="chord-name">${chord.name || ''}</span>
                <span class="chord-duration">${chord.duration_beats || 4}b</span>`;
            container.appendChild(div);
        });
    },

    async playChords() {
        if (!app.state.currentProgression) return app.showError('Generate chords first');
        playback.loadData(app.state.currentProgression.progression, app.state.currentMelodies);
        await playback.playChordsOnly();
    },

    proceedToMelodies() {
        if (!app.state.currentProgression) return app.showError('Generate a progression first');
        app.showView('melodies');
        melodiesUI.setProgression(app.state.currentProgression);
    }
};
