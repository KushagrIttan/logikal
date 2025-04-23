import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


st.title("🔍 Compliance Predictor")

with st.form("shipment_form"):
    parcel_id = st.text_input("Parcel ID")
    declared_value = st.number_input("Declared Value ($)", min_value=0.0)
    weight = st.number_input("Weight (kg)", min_value=0.1)
    destination = st.selectbox("Destination Country", ["USA", "Canada", "Germany", "India", "China"])
    submitted = st.form_submit_button("Check Compliance")

if submitted:
    compliance_passed = declared_value < 2000  # Fake compliance rule
    st.session_state["shipment"] = {
        "Parcel ID": parcel_id,
        "Declared Value": f"${declared_value}",
        "Weight": f"{weight} kg",
        "Destination": destination,
        "Compliance Status": "✅ Compliant" if compliance_passed else "❌ Flagged",
        "Remarks": "All checks passed." if compliance_passed else "Declared value exceeds limit. Attach Form XYZ."
    }
    st.success("Redirecting to Validation...")
    st.switch_page("pages/val_true.py")
    st.experimental_rerun()