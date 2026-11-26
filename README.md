💥 Multi-Asset Margin Call & Liquidation Cascade Engine ⚡📉

An interactive quantitative risk and cascade-simulation engine built in Python to model margin shortfalls, forced liquidation tiers, and liquidity contagion across leveraged multi-asset portfolios during market stress. 🧠🔥

🧠 What This Engine Does 🎯

In leveraged trading books, a price drop rarely stays confined to a single position. When asset values fall and margin deficits expand, forced liquidations can drain market liquidity—triggering a chain reaction (cascade) that places extra stress on remaining positions. 🛡️⚙️

This engine computes margin shortfalls, classifies liquidation severity using clear decision thresholds, and runs a multi-step cascade loop so you can see how contagion spreads across a portfolio. 📊🚀

🚀 Key Capabilities ✨

1. Margin Shortfall Engine: Evaluates available margin buffer against price shocks and volatility jumps to detect margin deficits early. 🧮💰
2. Liquidation Tier Classifier: Categorizes positions into SAFE, MARGIN_WARNING, FORCED_TRIM, or FULL_LIQUIDATION using structured if / elif / else logic. 🚨⚖️
3. Cascade Spillover Simulation: Models how forced liquidations tighten liquidity and transmit secondary pressure across remaining assets in the book. 🌊📉
4. Modular Function Design: Organizes calculation, tier classification, and cascade simulation into clean, reusable Python functions that return clear results. 🧩🔧

⚙️ How It Works 🔄

1. Compute Margin Shortfall (compute_margin_shortfall): Calculates stressed position value, required maintenance margin, and any margin shortfall or buffer. 📉🧮
2. Classify Liquidation Tier (classify_liquidation_tier): Checks shortfall and margin health to assign the exact risk tier for each asset. 🎯🚨
3. Simulate Cascade Loop (run_cascade_simulation): Tracks forced liquidations, increases liquidity pressure step by step, and returns the full simulated portfolio report. 🔄⚡

📁 Project Structure 📂

1. multi-asset-margin-cascade-engine/ 📦
2. engine/margin_cascade_engine.py — Complete Python implementation containing margin shortfall, liquidation tier classification, and cascade simulation functions. 💻⚙️
3. README.md — Project overview, architecture, local setup guide, links, and creator profile. 📖✨

🛠️ How to Run Locally 💻🚀

1. Clone the repository and open the project folder in your terminal
   (git clone https://github.com/techrabiya/multi-asset-margin-liquidation-simulator)

2. Run the Python engine script directly (python engine/margin_cascade_engine.py). ▶️🚀

🔗 Live Demo & Source Code 🌐💻
Live Application:https://multi-asset-margin-liquidation-simulator-8zish7rurtpyvpbtucder.streamlit.app/

👩‍💻 Created By 🌟🎓
  Rabia Razzaq Khan ✨7th-Grade Student | Aspiring Data Scientist & Quantitative Risk Modeling Enthusiast 🧠📊🚀

Focused on building real-world Python, SQL, and risk-engineering systems step by step. 💡🔥
