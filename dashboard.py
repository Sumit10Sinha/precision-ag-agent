import streamlit as st
import base64
import os
from PIL import Image

# Fixed import statement to match your exact function name
from agent_brain import run_farm_advisor 

# --- UI Configuration & Styling ---
# Safely open the logo file as an actual Image Object for the browser tab
try:
    img_icon = Image.open("logo.jpg")
except:
    try:
        img_icon = Image.open("logo.png") # Fallback just in case
    except:
        img_icon = "🌱" # Final fallback if the file is completely missing

# Pass the Image Object to page_icon
st.set_page_config(page_title="AgroSmart AI", page_icon=img_icon, layout="wide", initial_sidebar_state="collapsed")

# Helper function to load local image as a CSS background or HTML image
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# --- IMAGE LOADER ---
# Checks for .jpg format, with a fallback to .jpeg for the background
bg_base64 = get_base64_of_bin_file('website_banner_image.jpg')
if not bg_base64:
    bg_base64 = get_base64_of_bin_file('website_banner_image.jpeg')

# Checks for .jpg format, with a fallback to .png for the logo
logo_base64 = get_base64_of_bin_file('logo.jpg') 
if not logo_base64:
    logo_base64 = get_base64_of_bin_file('logo.png')

# Construct the background CSS
if bg_base64:
    # Slightly reduced the darkness of the overall gradient so the box stands out more
    bg_css = f"background-image: linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.3)), url('data:image/jpeg;base64,{bg_base64}');"
else:
    bg_css = "background-color: #1a4a28;"

# Construct the Logo HTML
if logo_base64:
    logo_html = f'<img src="data:image/jpeg;base64,{logo_base64}" class="hero-logo" alt="AgroSmart AI Logo">'
else:
    # Fallback just in case the logo is missing
    logo_html = '<div class="hero-title">🌱 AGROSMART AI</div>'

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Permanent+Marker&display=swap');
    
    /* Set entire app bottom background to white */
    .stApp {{
        background-color: #ffffff;
    }}
    
    /* Remove default Streamlit padding so the banner hits the very edges */
    .block-container {{
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }}

    /* --- HERO BANNER CSS --- */
    .hero-banner {{
        {bg_css}
        background-size: cover;
        background-position: center;
        width: 100vw;
        position: relative;
        left: 50%;
        right: 50%;
        margin-left: -50vw;
        margin-right: -50vw;
        padding: 80px 20px 100px 20px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }}
    
    /* --- NEW TRANSLUCENT CONTENT BOX --- */
    .hero-content-box {{
        background-color: rgba(0, 0, 0, 0.65); /* The dark translucent background */
        padding: 50px 40px;
        max-width: 900px;
        margin: 0 auto; /* Centers the box */
        /* Optional: Adding a slight blur effect to the background behind the box for a modern feel */
        backdrop-filter: blur(4px); 
        -webkit-backdrop-filter: blur(4px);
    }}
    
    /* Styling for your custom logo */
    .hero-logo {{
        max-height: 220px; 
        width: auto;
        margin: 0 auto 10px auto;
        display: block;
    }}
    
    .hero-title {{
        font-size: 4.5rem;
        font-weight: 900;
        margin-bottom: 0px;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }}
    
    .hero-slogan {{
        font-family: 'Permanent Marker', cursive;
        font-size: 2.2rem;
        color: #ffffff; /* Changed to white to match your new image */
        margin-top: 5px;
        margin-bottom: 25px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
    }}
    
    .hero-subtext {{
        font-size: 1.3rem;
        max-width: 800px;
        margin: 0 auto;
        color: #f8f9fa;
        line-height: 1.6;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}

    /* --- FIX TEXT COLORS FOR WHITE SECTION --- */
    .stMarkdown p, .stText, h2, label p {{
        color: #1e1e1e !important; 
    }}
    
    div[data-baseweb="base-input"] {{
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
        border-radius: 5px;
    }}
    div[data-baseweb="base-input"] input {{
        color: #1e1e1e !important;
        -webkit-text-fill-color: #1e1e1e !important;
    }}
    
    div[data-baseweb="select"] > div {{
        background-color: #ffffff !important;
        border: 1px solid #cccccc !important;
    }}
    div[data-baseweb="select"] span {{
        color: #1e1e1e !important;
    }}
    
    /* Button styling */
    div.stButton > button:first-child {{
        background-color: #2e7b32;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        width: 100%;
        margin-top: 15px;
    }}
    div.stButton > button:first-child:hover {{
        background-color: #1b5e20;
    }}
    div.stButton > button:first-child p {{
        color: #ffffff !important;
        font-size: 18px !important;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# --- FULL WIDTH HERO SECTION (TOP) ---
# Notice the new div class="hero-content-box" wrapping the content
st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-content-box">
            {logo_html}
            <div class="hero-slogan">THE ZERO-HARDWARE VIRTUAL AGRONOMIST</div>
            <div class="hero-subtext">This AI agent autonomously analyzes live weather data to optimize crop irrigation and conserve freshwater.</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# --- CENTERED FORM SECTION (BOTTOM) ---
spacer_left, main_content, spacer_right = st.columns([1.5, 3, 1.5])

with main_content:
    st.markdown("<h2 style='text-align: center; color: #1b5e20; margin-bottom: 30px;'>Configure Farm Details</h2>", unsafe_allow_html=True)

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
                    full_location = f"{city}, {state}"
                    result = run_farm_advisor(crop_type=crop_type, location=full_location)

                    st.markdown(f"""
                        <div style="background-color: #ffffff; padding: 25px; border-radius: 10px; color: #1e1e1e; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-left: 6px solid #2e7b32; margin-top: 30px;">
                            <h4 style="color: #2e7b32; margin-top: 0; font-size: 20px;">🌱 Agent Recommendation:</h4>
                            <div style="font-size: 16px; line-height: 1.6;">
                                {result}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"An error occurred while running the analysis: {e}")
        else:
            st.warning("Please fill in all the farm details before running the analysis.")