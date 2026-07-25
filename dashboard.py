import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage

# Import the compiled LangGraph app from your agent_brain.py file
from agent_brain import app

# 1. Set up the Web Page
st.set_page_config(page_title="AgroSmart AI", page_icon="🌱", layout="centered")

# 2. Inject Custom UI/UX CSS (Green Gradient & Clean Styling)
custom_css = """
<style>
/* Gradient Green Background */
.stApp {
    background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
}

/* Make text dark green/black for readability on the light background */
.stMarkdown, .stText, p, label, h1, h2, h3 {
    color: #1a4a20 !important; 
}

/* Style the primary action button */
.stButton>button {
    background-color: #2e7d32;
    color: white !important;
    border-radius: 8px;
    border: none;
    padding: 10px 24px;
    font-weight: bold;
    transition: all 0.3s ease;
    width: 100%;
}
.stButton>button:hover {
    background-color: #1b5e20;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
}

/* Style input fields and dropdowns */
.stTextInput>div>div>input, .stSelectbox>div>div>select {
    background-color: rgba(255, 255, 255, 0.9);
    border-radius: 6px;
    border: 1px solid #2e7d32;
    color: #000000 !important;
}

/* Style success/info boxes */
.stAlert {
    background-color: rgba(255, 255, 255, 0.8);
    border-left-color: #2e7d32;
    color: #1a4a20;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 3. Header & Logo Integration
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        # This will load your new transparent logo.png
        st.image("logo.png", use_container_width=True)
    except FileNotFoundError:
        st.markdown("<h2 style='text-align: center;'>💧 AgroSmart AI</h2>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; font-size: 1.1em; font-weight: 500;'>This AI agent autonomously analyzes live weather data to optimize crop irrigation and conserve freshwater.</p>", unsafe_allow_html=True)
st.divider()

# 4. Create Input Fields for the User
st.header("Farm Details")

# Comprehensive Pan-India Crop Dropdown
indian_crops = [
    "Rice (Paddy)", "Wheat", "Maize (Corn)", "Millets (Jowar, Bajra, Ragi)", 
    "Cotton", "Sugarcane", "Tea", "Coffee", "Jute", 
    "Pulses (Gram, Tur, Urad)", "Mustard", "Groundnut", "Soybean",
    "Potato", "Tomato", "Onion"
]
crop_type = st.selectbox("Select Crop Type:", options=indian_crops, index=1) # Defaults to Wheat

# State and Location Inputs Side-by-Side
col_state, col_city = st.columns(2)
with col_state:
    state = st.text_input("State (e.g., West Bengal):", value="West Bengal")
with col_city:
    city = st.text_input("City / District / Village:", value="Midnapore")

# Combine the location for the AI prompt
full_location = f"{city}, {state}, India"

st.write("") # Add a little spacing

# 5. Create the Action Button
if st.button("Run AI Analysis", type="primary"):
    
    if not state or not city:
        st.warning("Please provide both your State and City/District to proceed.")
    else:
        with st.spinner("Agent is fetching live weather data and reasoning..."):
            
            system_prompt = SystemMessage(
                content=(
                    "You are AgroSmart AI, an autonomous virtual agronomist. "
                    "Your goal is water conservation (SDG 6) and crop productivity (SDG 2). "
                    "When given a farm location, ALWAYS check the daily weather forecast using your tool. "
                    "If predicted rainfall is greater than 5.0 mm, explicitly advise to SKIP irrigation to save water. "
                    "Provide a concise, practical, professional recommendation for the farmer."
                )
            )
            
            user_prompt = HumanMessage(
                content=f"Please analyze the irrigation needs for my {crop_type} farm in {full_location} today."
            )
            
            inputs = {
                "messages": [system_prompt, user_prompt],
                "crop_type": crop_type,
                "farm_location": full_location
            }
            
            try:
                result = app.invoke(inputs)
                final_recommendation = result["messages"][-1].content
                
                st.success(f"Analysis Complete for {full_location}!")
                st.info(final_recommendation)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")