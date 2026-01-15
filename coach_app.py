import streamlit as st
import google.generativeai as genai
import os
import tempfile

# --- PASSWORD PROTECTION ---
# We will create a new secret called "APP_PASSWORD"
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def check_password():
    if st.session_state.password_input == st.secrets["APP_PASSWORD"]:
        st.session_state.authenticated = True
        del st.session_state.password_input
    else:
        st.error("Wrong Password")

if not st.session_state.authenticated:
    st.text_input("Enter Password:", type="password", key="password_input", on_change=check_password)
    st.stop()

# --- MAIN APP (Only runs if password is correct) ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("API Key not found.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

st.set_page_config(page_title="P.E. Command Center", page_icon="🏀")
st.title("📋 Coach's Class Logger")
st.write("Record your post-class notes.")

audio_value = st.audio_input("Record notes...")

if audio_value:
    st.info("Processing...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_value.read())
        temp_audio_path = temp_audio.name

    try:
        myfile = genai.upload_file(temp_audio_path)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = """
        You are an expert P.E. Teacher's Assistant. 
        Output THREE sections:
        1. **EMAIL SUMMARY**: Professional summary for parents.
        2. **BEHAVIOR LOG**: Disruptive behavior (First Name + Last Initial ONLY).
        3. **DATA & PRAISE**: Achievements and personal bests.
        """
        result = model.generate_content([myfile, prompt])
        st.success("Done!")
        st.markdown(result.text)
    except Exception as e:
        st.error(f"Error: {e}")
    finally:
        os.unlink(temp_audio_path)
