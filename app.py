
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# إعدادات الصفحة
st.set_page_config(page_title="Solar Panel Power Predictor", layout="wide")
st.title("🔆 AI-Based Prediction of Solar Panel Power Output")
st.markdown("Adjust the inputs below to see how **solar irradiance** and **module temperature** affect the maximum DC power.")

# الشريط الجانبي - المدخلات
st.sidebar.header("Input Parameters")

G = st.sidebar.slider(
    "Solar Irradiance G (W/m²)",
    min_value=0, max_value=1200, value=1000, step=10,
    help="Plane-of-array irradiance received by the panel surface"
)

T = st.sidebar.slider(
    "Module Temperature T (°C)",
    min_value=0, max_value=70, value=25, step=1,
    help="Operating temperature of the panel"
)

# ثوابت اللوح
P_stc = 400.0      # W (rated power at STC)
gamma = -0.004     # /°C (temperature coefficient of Pmax)
T_ref = 25.0       # °C

# حساب القدرة
P_pred = P_stc * (G / 1000.0) * (1 + gamma * (T - T_ref))
P_pred = max(P_pred, 0)  # لا قدرة سالبة

# عرض النتيجة
col1, col2, col3 = st.columns(3)
col1.metric("Irradiance G", f"{G} W/m²")
col2.metric("Module Temp T", f"{T} °C")
col3.metric("Predicted Pmax", f"{P_pred:.1f} W")

# الرسم البياني: Pmax كدالة لـ G عند T الحالية
G_range = np.linspace(0, 1200, 200)
P_curve = P_stc * (G_range / 1000.0) * (1 + gamma * (T - T_ref))
P_curve = np.maximum(P_curve, 0)

fig = go.Figure()
fig.add_trace(go.Scatter(x=G_range, y=P_curve, mode='lines',
                         name=f'Pmax vs G (at T={T}°C)',
                         line=dict(color='orange', width=3)))
fig.add_trace(go.Scatter(x=[G], y=[P_pred], mode='markers',
                         marker=dict(size=15, color='red'),
                         name='Current Operating Point'))
fig.update_layout(
    xaxis_title="Solar Irradiance G (W/m²)",
    yaxis_title="Maximum Power Pmax (W)",
    title="Power–Irradiance Characteristic",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

# التفسير الفيزيائي
st.subheader("📘 Physical Interpretation")
st.markdown(f"""
- **Increasing irradiance** raises the photocurrent, which lifts the whole I–V curve and increases power.
- **Increasing module temperature** reduces the open-circuit voltage more than it raises the current, so Pmax drops (γ = {gamma} /°C for crystalline silicon).
- At **G = {G} W/m²** and **T = {T} °C**, the predicted maximum DC power is **{P_pred:.1f} W**.
- The linear trend in G is an approximation; the true response is slightly sub-linear at low irradiance, which is one reason an **AI model (ANN)** is proposed for higher accuracy.
""")
