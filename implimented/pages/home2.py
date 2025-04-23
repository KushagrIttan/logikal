import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Set page config
st.set_page_config(page_title="LogiKal Route Selector", page_icon="🚚", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for buttons only
st.markdown(
    """
    <style>
        .main { background-color: #0E0E0E; }
        .stButton>button {
            background-color: #FF4B4B;
            color: white;
            border-radius: 10px;
            font-size: 20px;
            width: 100%;
            height: 60px;
        }
        .stButton>button:hover {
            background-color: #D43F3F;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page Title
st.markdown(
    "<h1 style='text-align: center; color: white;'>"
    "<span style='color: blue;'>Logi</span>"
    "<span style='color: red;'>कल</span> Compliance Validator</h1>",
    unsafe_allow_html=True
)

# Creating columns for text boxes
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🌍 **International Shipping**")
    st.info("Uses **Rule-Based Validation** to ensure strict compliance with customs regulations, tariffs, trade policies, and global shipping laws.")

with col2:
    st.markdown("### 📦 **Domestic Shipping**")
    st.info("Uses a **Machine Learning Classification Model** to optimize delivery routes and predict costs based on real-time data.")

# Creating columns for buttons
col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 3])

with col2:
    if st.button("🌍 International Shipping"):
        switch_page("international")

with col4:
    if st.button("📦 Domestic Shipping"):
        switch_page("domestic")
