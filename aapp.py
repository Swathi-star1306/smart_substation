import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
from fpdf import FPDF

# --- Simulated Data ---
def generate_data():
    return {
        "Grid Voltage (kV)": random.randint(220, 240),
        "Load Current (A)": random.randint(50, 200),
        "Power Factor": round(random.uniform(0.8, 1.0), 2),
        "Transformer Temp (°C)": random.randint(50, 80),
        "Frequency (Hz)": round(random.uniform(49.5, 50.5), 2),
        "Line Loss (%)": round(random.uniform(2.0, 5.0), 2),
        "Battery Status (%)": random.randint(50, 100),
    }

# --- PDF Report Generation ---
def generate_pdf(report_date):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt=f"Smart Substation Report - {report_date}", ln=True, align="C")
    pdf.ln(10)

    # Content
    pdf.set_font("Arial", size=12)
    for key, value in generate_data().items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    # Save PDF
    file_name = f"Substation_Report_{report_date}.pdf"
    pdf.output(file_name)
    return file_name

# --- Streamlit Dashboard ---
st.set_page_config(page_title="Smart Substation Dashboard", layout="wide")

# Header Section
st.markdown("<div style='font-size:40px; text-align:center; color:#FFD700;'>🌟 Smart Substation Dashboard 🌟</div>", unsafe_allow_html=True)
st.markdown("<div style='font-size:20px; text-align:center; color:#FFFFFF;'>Ensuring Efficiency, Safety, and Reliability in Power Management</div>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "", ["Live Data", "Trend Analysis", "Manual Control", "Reports"]
)

# --- Live Data Section ---
if menu == "Live Data":
    st.title("🔍 Live Data Monitoring")
    st.write("### Real-Time Metrics (Auto-Refreshing)")

    placeholder = st.empty()  # Placeholder for live data

    # Continuous Loop for Updating Data
    while True:
        data = generate_data()

        with placeholder.container():
            # Metrics Display
            col1, col2, col3 = st.columns(3)
            col1.metric("⚡ Grid Voltage (kV)", f"{data['Grid Voltage (kV)']} kV", delta=f"{random.randint(-3, 3)} kV")
            col2.metric("🔋 Load Current (A)", f"{data['Load Current (A)']} A", delta=f"{random.randint(-5, 5)} A")
            col3.metric("📈 Power Factor", data["Power Factor"])

            col4, col5, col6 = st.columns(3)
            col4.metric("🌡 Transformer Temp (°C)", f"{data['Transformer Temp (°C)']} °C", delta=f"{random.randint(-2, 2)} °C")
            col5.metric("⏳ Frequency (Hz)", f"{data['Frequency (Hz)']} Hz")
            col6.metric("📉 Line Loss (%)", f"{data['Line Loss (%)']} %")

            col7, col8 = st.columns(2)
            col7.metric("🔋 Battery Status (%)", f"{data['Battery Status (%)']} %", delta=f"{random.randint(-5, 5)} %")
            col8.metric("⚠️ Generator Status", "ON" if data['Load Current (A)'] > 150 else "OFF")

            # Alert
            if data["Transformer Temp (°C)"] > 75:
                st.error("⚠️ Transformer Temperature Critical!")
            if data["Line Loss (%)"] > 4.0:
                st.warning("⚠️ Line Loss Exceeding Safe Limits!")

        # Refresh every 2 seconds
        time.sleep(2)

# --- Trend Analysis Section ---
elif menu == "Trend Analysis":
    st.title("📊 Trend Analysis")
    st.write("### Monitor Historical Data Trends")

    # Placeholder data
    time_series = pd.date_range(start="2025-02-11 00:00", periods=10, freq="H")
    trend_data = {
        "Time": time_series,
        "Grid Voltage (kV)": [random.randint(220, 240) for _ in range(10)],
        "Load Current (A)": [random.randint(50, 200) for _ in range(10)],
        "Transformer Temp (°C)": [random.randint(50, 80) for _ in range(10)],
    }
    df = pd.DataFrame(trend_data).set_index("Time")

    st.line_chart(df)

# --- Manual Control Section ---
elif menu == "Manual Control":
    st.title("🔧 Manual Control")
    st.write("### Override Settings")

    grid_status = st.radio("Grid Power", ["ON", "OFF"])
    generator_status = "ON" if grid_status == "OFF" else st.radio("Diesel Generator", ["ON", "OFF"])
    transformer_status = st.radio("Transformer", ["ON", "OFF"])

    st.write("### Current Settings:")
    st.write(f"Grid Power: {grid_status}")
    st.write(f"Diesel Generator: {generator_status}")
    st.write(f"Transformer: {transformer_status}")

    if st.button("Apply Changes"):
        st.success("Manual Control Settings Applied Successfully!")

# --- Reports Section ---
elif menu == "Reports":
    st.title("📑 Reports")
    st.write("### Generate and Email Daily Reports")

    # Date picker for reports
    report_date = st.date_input("Select Report Date", value=datetime.today())

    if st.button("Generate Report"):
        pdf_path = generate_pdf(report_date)
        with open(pdf_path, "rb") as file:
            st.download_button("Download Report", file, file_name=pdf_path)
        st.success("Report Generated Successfully!")


