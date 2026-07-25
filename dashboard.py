import streamlit as st

# Import your AI logic from your agent_brain file
# NOTE: Make sure "run_agent" is the actual name of your function! 
from agent_brain import run_agent 

# --- UI Configuration & Styling ---
st.set_page_config(page_title="AgroSmart AI", page_icon="🌱", layout="centered")

# Custom CSS to set the green gradient background and style the button
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #ccff99, #99ffcc);
    }
    div.stButton > button:first-child {
        background-color: #2e7b32;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }
    div.stButton > button:first-child:hover {
        background-color: #1b5e20;
        color: white;
    }
    /* Make standard text dark for readability */
    .stMarkdown, .stText {
        color: #1e1e1e !important; 
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
# Ensure "logo.png" is in the same folder as this script
try:
    st.image("logo.png", use_column_width=False, width=150)
except:
    st.markdown("<h1 style='text-align: center;'>🌱</h1>", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #1b5e20;'>AGROSMART AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold; color: #1e1e1e;'>This AI agent autonomously analyzes live weather data to optimize crop irrigation and conserve freshwater.</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Input Section ---
st.markdown("<h2 style='color: #1b5e20;'>Farm Details</h2>", unsafe_allow_html=True)

crop_type = st.selectbox("Select Crop Type:", ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane", "Other"])

col1, col2 = st.columns(2)
with col1:
    state = st.text_input("State (e.g., West Bengal):", "West Bengal")
with col2:
    city = st.text_input("City / District / Village:", "Midnapore")

# --- Action Section ---
if st.button("Run AI Analysis"):
    if crop_type and state and city:
        with st.spinner("Agent is analyzing live weather data..."):
            try:
                # Call the backend agent function
                result = run_agent(crop_type, state, city)

                # --- FIXED UI OUTPUT BOX ---
                st.markdown(f"""
                    <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; color: #1e1e1e; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #2e7b32; margin-top: 20px;">
                        <h4 style="color: #2e7b32; margin-top: 0;">🌱 Agent Recommendation:</h4>
                        <div style="font-size: 16px; line-height: 1.6;">
                            {result}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"An error occurred while running the analysis: {e}")
    else:
        st.warning("Please fill in all the farm details before running the analysis.")