from groq import Groq

# =========================================================
# GROQ API KEY
# =========================================================

API_KEY = "Get_Your_API_Key"

# =========================================================
# CREATE CLIENT
# =========================================================

client = Groq(api_key=API_KEY)

# =========================================================
# EMI CHATBOT
# =========================================================

def ask_emi_chatbot(
    user_query,
    loan_context
):

    system_prompt = f"""
You are an EMI Planner Assistant inside a finance dashboard.

Rules:
- Answer only EMI, loan, repayment, interest,
  affordability, schedule, and comparison related questions.
- Use the current loan context whenever useful.
- Keep answers short, clear, and student-friendly.
- Do not invent numbers when exact values
  are already provided in the context.
- If the user asks unrelated questions,
  politely say you only help with loan and EMI planning.

Current loan context:
{loan_context}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[

                {
                    "role": "system",
                    "content": system_prompt
                },

                {
                    "role": "user",
                    "content": user_query
                }
            ],

            temperature=0.3,
            max_tokens=250
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq Error: {str(e)}"

# =========================================================
# AI LOAN INSIGHTS
# =========================================================

def get_ai_loan_insights(
    loan_context
):

    system_prompt = f"""
You are an EMI analysis assistant.

Based on the loan details below, return:
1. A short summary of the loan burden.
2. Whether the EMI looks affordable.
3. One suggestion to reduce cost.

Keep the answer in 3 bullet points only.
Use simple language.

Loan details:
{loan_context}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                }
            ],

            temperature=0.3,
            max_tokens=200
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq Error: {str(e)}"

# =========================================================
# AI COMPARISON INSIGHT
# =========================================================

def get_ai_comparison_insight(
    comparison_table_text
):

    system_prompt = f"""
You are a loan comparison assistant.

Read the loan comparison data and answer:
- Which loan looks better overall?
- Why?
- What tradeoff should the user know?

Keep the answer short and simple.

Comparison data:
{comparison_table_text}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.1-8b-instant",

            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                }
            ],

            temperature=0.3,
            max_tokens=200
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Groq Error: {str(e)}"