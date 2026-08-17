from pathlib import Path

import streamlit as st


ICON_PATH = Path(__file__).parent / "assets" / "ghostwriter-mark-quaver.svg"


def apply_theme():
    # css for making streamlit look less plain
    st.markdown(
        """
        <style>
        /* main colors */
        :root {
            --gw-bg: #ffffff;
            --gw-ink: #1a1a1a;
            --gw-muted: #636366;
            --gw-panel: #f2f2f7;
            --gw-panel-strong: #e5e5ea;
            --gw-border: #d1d1d6;
            --gw-purple: #805ad5;
            /* the rgb triplet lets the wash tints below derive from the brand
               purple itself, instead of a second hardcoded purple */
            --gw-purple-rgb: 128, 90, 213;
            /* tint is a surface, ink is for text - one token cannot do both */
            --gw-purple-tint: #faf5ff;
            --gw-purple-ink: #6b46c1;
            --gw-white: #ffffff;
            --gw-sidebar: #f7f7fa;

            /* status colours, same 600-level weight as the brand purple */
            --gw-danger: #c53030;
            --gw-warning: #b7791f;
            --gw-success: #2f855a;
            --gw-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }

        /* light app background */
        .stApp {
            background-color: var(--gw-bg);
            color: var(--gw-ink);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-size: 0.9rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3 {
            color: var(--gw-ink);
            font-weight: 600;
            letter-spacing: -0.02em;
        }

        h1 { font-size: 1.8rem; }
        h2 { font-size: 1.4rem; }
        h3 { font-size: 1.1rem; }

        p, label, span, div {
            color: var(--gw-ink);
        }

        .stCaption,
        [data-testid="stCaptionContainer"] {
            color: var(--gw-muted);
            font-size: 0.8rem;
        }

        [data-testid="stSidebar"] {
            background: var(--gw-sidebar);
            border-right: 1px solid var(--gw-border);
        }

        /* side menu */
        [data-testid="stSidebar"] > div:first-child {
            padding-top: 1rem;
        }

        .gw-brand {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            gap: 0.5rem;
            padding: 0 0 1rem;
            border-bottom: 1px solid var(--gw-border);
            margin-bottom: 1rem;
        }

        .gw-logo-mark {
            display: grid;
            place-items: center;
            width: 32px;
            height: 32px;
            flex: 0 0 auto;
        }

        .gw-logo-mark svg {
            display: block;
            width: 100%;
            height: 100%;
        }

        .gw-title {
            margin: 0;
            color: var(--gw-ink);
            font-size: 1rem;
            line-height: 1;
            font-weight: 600;
        }

        .gw-tagline {
            margin: 0.1rem 0 0;
            color: var(--gw-muted);
            font-size: 0.7rem;
        }

        [data-testid="stSidebar"] [role="radiogroup"] {
            display: grid;
            gap: 0.25rem;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            min-height: 2.5rem;
            padding: 0.25rem 0.75rem;
            border: none;
            border-radius: 8px;
            background: transparent;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: rgba(var(--gw-purple-rgb), 0.1);
        }

        [data-testid="stSidebarNavigation"] ul li:has(input:checked) {
            background-color: rgba(var(--gw-purple-rgb), 0.2);
        }

        .gw-sidebar-context {
            margin-top: 1rem;
            padding: 0.75rem;
            border: 1px solid var(--gw-border);
            border-radius: 12px;
            background: var(--gw-panel);
        }

        /* little song summary */
        .gw-mini-label {
            margin: 0 0 0.25rem;
            color: var(--gw-purple-ink);
            font-size: 0.65rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .gw-sidebar-song {
            margin: 0;
            color: var(--gw-ink);
            font-size: 0.8rem;
            line-height: 1.4;
        }

        .gw-sidebar-note {
            margin: 0.25rem 0 0;
            color: var(--gw-muted);
            font-size: 0.7rem;
        }

        /* main ai landing area */
        .gw-hero {
            max-width: 600px;
            margin: 4vh auto 2rem;
            text-align: center;
        }

        .gw-ai-mark {
            display: grid;
            place-items: center;
            width: 60px;
            height: 32px;
            margin: 0 auto 0.75rem;
            border-radius: 16px;
            color: var(--gw-white);
            background: var(--gw-purple);
            font-size: 0.75rem;
            font-weight: 600;
        }

        .gw-eyebrow {
            margin: 0 0 0.25rem;
            color: var(--gw-purple-ink);
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .gw-hero h1 {
            margin: 0;
            font-size: 2.2rem;
            line-height: 1.1;
        }

        .gw-hero-copy {
            max-width: 480px;
            margin: 0.75rem auto 0;
            color: var(--gw-muted);
            font-size: 0.9rem;
            line-height: 1.5;
        }

        .gw-page-heading {
            max-width: 720px;
            margin-bottom: 1.5rem;
        }

        .gw-page-heading h1 {
            margin: 0;
            font-size: 1.8rem;
        }

        .gw-page-heading p:last-child {
            margin-top: 0.5rem;
            color: var(--gw-muted);
            font-size: 0.9rem;
        }

        /* make the normal streamlit buttons fit the design */
        .stButton > button,
        .stDownloadButton > button {
            min-height: 2.5rem;
            border-radius: 8px;
            border: 1px solid var(--gw-border);
            background: var(--gw-panel-strong);
            color: var(--gw-ink);
            font-size: 0.85rem;
            transition: all 0.2s;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            border-color: var(--gw-purple);
            color: var(--gw-purple-ink);
            background: rgba(var(--gw-purple-rgb), 0.05);
        }

        /* the override above also caught type="primary" buttons, which left the
           app with no visually primary action - give them the brand purple back */
        .stButton > button[kind="primary"] {
            border-color: var(--gw-purple);
            background: var(--gw-purple);
            font-weight: 600;
        }

        /* the blanket "p, label, span, div" colour rule above beats anything set
           on the button itself, so the label has to be targeted directly */
        .stButton > button[kind="primary"],
        .stButton > button[kind="primary"] p,
        .stButton > button[kind="primary"] div,
        .stButton > button[kind="primary"] span {
            color: var(--gw-white);
        }

        .stButton > button[kind="primary"]:hover {
            border-color: var(--gw-purple-ink);
            background: var(--gw-purple-ink);
        }

        .stTextInput input,
        .stTextArea textarea,
        [data-baseweb="select"] > div {
            border-color: var(--gw-border);
            background-color: var(--gw-panel) !important;
            color: var(--gw-ink) !important;
            border-radius: 8px;
            font-size: 0.9rem !important;
        }

        .stTextArea textarea {
            padding: 0.75rem;
        }

        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stExpander"] {
            border-color: var(--gw-border);
            background: var(--gw-panel);
            border-radius: 12px;
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
    icon_svg = ICON_PATH.read_text(encoding="utf-8")

    st.markdown(
        f"""
        <div class="gw-brand">
            <div class="gw-logo-mark">{icon_svg}</div>
            <div>
                <h1 class="gw-title">GhostWriter</h1>
                <p class="gw-tagline">Ghost, lyrics, chords</p>
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
