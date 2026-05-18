import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from calculator import calculate_totals
from schedule import generate_schedule
from guidance import generate_guidance
from chatbot import (
    ask_emi_chatbot,
    get_ai_loan_insights
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Finance Dashboard",
    page_icon="💸",
    layout="wide"
)

# =========================================================
# SESSION STATES
# =========================================================

if "dashboard" not in st.session_state:
    st.session_state.dashboard = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================
# MODERN FINTECH CSS
# =========================================================

st.markdown("""
<style>

/* =========================================================
GLOBAL
========================================================= */

html, body, [class*="css"] {

    font-family: 'Poppins', sans-serif;

    color: white;
}

/* ========================================================= */

.stApp {

    background:
    radial-gradient(circle at top left, #111827, #020617);

    color: white;
}

/* ========================================================= */

.main {

    background: transparent;
}

/* ========================================================= */

.block-container {

    padding-top: 1rem;

    padding-left: 2rem;

    padding-right: 2rem;
}

/* =========================================================
SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
        180deg,
        #020617,
        #0f172a,
        #111827
    );

    border-right:
    1px solid rgba(255,255,255,0.08);
}

/* ========================================================= */

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* =========================================================
SIDEBAR TITLE
========================================================= */

.sidebar-title {

    padding-top: 10px;

    padding-bottom: 25px;
}

.sidebar-title h1 {

    color: white;

    font-size: 32px;

    line-height: 1.4;
}

.sidebar-title span {

    color: #38bdf8;
}

/* =========================================================
RADIO BUTTONS
========================================================= */

.stRadio > div {

    gap: 14px;
}

.stRadio label {

    background:
    rgba(255,255,255,0.04);

    border:
    1px solid rgba(255,255,255,0.08);

    padding: 14px 18px;

    border-radius: 16px;

    width: 100%;

    transition: 0.3s ease;

    font-size: 16px !important;

    font-weight: 500 !important;
}

.stRadio label:hover {

    background:
    linear-gradient(
        135deg,
        rgba(37,99,235,0.25),
        rgba(124,58,237,0.25)
    );

    border:
    1px solid #38bdf8;

    box-shadow:
    0px 0px 15px rgba(56,189,248,0.2);
}

/* =========================================================
HERO SECTION
========================================================= */

.hero {

    background:
    linear-gradient(
        135deg,
        rgba(37,99,235,0.15),
        rgba(124,58,237,0.15)
    );

    border:
    1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(18px);

    border-radius: 28px;

    padding: 45px;

    margin-bottom: 30px;

    box-shadow:
    0px 0px 30px rgba(37,99,235,0.12);
}

.hero h1 {

    font-size: 62px;

    color: white;

    margin-bottom: 15px;
}

.hero p {

    color: #cbd5e1;

    font-size: 20px;

    line-height: 1.8;
}

/* =========================================================
ABOUT CARD
========================================================= */

.about-card {

    background:
    rgba(15,23,42,0.8);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius: 28px;

    padding: 35px;

    margin-bottom: 35px;
}

.about-card h2 {

    color: white;

    font-size: 42px;

    margin-bottom: 18px;
}

.about-card p {

    color: #cbd5e1;

    font-size: 18px;

    line-height: 1.8;
}

/* =========================================================
FEATURE GRID
========================================================= */

.feature-grid {

    display: grid;

    grid-template-columns: repeat(3, 1fr);

    gap: 18px;

    margin-top: 25px;
}

.feature-box {

    background:
    rgba(255,255,255,0.03);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius: 18px;

    padding: 22px;

    transition: 0.3s ease;
}

.feature-box:hover {

    transform: translateY(-5px);

    border:
    1px solid #38bdf8;

    box-shadow:
    0px 0px 18px rgba(56,189,248,0.15);
}

.feature-box h4 {

    color: white;

    margin-top: 12px;

    font-size: 18px;
}

.feature-box p {

    color: #94a3b8;

    font-size: 14px;
}

/* =========================================================
FORM CARD
========================================================= */

.form-card {

    background:
    rgba(15,23,42,0.8);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius: 28px;

    padding: 35px;

    margin-bottom: 30px;
}

/* =========================================================
INPUTS
========================================================= */

label {

    color: #e2e8f0 !important;

    font-weight: 500 !important;
}

.stNumberInput input,
.stTextInput input,
.stTextArea textarea {

    background:
    rgba(255,255,255,0.04) !important;

    color: white !important;

    border-radius: 14px !important;

    border:
    1px solid rgba(255,255,255,0.08) !important;

    font-size: 17px !important;

    font-weight: 600 !important;
}

/* =========================================================
BUTTONS
========================================================= */

.stButton > button {

    background:
    linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );

    color: white;

    border: none;

    border-radius: 14px;

    padding: 14px;

    font-weight: 600;

    transition: 0.3s ease;

    width: 100%;
}

.stButton > button:hover {

    transform: scale(1.02);

    box-shadow:
    0px 0px 18px rgba(37,99,235,0.3);
}

/* =========================================================
SECTION TITLE
========================================================= */

.section-title {

    font-size: 40px;

    font-weight: 700;

    margin-bottom: 25px;

    color: white;
}

/* =========================================================
METRIC CARDS
========================================================= */

.metric-card {

    border-radius: 24px;

    padding: 30px;

    min-height: 220px;

    color: white;

    border:
    1px solid rgba(255,255,255,0.08);

    transition: 0.3s ease;
}

.metric-card:hover {

    transform: translateY(-6px);
}

.metric-card h4 {

    font-size: 22px;

    margin-bottom: 30px;
}

.metric-card h2 {

    font-size: 50px;

    font-weight: 700;

    margin-bottom: 15px;
}

.metric-card p {

    color: rgba(255,255,255,0.75);

    font-size: 16px;
}

/* =========================================================
CARD COLORS
========================================================= */

.blue-card {

    background:
    linear-gradient(
        135deg,
        #1d4ed8,
        #1e3a8a
    );
}

.green-card {

    background:
    linear-gradient(
        135deg,
        #059669,
        #065f46
    );
}

.purple-card {

    background:
    linear-gradient(
        135deg,
        #7c3aed,
        #4c1d95
    );
}

.orange-card {

    background:
    linear-gradient(
        135deg,
        #ea580c,
        #9a3412
    );
}

/* =========================================================
CHATBOT
========================================================= */

.chat-box {

    background:
    rgba(15,23,42,0.8);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 25px;
}

.user-msg {

    background:
    linear-gradient(
        135deg,
        #2563eb,
        #7c3aed
    );

    padding: 14px;

    border-radius: 14px;

    margin-bottom: 12px;

    width: fit-content;

    margin-left: auto;

    max-width: 80%;
}

.bot-msg {

    background:
    rgba(30,41,59,0.9);

    padding: 14px;

    border-radius: 14px;

    margin-bottom: 12px;

    width: fit-content;

    max-width: 80%;
}

footer {

    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("""

<div class='sidebar-title'>

<h1>💼 AI Finance <br><span>Dashboard</span></h1>

</div>

""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Analytics",
        "Repayment Schedule",
        "AI Assistant"
    ]
)

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""

<div class='hero'>

<h1>💸 AI Finance Dashboard</h1>

<p>

A futuristic AI-powered fintech platform for EMI planning,
loan analytics, financial risk prediction,
smart repayment optimization,
and intelligent AI financial assistance.

</p>

</div>

""", unsafe_allow_html=True)

# =========================================================
# FORM SECTION
# =========================================================

if not st.session_state.dashboard:

    st.markdown("""
    <div class='section-title'>
    📋 Loan Application Form
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='form-card'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        principal = st.number_input(
            "Loan Amount (₹)",
            min_value=1000.0,
            value=700000.0,
            step=1000.0
        )

        annual_rate = st.number_input(
            "Interest Rate (%)",
            min_value=0.1,
            value=10.0,
            step=0.1
        )

        tenure_years = st.slider(
            "Loan Tenure (Years)",
            1,
            30,
            5
        )

    with col2:

        monthly_income = st.number_input(
            "Monthly Income (₹)",
            min_value=1.0,
            value=43000.0,
            step=1000.0
        )

        existing_emi = st.number_input(
            "Existing EMI (₹)",
            min_value=0.0,
            value=0.0,
            step=1000.0
        )

        savings = st.number_input(
            "Monthly Savings (₹)",
            min_value=0.0,
            value=10000.0,
            step=1000.0
        )

    with col3:

        credit_score = st.slider(
            "Credit Score",
            300,
            900,
            750
        )

        age = st.slider(
            "Age",
            18,
            65,
            28
        )

        dependents = st.slider(
            "Dependents",
            0,
            10,
            2
        )

    if st.button("🚀 Generate Dashboard"):

        st.session_state.dashboard = True

        st.session_state.principal = principal
        st.session_state.rate = annual_rate
        st.session_state.tenure = tenure_years
        st.session_state.income = monthly_income
        st.session_state.credit = credit_score
        st.session_state.existing_emi = existing_emi
        st.session_state.savings = savings
        st.session_state.age = age
        st.session_state.dependents = dependents

        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# SHOW DASHBOARD AFTER BUTTON CLICK
# =========================================================

else:

    principal = st.session_state.principal
    annual_rate = st.session_state.rate
    tenure_years = st.session_state.tenure
    monthly_income = st.session_state.income
    existing_emi = st.session_state.existing_emi
    credit_score = st.session_state.credit
    savings = st.session_state.savings

    months = int(tenure_years * 12)

    totals = calculate_totals(
        principal,
        annual_rate,
        months
    )

    emi = totals["emi"]
    total_payment = totals["total_payment"]
    total_interest = totals["total_interest"]

    schedule_df = generate_schedule(
        principal,
        annual_rate,
        months
    )

    affordability_ratio = (
        (emi + existing_emi)
        / max(monthly_income, 1)
    ) * 100

    if affordability_ratio < 35:

        risk = "Low Risk"
        score = 90

    elif affordability_ratio < 50:

        risk = "Moderate Risk"
        score = 65

    else:

        risk = "High Risk"
        score = 40

    loan_context = f"""
    Loan Amount: ₹{principal}
    EMI: ₹{emi}
    Interest Rate: {annual_rate}%
    Risk: {risk}
    """

    # =====================================================
    # DASHBOARD PAGE
    # =====================================================

    if page == "Dashboard":

        st.markdown("""
        <div class='section-title'>
        📊 Financial Overview
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.markdown(f"""
            <div class='metric-card blue-card'>
            <h4>💳 Monthly EMI</h4>
            <h2>₹ {emi:,.0f}</h2>
            <p>Your monthly installment</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:

            st.markdown(f"""
            <div class='metric-card green-card'>
            <h4>💰 Total Payment</h4>
            <h2>₹ {total_payment:,.0f}</h2>
            <p>Total amount to be paid</p>
            </div>
            """, unsafe_allow_html=True)

        with c3:

            st.markdown(f"""
            <div class='metric-card purple-card'>
            <h4>📈 Interest</h4>
            <h2>₹ {total_interest:,.0f}</h2>
            <p>Total interest amount</p>
            </div>
            """, unsafe_allow_html=True)

        with c4:

            st.markdown(f"""
            <div class='metric-card orange-card'>
            <h4>⚠ Risk Level</h4>
            <h2>{risk}</h2>
            <p>Your financial risk status</p>
            </div>
            """, unsafe_allow_html=True)

    # =====================================================
    # ANALYTICS PAGE
    # =====================================================

    elif page == "Analytics":

        st.subheader("📈 Financial Analytics")

        col1, col2 = st.columns(2)

        with col1:

            pie_df = pd.DataFrame({
                "Type": ["Principal", "Interest"],
                "Amount": [principal, total_interest]
            })

            fig = px.pie(
                pie_df,
                names="Type",
                values="Amount",
                hole=0.6,
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': "Financial Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#38bdf8"}
                }
            ))

            gauge.update_layout(
                template="plotly_dark",
                height=450
            )

            st.plotly_chart(
                gauge,
                use_container_width=True
            )

    # =====================================================
    # REPAYMENT SCHEDULE PAGE
    # =====================================================

    elif page == "Repayment Schedule":

        st.markdown("""
        <div class='section-title'>
        📅 Loan Repayment Schedule
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            schedule_df,
            use_container_width=True,
            height=600
        )

        csv = schedule_df.to_csv(index=False)

        st.download_button(
            label="⬇ Download Repayment Schedule",
            data=csv,
            file_name="loan_repayment_schedule.csv",
            mime="text/csv"
        )

    # =====================================================
    # AI ASSISTANT PAGE
    # =====================================================

    elif page == "AI Assistant":

        st.markdown("""
        <div class='section-title'>
        🤖 AI Finance Assistant
        </div>
        """, unsafe_allow_html=True)

        ai_insight = get_ai_loan_insights(
            loan_context
        )

        st.markdown("""
        <div class='chat-box'>
        """, unsafe_allow_html=True)

        st.markdown("""
        <h2 style="
            color:white;
            margin-bottom:20px;
            font-size:28px;
        ">
        💡 AI Financial Insights
        </h2>
        """, unsafe_allow_html=True)

        st.write(ai_insight)

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        for msg in st.session_state.messages:

            if msg["role"] == "user":

                st.markdown(
                    f"""
                    <div class='user-msg'>
                    {msg["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class='bot-msg'>
                    {msg["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        user_prompt = st.text_input(
            "Ask anything about EMI, loans, savings..."
        )

        if st.button("🚀 Generate AI Assistant Response"):

            if user_prompt.strip() != "":

                st.session_state.messages.append({
                    "role": "user",
                    "content": user_prompt
                })

                reply = ask_emi_chatbot(
                    user_prompt,
                    loan_context
                )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply
                })

                st.rerun()