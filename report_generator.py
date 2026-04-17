import json
from io import BytesIO

import anthropic
from docx import Document
from docx.shared import Inches

# ============================================================
# SYSTEM PROMPT — vul hier jouw instructies in voor de AI
# Beschrijf hoe de data en klantdoelen verwerkt moeten worden
# tot gegenereerde tekst in het rapport.
# ============================================================
SYSTEM_PROMPT = """Je bent een IT-adviseur die rapportages schrijft over de installed base van klanten.

[VULL HIER JE INSTRUCTIES IN]
"""
# ============================================================


def generate_ai_text(doelen: str, chart_data: dict) -> str:
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2000,
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": (
                    f"Klantdoelen:\n{doelen}\n\n"
                    f"Dashboard data:\n{json.dumps(chart_data, ensure_ascii=False, indent=2)}"
                ),
            }
        ],
    )

    return response.content[0].text


def generate_report(doelen: str, chart_data: dict, charts: dict) -> bytes:
    ai_text = generate_ai_text(doelen, chart_data)

    doc = Document()
    doc.add_heading("Installed Base Rapport", 0)

    doc.add_heading("Klantdoelen", 1)
    doc.add_paragraph(doelen)

    doc.add_heading("Analyse", 1)
    for paragraph in ai_text.split("\n\n"):
        if paragraph.strip():
            doc.add_paragraph(paragraph.strip())

    doc.add_heading("Visualisaties", 1)
    for img_bytes in charts.values():
        doc.add_picture(BytesIO(img_bytes), width=Inches(6))
        doc.add_paragraph()

    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output.getvalue()
