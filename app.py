import streamlit as st
import math

# Configure page metadata and styling
st.set_page_config(
    page_title="Pneumatic & Gas Expansion Geometric Calculator",
    page_icon="🥔",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom injection for sleek styling
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stNumberInput div div input { font-weight: bold; }
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Geometric Volume & Ratio Calculator")
st.write("Optimise pressure vessel and expansion tube layouts using internal engineering standards.")

# --- SIDEBAR: THEORY & INPUT CONFIGURATION ---
st.sidebar.header("⚙️ Configuration & Reference")

# Unit Selection Toggle
unit_system = st.sidebar.radio(
    "Preferred Measurement Units",
    ["Metric (Millimetres)", "Imperial (Inches)"]
)
is_metric = (unit_system == "Metric (Millimetres)")

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 📘 Gas Expansion Principles
Internal volume ratios determine how efficiently energy is transferred from a pressure chamber to an expansion barrel.

* **High-Efficiency Sweep (0.6:1 – 0.8:1):** 
  Based on gas-dynamic simulation modeling (like *EVBEC* frameworks), this window ensures the expanding medium matches the velocity profile of the moving projectile. It prevents excessive muzzle blast and fuel waste.
* **Classic Legacy Baseline (1.5:1 – 2.0:1):** 
  The traditional rule-of-thumb baseline designed to ensure maximum chemical residency time at lower operating pressures.
""")

# --- MAIN UI LAYOUT: COMPONENT DIMENSIONS ---
st.header("📐 Component Dimensions")
col1, col2 = st.columns(2)

# Set input parameters dynamically based on chosen unit system
if is_metric:
    unit_label = "mm"
    step_val = 1.0
    c_dia_default = 90.0
    c_len_default = 500.0
    b_dia_default = 50.0
    b_len_default = 1500.0
else:
    unit_label = "inches"
    step_val = 0.125
    c_dia_default = 3.5
    c_len_default = 20.0
    b_dia_default = 2.0
    b_len_default = 60.0

with col1:
    st.subheader("Chamber Cylinder")
    raw_c_dia = st.number_input(f"Chamber Inner Diameter ({unit_label})", min_value=0.1, value=c_dia_default, step=step_val)
    raw_c_len = st.number_input(f"Chamber Internal Length ({unit_label})", min_value=0.1, value=c_len_default, step=step_val)

with col2:
    st.subheader("Barrel Cylinder")
    raw_b_dia = st.number_input(f"Barrel Inner Diameter ({unit_label})", min_value=0.1, value=b_dia_default, step=step_val)
    
    calc_mode = st.checkbox("Toggle Dynamic Target Ratio Finder", value=False)
    
    if not calc_mode:
        raw_b_len = st.number_input(f"Barrel Internal Length ({unit_label})", min_value=0.1, value=b_len_default, step=step_val)

# Convert all raw inputs to millimetres internally for standardized processing
if is_metric:
    c_dia, c_length = raw_c_dia, raw_c_len
    b_dia = raw_b_dia
    if not calc_mode:
        b_length = raw_b_len
else:
    # 1 inch = 25.4 mm
    c_dia = raw_c_dia * 25.4
    c_length = raw_c_len * 25.4
    b_dia = raw_b_dia * 25.4
    if not calc_mode:
        b_length = raw_b_len * 25.4

# --- DYNAMIC TARGET RATIO FINDER ---
if calc_mode:
    st.markdown("### 🎯 Target Ratio Optimization")
    st.write("Lock in a specific performance ratio to dynamically compute your necessary barrel length.")
    
    target_ratio = st.slider("Select Target Chamber-to-Barrel Ratio", min_value=0.4, max_value=2.5, value=0.75, step=0.05)
    
    # Formula derived from: Ratio = Vol_Chamber / Vol_Barrel
    # Barrel Length = Chamber Length / Target Ratio * (Chamber Diameter / Barrel Diameter)^2
    b_length = (c_length / target_ratio) * ((c_dia / b_dia) ** 2)
    
    # Format recommendation string back into user units
    recommended_len = b_length if is_metric else (b_length / 25.4)
    st.info(f"💡 Target Match: To achieve an exact **{target_ratio:.2f} : 1** ratio, your **Barrel Length must be: {recommended_len:.2f} {unit_label}**.")

# --- ANALYTICAL CALCULATIONS ---
# Calculate volumes in cubic millimetres (mm³) and convert to standard Cubic Centimetres / Millilitres (cm³ or mL)
c_volume_ml = (math.pi * ((c_dia / 2) ** 2) * c_length) / 1000.0
b_volume_ml = (math.pi * ((b_dia / 2) ** 2) * b_length) / 1000.0
resulting_ratio = c_volume_ml / b_volume_ml

st.markdown("---")

# --- RESULTS DASHBOARD ---
st.header("📊 Volumetric Analysis")
m_col1, m_col2, m_col3 = st.columns(3)

# Display fluid volumes in metric mL alongside imperial fluid ounces for complete clarity
c_vol_display = f"{c_volume_ml:.1f} mL / {(c_volume_ml * 0.033814):.1f} fl oz"
b_vol_display = f"{b_volume_ml:.1f} mL / {(b_volume_ml * 0.033814):.1f} fl oz"

m_col1.metric("Chamber Volume", c_vol_display)
m_col2.metric("Barrel Volume", b_vol_display)
m_col3.metric("Evaluated Ratio", f"{resulting_ratio:.2f} : 1")

# --- CUSTOM PROGRESS BAR ACCORDING TO INDUSTRY THEORIES ---
st.write("**Ratio Performance Spectrum:**")
progress_normalized = min(max((resulting_ratio - 0.4) / (2.0 - 0.4), 0.0), 1.0)
st.progress(progress_normalized)

# --- VERDICT CONTEXT ---
st.subheader("📋 Performance Evaluation")

if 0.6 <= resulting_ratio <= 0.8:
    st.success(f"**Highly Optimized ({resulting_ratio:.2f}:1):** This configuration falls precisely within the modern SpudFiles velocity threshold. Internal gas flow kinetics are optimized for rapid energy transfer without pressure waste.")
elif 0.8 < resulting_ratio <= 1.2:
    st.info(f"**Balanced Performance ({resulting_ratio:.2f}:1):** A highly functional transitional configuration. It provides excellent pressure retention characteristics while scaling safely with larger volume components.")
elif 1.2 < resulting_ratio <= 2.0:
    st.warning(f"**Legacy Combustion Baseline ({resulting_ratio:.2f}:1):** Matches historical combustion designs. While fully functional, the physical footprint of the chamber is larger than modern gas expansion dynamics require.")
elif resulting_ratio < 0.6:
    st.warning(f"**Volumetrically Restricted ({resulting_ratio:.2f}:1):** The storage chamber volume is insufficient relative to the displacement area of the expansion barrel. Internal pressure drop will happen rapidly, limiting velocity limits.")
else:
    st.error(f"**Diminishing Returns Zone ({resulting_ratio:.2f}:1):** The chamber volume heavily overpowers the displacement capacity of the barrel. Excess pressure medium will blow out at the muzzle, creating substantial noise signatures without mechanical velocity gains.")

st.markdown("---")

# --- PIPING PRESSURE & STRUCTURAL INTEGRITY REFERENCE ---
st.header("⚠️ Material Pressure Limits (Standard Schedule 40)")
st.caption("Reference guidelines for solid-wall PVC compounds at standard ambient temperatures (23°C / 73°F).")

p_col1, p_col2 = st.columns(2)

with p_col1:
    st.markdown("**Chamber Diameter Reference:**")
    if c_dia <= 60.5: # 2 inch standard nominal
        st.success("🔒 50mm (2\") Schedule 40: Rated for ~280 PSI / 1.93 MPa.")
    elif c_dia <= 90.0: # 3 inch standard nominal
        st.info("⚡ 80mm (3\") Schedule 40: Rated for ~260 PSI / 1.79 MPa.")
    else:
        st.warning("⚠️ 100mm+ (4\"+) Schedule 40: Rated limit drops down to ~220 PSI / 1.52 MPa.")

with p_col2:
    st.markdown("**Core Structural Reminders:**")
    st.markdown("""
    * **Pressure vs. Diameter:** Large pipes have significantly thinner effective wall containment properties relative to internal surface area. Never assume a 4\" pipe holds the same threshold as a 2\" pipe.
    * **Material Type:** Only utilize solid-wall, pressure-rated PVC compounds manufactured to clear geometric specifications (e.g., Schedule 40/80). Never use cellular core or structural DWV (Drain, Waste, Vent) variations for containing compressed mediums.
    """)

