def render_piano(revised_notes):
    html = f"""
            <div id="piano" style="display: flex; position: relative; height: 150px; margin: 20px;">
            </div>

            <script>
                const activeNotes = {revised_notes};
                const whiteKeys = ["C", "D", "E", "F", "G", "A", "B"];
                const blackKeys = [
        {{note: "C#", left: 25}},
        {{note: "D#", left: 65}},
        {{note: "F#", left: 140}},
        {{note: "G#", left: 185}},
        {{note: "A#", left: 225}},
    ]
                const piano = document.getElementById("piano");

                whiteKeys.forEach(note => {{
                    const key = document.createElement("div");
                    key.style.width = "40px";
                    key.style.height = "140px";
                    key.style.border = "1px solid black"
                    key.style.position = "relative"
                    key.style.display = "inline-block";

                    if (activeNotes.includes(note)) {{
                        key.style.backgroundColor = "lightgreen";
                    }} else {{
                        key.style.backgroundColor = "white";
                    }}

                    piano.appendChild(key);
                }});
                blackKeys.forEach(({{note, left}}) => {{
                    const key = document.createElement("div");
                    key.style.width = "25px";
                    key.style.height = "90px";
                    key.style.border = "1px solid black";
                    key.style.position = "absolute";
                    key.style.left = left + "px";
                    key.style.zIndex = "1";

                    if (activeNotes.includes(note)) {{
                        key.style.backgroundColor = "lightgreen";
                    }}else{{
                        key.style.backgroundColor = "black";
                    }}

                    piano.appendChild(key);

            }});

    const frequencies = {{
        "C": 261.63, "C#": 277.18, "D": 293.66,
        "D#": 311.13, "E": 329.63, "F": 349.23,
        "F#": 369.99, "G": 392.00, "G#": 415.30,
        "A": 440.00, "A#": 466.16, "B": 493.88
    }};

    const btn = document.createElement("button");
    btn.innerText = "▶ Play Chord";
    btn.style.display = "block";
    document.getElementById("piano").after(btn);

    btn.addEventListener("mousedown", () => {{
        window.chordCtx = new AudioContext();
        window.chordCtx.resume();
        window.chordOscs = [];
        activeNotes.forEach(note => {{
            [1, 2, 4].forEach((harmonic, i) => {{
                const osc = window.chordCtx.createOscillator();
                const gain = window.chordCtx.createGain();
                osc.type = "sine";
                osc.frequency.value = frequencies[note] * harmonic;
                const vol = [0.5, 0.25, 0.1][i];
                osc.connect(gain);
                gain.connect(window.chordCtx.destination);
                osc.start();
                gain.gain.setValueAtTime(vol, window.chordCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.00001, window.chordCtx.currentTime + 2.5);
                osc.stop(window.chordCtx.currentTime + 2.5);
                window.chordOscs.push({{osc, gain}});
            }});
        }});
    }});

    btn.addEventListener("mouseup", () => {{
        if (window.chordOscs) {{
            window.chordOscs.forEach(({{osc, gain}}) => {{
                gain.gain.exponentialRampToValueAtTime(0.00001, window.chordCtx.currentTime + 0.3);
                osc.stop(window.chordCtx.currentTime + 0.3);
            }});
        }}
    }});
            </script>
            """
    return html