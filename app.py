import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import urllib.parse
import urllib.request
import json
import io
import html


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Neural Translator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""


# ============================================================
# DAY / NIGHT THEME
# ============================================================

if st.session_state.dark_mode:

    BG = "#070b17"
    CARD = "rgba(20, 27, 48, 0.72)"
    TEXT = "#f8fafc"
    MUTED = "#94a3b8"
    BORDER = "rgba(129, 140, 248, 0.35)"
    INPUT_BG = "rgba(15, 23, 42, 0.75)"
    ACCENT = "#a855f7"
    ACCENT2 = "#6366f1"

else:

    BG = "#eef2ff"
    CARD = "rgba(255, 255, 255, 0.78)"
    TEXT = "#111827"
    MUTED = "#64748b"
    BORDER = "rgba(99, 102, 241, 0.30)"
    INPUT_BG = "rgba(255, 255, 255, 0.90)"
    ACCENT = "#7c3aed"
    ACCENT2 = "#4f46e5"


# ============================================================
# CUSTOM CSS
# ============================================================

custom_css = f"""
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

* {{
    font-family: 'Inter', sans-serif;
}}

.stApp {{
    background:
        radial-gradient(
            circle at 10% 20%,
            rgba(99, 102, 241, 0.18),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 80%,
            rgba(168, 85, 247, 0.18),
            transparent 30%
        ),
        {BG};

    color: {TEXT};

    transition:
        background 0.4s ease,
        color 0.4s ease;
}}


/* Main container */

.block-container {{
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}}


/* Header */

.hero {{
    text-align: center;
    padding: 35px 20px 20px 20px;
    margin-bottom: 20px;
    border-radius: 25px;
    background: {CARD};
    border: 1px solid {BORDER};
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    box-shadow:
        0 15px 45px rgba(0,0,0,0.12);
}}

.hero h1 {{
    font-size: 3rem;
    font-weight: 800;
    margin: 0 0 8px 0;

    background:
        linear-gradient(
            90deg,
            {ACCENT2},
            {ACCENT}
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.hero p {{
    color: {MUTED};
    font-size: 1rem;
    margin: 6px 0;
}}


/* Glass cards */

.glass-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 22px;
    padding: 25px;

    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    box-shadow:
        0 15px 45px rgba(0,0,0,0.12);

    margin-bottom: 20px;
}}


/* Labels */

.section-title {{
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 12px;
    color: {TEXT};
}}


/* Text area */

.stTextArea textarea {{
    background: {INPUT_BG} !important;
    color: {TEXT} !important;

    border: 1px solid {BORDER} !important;

    border-radius: 15px !important;

    font-size: 1rem !important;
    padding: 15px !important;
}}


/* Selectbox */

.stSelectbox > div > div {{
    background: {INPUT_BG} !important;
    color: {TEXT} !important;

    border-radius: 14px !important;

    border: 1px solid {BORDER} !important;
}}


/* Buttons */

.stButton > button {{
    width: 100%;

    border: none;
    border-radius: 14px;

    padding: 0.75rem 1rem;

    font-weight: 700;
    color: white !important;

    background:
        linear-gradient(
            90deg,
            {ACCENT2},
            {ACCENT}
        );

    transition: all 0.25s ease;

    box-shadow:
        0 8px 22px rgba(99,102,241,0.22);
}}

.stButton > button:hover {{
    transform:
        translateY(-3px) scale(1.01);

    box-shadow:
        0 12px 30px rgba(168,85,247,0.35);
}}


/* Translation result */

.result-card {{
    background:
        linear-gradient(
            135deg,
            rgba(99,102,241,0.12),
            rgba(168,85,247,0.12)
        );

    border: 1px solid {BORDER};

    border-radius: 18px;

    padding: 22px;

    min-height: 150px;

    transition: all 0.25s ease;

    animation: fadeIn 0.5s ease;

    overflow-wrap: anywhere;
}}

.result-card:hover {{
    transform:
        translateY(-4px);

    box-shadow:
        0 15px 35px rgba(99,102,241,0.18);
}}

.result-label {{
    color: {ACCENT};

    font-size: 0.85rem;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 1px;

    margin-bottom: 10px;
}}

.result-text {{
    color: {TEXT};

    font-size: 1.15rem;

    line-height: 1.7;

    margin-top: 8px;

    word-wrap: break-word;

    overflow-wrap: anywhere;

    white-space: pre-wrap;
}}


/* Divider */

.divider {{
    height: 1px;

    background: {BORDER};

    margin: 25px 0;
}}


/* Animations */

@keyframes fadeIn {{

    from {{
        opacity: 0;
        transform: translateY(10px);
    }}

    to {{
        opacity: 1;
        transform: translateY(0);
    }}

}}


/* Hide Streamlit branding */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header {{
    background: transparent !important;
}}


/* Audio player */

audio {{
    width: 100%;
}}

</style>
"""

st.markdown(
    custom_css,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """<div class="hero"><h1>✨ AI Neural Translator</h1><p>Translate • Speak • Listen • Understand</p><p>CodeAlpha AI Internship — Task 1</p></div>""",
    unsafe_allow_html=True
)


# ============================================================
# THEME BUTTON
# ============================================================

theme_col1, theme_col2, theme_col3 = st.columns(
    [4, 2, 4]
)

with theme_col2:

    if st.session_state.dark_mode:
        theme_button = "☀️ Day Mode"
    else:
        theme_button = "🌙 Night Mode"

    if st.button(theme_button):

        st.session_state.dark_mode = (
            not st.session_state.dark_mode
        )

        st.rerun()


# ============================================================
# LANGUAGES
# ============================================================

LANGUAGES = {

    "English": "en",
    "Urdu": "ur",
    "Sindhi": "sd",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Arabic": "ar",
    "Japanese": "ja"

}


# ============================================================
# TRANSLATION FUNCTION
# ============================================================

@st.cache_data(ttl=3600)
def translate_text(
    text,
    source_lang,
    target_lang
):

    try:

        encoded_text = urllib.parse.quote(text)

        url = (
            "https://api.mymemory.translated.net/get"
            f"?q={encoded_text}"
            f"&langpair={source_lang}|{target_lang}"
        )

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=20
        ) as response:

            data = json.loads(
                response.read().decode("utf-8")
            )

        if data.get("responseStatus") != 200:

            raise Exception(
                data.get(
                    "responseDetails",
                    "Translation service error."
                )
            )

        translated = data.get(
            "responseData",
            {}
        ).get(
            "translatedText",
            ""
        )

        if not translated:

            raise Exception(
                "No translation returned."
            )

        return translated.strip()

    except Exception as e:

        raise Exception(str(e))


# ============================================================
# SPEECH TO TEXT
# ============================================================

def speech_to_text(
    audio_file,
    language_code
):

    recognizer = sr.Recognizer()

    try:

        audio_bytes = audio_file.getvalue()

        audio_source = sr.AudioFile(
            io.BytesIO(audio_bytes)
        )

        with audio_source as source:

            audio_data = recognizer.record(source)

        speech_languages = {

            "en": "en-US",
            "ur": "ur-PK",
            "sd": "sd",
            "es": "es-ES",
            "fr": "fr-FR",
            "de": "de-DE",
            "zh-CN": "zh-CN",
            "ar": "ar-SA",
            "ja": "ja-JP"

        }

        recognition_language = speech_languages.get(
            language_code,
            "en-US"
        )

        text = recognizer.recognize_google(
            audio_data,
            language=recognition_language
        )

        return text

    except sr.UnknownValueError:

        raise Exception(
            "I couldn't understand the speech. "
            "Please speak clearly and try again."
        )

    except sr.RequestError:

        raise Exception(
            "Speech recognition service is unavailable. "
            "Please check your internet connection."
        )

    except Exception as e:

        raise Exception(
            f"Speech recognition error: {str(e)}"
        )


# ============================================================
# TEXT TO SPEECH
# ============================================================

def create_speech(
    text,
    language_code
):

    tts_languages = {

        "en": "en",
        "ur": "ur",
        "sd": "sd",
        "es": "es",
        "fr": "fr",
        "de": "de",
        "zh-CN": "zh-CN",
        "ar": "ar",
        "ja": "ja"

    }

    tts_language = tts_languages.get(
        language_code,
        "en"
    )

    audio = io.BytesIO()

    tts = gTTS(
        text=text,
        lang=tts_language,
        slow=False
    )

    tts.write_to_fp(audio)

    audio.seek(0)

    return audio


# ============================================================
# LANGUAGE SELECTION
# ============================================================

st.markdown(
    '<div class="glass-card">',
    unsafe_allow_html=True
)

lang_col1, lang_col2 = st.columns(2)


with lang_col1:

    st.markdown(
        '<div class="section-title">🪐 Source Language</div>',
        unsafe_allow_html=True
    )

    source_lang_name = st.selectbox(
        "Source Language",
        list(LANGUAGES.keys()),
        label_visibility="collapsed"
    )


with lang_col2:

    st.markdown(
        '<div class="section-title">☄️ Target Language</div>',
        unsafe_allow_html=True
    )

    target_lang_name = st.selectbox(
        "Target Language",
        list(LANGUAGES.keys()),
        index=1,
        label_visibility="collapsed"
    )


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INPUT AND OUTPUT
# ============================================================

input_col, output_col = st.columns(
    2,
    gap="large"
)


# ============================================================
# INPUT
# ============================================================

with input_col:

    st.markdown(
        '<div class="glass-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">📜 Enter Your Text</div>',
        unsafe_allow_html=True
    )

    source_text = st.text_area(
        "Text Input",
        value=st.session_state.speech_text,
        height=180,
        placeholder="Type something here...",
        label_visibility="collapsed"
    )

    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">🎙️ Speech Input</div>',
        unsafe_allow_html=True
    )

    audio_input = st.audio_input(
        "Record your voice"
    )

    if audio_input:

        if st.button(
            "🎤 Convert Speech to Text"
        ):

            with st.spinner(
                "Listening and converting speech..."
            ):

                try:

                    detected_text = speech_to_text(
                        audio_input,
                        LANGUAGES[source_lang_name]
                    )

                    st.session_state.speech_text = detected_text

                    st.success(
                        "Speech converted successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(str(e))

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# OUTPUT
# ============================================================

with output_col:

    st.markdown(
        '<div class="glass-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">🫧 Translation Result</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SIDE-BY-SIDE RESULT BOXES
    # --------------------------------------------------------

    result_col1, result_col2 = st.columns(
        2,
        gap="medium"
    )


    # --------------------------------------------------------
    # ORIGINAL TEXT
    # --------------------------------------------------------

    with result_col1:

        safe_original = html.escape(
            source_text
            if source_text
            else "Your original text will appear here..."
        )

        st.markdown(
            f"""<div class="result-card"><div class="result-label">🔤 Original • {html.escape(source_lang_name)}</div><div class="result-text">{safe_original}</div></div>""",
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # TRANSLATED TEXT
    # --------------------------------------------------------

    with result_col2:

        if st.session_state.translated_text:

            safe_translation = html.escape(
                st.session_state.translated_text
            )

            st.markdown(
                f"""<div class="result-card"><div class="result-label">🌍 Translated • {html.escape(target_lang_name)}</div><div class="result-text">{safe_translation}</div></div>""",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """<div class="result-card"><div class="result-label">🌍 Translation</div><div class="result-text">Your translation will appear here...</div></div>""",
                unsafe_allow_html=True
            )


    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # VOICE OUTPUT
    # ========================================================

    if st.session_state.translated_text:

        st.markdown(
            '<div class="section-title">🔊 Listen to Translation</div>',
            unsafe_allow_html=True
        )

        try:

            speech_audio = create_speech(
                st.session_state.translated_text,
                LANGUAGES[target_lang_name]
            )

            st.audio(
                speech_audio,
                format="audio/mp3"
            )

        except Exception:

            st.warning(
                "Voice output is unavailable for this language."
            )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# TRANSLATE BUTTON
# ============================================================

st.write("")

translate_col1, translate_col2, translate_col3 = st.columns(
    [2, 1, 2]
)

with translate_col2:

    if st.button(
        "🔄Translate Now"
    ):

        text_to_translate = source_text.strip()

        if not text_to_translate:

            st.warning(
                "Please enter text or record your voice first."
            )

        elif source_lang_name == target_lang_name:

            st.warning(
                "Please select different source and target languages."
            )

        else:

            source_code = LANGUAGES[source_lang_name]
            target_code = LANGUAGES[target_lang_name]

            with st.spinner("Translating..."):

                try:

                    translated = translate_text(
                        text_to_translate,
                        source_code,
                        target_code
                    )

                    st.session_state.translated_text = translated

                    st.success(
                        "Translation completed!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Translation Error: {str(e)}"
                    )


# ============================================================
# CLEAR BUTTON
# ============================================================

st.write("")

clear_col1, clear_col2, clear_col3 = st.columns(
    [3, 1, 3]
)

with clear_col2:

    if st.button(
        "🗑️ Clear"
    ):

        st.session_state.translated_text = ""
        st.session_state.speech_text = ""

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """<div style="text-align:center; color:#64748b; font-size:0.85rem; padding:20px;">
✨ AI Neural Translator<br>
CodeAlpha AI Internship — Task 1<br>
Translate • Speak • Listen
</div>""",
    unsafe_allow_html=True
)
