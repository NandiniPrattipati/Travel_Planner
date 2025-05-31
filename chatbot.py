# travel_itinerary_app.py

import streamlit as st
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
import os

# --- Page Setup ---
st.set_page_config(page_title="Travel Itinerary Planner", page_icon="🌍")
st.title("🌍 Travel Itinerary Planner")
st.markdown("Plan your perfect trip in seconds with AI ✈️")

# --- Input Fields ---
place = st.text_input("Enter destination (e.g., Paris, Japan)")
days = st.slider("Number of days", 1, 14, 3)
style = st.selectbox("Preferred travel style", ["Adventure", "Budget", "Luxury", "Cultural", "Foodie", "Relaxing"])

# --- API Key (via secrets) ---
if "GROQ_API_KEY" not in st.secrets:
    st.error("Please set your GROQ_API_KEY in .streamlit/secrets.toml")
    st.stop()

groq_api_key = st.secrets["GROQ_API_KEY"]

# --- LLM Setup ---
os.environ["GROQ_API_KEY"] = groq_api_key
llm = ChatGroq(temperature=0.7, groq_api_key=groq_api_key, model_name="mistral-saba-24b")


# --- Prompt Template ---
prompt = PromptTemplate(
    input_variables=["place", "days", "style"],
    template="""
You are a helpful travel assistant.
Create a {days}-day travel itinerary for {place}.
The traveler prefers {style} experiences.
Include:
- Day-by-day plan
- Attractions or activities
- Food/restaurant suggestions
- 1 travel tip at the end

Format it clearly.
"""
)

# # --- Button Action ---
# if st.button("Generate Itinerary", key="generate") and place:
#     with st.spinner("Planning your trip..."):
#         formatted_prompt = prompt.format(place=place, days=days, style=style)
#         response = llm([HumanMessage(content=formatted_prompt)])
#         st.success("Here's your personalized itinerary!")
#         st.write(response.content)

# elif st.button("Generate Itinerary", key="generate_no_place") and not place:
#     st.warning("Please enter a destination first.")
if st.button("🧳 Plan My Trip", key="plan_trip"):
    if place:
        with st.spinner("Planning your trip..."):
            formatted_prompt = prompt.format(place=place, days=days, style=style)
            response = llm([HumanMessage(content=formatted_prompt)])
            st.success("Here's your personalized itinerary!")
            st.write(response.content)
    else:
        st.warning("Please enter a destination first.")