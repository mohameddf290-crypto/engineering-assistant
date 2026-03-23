const melodiesUI = {
    complexity: 'medium',
    mode: 'normal',
    length: 4,
    role: 'lead',

    setComplexity(c) {
        this.complexity = c;
        this._updateToggle('.controls-section .toggle-group:not(.role-group)', c, ['simple', 'medium', 'complex']);
    },

    setMode(m) {
        this.mode = m;
    },

    setLength(l) {
        this.length = l;
    },

    setRole(r) {
        this.role = r;
        document.querySelectorAll('.role-group .toggle-btn').forEach(b => {
            const map = { 'Lead': 'lead', 'Counter': 'counter_melody', 'Ear Candy': 'ear_candy', 'Pad': 'pad_melody', 'Bass': 'bass_line' };
            b.classList.toggle('active', map[b.textContent] === r);
        });
    },

    _updateToggle(selector, value, options) {
        // Not used — role toggles are handled inline in setRole
    },

    setProgression(prog) {
        app.state.currentProgression = prog;
        const container = document.getElementById('melody-chord-display');
        if (!container) return;
        container.innerHTML = (prog.progression || []).map(c =>
            `<span class="chord-pill">${c.name || ''}</span>`).join('');
    },

    async generate() {
        const prog = app.state.currentProgression;
        if (!prog) return app.showError('No progression. Go to Chord Generator first.');

        try {
            const result = await app.apiCall('/melodies/generate', 'POST', {
                progression: prog.progression,
                key: app.state.currentKey || 'C',
                scale: app.state.currentScale || 'major',
                complexity: this.complexity,
                mode: this.mode,
                role: this.role,
                length: this.length
            });
            app.state.currentMelodies[this.role] = result.melody;
            this.renderRolesPanel();
            pianoRoll.renderMelodies('melody-canvas', app.state.currentMelodies, prog.progression, this.length);
            playback.loadData(prog.progression, app.state.currentMelodies);
        } catch (e) {
            app.showError('Failed to generate melody: ' + e.message);
        }
    },

    async regenerateSimilar() {
        const melody = app.state.currentMelodies[this.role];
        if (!melody) return this.generate();
        const prog = app.state.currentProgression;
        try {
            const result = await app.apiCall('/melodies/regenerate-similar', 'POST', {
                melody, progression: prog.progression,
                key: app.state.currentKey || 'C', scale: app.state.currentScale || 'major', role: this.role
            });
            app.state.currentMelodies[this.role] = result.melody;
            this.renderRolesPanel();
            pianoRoll.renderMelodies('melody-canvas', app.state.currentMelodies, prog.progression, this.length);
        } catch (e) {
            app.showError('Failed: ' + e.message);
        }
    },

    async regenerateDifferent() {
        const melody = app.state.currentMelodies[this.role];
        if (!melody) return this.generate();
        const prog = app.state.currentProgression;
        try {
            const result = await app.apiCall('/melodies/regenerate-different', 'POST', {
                melody, progression: prog.progression,
                key: app.state.currentKey || 'C', scale: app.state.currentScale || 'major', role: this.role
            });
            app.state.currentMelodies[this.role] = result.melody;
            this.renderRolesPanel();
            pianoRoll.renderMelodies('melody-canvas', app.state.currentMelodies, prog.progression, this.length);
        } catch (e) {
            app.showError('Failed: ' + e.message);
        }
    },

    async addRole() {
        const roles = ['lead', 'counter_melody', 'ear_candy', 'pad_melody', 'bass_line'];
        const existingRoles = Object.keys(app.state.currentMelodies);
        const nextRole = roles.find(r => !existingRoles.includes(r));
        if (!nextRole) return app.showError('All roles already added');

        const lead = app.state.currentMelodies['lead'] || null;
        const prog = app.state.currentProgression;
        if (!prog) return app.showError('Generate a progression first');

        try {
            const result = await app.apiCall('/melodies/generate-role', 'POST', {
                progression: prog.progression,
                key: app.state.currentKey || 'C', scale: app.state.currentScale || 'major',
                role: nextRole, lead_melody: lead
            });
            app.state.currentMelodies[nextRole] = result.melody;
            this.renderRolesPanel();
            pianoRoll.renderMelodies('melody-canvas', app.state.currentMelodies, prog.progression, this.length);
            playback.loadData(prog.progression, app.state.currentMelodies);
        } catch (e) {
            app.showError('Failed to add role: ' + e.message);
        }
    },

    async elongate() {
        const melody = app.state.currentMelodies[this.role];
        if (!melody) return app.showError('Generate melody first');
        const prog = app.state.currentProgression;
        try {
            const result = await app.apiCall('/melodies/elongate', 'POST', {
                melody, progression: prog.progression,
                key: app.state.currentKey || 'C', scale: app.state.currentScale || 'major'
            });
            app.state.currentMelodies[this.role] = result.melody;
            pianoRoll.renderMelodies('melody-canvas', app.state.currentMelodies, prog.progression, this.length * 2);
        } catch (e) {
            app.showError('Elongate failed: ' + e.message);
        }
    },

    renderRolesPanel() {
        const container = document.getElementById('active-roles');
        if (!container) return;
        container.innerHTML = '';
        const roleColors = {
            lead: '#7c3aed', counter_melody: '#06b6d4', ear_candy: '#f59e0b',
            pad_melody: '#10b981', bass_line: '#ef4444'
        };
        Object.keys(app.state.currentMelodies).forEach(role => {
            const div = document.createElement('div');
            div.className = 'role-item';
            const color = roleColors[role] || '#888';
            div.innerHTML = `<span class="role-dot" style="background:${color}"></span>
                <span class="role-name">${role.replace(/_/g, ' ')}</span>
                <button class="btn-small" onclick="melodiesUI.setRole('${role}')">Select</button>
                <button class="btn-small danger" onclick="melodiesUI.removeRole('${role}')">✕</button>`;
            container.appendChild(div);
        });
    },

    removeRole(role) {
        delete app.state.currentMelodies[role];
        this.renderRolesPanel();
        const prog = app.state.currentProgression;
        if (prog) pianoRoll.renderMelodies('melody-canvas', app.state.currentMelodies, prog.progression, this.length);
    }
};
