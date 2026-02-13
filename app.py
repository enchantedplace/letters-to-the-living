import streamlit as st
import time
from io import BytesIO
from fpdf import FPDF
from datetime import datetime

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Letters to the Living",
    page_icon="💌",
    layout="centered",
)

# ──────────────────────────────────────────────
# Minimal CSS for the dark forest theme
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,400&family=Quicksand:wght@300;400;500;600&display=swap');

.stApp {
    background-color: #1a1a12 !important;
}
header[data-testid="stHeader"] {
    background-color: #1a1a12 !important;
}

/* Typography — exclude span to preserve Streamlit icon fonts */
.stApp, .stApp p, .stApp li, .stApp label, .stApp div {
    color: #e8dcc8 !important;
    font-family: 'Quicksand', sans-serif !important;
}
/* Restore Material icon font for Streamlit toggle/expand icons */
.stApp [data-testid*="Icon"],
.stApp [data-testid="stExpanderToggleIcon"],
.stApp .material-symbols-rounded {
    font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    -webkit-font-feature-settings: 'liga' !important;
    font-feature-settings: 'liga' !important;
}
.stApp h1, .stApp h2, .stApp h3 {
    font-family: 'Cormorant Garamond', Georgia, serif !important;
    color: #e8dcc8 !important;
    font-weight: 300 !important;
}

/* Expander styling */
[data-testid="stExpander"] {
    background: rgba(42,42,30,0.6) !important;
    border: 1px solid rgba(107,143,78,0.15) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] details,
[data-testid="stExpander"] summary,
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    background: transparent !important;
    border: none !important;
}

/* Text area */
textarea {
    background-color: #2a2a1e !important;
    color: #e8dcc8 !important;
    border: 1px solid rgba(107,143,78,0.2) !important;
    border-radius: 10px !important;
    font-family: 'Quicksand', sans-serif !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
    background-color: #6b8f4e !important;
    color: #1a1a12 !important;
    border: none !important;
    border-radius: 50px !important;
    font-family: 'Quicksand', sans-serif !important;
    font-weight: 600 !important;
}
.stDownloadButton > button {
    background-color: #c4896e !important;
    width: 100%;
}

/* Divider */
hr {
    border-color: rgba(107,143,78,0.25) !important;
}

/* Hide chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PDF generation helper
# ──────────────────────────────────────────────
def _safe(text: str) -> str:
    """Replace Unicode characters unsupported by FPDF built-in fonts."""
    replacements = {
        "\u2014": "--",   # em-dash
        "\u2013": "-",    # en-dash
        "\u2018": "'",    # left single quote
        "\u2019": "'",    # right single quote
        "\u201c": '"',    # left double quote
        "\u201d": '"',    # right double quote
        "\u2026": "...",  # ellipsis
        "\u00a0": " ",    # non-breaking space
        "\u2022": "-",    # bullet
    }
    for char, repl in replacements.items():
        text = text.replace(char, repl)
    return text.encode("latin-1", "replace").decode("latin-1")


def generate_pdf(journal_a_text: str, journal_b_text: str) -> bytes:
    """Build a styled PDF from the user's two journal entries."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()

    # Title
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 15, _safe("Letters to the Living"), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(160, 120, 100)
    pdf.cell(0, 8, _safe("A Valentine's Nature Walk & Writing Workshop"), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(130, 130, 130)
    pdf.cell(0, 8, _safe(f"Written on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(12)

    # Divider line
    pdf.set_draw_color(107, 143, 78)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(10)

    # Prompt A
    if journal_a_text.strip():
        pdf.set_text_color(196, 137, 110)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, _safe("Prompt A - The Imprint"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 6, _safe("What came up for you during the walk?"), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        pdf.set_text_color(50, 50, 50)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, _safe(journal_a_text.strip()))
        pdf.ln(10)

    # Divider
    if journal_a_text.strip() and journal_b_text.strip():
        pdf.set_draw_color(107, 143, 78)
        pdf.line(30, pdf.get_y(), 180, pdf.get_y())
        pdf.ln(10)

    # Prompt B
    if journal_b_text.strip():
        pdf.set_text_color(196, 137, 110)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, _safe("Prompt B - A Letter to the Living"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 6, _safe("A letter to the living -- human, spirit, tree, or forest."), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)
        pdf.set_text_color(50, 50, 50)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, _safe(journal_b_text.strip()))
        pdf.ln(10)

    # Footer quote
    pdf.ln(5)
    pdf.set_draw_color(107, 143, 78)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(107, 143, 78)
    pdf.cell(0, 8, _safe("In the forest, love is not a transaction; it is a shared circular system."), new_x="LMARGIN", new_y="NEXT", align="C")

    return bytes(pdf.output())


# ──────────────────────────────────────────────
# Timer helper
# ──────────────────────────────────────────────
def render_timer(minutes: int, key: str):
    """Simple countdown timer button."""
    if st.button(f"Start {minutes}-Minute Timer", key=key):
        placeholder = st.empty()
        remaining = minutes * 60
        while remaining > 0:
            m, s = divmod(remaining, 60)
            placeholder.markdown(f"**{m:02d}:{s:02d}** remaining")
            time.sleep(1)
            remaining -= 1
        placeholder.success("Time's up! Well done.")


# ══════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════
st.markdown("&nbsp;", unsafe_allow_html=True)

col_l, col_c, col_r = st.columns([1, 3, 1])
with col_c:
    st.markdown(
        "<p style='text-align:center; font-size:0.7rem; letter-spacing:0.3em; "
        "text-transform:uppercase; color:#6b8f4e;'>💌 Digital Guide</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h1 style='text-align:center; font-size:2.8rem; margin-bottom:0;'>"
        "Letters to the Living</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; font-size:0.85rem; letter-spacing:0.12em; "
        "text-transform:uppercase; color:#c4896e;'>"
        "A Valentine's Nature Walk &amp; Writing Workshop</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; font-size:0.85rem; opacity:0.5;'>"
        "February 14th &nbsp;|&nbsp; 10:00 AM PST</p>",
        unsafe_allow_html=True,
    )

st.divider()

# ══════════════════════════════════════════════
#  THE INVITATION
# ══════════════════════════════════════════════
st.markdown("<h2 style='color:#c4896e !important;'>The Invitation</h2>", unsafe_allow_html=True)

st.markdown(
    "> *\"Love,\" as seen on Valentine's stickers, is often red hearts and easy purchases. "
    "We have traded the means of love for the cost of convenience.*"
)

st.markdown(
    "Today, we invite you to forget what love has \"meant\" to you in the past. "
    "We invite you to allow the forest to redefine it."
)

st.markdown("")

# ══════════════════════════════════════════════
#  HOW TO JOIN
# ══════════════════════════════════════════════
st.markdown("<h2 style='color:#6b8f4e !important;'>How to Join Us</h2>", unsafe_allow_html=True)

st.markdown("🎧 **Audio On** — Keep your headphones in for Part I.")
st.markdown("🌿 **Safety First** — Wander, but stay aware of your path.")
st.markdown(
    "🔄 **The Transition** — At 30 minutes we end the audio call. "
    "You can write in solitude, or join back after a 5-minute break for guided prompts."
)

st.divider()

# ══════════════════════════════════════════════
#  PART I: THE WALK
# ══════════════════════════════════════════════
st.markdown(
    "<p style='text-align:center; font-size:0.7rem; letter-spacing:0.25em; "
    "text-transform:uppercase; color:#6b8f4e;'>Part I</p>",
    unsafe_allow_html=True,
)
st.markdown("<h2 style='text-align:center;'>The Walk</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; opacity:0.6; font-size:0.85rem;'>🎧 Audio Guided</p>",
    unsafe_allow_html=True,
)
st.caption("_We are walking — but we are walking with intentionality._")
st.markdown("")

# ── Step 1 ──
with st.expander("**① Walking with Presence** — 48 Steps · 15 min", expanded=True):
    render_timer(15, key="timer_walk")

    st.caption(
        "_Synchronize your breath with your movement. "
        "Don't worry about perfect counting — focus on the rhythm._"
    )

    st.markdown("**Set 1 (12 Steps): Rooting**")
    st.markdown(
        "- **Inhale:** Imagine roots growing from your feet.\n"
        "- **Exhale:** Release the worries and judgments. Let them blow away like wind."
    )

    st.markdown("**Set 2 (12 Steps): Lightness**")
    st.markdown(
        "- **Inhale:** Feel an uplifting force pulling the crown of your head toward the sky.\n"
        "- **Exhale:** Release the heaviness. Become lighter with every step."
    )

    st.markdown("**Set 3 (12 Steps): Wonder**")
    st.markdown(
        "- **Inhale:** Invite in curiosity and freedom.\n"
        "- **Exhale:** Release the \"masks\" you wear and the \"shoulds\" you carry."
    )

    st.markdown("**Set 4 (12 Steps): Love**")
    st.markdown(
        "- **Inhale:** Breathe in Love — raw, wild, and green.\n"
        "- **Exhale:** Breathe out Fear."
    )


# ── Step 2 ──
with st.expander("**② Orientation & Senses** — Transition"):
    st.markdown(
        "*Stop walking. Stand still. You are accepted here. "
        "Love here is not founded in formality, but in the freedom of acceptance.*"
    )
    st.markdown("")
    st.markdown("**👁 Look:** Right, Left, Behind, Up — *What notices you?*")
    st.markdown("")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("👃 What do you smell?")
        st.markdown("👅 What do you taste?")
    with col2:
        st.markdown("👂 What do you hear?")
        st.markdown("🤲 What do you touch?")


# ── Step 3 ──
with st.expander("**③ The Shape of Connection** — Moss Wisdom"):
    st.info(
        "🌱 **Did you know?** Beneath the moss you are standing near, there is a vast hidden network. "
        "Mosses and fungi (mycelium) act as the \"Wood Wide Web,\" transferring nutrients "
        "from strong trees to weaker ones."
    )
    st.markdown(
        "> *In the forest, love is not a transaction; it is a shared circular system.*"
    )


# ── Step 4 ──
with st.expander("**④ Visualization: The Center** — 5 min"):
    render_timer(5, key="timer_viz")
    st.markdown("Close your eyes (or keep them half-open). Sense the center of your body.")
    st.markdown(
        "<p style='font-family: Cormorant Garamond, serif; font-style: italic; "
        "color: #c4896e; text-align: center; font-size: 1.05rem; margin-top: 1rem;'>"
        "If this new definition of Love had a shape, what would it look like inside you right now?"
        "</p>",
        unsafe_allow_html=True,
    )


st.divider()


# ══════════════════════════════════════════════
#  PART II: THE WRITING
# ══════════════════════════════════════════════
st.markdown(
    "<p style='text-align:center; font-size:0.7rem; letter-spacing:0.25em; "
    "text-transform:uppercase; color:#c4896e;'>Part II</p>",
    unsafe_allow_html=True,
)
st.markdown("<h2 style='text-align:center;'>The Writing</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; opacity:0.6; font-size:0.85rem;'>✍️ Self-Guided</p>",
    unsafe_allow_html=True,
)
st.caption("_We will now disconnect from the audio to write. Find a place to sit or lean._")
st.markdown("")


# ── Prompt A ──
with st.expander("**Prompt A — The Imprint** · Journal Reflection · 5 min", expanded=True):
    render_timer(5, key="timer_promptA")
    st.markdown("**What came up for you during the walk?**")
    st.caption("_Capture the raw thoughts, emotions, or physical sensations before they fade._")
    journal_a = st.text_area(
        "Prompt A",
        placeholder="Begin writing here... let the words flow without judgment.",
        height=180,
        key="journal_a",
        label_visibility="collapsed",
    )


# ── Prompt B ──
with st.expander("**Prompt B — A Letter to the Living** · Main Exercise · 20 min", expanded=True):
    render_timer(20, key="timer_promptB")

    st.markdown(
        "We are writing a letter to **\"The Living.\"** "
        "You get to define what that means — a specific human, a spirit, a tree, or the forest itself."
    )
    st.markdown(
        "📜 **The Constraint:** Write as if the trees can read your letter over your shoulder. "
        "Your thoughts and actions must align."
    )
    st.markdown(
        "🔥 **The Challenge:** Write beyond your comfort zone. "
        "Reach for emotional authenticity."
    )
    st.markdown("")
    st.markdown("*Guiding Questions:*")
    st.markdown(
        "- What does this new kind of love feel like, taste like, and smell like?\n"
        "- What stories would you tell the trees about your heart?\n"
        "- If you stripped away the \"convenience\" of modern love, what remains?"
    )
    st.markdown("")

    journal_b = st.text_area(
        "Prompt B",
        placeholder="Dear Living...",
        height=280,
        key="journal_b",
        label_visibility="collapsed",
    )


# ══════════════════════════════════════════════
#  DOWNLOAD PDF
# ══════════════════════════════════════════════
st.divider()

st.markdown("<h2 style='text-align:center;'>Save Your Words</h2>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; opacity:0.7; font-size:0.9rem;'>"
    "When you are finished, download your journal entries as a PDF to keep.</p>",
    unsafe_allow_html=True,
)
st.markdown("")

has_text = bool((journal_a and journal_a.strip()) or (journal_b and journal_b.strip()))

if has_text:
    try:
        pdf_bytes = generate_pdf(journal_a or "", journal_b or "")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="Download My Journal (PDF)",
                data=pdf_bytes,
                file_name=f"letters_to_the_living_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
            )
    except Exception as e:
        st.error(f"Could not generate PDF: {e}")
else:
    st.markdown(
        "<p style='text-align:center; opacity:0.4; font-size:0.85rem; font-style:italic;'>"
        "Write something in the prompts above and the download button will appear here.</p>",
        unsafe_allow_html=True,
    )

# ── Footer ──
st.markdown("")
st.markdown(
    "<p style='text-align:center; opacity:0.35; font-style:italic; "
    "font-family: Cormorant Garamond, serif; font-size: 0.95rem; padding: 2rem 0;'>"
    "Thank you for walking with us.</p>",
    unsafe_allow_html=True,
)
