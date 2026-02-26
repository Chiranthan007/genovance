import os
import google.generativeai as genai
import streamlit as st

from dotenv import load_dotenv
load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not GENAI_API_KEY:
    st.error("API key not found. Please set GENAI_API_KEY.")
    st.stop()

genai.configure(api_key=GENAI_API_KEY)

# Initialize model
model = genai.GenerativeModel("gemini-2.5-flash")

# 👇 ADD THE FUNCTION HERE
def generate_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {e}"

st.set_page_config(page_title="Genovance", layout="wide")

st.title("Genovance")
st.subheader("AI-Powered Business Growth Assistant")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(
    ["Campaign Strategy", "Sales Pitch", "Lead Scoring"]
)

with tab1:
    st.header("Campaign Strategy Generator")
    st.write("Generate a strategic marketing campaign plan.")

    business_type = st.text_input("Business Type", value="SaaS productivity app")
    target_audience = st.text_input("Target Audience", value="College students and young professionals")
    budget = st.selectbox("Marketing Budget", ["Low", "Medium", "High"])
    goal = st.selectbox("Primary Goal", ["Brand Awareness", "Lead Generation", "Sales Conversion"])

    generate_btn = st.button("Generate Campaign Strategy")

    if generate_btn:
        with st.spinner("Generating strategy..."):
            prompt = f"""
You are a marketing strategist.

Based on the following inputs, generate a structured campaign plan.

Business Type: {business_type}
Target Audience: {target_audience}
Budget Level: {budget}
Primary Goal: {goal}

Provide the output in the following structured format:

1. Market Insight
2. Campaign Concept
3. Recommended Channels (bullet points)
4. Sample Ad Copy
5. Key Performance Metrics to Track

Keep it strategic, clear, and concise.
"""
            result = generate_ai_response(prompt)

        st.markdown("### Campaign Strategy Output")
        st.write(result)


with tab2:
    st.header("Sales Pitch Generator")
    st.write("Create a persuasive sales pitch for your product.")
    st.info("Coming soon in next build phase.")


with tab3:
    st.header("Lead Scoring & Analysis")
    st.write("Evaluate and prioritize potential leads.")
    st.info("Coming soon in next build phase.")