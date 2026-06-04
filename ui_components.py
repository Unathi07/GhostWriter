import streamlit as st


def apply_theme():
    # css for making streamlit look less plain
    st.markdown(
        """
        <style>
        /* main colors */
        :root {
            --gw-bg: #f8fbff;
            --gw-ink: #20313d;
            --gw-muted: #6d7b86;
            --gw-panel: rgba(255, 255, 255, 0.84);
            --gw-panel-strong: #ffffff;
            --gw-border: rgba(77, 116, 142, 0.18);
            --gw-blue: #3f8fbd;
            --gw-blue-deep: #17658d;
            --gw-mint: #cfeee1;
            --gw-cream: #fff5ea;
            --gw-shadow: 0 24px 70px rgba(55, 94, 119, 0.16);
        }

        /* soft ai page background */
        .stApp {
            background:
                radial-gradient(circle at 51% 36%, rgba(181, 224, 255, 0.72) 0, rgba(181, 224, 255, 0.44) 20%, rgba(248, 251, 255, 0) 46%),
                linear-gradient(135deg, var(--gw-cream) 0%, #f9fcff 42%, #f2faf6 100%);
            color: var(--gw-ink);
            font-family: "Trebuchet MS", "Aptos", sans-serif;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1120px;
            padding-top: 3.5rem;
            padding-bottom: 3.5rem;
        }

        h1, h2, h3 {
            color: var(--gw-ink);
            font-family: Georgia, "Times New Roman", serif;
            letter-spacing: -0.04em;
            font-weight: 500;
        }

        p, label, span, div {
            color: var(--gw-ink);
        }

        .stCaption,
        [data-testid="stCaptionContainer"] {
            color: var(--gw-muted);
        }

        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, 0.74);
            border-right: 1px solid var(--gw-border);
            box-shadow: 14px 0 45px rgba(53, 95, 126, 0.08);
            backdrop-filter: blur(18px);
        }

        /* side menu */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1.4rem;
        }

        .gw-brand {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 0.75rem;
            padding: 0.25rem 0 1.25rem;
            border-bottom: 1px solid var(--gw-border);
            margin-bottom: 1rem;
        }

        .gw-logo-mark {
            display: grid;
            place-items: center;
            width: 44px;
            height: 44px;
            flex: 0 0 auto;
            border-radius: 15px;
            background: linear-gradient(140deg, #fdfdf8 0%, #bde4ff 54%, var(--gw-mint) 100%);
            border: 1px solid rgba(42, 112, 153, 0.18);
            box-shadow: 0 12px 28px rgba(63, 143, 189, 0.18);
            color: var(--gw-blue-deep);
            font-size: 0.8rem;
            font-weight: 850;
            letter-spacing: 0.08em;
        }

        .gw-title {
            margin: 0;
            color: var(--gw-ink);
            font-family: Georgia, "Times New Roman", serif;
            font-size: 1.25rem;
            line-height: 1;
            font-weight: 600;
        }

        .gw-tagline {
            margin: 0.2rem 0 0;
            color: var(--gw-muted);
            font-size: 0.78rem;
        }

        [data-testid="stSidebar"] [role="radiogroup"] {
            display: grid;
            gap: 0.55rem;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            min-height: 3rem;
            padding: 0.4rem 0.75rem;
            border: 1px solid var(--gw-border);
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.56);
            box-shadow: 0 10px 26px rgba(72, 113, 143, 0.08);
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            border-color: rgba(63, 143, 189, 0.38);
            background: rgba(255, 255, 255, 0.9);
        }

        .gw-sidebar-context {
            margin-top: 1.4rem;
            padding: 1rem;
            border: 1px solid var(--gw-border);
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.58);
        }

        /* little song summary */
        .gw-mini-label {
            margin: 0 0 0.45rem;
            color: var(--gw-blue-deep);
            font-size: 0.72rem;
            font-weight: 850;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }

        .gw-sidebar-song {
            margin: 0;
            color: var(--gw-ink);
            font-size: 0.92rem;
            line-height: 1.45;
        }

        .gw-sidebar-note {
            margin: 0.45rem 0 0;
            color: var(--gw-muted);
            font-size: 0.78rem;
        }

        /* main ai landing area */
        .gw-hero {
            max-width: 790px;
            margin: 6vh auto 2.2rem;
            text-align: center;
            animation: gwFadeUp 0.55s ease-out both;
        }

        .gw-ai-mark {
            display: grid;
            place-items: center;
            width: 58px;
            height: 58px;
            margin: 0 auto 1.1rem;
            border-radius: 21px;
            color: var(--gw-blue-deep);
            background:
                linear-gradient(#ffffff, #ffffff) padding-box,
                linear-gradient(140deg, #78c5ff, #cfeee1, #ffe0c0) border-box;
            border: 2px solid transparent;
            box-shadow: var(--gw-shadow);
            font-size: 0.9rem;
            font-weight: 900;
            letter-spacing: 0.1em;
        }

        .gw-eyebrow {
            margin: 0 0 0.4rem;
            color: var(--gw-blue-deep);
            font-size: 0.78rem;
            font-weight: 850;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .gw-hero h1 {
            margin: 0;
            font-size: clamp(2.8rem, 6vw, 5.4rem);
            line-height: 0.94;
        }

        .gw-hero-copy {
            max-width: 560px;
            margin: 1.1rem auto 0;
            color: var(--gw-muted);
            font-size: 1.04rem;
            line-height: 1.7;
        }

        .gw-page-heading {
            max-width: 720px;
            margin-bottom: 1.8rem;
            animation: gwFadeUp 0.5s ease-out both;
        }

        .gw-page-heading h1 {
            margin: 0;
            font-size: clamp(2.4rem, 5vw, 4.6rem);
            line-height: 0.96;
        }

        .gw-page-heading p:last-child {
            margin-top: 0.8rem;
            color: var(--gw-muted);
            font-size: 1.04rem;
        }

        /* make the normal streamlit buttons fit the design */
        .stButton > button,
        .stDownloadButton > button {
            min-height: 2.9rem;
            border-radius: 999px;
            border: 1px solid var(--gw-border);
            background: var(--gw-panel-strong);
            color: var(--gw-ink);
            box-shadow: 0 10px 28px rgba(69, 102, 123, 0.1);
            transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: rgba(63, 143, 189, 0.6);
            color: var(--gw-blue-deep);
            box-shadow: 0 14px 36px rgba(63, 143, 189, 0.18);
            transform: translateY(-1px);
        }

        .stTextInput input,
        .stTextArea textarea,
        [data-baseweb="select"] > div {
            border-color: var(--gw-border);
            background-color: var(--gw-panel);
            color: var(--gw-ink);
            border-radius: 24px;
            box-shadow: var(--gw-shadow);
        }

        .stTextArea textarea {
            padding: 1.15rem 1.25rem;
            line-height: 1.55;
        }

        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stExpander"] {
            border-color: var(--gw-border);
            background: rgba(255, 255, 255, 0.68);
            border-radius: 22px;
            box-shadow: 0 14px 42px rgba(72, 113, 143, 0.08);
        }

        hr {
            border-color: var(--gw-border);
        }

        /* little fade-in */
        @keyframes gwFadeUp {
            from {
                opacity: 0;
                transform: translateY(14px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* phone layout */
        @media (max-width: 760px) {
            .block-container {
                padding-top: 2rem;
            }

            .gw-hero {
                margin-top: 1.2rem;
                text-align: left;
            }

            .gw-ai-mark {
                margin-left: 0;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_brand_header():
    # small logo so the sidebar does not feel crowded
    st.markdown(
        """
        <div class="gw-brand">
            <div class="gw-logo-mark">GW</div>
            <div>
                <h1 class="gw-title">GhostWriter</h1>
                <p class="gw-tagline">AI, lyrics, chords</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_progression_chords(progression):
    # chord blocks are easier to read than one long line
    chord_columns = st.columns(4)

    for index, chord_name in enumerate(progression):
        with chord_columns[index % 4]:
            with st.container(border=True):
                st.markdown(f"**{index + 1}. {chord_name}**")


def show_add_chord_buttons(chords, key_prefix):
    # quick buttons for adding chords
    chord_columns = st.columns(4)

    for index, chord_name in enumerate(chords):
        # streamlit needs every button to have its own key
        button_key = f"{key_prefix}_{index}_{chord_name}"

        with chord_columns[index % 4]:
            if st.button(chord_name, key=button_key):
                st.session_state.progression.append(chord_name)
                st.rerun()
