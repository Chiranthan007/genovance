import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv

# =========================
# Setup
# =========================
load_dotenv()
PRIMARY_KEY = os.getenv("GENAI_API_KEY_PRIMARY")
BACKUP_KEY = os.getenv("GENAI_API_KEY_BACKUP")

if not PRIMARY_KEY:
    st.error("Primary API key missing.")
    st.stop()

# Start with primary key
genai.configure(api_key=PRIMARY_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")


# =========================
# Safe AI Wrapper
# =========================
def generate_ai_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        error_str = str(e).lower()

        if ("429" in error_str or "quota" in error_str) and BACKUP_KEY:
            try:
                genai.configure(api_key=BACKUP_KEY)
                backup_model = genai.GenerativeModel("models/gemini-2.5-flash")
                response = backup_model.generate_content(prompt)
                return response.text
            except Exception:
                pass

        return f"Error generating response: {e}"


# =========================
# App Layout
# =========================
st.set_page_config(page_title="Genovance", layout="wide")

st.title("Genovance")
st.subheader("Unified AI Co-Pilot for Strategy, Messaging & Conversion")
st.markdown(
"""
Genovance mirrors the real startup growth lifecycle:

**1. Strategy → 2. Messaging → 3. Conversion Intelligence**

An integrated GenAI engine that helps founders design campaigns,
craft persuasive positioning, and prioritize high-value leads.
"""
)

st.markdown("---")

tab1, tab2, tab3 = st.tabs(
    ["Strategy Layer", "Messaging Layer", "Conversion Intelligence Layer"]
)

# =========================
# 1️⃣ Strategy Layer
# =========================
with tab1:
    st.header("Campaign Strategy Intelligence")

    if "campaign_result" not in st.session_state:
        st.session_state.campaign_result = ""

    with st.form("campaign_form"):
        business_type = st.text_input(
            "Business Type",
            value="SaaS productivity app"
        )
        target_audience = st.text_input(
            "Target Audience",
            value="College students and young professionals"
        )
        budget = st.selectbox(
            "Marketing Budget",
            ["Low", "Medium", "High"]
        )
        goal = st.selectbox(
            "Primary Goal",
            ["Brand Awareness", "Lead Generation", "Sales Conversion"]
        )

        submitted = st.form_submit_button("Generate Strategic Plan")

    if submitted:
        prompt = f"""
You are a senior growth strategist.

Business: {business_type}
Target Audience: {target_audience}
Budget Level: {budget}
Primary Goal: {goal}

Deliver a structured strategic campaign plan:

1. Market Insight
2. Strategic Campaign Concept
3. Channel Selection Rationale
4. Sample Executive-Level Ad Copy
5. Key Performance Metrics

Tone: Professional, strategic, investor-ready.
"""

        with st.spinner("Generating strategic intelligence..."):
            st.session_state.campaign_result = generate_ai_response(prompt)

    st.markdown("### Strategic Output")
    if st.session_state.campaign_result:
        st.markdown(st.session_state.campaign_result)
    else:
        st.info("Generated strategy will appear here.")


# =========================
# 2️⃣ Messaging Layer
# =========================
with tab2:
    st.header("Sales Positioning Intelligence")

    product_name = st.text_input(
        "Product / Service Name",
        value="FocusFlow App"
    )
    product_description = st.text_area(
        "Product Description",
        value="An AI-powered productivity system that optimizes task planning and focus sessions."
    )
    target_customer = st.text_input(
        "Target Customer",
        value="College students struggling with time management"
    )
    unique_value = st.text_input(
        "Unique Value Proposition",
        value="AI-based adaptive scheduling and distraction analytics"
    )

    if st.button("Generate Persuasive Positioning"):

        prompt = f"""
You are a senior sales strategist.

Product: {product_name}
Description: {product_description}
Target Customer: {target_customer}
Unique Value: {unique_value}

Deliver:

1. Executive Hook
2. Core Pain Point Framing
3. Solution Narrative
4. Value Proposition Expansion
5. Conversion-Focused Call to Action

Tone: Confident, persuasive, outcome-oriented.
"""

        with st.spinner("Generating messaging intelligence..."):
            pitch_result = generate_ai_response(prompt)

        st.markdown("### Messaging Output")
        st.markdown(pitch_result)


# =========================
# 3️⃣ Conversion Intelligence Layer
# =========================
with tab3:
    st.header("Lead Qualification & Conversion Intelligence")

    company_size = st.selectbox(
        "Company Size",
        [
            "Student / Individual",
            "Startup (1-10)",
            "Small Business (10-50)",
            "Medium Business (50-200)",
            "Enterprise (200+)"
        ]
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
        [
            "Visited Website Once",
            "Downloaded Brochure",
            "Requested Demo / Contacted Sales"
        ]
    )

    if st.button("Analyze Lead Potential"):

        score = 0

        # Deterministic weighted scoring
        if company_size == "Enterprise (200+)":
            score += 30
        elif company_size == "Medium Business (50-200)":
            score += 20
        elif company_size == "Small Business (10-50)":
            score += 15
        else:
            score += 10

        if budget_level == "High":
            score += 30
        elif budget_level == "Moderate":
            score += 20
        else:
            score += 10

        if urgency == "Ready to Buy Soon":
            score += 25
        elif urgency == "Considering Options":
            score += 15
        else:
            score += 5

        if engagement == "Requested Demo / Contacted Sales":
            score += 25
        elif engagement == "Downloaded Brochure":
            score += 15
        else:
            score += 5

        normalized_score = round((score / 110) * 100)

        st.markdown("### Lead Intelligence Score")
        st.success(f"Score: {normalized_score} / 100")

        if normalized_score >= 80:
            category = "High-Intent Conversion Opportunity"
        elif normalized_score >= 50:
            category = "Warm Opportunity"
        else:
            category = "Early-Stage Prospect"

        st.markdown(f"**Classification:** {category}")

        # AI Strategic Interpretation Layer
        explanation_prompt = f"""
You are a senior revenue strategist.

Lead Score: {normalized_score}/100
Classification: {category}
Company Size: {company_size}
Budget Level: {budget_level}
Urgency: {urgency}
Engagement: {engagement}

Provide:

1. Why this lead achieved this score
2. Strategic next step for sales team
3. Recommended communication tone

Keep it concise, executive-level, and actionable.
"""

        with st.spinner("Generating conversion intelligence..."):
            advisory = generate_ai_response(explanation_prompt)

        st.markdown("### Strategic Conversion Advisory")
        st.markdown(advisory)