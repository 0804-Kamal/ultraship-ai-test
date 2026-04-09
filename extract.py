import os
import json
from openai import OpenAI

os.environ["OPENAI_API_KEY"] = "your-openai-key-here"

def extract_data(text):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": """You are a logistics data extraction expert. 
Extract ALL fields from the document very carefully.
Look for carrier name in sections like 'Carrier Details', 'Driver Details', or anywhere a company name appears.
Look for pickup datetime in 'Shipping Date', 'Shipping Time', 'Pickup' sections.
Return ONLY valid JSON, no extra text."""
            },
            {
                "role": "user",
                "content": f"""Extract these exact fields from the logistics document below.
Be very thorough — search the entire document for each field.

Fields to extract:
- shipment_id (look for Reference ID, Load ID, Shipment No)
- shipper (company name at pickup location)
- consignee (company name at delivery/drop location)
- pickup_datetime (look for Shipping Date + Shipping Time or Pickup Date/Time)
- delivery_datetime (look for Delivery Date + Delivery Time)
- equipment_type (Flatbed, Reefer, Van etc)
- mode (FTL, LTL etc)
- rate (dollar amount)
- currency (USD etc)
- weight (with unit)
- carrier_name (look for Carrier column, company name, SWIFT SHIFT etc)

Document:
{text[:4000]}

Return ONLY this JSON format:
{{
  "shipment_id": "...",
  "shipper": "...",
  "consignee": "...",
  "pickup_datetime": "...",
  "delivery_datetime": "...",
  "equipment_type": "...",
  "mode": "...",
  "rate": "...",
  "currency": "...",
  "weight": "...",
  "carrier_name": "..."
}}

Use null only if truly not found anywhere in the document."""
            }
        ],
        temperature=0
    )

    try:
        raw = response.choices[0].message.content
        clean = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception as e:
        return {"error": f"Extraction failed: {str(e)}"}
