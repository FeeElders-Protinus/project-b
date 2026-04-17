import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from report_generator import generate_report

st.set_page_config(page_title="Installed Base Dashboard", layout="wide")


@st.cache_data
def load_data():
    df = pd.read_csv("Installed Base - Fake Data.csv", encoding="latin-1")
    df.columns = df.columns.str.strip()
    df = df[df["Beschrijving"].notna() & (df["Beschrijving"].str.strip() != "")]
    return df


df = load_data()

st.title("Installed Base Dashboard")

# KPI metrics
total = len(df)
open_source_count = (df["Type product"] == "Open source").sum()
eu_count = (df["Beursregio"] == "EU").sum()

col1, col2, col3 = st.columns(3)
col1.metric("Totaal producten", total)
col2.metric("Open source", f"{open_source_count / total * 100:.1f}%", f"{open_source_count} producten")
col3.metric("EU-gebaseerd", f"{eu_count / total * 100:.1f}%", f"{eu_count} producten")

st.divider()

# Charts
col_left, col_right = st.columns(2)

with col_left:
    fig_type = px.pie(
        df, names="Type product",
        title="Verdeling Type product",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    st.plotly_chart(fig_type, use_container_width=True)

with col_right:
    fig_regio = px.pie(
        df, names="Beursregio",
        title="Verdeling Beursregio",
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    st.plotly_chart(fig_regio, use_container_width=True)

cat_counts = df["Productcategorie"].value_counts().reset_index()
cat_counts.columns = ["Productcategorie", "Aantal"]
fig_cat = px.bar(
    cat_counts, x="Productcategorie", y="Aantal",
    title="Verdeling Productcategorie",
    color_discrete_sequence=["#636EFA"],
)
st.plotly_chart(fig_cat, use_container_width=True)

st.divider()

# Customer goals input
st.subheader("Klantdoelen")
doelen = st.text_area(
    "Beschrijf de doelen van de klant:",
    placeholder="Bijv. De klant wil 60% open source software gebruiken en minimaal 70% bij EU-gebaseerde leveranciers afnemen.",
    height=150,
)

if st.button("Genereer rapport", type="primary", disabled=not doelen):
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

        rapport_bytes = generate_report(doelen, chart_data, charts)
        st.session_state["rapport_bytes"] = rapport_bytes

if st.session_state.get("rapport_bytes"):
    st.success("Rapport gegenereerd!")
    st.download_button(
        label="Download rapport (.docx)",
        data=st.session_state["rapport_bytes"],
        file_name="installed_base_rapport.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
