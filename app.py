import streamlit as st
import os
from tempfile import NamedTemporaryFile
from gtts import gTTS
from googletrans import LANGUAGES, Translator
import whisper

# Streamlit Page Configurations
st.set_page_config(
    page_title="Audio Translator",
    page_icon="🎵",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #000000;
    }
    .css-1d391kg, .css-1kyxreq {
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        background-color: #1e1e1e;
        color: white;
    }
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        height: 50px;
        font-size: 18px;
    }
    .stSelectbox > div {
        background-color: #333333;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎵 Audio Translation App")
st.subheader("📤 Upload an Audio File, Then Select Target Language for Conversion")

# Available languages (all from googletrans LANGUAGES)
languages = {"Select a language": ""}
languages.update({name.capitalize(): code for code, name in LANGUAGES.items()})

audio_file = st.file_uploader("Choose an audio file (wav, mp3, m4a)", type=["wav", "mp3", "m4a"])

if audio_file is not None:
    target_language = st.selectbox("🌐 Select the target language:", list(languages.keys()))

    if target_language != "Select a language":
        with st.spinner("🔄 Processing audio, please wait..."):
            # Save uploaded audio
            with NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(audio_file.read())
                tmp_file_path = tmp_file.name

            # Load Whisper model
            model = whisper.load_model("base")
            result = model.transcribe(tmp_file_path)
            english_text = result["text"]

            # Translate text
            translator = Translator()
            translated_text = translator.translate(english_text, dest=languages[target_language]).text

            # Convert translated text to speech
            tts = gTTS(text=translated_text, lang=languages[target_language])
            output_audio_path = "translated_audio.mp3"
            tts.save(output_audio_path)

            # Audio playback and download
            st.audio(output_audio_path, format='audio/mp3')
            st.download_button(
                label="📥 Download Translated Audio",
                data=open(output_audio_path, "rb").read(),
                file_name="translated_audio.mp3",
                mime="audio/mp3"
            )

            st.success("🎉 Translated audio is ready for download!")

            # Cleanup
            os.remove(output_audio_path)
            os.remove(tmp_file_path)
else:
    st.info("ℹ️ Please upload an audio file first. After that, select a target language to start processing.")
