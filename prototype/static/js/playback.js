const playback = {
    isPlaying: false,
    bpm: 120,
    chordData: null,
    melodyData: {},
    synths: {},

    setBPM(bpm) {
        this.bpm = parseInt(bpm);
        const display = document.getElementById('bpm-display');
        if (display) display.textContent = bpm;
        const chordDisplay = document.getElementById('chord-bpm-display');
        if (chordDisplay) chordDisplay.textContent = bpm;
        if (typeof Tone !== 'undefined') Tone.getTransport().bpm.value = this.bpm;
    },

    loadData(progression, melodies) {
        this.chordData = progression;
        this.melodyData = melodies || {};
    },

    getSynth(role) {
        if (this.synths[role]) return this.synths[role];
        let synth;
        switch (role) {
            case 'lead':
                synth = new Tone.Synth({ oscillator: { type: 'sawtooth' }, envelope: { attack: 0.05, decay: 0.1, sustain: 0.6, release: 0.5 } }).toDestination();
                break;
            case 'counter_melody':
                synth = new Tone.Synth({ oscillator: { type: 'square' }, envelope: { attack: 0.05, decay: 0.1, sustain: 0.5, release: 0.5 } }).toDestination();
                break;
            case 'ear_candy':
                synth = new Tone.Synth({ oscillator: { type: 'sine' }, envelope: { attack: 0.01, decay: 0.3, sustain: 0.3, release: 0.8 } }).toDestination();
                break;
            case 'pad_melody':
                synth = new Tone.PolySynth(Tone.Synth, { oscillator: { type: 'triangle' }, envelope: { attack: 0.3, decay: 0.2, sustain: 0.8, release: 1.5 } }).toDestination();
                break;
            case 'bass_line':
                synth = new Tone.Synth({ oscillator: { type: 'triangle' }, envelope: { attack: 0.01, decay: 0.2, sustain: 0.7, release: 0.3 } }).toDestination();
                break;
            default:
                synth = new Tone.Synth().toDestination();
        }
        if (synth.volume) synth.volume.value = -12;
        this.synths[role] = synth;
        return synth;
    },

    midiToNote(midi) {
        const notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        const octave = Math.floor(midi / 12) - 1;
        return notes[midi % 12] + octave;
    },

    async playChordsOnly() {
        if (!this.chordData) return;
        await Tone.start();
        Tone.getTransport().stop();
        Tone.getTransport().cancel();

        Tone.getTransport().bpm.value = this.bpm;
        const chordSynth = new Tone.PolySynth(Tone.Synth, {
            oscillator: { type: 'triangle' },
            envelope: { attack: 0.1, decay: 0.2, sustain: 0.7, release: 0.8 }
        }).toDestination();
        chordSynth.volume.value = -12;

        const secPerBeat = 60 / this.bpm;
        let t = 0;
        this.chordData.forEach(chord => {
            const notes = (chord.midi_notes || []).map(m => this.midiToNote(m));
            const dur = (chord.duration_beats || 4) * secPerBeat;
            Tone.getTransport().schedule(time => {
                chordSynth.triggerAttackRelease(notes, dur - 0.1, time);
            }, t);
            t += (chord.duration_beats || 4) * secPerBeat;
        });

        Tone.getTransport().start();
        this.isPlaying = true;
        const btn = document.getElementById('play-btn');
        if (btn) btn.textContent = '⏸ Pause';
    },

    async playAll() {
        if (!this.chordData) return;
        await Tone.start();
        Tone.getTransport().stop();
        Tone.getTransport().cancel();
        Tone.getTransport().bpm.value = this.bpm;

        // Play chords
        const chordSynth = new Tone.PolySynth(Tone.Synth, {
            oscillator: { type: 'triangle' },
            envelope: { attack: 0.1, decay: 0.2, sustain: 0.7, release: 0.8 }
        }).toDestination();
        chordSynth.volume.value = -12;

        const secPerBeat = 60 / this.bpm;
        let t = 0;
        this.chordData.forEach(chord => {
            const notes = (chord.midi_notes || []).map(m => this.midiToNote(m));
            const dur = (chord.duration_beats || 4) * secPerBeat;
            Tone.getTransport().schedule(time => {
                chordSynth.triggerAttackRelease(notes, dur - 0.1, time);
            }, t);
            t += (chord.duration_beats || 4) * secPerBeat;
        });

        // Play melodies
        Object.entries(this.melodyData).forEach(([role, notes]) => {
            if (!notes || !notes.length) return;
            const synth = this.getSynth(role);
            notes.forEach(note => {
                const noteTime = note.position_beats * secPerBeat;
                const dur = note.duration_beats * secPerBeat - 0.05;
                const noteName = this.midiToNote(note.pitch_midi);
                Tone.getTransport().schedule(time => {
                    try {
                        if (synth.triggerAttackRelease) {
                            synth.triggerAttackRelease(noteName, Math.max(0.05, dur), time);
                        }
                    } catch (e) { /* ignore playback errors */ }
                }, noteTime);
            });
        });

        Tone.getTransport().start();
        this.isPlaying = true;
        const btn = document.getElementById('play-btn');
        if (btn) btn.textContent = '⏸ Pause';
    },

    async togglePlay() {
        if (this.isPlaying) {
            this.stop();
        } else {
            await this.playAll();
        }
    },

    stop() {
        if (typeof Tone !== 'undefined') {
            Tone.getTransport().stop();
            Tone.getTransport().cancel();
        }
        this.isPlaying = false;
        const btn = document.getElementById('play-btn');
        if (btn) btn.textContent = '▶ Play';
    }
};
