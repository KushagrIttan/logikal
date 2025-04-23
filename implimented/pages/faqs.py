import streamlit as st

st.title("❓ Frequently Asked Questions")
faqs = {
        "What is shipment compliance?": "Shipment compliance ensures parcels meet legal and regulatory requirements before international shipping.",
        "What happens if my parcel is flagged?": "If flagged, the system will explain why and suggest corrective actions.",
        "Can I add new compliance rules?": "Currently, rules are predefined, but future versions may allow admin rule customization.",
        "How does the chatbot help?": "The chatbot provides instant answers regarding compliance rules and flagged shipments."
    }
for q, a in faqs.items():
        with st.expander(q):
            st.write(a)
