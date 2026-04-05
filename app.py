import streamlit as st
from code import graph

st.set_page_config(page_title="AI Travel Planner", layout="wide")

# -------------------------------
# STYLING
# -------------------------------
st.markdown("""
<style>
    .stTextInput input {
        font-size: 16px;
        padding: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.title("✈️ AI Agentic Travel Planner")
st.write("Plan your trip using AI agents (Flights ✈️ Hotels 🏨 Itinerary 📍)")

# -------------------------------
# INPUT
# -------------------------------
user_input = st.text_input(
    "Enter your travel plan:",
    placeholder="e.g. Plan a 3-day trip from Bangalore to Goa under ₹20000"
)

# Quick suggestions
col1, col2 = st.columns(2)

with col1:
    if st.button("Goa Trip"):
        user_input = "Plan a 3-day trip to Goa under ₹15000"

with col2:
    if st.button("Maldives Trip"):
        user_input = "Plan a Maldives luxury trip"

# -------------------------------
# GENERATE BUTTON
# -------------------------------
if st.button("Generate Plan 🚀"):

    if user_input.strip() == "":
        st.warning("Please enter a travel query")

    else:
        with st.spinner("Planning your trip... 🤖"):
            result = graph.invoke({
                "user_input": user_input,
                "flights": "",
                "hotels": "",
                "itinerary": "",
                "budget_check": "",
                "final_plan": ""
            })

        st.success("✅ Plan Generated!")

        # -------------------------------
        # CHAT STYLE OUTPUT
        # -------------------------------
        st.chat_message("user").write(user_input)
        st.chat_message("assistant").write(result["final_plan"])

        # -------------------------------
        # DASHBOARD VIEW
        # -------------------------------
        st.markdown("## 📊 Detailed Breakdown")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✈️ Flights")
            st.info(result["flights"])

            st.markdown("### 🏨 Hotels")
            st.info(result["hotels"])

        with col2:
            st.markdown("### 📍 Itinerary")
            st.success(result["itinerary"])

            st.markdown("### 💰 Budget")
            st.warning(result["budget_check"])