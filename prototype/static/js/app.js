/* Main application state and API layer */
const app = {
    state: {
        currentProgression: null,
        keptProgressions: [],
        currentMelodies: {},
        currentKey: 'C',
        currentScale: 'major',
        currentLength: 4,
        selectedEmotions: [],
        view: 'chords'
    },

    showView(viewName) {
        document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
        document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(viewName + '-view').classList.add('active');
        document.getElementById('nav-' + viewName).classList.add('active');
        this.state.view = viewName;
    },

    async apiCall(endpoint, method = 'GET', body = null, isFormData = false) {
        const opts = { method, headers: {} };
        if (body) {
            if (isFormData) {
                opts.body = body;
            } else {
                opts.headers['Content-Type'] = 'application/json';
                opts.body = JSON.stringify(body);
            }
        }
        const res = await fetch('/api' + endpoint, opts);
        if (!res.ok) throw new Error('API error: ' + res.status);
        return res.json();
    },

    showError(msg) {
        console.error(msg);
        const toast = document.createElement('div');
        toast.className = 'toast error';
        toast.textContent = msg;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    },

    showLoading(show) {
        // placeholder for spinner
    }
};

/* Initialize emotion chips and drop zones */
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const data = await app.apiCall('/chords/emotions');
        const container = document.getElementById('emotion-chips');
        data.emotions.forEach(emotion => {
            const chip = document.createElement('button');
            chip.className = 'emotion-chip';
            chip.textContent = emotion;
            chip.dataset.emotion = emotion;
            chip.addEventListener('click', () => {
                chip.classList.toggle('active');
                const idx = app.state.selectedEmotions.indexOf(emotion);
                if (idx >= 0) app.state.selectedEmotions.splice(idx, 1);
                else app.state.selectedEmotions.push(emotion);
            });
            container.appendChild(chip);
        });
    } catch (e) {
        console.error('Failed to load emotions', e);
    }

    // Set up audio drop zones
    _setupDropZone('chord-audio-drop', 'chord-audio-input', async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        try {
            const result = await app.apiCall('/chords/analyze-audio', 'POST', formData, true);
            app.state.currentProgression = result;
            chordsUI.displayProgression(result);
            pianoRoll.renderChords('chord-canvas', result.progression, chordsUI.currentLength);
        } catch (e) {
            app.showError('Audio analysis failed: ' + e.message);
        }
    });

    _setupDropZone('melody-audio-drop', 'melody-audio-input', async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        try {
            const result = await app.apiCall('/melodies/analyze-audio', 'POST', formData, true);
            app.state.currentMelodies[result.role || 'lead'] = result.melody;
            melodiesUI.renderRolesPanel();
            if (app.state.currentProgression) {
                pianoRoll.renderMelodies('melody-canvas', app.state.currentMelodies,
                    app.state.currentProgression.progression, melodiesUI.length);
            }
        } catch (e) {
            app.showError('Audio analysis failed: ' + e.message);
        }
    });
});

function _setupDropZone(zoneId, inputId, onFile) {
    const zone = document.getElementById(zoneId);
    const input = document.getElementById(inputId);
    if (!zone || !input) return;

    zone.addEventListener('click', () => input.click());
    zone.addEventListener('dragover', (e) => { e.preventDefault(); zone.classList.add('drag-over'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
    zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.classList.remove('drag-over');
        if (e.dataTransfer.files.length) onFile(e.dataTransfer.files[0]);
    });
    input.addEventListener('change', () => { if (input.files.length) onFile(input.files[0]); });
}
