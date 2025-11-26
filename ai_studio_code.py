import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="The Racing Logic Model", layout="wide")

# Sidebar for API Key (so you don't hardcode it)
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.markdown("[Get a Free Key Here](https://aistudio.google.com/app/apikey)")

# Main Title
st.title("🏇 The Fundamental Handicapping Model")
st.markdown("Paste the raw text from Racing Australia, Punters, or Tabtouch below.")

# The Logic Core (Our Framework)
SYSTEM_PROMPT = """
You are an expert Horse Racing Handicapper using the "Fundamental Handicapping Approach v2.0".
Your goal is to price the field to a 100% market and identify value.

THE ENGINES:
1. Engine A (Class Compression): Look for horses dropping in grade (e.g. Metro to Country). Apply a bonus.
   - UPGRADE: If a horse has >33% Win Rate at the specific track, multiply probability by 1.25x (Track Specialist).
2. Engine B (Speed Map): Identify the likely leader and box-seat runner. Upgrade them. Downgrade backmarkers on tight tracks.
3. Engine C (Weight Logic): 
   - Standard: Heavy weight on long distance is a negative.
   - Relative Swing: If Horse A meets Horse B >3kg better off for a defeat of <2L previously, Horse A gets a massive rating bonus.
4. Engine D (Intent): Look for "Blinkers ON", "Gelded", or 3rd/4th run of prep (Peak Cycle).

THE FORGIVENESS PROTOCOL:
- Do not judge a horse solely on its last start number (e.g. 9th).
- Forgive: Wide runs, wrong distance, or higher grade.
- Look for hidden merit.

OUTPUT FORMAT:
1. Analysis of Key Runners (apply the engines).
2. The Marked Market Table (Horse, Raw Rating, Probability, True Price).
3. The Betting Strategy (The Safe Play, The Value Bet, The Lay).
"""

# Input Area
race_data = st.text_area("Paste Race Form Here:", height=300)

# The "Handicap" Button
if st.button("Handicap This Race"):
    if not api_key:
        st.error("Please enter an API Key in the sidebar.")
    elif not race_data:
        st.error("Please paste some race data.")
    else:
        try:
            # Configure Gemini
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            
            with st.spinner('Analyzing Engines A, B, C & D...'):
                # Construct the full prompt
                full_query = f"{SYSTEM_PROMPT}\n\nHERE IS THE RACE DATA:\n{race_data}"
                
                # Get response
                response = model.generate_content(full_query)
                
                # Display Result
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"An error occurred: {e}")