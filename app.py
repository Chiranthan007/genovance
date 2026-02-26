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

    product_name = st.text_input("Product / Service Name", value="FocusFlow App")
    product_description = st.text_area(
        "Product Description",
        value="A productivity app that helps students manage tasks, deadlines, and focus sessions efficiently."
    )
    target_customer = st.text_input(
        "Target Customer",
        value="College students struggling with time management"
    )
    unique_value = st.text_input(
        "Unique Value Proposition",
        value="AI-powered smart scheduling and distraction tracking"
    )

    generate_pitch_btn = st.button("Generate Sales Pitch")

    if generate_pitch_btn:
        with st.spinner("Generating sales pitch..."):
            prompt = f"""
You are a sales strategist.

Based on the following inputs, create a structured and persuasive sales pitch.

Product Name: {product_name}
Product Description: {product_description}
Target Customer: {target_customer}
Unique Value Proposition: {unique_value}

Structure the pitch clearly using:

1. Hook
2. Problem Statement
3. Solution
4. Value Proposition
5. Closing Call-to-Action

Keep it clear, compelling, and moderately concise.
"""
            pitch_result = generate_ai_response(prompt)

        st.markdown("### Sales Pitch Output")
        st.write(pitch_result)


with tab3:
    st.header("Lead Scoring Engine")
    st.write("Evaluate the quality of a potential lead based on structured inputs.")

    company_size = st.selectbox(
        "Company Size",
        ["Student / Individual", "Startup (1-10)", "Small Business (10-50)", "Medium Business (50-200)", "Enterprise (200+)"]
    )

    budget_level = st.selectbox(
        "Budget Level",
        ["Low", "Moderate", "High"]
    )

    urgency = st.selectbox(
        "Purchase Urgency",
        ["Just Exploring", "Considering Options", "Ready to Buy Soon"]
    )

    engagement = st.selectbox(
        "Engagement Level",
        ["Visited Website Once", "Downloaded Brochure", "Requested Demo / Contacted Sales"]
    )

    generate_score_btn = st.button("Calculate Lead Score")

    if generate_score_btn:
        score = 0

        # Company size scoring
        if company_size == "Enterprise (200+)":
            score += 30
        elif company_size == "Medium Business (50-200)":
            score += 20
        elif company_size == "Small Business (10-50)":
            score += 15
        else:
            score += 10

        # Budget scoring
        if budget_level == "High":
            score += 30
        elif budget_level == "Moderate":
            score += 20
        else:
            score += 10

        # Urgency scoring
        if urgency == "Ready to Buy Soon":
            score += 25
        elif urgency == "Considering Options":
            score += 15
        else:
            score += 5

        # Engagement scoring
        if engagement == "Requested Demo / Contacted Sales":
            score += 25
        elif engagement == "Downloaded Brochure":
            score += 15
        else:
            score += 5

        st.markdown("### Lead Score Result")
        st.success(f"Lead Score: {score} / 110")

        if score >= 80:
            st.write("🔥 High-Quality Lead — Prioritize Immediately")
        elif score >= 55:
            st.write("⚡ Moderate Lead — Nurture Strategically")
        else:
            st.write("🌱 Early-Stage Lead — Add to Marketing Funnel")