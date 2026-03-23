const pianoRoll = {
    MIDI_MIN: 24,
    MIDI_MAX: 96,

    getNoteY(canvas, midi) {
        const range = this.MIDI_MAX - this.MIDI_MIN;
        return canvas.height - ((midi - this.MIDI_MIN) / range) * (canvas.height - 20) - 10;
    },

    getTimeX(canvas, beatPos, totalBeats) {
        return 40 + (beatPos / totalBeats) * (canvas.width - 50);
    },

    renderChords(canvasId, progression, lengthBars) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const totalBeats = (lengthBars || 4) * 4;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#0d0d15';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        this._drawGrid(ctx, canvas, totalBeats);

        let beatPos = 0;
        const chordColors = [
            'rgba(124,58,237,0.7)', 'rgba(6,182,212,0.7)', 'rgba(16,185,129,0.7)',
            'rgba(245,158,11,0.7)', 'rgba(239,68,68,0.7)', 'rgba(236,72,153,0.7)'
        ];

        (progression || []).forEach((chord, i) => {
            const x = this.getTimeX(canvas, beatPos, totalBeats);
            const dur = chord.duration_beats || 4;
            const nextX = this.getTimeX(canvas, beatPos + dur, totalBeats);
            const w = nextX - x - 2;

            const color = chordColors[i % chordColors.length];
            (chord.midi_notes || []).forEach((midi) => {
                const y = this.getNoteY(canvas, midi);
                const noteH = Math.max(3, (canvas.height - 20) / (this.MIDI_MAX - this.MIDI_MIN));
                ctx.fillStyle = color;
                ctx.fillRect(x, y - noteH / 2, w, noteH + 1);
            });

            ctx.fillStyle = '#fff';
            ctx.font = '11px monospace';
            ctx.fillText(chord.name || '', x + 4, 16);

            beatPos += dur;
        });

        this._drawYAxis(ctx, canvas);
    },

    renderMelodies(canvasId, melodies, progression, lengthBars) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const totalBeats = (lengthBars || 4) * 4;
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        ctx.fillStyle = '#0d0d15';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        this._drawGrid(ctx, canvas, totalBeats);

        // Draw chord background
        let beatPos = 0;
        if (progression) {
            progression.forEach((chord, i) => {
                const x = this.getTimeX(canvas, beatPos, totalBeats);
                const dur = chord.duration_beats || 4;
                const nextX = this.getTimeX(canvas, beatPos + dur, totalBeats);
                ctx.fillStyle = i % 2 === 0 ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.06)';
                ctx.fillRect(x, 0, nextX - x, canvas.height);

                ctx.fillStyle = 'rgba(255,255,255,0.4)';
                ctx.font = '10px monospace';
                ctx.fillText(chord.name || '', x + 4, 14);

                beatPos += dur;
            });
        }

        // Draw melody notes
        const roleColors = {
            lead: '#7c3aed', counter_melody: '#06b6d4', ear_candy: '#f59e0b',
            pad_melody: '#10b981', bass_line: '#ef4444'
        };

        Object.entries(melodies).forEach(([role, notes]) => {
            const color = roleColors[role] || '#888';
            (notes || []).forEach(note => {
                const x = this.getTimeX(canvas, note.position_beats, totalBeats);
                const w = Math.max(4, (note.duration_beats / totalBeats) * (canvas.width - 50) - 2);
                const y = this.getNoteY(canvas, note.pitch_midi);
                const noteH = 8;

                ctx.fillStyle = color;
                ctx.beginPath();
                if (ctx.roundRect) {
                    ctx.roundRect(x, y - noteH / 2, w, noteH, 2);
                } else {
                    ctx.rect(x, y - noteH / 2, w, noteH);
                }
                ctx.fill();

                // Velocity indicator
                ctx.fillStyle = 'rgba(255,255,255,0.3)';
                ctx.fillRect(x, y - noteH / 2, 3, noteH);
            });
        });

        this._drawYAxis(ctx, canvas);
    },

    _drawGrid(ctx, canvas, totalBeats) {
        for (let b = 0; b <= totalBeats; b++) {
            const x = this.getTimeX(canvas, b, totalBeats);
            ctx.strokeStyle = b % 4 === 0 ? 'rgba(255,255,255,0.15)' : 'rgba(255,255,255,0.05)';
            ctx.lineWidth = b % 4 === 0 ? 1.5 : 0.5;
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();

            if (b % 4 === 0) {
                ctx.fillStyle = 'rgba(255,255,255,0.5)';
                ctx.font = '9px monospace';
                ctx.fillText('Bar' + (b / 4 + 1), x + 2, canvas.height - 3);
            }
        }

        for (let midi = this.MIDI_MIN; midi <= this.MIDI_MAX; midi++) {
            if (midi % 12 === 0) {
                const y = this.getNoteY(canvas, midi);
                ctx.strokeStyle = 'rgba(255,255,255,0.1)';
                ctx.lineWidth = 0.5;
                ctx.beginPath();
                ctx.moveTo(40, y);
                ctx.lineTo(canvas.width, y);
                ctx.stroke();
            }
        }
    },

    _drawYAxis(ctx, canvas) {
        ctx.fillStyle = '#13131a';
        ctx.fillRect(0, 0, 40, canvas.height);

        for (let midi = this.MIDI_MIN; midi <= this.MIDI_MAX; midi += 12) {
            const y = this.getNoteY(canvas, midi);
            const octave = Math.floor(midi / 12) - 1;
            ctx.fillStyle = '#aaa';
            ctx.font = '9px monospace';
            ctx.fillText('C' + octave, 2, y + 3);
        }
    }
};
