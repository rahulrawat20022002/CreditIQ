import json
from groq import Groq

EMPLOYMENT_DURATION_DISPLAY = {
    "unemployed":   "Unemployed",
    "< 1 year":     "Less than 1 year",
    "1<=X<4 years": "1–4 years",
    "4<=X<7 years": "4–7 years",
    ">= 7 years":   "7+ years",
}


def get_explanation(data: dict, pred_result: dict, api_key: str) -> str:
    explain_data = dict(data)
    raw_dur = data.get("employment_duration", "")
    explain_data["employment_duration"] = EMPLOYMENT_DURATION_DISPLAY.get(raw_dur, raw_dur)

    client  = Groq(api_key=api_key)
    verdict = "APPROVED" if pred_result["approved"] else "REJECTED"

    prompt = f"""The credit model returned:

VERDICT: {verdict}
Creditworthiness Probability: {pred_result['prob_good']}%
Default Risk: {pred_result['prob_bad']}%

Applicant Profile: {json.dumps(explain_data, indent=2)}

Write a concise professional explanation (5–7 sentences) for the loan officer covering:
- Why the model gave this verdict
- Top 2–3 positive factors
- Top 2–3 risk factors  
- One actionable recommendation for the loan officer

Use **bold** for key terms. Be direct, professional, and free of jargon."""

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a senior credit analyst. Be concise, structured, and professional. Avoid technical ML terminology."},
            {"role": "user",   "content": prompt},
        ],
        max_tokens=500,
    )
    return resp.choices[0].message.content
