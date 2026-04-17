import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from report_generator import generate_report

st.set_page_config(page_title="Installed Base Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://api.fontshare.com/v2/css?f[]=general-sans@400,300,500,600&display=swap');

html, body, [class*="css"] {
    font-family: 'General Sans', sans-serif;
}

/* Verwijder standaard Streamlit padding */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 32px !important;
    padding-right: 32px !important;
    max-width: 100% !important;
}

/* Verberg Streamlit header/toolbar */
header[data-testid="stHeader"] { display: none; }
#MainMenu { display: none; }
footer { display: none; }

/* Topbalk */
.topbar {
    background-color: #00244d;
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0;
    margin-left: -32px;
    margin-right: -32px;
}
.topbar-title {
    color: white;
    font-size: 1.3rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.topbar-sub {
    color: #80b3e0;
    font-size: 0.85rem;
    margin-top: 2px;
}

/* KPI card */
.kpi-card {
    background: white;
    border-left: 4px solid #15a35f;
    border-radius: 8px;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(0,36,77,0.08);
}
.kpi-label {
    color: #6b7280;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 4px;
}
.kpi-value {
    color: #00244d;
    font-size: 2rem;
    font-weight: 600;
    line-height: 1;
}

/* Content padding */
.main-content {
    padding: 12px 20px 0 20px;
    background: #F6F6EC;
    min-height: calc(100vh - 60px);
}

/* Chart cards */
.chart-card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,36,77,0.08);
    padding: 8px;
    height: 100%;
}

[data-testid="stMetricValue"] { display: none; }

/* Textarea */
textarea {
    border-radius: 6px !important;
    border-color: #d1d5db !important;
    font-family: 'General Sans', sans-serif !important;
    font-size: 0.9rem !important;
}

/* Klantselectie scherm */
.select-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
}
</style>
""", unsafe_allow_html=True)

BRAND_COLORS = ["#00244d", "#15a35f", "#FF863F", "#4d8fcc", "#110E17"]

KLANTEN = [
    "— Selecteer een klant —",
    "Provincie Zeeland",
    "Provincie Groningen",
    "Provincie Drenthe",
    "Gemeente Rotterdam",
    "Gemeente Den Haag",
    "Gemeente Utrecht",
    "Gemeente Eindhoven",
    "Gemeente Groningen",
    "Waterschap Scheldestromen",
    "Waterschap Brabantse Delta",
    "Waterschap Rivierenland",
    "Rijkswaterstaat",
    "UWV",
    "Belastingdienst",
    "Dienst Justitiële Inrichtingen",
    "Erasmus MC",
    "Amsterdam UMC",
    "Universiteit Utrecht",
    "Technische Universiteit Delft",
    "Hogeschool Rotterdam",
]

CAT_COLORS = [
    "#001829", "#00244d", "#003570", "#004796", "#1a6ab5",
    "#4d8fcc", "#80b3e0", "#b3d1f0", "#cce0f7", "#e6f0fb",
]

CHART_LAYOUT = dict(
    font_family="General Sans",
    paper_bgcolor="white",
    plot_bgcolor="white",
    margin=dict(t=36, b=8, l=8, r=8),
    legend=dict(font=dict(size=11)),
    title_font=dict(size=13, color="#00244d"),
)


@st.cache_data
def load_data():
    df = pd.read_csv("Installed Base - Fake Data CORRECT.csv", encoding="latin-1")
    df.columns = df.columns.str.strip()
    df = df[df["Beschrijving"].notna() & (df["Beschrijving"].str.strip() != "")]
    return df


# --- Topbalk ---
st.markdown('<div class="topbar"><div><div class="topbar-title">Installed Base Dashboard</div><div class="topbar-sub">Protinus IT</div></div></div>', unsafe_allow_html=True)

# --- Klantselectie ---
if "klantnaam" not in st.session_state:
    st.session_state["klantnaam"] = KLANTEN[0]

with st.container():
    st.markdown('<div style="padding: 12px 20px;">', unsafe_allow_html=True)
    klantnaam = st.selectbox("Klant", KLANTEN, key="klantnaam")
    st.markdown('</div>', unsafe_allow_html=True)

if klantnaam == KLANTEN[0]:
    st.markdown("""
    <div style="text-align:center; padding: 80px 0; color: #6b7280; font-size: 1.1rem;">
        Selecteer een klant om het dashboard te laden.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# --- Data & berekeningen ---
df = load_data()
total = len(df)
open_source_count = (df["Type product"] == "Open source").sum()
eu_count = (df["Beursregio"] == "EU").sum()

# --- Charts aanmaken ---
fig_type = px.pie(df, names="Type product", title="Type product",
                  color_discrete_sequence=BRAND_COLORS)
fig_type.update_layout(**CHART_LAYOUT)
fig_type.update_traces(textfont_size=11)

fig_regio = px.pie(df, names="Beursregio", title="Beursregio",
                   color_discrete_sequence=BRAND_COLORS)
fig_regio.update_layout(**CHART_LAYOUT)
fig_regio.update_traces(textfont_size=11)

cat_counts = df["Productcategorie"].value_counts().reset_index()
cat_counts.columns = ["Productcategorie", "Aantal"]
fig_cat = px.bar(cat_counts, x="Productcategorie", y="Aantal",
                 title="Productcategorie",
                 color="Productcategorie",
                 color_discrete_sequence=CAT_COLORS)
fig_cat.update_layout(**CHART_LAYOUT, showlegend=False,
                      xaxis=dict(tickfont=dict(size=10), title=None),
                      yaxis=dict(title=None, gridcolor="#f0f0f0"))

# --- Dashboard layout ---

# Rij 1: Grafieken
c1, c2, c3 = st.columns(3)
with c1:
    st.plotly_chart(fig_type, use_container_width=True, config={"displayModeBar": False})
with c2:
    st.plotly_chart(fig_regio, use_container_width=True, config={"displayModeBar": False})
with c3:
    st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})

# Rij 2: KPI links, klantdoelen rechtsonder
kpi_col, spacer, input_col = st.columns([1, 0.1, 2.5])

with kpi_col:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Klant</div>
        <div style="color:#00244d; font-size:1.1rem; font-weight:600; margin-bottom:12px;">{klantnaam}</div>
        <div class="kpi-label">Totaal producten</div>
        <div class="kpi-value">{total}</div>
    </div>
    """, unsafe_allow_html=True)

with input_col:
    doelen = st.text_area(
        "Klantdoelen",
        placeholder="Beschrijf de doelen van de klant, bijv. 60% open source en 70% EU-leveranciers.",
        height=100,
        label_visibility="visible",
    )
    btn_col, dl_col = st.columns([1, 2])
    with btn_col:
        generate = st.button("Genereer rapport", type="primary", disabled=not doelen, use_container_width=True)
    with dl_col:
        if st.session_state.get("rapport_bytes"):
            st.download_button(
                label="Download rapport (.docx)",
                data=st.session_state["rapport_bytes"],
                file_name=f"installed_base_rapport_{klantnaam.strip().replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )

if generate:
    with st.spinner("AI genereert analyse en rapport..."):
        chart_data = {
            "type_product": df["Type product"].value_counts().to_dict(),
            "beursregio": df["Beursregio"].value_counts().to_dict(),
            "productcategorie": df["Productcategorie"].value_counts().to_dict(),
            "metrics": {
                "totaal_producten": int(total),
                "open_source_percentage": round(open_source_count / total * 100, 1),
                "eu_percentage": round(eu_count / total * 100, 1),
            },
        }
        charts = {
            "type_product": pio.to_image(fig_type, format="png", scale=2),
            "beursregio": pio.to_image(fig_regio, format="png", scale=2),
            "productcategorie": pio.to_image(fig_cat, format="png", scale=2),
        }
        st.session_state["rapport_bytes"] = generate_report(doelen, chart_data, charts)
        st.success("Rapport gegenereerd!")
        st.rerun()