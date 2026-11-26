import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Multi-Asset Margin & Liquidation Simulator",
    layout="wide",
)


def compute_margin_shortfall(
    position_value: float,
    margin_posted: float,
    price_shock_pct: float,
    volatility_factor: float,
    maintenance_margin_rate: float = 0.25,
) -> dict:
    shock_multiplier = 1.0 + max(0.0, volatility_factor - 1.0) * 0.25
    effective_shock = price_shock_pct * shock_multiplier
    stressed_value = max(0.0, position_value * (1.0 + effective_shock))
    required_margin = stressed_value * maintenance_margin_rate

    raw_shortfall = required_margin - margin_posted
    margin_shortfall = round(max(0.0, raw_shortfall), 2)
    margin_buffer = round(-raw_shortfall, 2)

    return {
        "stressed_value": round(stressed_value, 2),
        "required_margin": round(required_margin, 2),
        "margin_shortfall": margin_shortfall,
        "margin_buffer": margin_buffer,
    }


def classify_liquidation_tier(
    margin_shortfall: float,
    margin_posted: float,
    required_margin: float,
) -> str:
    if required_margin <= 0:
        return "SAFE"

    shortfall_ratio = margin_shortfall / required_margin
    equity_ratio = margin_posted / required_margin

    if equity_ratio <= 0.50 or shortfall_ratio >= 0.50:
        return "FULL_LIQUIDATION"
    elif shortfall_ratio >= 0.20:
        return "FORCED_TRIM"
    elif margin_shortfall > 0:
        return "MARGIN_WARNING"
    else:
        return "SAFE"


def run_cascade_simulation(
    positions: list[dict],
    base_shock_pct: float = -0.18,
    base_volatility: float = 1.6,
    cascade_spillover_step: float = 0.04,
) -> list[dict]:
    cascade_results = []
    accumulated_contagion = 0.0

    for item in positions:
        asset_name = item["asset"]
        position_value = float(item["position_value"])
        margin_posted = float(item["margin_posted"])
        maintenance_rate = float(item.get("maintenance_margin_rate", 0.25))

        current_shock = base_shock_pct - accumulated_contagion
        current_volatility = base_volatility + (accumulated_contagion * 2.0)

        metrics = compute_margin_shortfall(
            position_value=position_value,
            margin_posted=margin_posted,
            price_shock_pct=current_shock,
            volatility_factor=current_volatility,
            maintenance_margin_rate=maintenance_rate,
        )

        tier = classify_liquidation_tier(
            margin_shortfall=metrics["margin_shortfall"],
            margin_posted=margin_posted,
            required_margin=metrics["required_margin"],
        )

        if tier == "FULL_LIQUIDATION":
            accumulated_contagion += cascade_spillover_step
        elif tier == "FORCED_TRIM":
            accumulated_contagion += cascade_spillover_step * 0.5

        cascade_results.append(
            {
                "asset": asset_name,
                "tier": tier,
                "stressed_value": metrics["stressed_value"],
                "required_margin": metrics["required_margin"],
                "margin_shortfall": metrics["margin_shortfall"],
                "margin_buffer": metrics["margin_buffer"],
                "contagion_applied": round(accumulated_contagion, 4),
            }
        )

    return cascade_results


st.title("Multi-Asset Margin & Liquidation Simulator")
st.write("Simulate margin shortfalls, liquidation tiers, and cascade contagion across assets.")

base_shock_pct = st.sidebar.slider("Base Price Shock", min_value=-0.45, max_value=0.0, value=-0.18, step=0.01)
base_volatility = st.sidebar.slider("Base Volatility Factor", min_value=1.0, max_value=4.0, value=1.6, step=0.1)
cascade_spillover_step = st.sidebar.slider("Cascade Spillover Step", min_value=0.0, max_value=0.15, value=0.04, step=0.01)

sample_positions = [
    {"asset": "NIFTY_FUT", "position_value": 1200000.0, "margin_posted": 240000.0, "maintenance_margin_rate": 0.25},
    {"asset": "BANKNIFTY_FUT", "position_value": 1000000.0, "margin_posted": 230000.0, "maintenance_margin_rate": 0.25},
    {"asset": "USDINR_FUT", "position_value": 800000.0, "margin_posted": 220000.0, "maintenance_margin_rate": 0.20},
    {"asset": "GOLD_FUT", "position_value": 600000.0, "margin_posted": 180000.0, "maintenance_margin_rate": 0.20},
]

output = run_cascade_simulation(
    sample_positions,
    base_shock_pct=base_shock_pct,
    base_volatility=base_volatility,
    cascade_spillover_step=cascade_spillover_step,
)

df_output = pd.DataFrame(output)

col1, col2, col3 = st.columns(3)
col1.metric("Total Margin Shortfall", f"₹{df_output['margin_shortfall'].sum():,.2f}")
col2.metric("Liquidations Triggered", int((df_output["tier"] == "FULL_LIQUIDATION").sum()))
col3.metric("Max Contagion Applied", f"{df_output['contagion_applied'].max():.2%}")

st.dataframe(df_output, use_container_width=True)
