import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

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
# CSV STORAGE FILES
# =========================================================

USER_DATA_FILE = "user_details.csv"
COMPARISON_FILE = "loan_comparison.csv"

# =========================================================
# CREATE CSV FILES IF NOT EXISTS
# =========================================================

if not os.path.exists(USER_DATA_FILE):

    user_df = pd.DataFrame(columns=[
        "Timestamp",
        "Loan Amount",
        "Interest Rate",
        "Tenure",
        "Monthly Income",
        "Existing EMI",
        "Savings",
        "Credit Score",
        "Age",
        "Dependents"
    ])

    user_df.to_csv(USER_DATA_FILE, index=False)

if not os.path.exists(COMPARISON_FILE):

    comparison_df = pd.DataFrame(columns=[
        "Loan Amount",
        "Interest Rate",
        "Tenure",
        "Monthly EMI",
        "Total Payment",
        "Total Interest"
    ])

    comparison_df.to_csv(COMPARISON_FILE, index=False)

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

html, body, [class*="css"] {

    font-family: 'Poppins', sans-serif;
    color: white;
}

.stApp {

    background:
    radial-gradient(circle at top left, #111827, #020617);

    color: white;
}

.main {

    background: transparent;
}

.block-container {

    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

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

section[data-testid="stSidebar"] * {

    color: white !important;
}

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
    width: 100%;
}

.metric-card {

    border-radius: 24px;
    padding: 30px;
    min-height: 220px;
    color: white;
    border:
    1px solid rgba(255,255,255,0.08);
}

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

.section-title {

    font-size: 38px;
    font-weight: 700;
    margin-bottom: 25px;
    color: white;
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
        "Loan Comparison",
        "Repayment Schedule",
        "AI Assistant"
    ]
)

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""

<div style="
background:linear-gradient(135deg, rgba(37,99,235,0.2), rgba(124,58,237,0.2));
padding:40px;
border-radius:28px;
margin-bottom:30px;
">

<h1 style="font-size:60px;">
💸 AI Finance Dashboard
</h1>

<p style="font-size:20px;color:#cbd5e1;">

AI-powered fintech platform for EMI planning,
loan analytics,
repayment optimization,
and intelligent financial insights.

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

    col1, col2, col3 = st.columns(3)

    with col1:

        principal = st.number_input(
            "Loan Amount (₹)",
            min_value=1000.0,
            value=700000.0
        )

        annual_rate = st.number_input(
            "Interest Rate (%)",
            min_value=0.1,
            value=10.0
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
            value=43000.0
        )

        existing_emi = st.number_input(
            "Existing EMI (₹)",
            min_value=0.0,
            value=0.0
        )

        savings = st.number_input(
            "Monthly Savings (₹)",
            min_value=0.0,
            value=10000.0
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

        # =====================================================
        # SAVE USER DETAILS TO CSV
        # =====================================================

        new_user = pd.DataFrame([{
            "Timestamp": datetime.now(),
            "Loan Amount": principal,
            "Interest Rate": annual_rate,
            "Tenure": tenure_years,
            "Monthly Income": monthly_income,
            "Existing EMI": existing_emi,
            "Savings": savings,
            "Credit Score": credit_score,
            "Age": age,
            "Dependents": dependents
        }])

        new_user.to_csv(
            USER_DATA_FILE,
            mode='a',
            header=False,
            index=False
        )

        st.session_state.dashboard = True

        st.session_state.principal = principal
        st.session_state.rate = annual_rate
        st.session_state.tenure = tenure_years
        st.session_state.income = monthly_income
        st.session_state.credit = credit_score
        st.session_state.existing_emi = existing_emi
        st.session_state.savings = savings

        st.rerun()

# =========================================================
# DASHBOARD LOGIC
# =========================================================

else:

    principal = st.session_state.principal
    annual_rate = st.session_state.rate
    tenure_years = st.session_state.tenure
    monthly_income = st.session_state.income
    existing_emi = st.session_state.existing_emi

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
            </div>
            """, unsafe_allow_html=True)

        with c2:

            st.markdown(f"""
            <div class='metric-card green-card'>
            <h4>💰 Total Payment</h4>
            <h2>₹ {total_payment:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)

        with c3:

            st.markdown(f"""
            <div class='metric-card purple-card'>
            <h4>📈 Interest</h4>
            <h2>₹ {total_interest:,.0f}</h2>
            </div>
            """, unsafe_allow_html=True)

        with c4:

            affordability_ratio = (
                (emi + existing_emi)
                / max(monthly_income, 1)
            ) * 100

            risk = "Low Risk"

            if affordability_ratio > 50:
                risk = "High Risk"

            elif affordability_ratio > 35:
                risk = "Moderate Risk"

            st.markdown(f"""
            <div class='metric-card orange-card'>
            <h4>⚠ Risk Level</h4>
            <h2>{risk}</h2>
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

            score = 85

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
    # LOAN COMPARISON PAGE
    # =====================================================

    elif page == "Loan Comparison":

        st.markdown("""
        <div class='section-title'>
        🔍 Loan Comparison
        </div>
        """, unsafe_allow_html=True)

        compare_loan = st.number_input(
            "Comparison Loan Amount",
            min_value=1000.0,
            value=500000.0
        )

        compare_rate = st.number_input(
            "Comparison Interest Rate (%)",
            min_value=0.1,
            value=8.5
        )

        compare_tenure = st.slider(
            "Comparison Tenure",
            1,
            30,
            10
        )

        if st.button("📊 Compare Loans"):

            compare_months = compare_tenure * 12

            compare_totals = calculate_totals(
                compare_loan,
                compare_rate,
                compare_months
            )

            comparison_df = pd.DataFrame({

                "Loan Type": [
                    "Current Loan",
                    "Comparison Loan"
                ],

                "Loan Amount": [
                    principal,
                    compare_loan
                ],

                "Interest Rate": [
                    annual_rate,
                    compare_rate
                ],

                "EMI": [
                    emi,
                    compare_totals["emi"]
                ],

                "Total Payment": [
                    total_payment,
                    compare_totals["total_payment"]
                ],

                "Interest": [
                    total_interest,
                    compare_totals["total_interest"]
                ]
            })

            st.dataframe(
                comparison_df,
                use_container_width=True
            )

            fig = px.bar(
                comparison_df,
                x="Loan Type",
                y="EMI",
                color="Loan Type",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            comparison_df.to_csv(
                COMPARISON_FILE,
                index=False
            )

            csv = comparison_df.to_csv(index=False)

            st.download_button(
                label="⬇ Download Comparison Report",
                data=csv,
                file_name="loan_comparison_report.csv",
                mime="text/csv"
            )

    # =====================================================
    # REPAYMENT SCHEDULE
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
    # AI ASSISTANT
    # =====================================================

    elif page == "AI Assistant":

        st.markdown("""
        <div class='section-title'>
        🤖 AI Finance Assistant
        </div>
        """, unsafe_allow_html=True)

        loan_context = f"""

        Loan Amount: ₹{principal}
        EMI: ₹{emi}
        Interest Rate: {annual_rate}%

        """

        ai_insight = get_ai_loan_insights(
            loan_context
        )

        st.write(ai_insight)

        for msg in st.session_state.messages:

            st.chat_message(msg["role"]).write(
                msg["content"]
            )

        user_prompt = st.chat_input(
            "Ask about loans, EMI, savings..."
        )

        if user_prompt:

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
