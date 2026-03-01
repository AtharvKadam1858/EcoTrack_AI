from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import anthropic
import os
import json

app = Flask(__name__)
CORS(app)

# Anthropic client (uses ANTHROPIC_API_KEY env var automatically)
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

# ── Emission Factors (BEE India / IPCC) ──
ENERGY_EF = 0.82    # kg CO2 per kWh (India grid average)
WATER_EF  = 0.0003  # kg CO2 per litre
PAPER_EF  = 20.0    # kg CO2 per ream

def calc_carbon(energy, water, paper):
    return round(energy * ENERGY_EF + water * WATER_EF + paper * PAPER_EF, 2)

def calc_score(energy, water, paper, employees=10):
    if employees < 1:
        employees = 1
    pe = energy / employees
    pw = water / employees
    pp = paper / employees
    bench_e, bench_w, bench_p = 200, 400, 1
    score = 100
    if pe > bench_e:
        score -= min(30, ((pe - bench_e) / bench_e) * 30)
    if pw > bench_w:
        score -= min(25, ((pw - bench_w) / bench_w) * 25)
    if pp > bench_p:
        score -= min(20, ((pp - bench_p) / bench_p) * 20)
    return max(10, round(score))

# ── Routes ──
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    energy    = float(data.get("energy", 0))
    water     = float(data.get("water", 0))
    paper     = float(data.get("paper", 0))
    employees = int(data.get("employees", 10))

    carbon = calc_carbon(energy, water, paper)
    score  = calc_score(energy, water, paper, employees)

    # Breakdown
    e_co2 = round(energy * ENERGY_EF, 2)
    w_co2 = round(water  * WATER_EF,  2)
    p_co2 = round(paper  * PAPER_EF,  2)

    return jsonify({
        "carbon": carbon,
        "score":  score,
        "breakdown": {
            "energy_co2": e_co2,
            "water_co2":  w_co2,
            "paper_co2":  p_co2
        }
    })

@app.route("/api/ai-insights", methods=["POST"])
def ai_insights():
    data     = request.get_json()
    energy   = float(data.get("energy",    0))
    water    = float(data.get("water",     0))
    paper    = float(data.get("paper",     0))
    employees= int(data.get("employees",  10))
    question = data.get("question", "").strip()
    carbon   = calc_carbon(energy, water, paper)
    score    = calc_score(energy, water, paper, employees)

    prompt = f"""You are EcoTrack AI, a sustainability intelligence assistant for Indian offices.
Help office managers reduce carbon footprint and achieve Net Zero goals.

Office Data This Month:
- Energy: {energy} kWh  →  {round(energy*ENERGY_EF,1)} kg CO₂
- Water:  {water} litres →  {round(water*WATER_EF,3)} kg CO₂
- Paper:  {paper} reams  →  {round(paper*PAPER_EF,1)} kg CO₂
- Total Carbon Footprint: {carbon} kg CO₂
- Green Score: {score}/100
- Employees: {employees}

User Question: {question if question else "Analyze my data and give detailed sustainability recommendations"}

Provide:
1. Performance summary (2-3 lines)
2. Top 4 specific, actionable recommendations with ₹ savings (Indian Rupees)
3. Carbon footprint context (what {carbon} kg CO₂ equals in real terms)
4. 3-month quick-win action plan
5. Relevant Indian certifications to aim for (GRIHA, BEE Star, BRSR)

Be specific, practical, and encouraging. Format with clear sections using emojis."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        reply = message.content[0].text
    except Exception as e:
        # Intelligent fallback
        lines = []
        lines.append("🌿 EcoTrack AI Analysis\n")
        lines.append(f"📊 Performance Summary:")
        lines.append(f"Your office generated {carbon} kg CO₂ this month. Green Score: {score}/100.")
        if score >= 70:
            lines.append("✅ Good performance — keep optimising!\n")
        else:
            lines.append("⚠️ Improvement needed — follow the tips below.\n")

        lines.append("💡 Top Recommendations:")
        if energy > 3000:
            lines.append("⚡ Energy: Set AC to 24°C & enable auto-sleep on computers → Save ₹12,000/yr")
        lines.append("💧 Water: Install motion-sensor faucets → Save ₹6,000/yr")
        lines.append("📄 Paper: Go digital-first for internal docs → Save ₹5,000/yr")
        lines.append("🌱 Carbon: Conduct quarterly energy audit → Save ₹25,000+/yr\n")

        lines.append(f"🌫️ Context: {carbon} kg CO₂ = driving ~{round(carbon/0.21)} km by car\n")

        lines.append("🗓️ 3-Month Plan:")
        lines.append("Month 1: LED upgrade + power management policies")
        lines.append("Month 2: Water conservation + paper reduction drive")
        lines.append("Month 3: Apply for BEE Star Rating / GRIHA certification")

        reply = "\n".join(lines)

    return jsonify({"response": reply})

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "app": "EcoTrack AI"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
