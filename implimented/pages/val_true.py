import streamlit as st
import json
from streamlit_lottie import st_lottie
# Load Lottie animations
def load_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


# Load animations from source folder
compliance_animation = load_lottie("compliance.json")
flagged_animation = load_lottie("flagged.json")

st.title("📜 Shipment Compliance Validation")

shipment_details = st.session_state.get("shipment", None)
if shipment_details:
    check_passed = shipment_details["Compliance Status"] == "✅ Compliant"

    if check_passed:
        st_lottie(compliance_animation, height=200)
        st.success("✅ Shipment is Compliant!")
    else:
        st_lottie(flagged_animation, height=200)
        st.error("❌ Shipment is Flagged!")

    st.subheader("📦 Shipment Details")
    for key, value in shipment_details.items():
        st.write(f"**{key}:** {value}")

    # LogiKal Chatbot
    from app_v1 import generate_llama2_response as llama2_response

    st.markdown("<h3 style='text-align: center;'>💬 LogiKal Chatbot</h3>", unsafe_allow_html=True)
    query = st.text_input("", placeholder="Ask about shipment compliance...")
    if query:
        response = llama2_response(query)
        st.write("### 🤖 Response:")
        st.write(response)
else:
    st.warning("No shipment details found. Please use the Predictor page first.")