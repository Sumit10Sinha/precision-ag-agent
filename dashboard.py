import streamlit as st

# Fixed import statement to match your exact function name
from agent_brain import run_farm_advisor 

# --- UI Configuration & Styling ---
st.set_page_config(page_title="AgroSmart AI", page_icon="🌱", layout="centered")

# Custom CSS to set the green gradient background and fix Dark Mode clashes
st.markdown("""
    <style>
    /* Base background */
    .stApp {
        background: linear-gradient(to bottom right, #ccff99, #99ffcc);
    }
    
    /* Force all labels, subtitles, and standard text to be dark */
    label p, .stMarkdown p, .stText {
        color: #1e1e1e !important; 
    }
    
    /* FIX: Force text inputs to have a white background and dark text */
    div[data-baseweb="base-input"] {
        background-color: #ffffff !important;
    }
    div[data-baseweb="base-input"] input {
        color: #1e1e1e !important;
        -webkit-text-fill-color: #1e1e1e !important;
    }
    
    /* FIX: Force select dropdowns to have a white background and dark text */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
    }
    div[data-baseweb="select"] span {
        color: #1e1e1e !important;
    }
    
    /* Button styling */
    div.stButton > button:first-child {
        background-color: #2e7b32;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }
    div.stButton > button:first-child:hover {
        background-color: #1b5e20;
    }
    
    /* Ensure the text inside the button stays strictly white */
    div.stButton > button:first-child p {
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
# Displaying your logo image (which already contains the AGROSMART AI text)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        # Allowing the image to scale naturally to look like your screenshot
        st.image("logo.png", use_column_width=True) 
    except:
        st.markdown("<h1 style='text-align: center;'>🌱</h1>", unsafe_allow_html=True)

# NEW SLOGAN (Replacing the duplicate title text)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');
    .slogan {
        text-align: center;
        font-family: 'Permanent Marker', cursive;
        color: #1a4a28; 
        font-size: 26px;
        margin-top: -10px;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }
    </style>
    <div class="slogan">THE ZERO-HARDWARE VIRTUAL AGRONOMIST</div>
""", unsafe_allow_html=True)

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
                # Combine city and state into a single location string
                full_location = f"{city}, {state}"
                
                # Call your correctly named backend function
                result = run_farm_advisor(crop_type=crop_type, location=full_location)

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