import streamlit as st
import google.generativeai as genai
import os
import tempfile

# --- CONFIGURATION ---
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("API Key not found. Please set it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# --- THE APP INTERFACE ---
st.set_page_config(page_title="P.E. Command Center", page_icon="🏀")

st.title("📋 Coach's Class Logger")
st.write("Record your post-class notes. Gemini will sort them for you.")

# --- AUDIO RECORDER ---
audio_value = st.audio_input("Record your notes (e.g., 'Period 2, 4th Grade...')")

if audio_value:
    st.info("Processing audio... please wait.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_value.read())
        temp_audio_path = temp_audio.name

    try:
        # Upload to Gemini
        myfile = genai.upload_file(temp_audio_path)
        
        # Create the AI Model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # The Instructions
        prompt = """
        You are an expert P.E. Teacher's Assistant. 
        Listen to this audio recording of the teacher's class notes.
        
        Please output THREE distinct sections:
        
        1. **EMAIL SUMMARY**: A polite, professional summary of the activities done, suitable for a weekly email to parents. Use simple, clear language.
        2. **BEHAVIOR LOG**: List any students mentioned for disruptive behavior (Use First Name + Last Initial only). If none, write "No incidents."
        3. **DATA & PRAISE**: List any specific student achievements, personal bests (numbers/stats), or students deserving of praise.
        """
        
        result = model.generate_content([myfile, prompt])
        
        st.success("Analysis Complete!")
        st.markdown(result.text)
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
        
    finally:
        os.unlink(temp_audio_path)
