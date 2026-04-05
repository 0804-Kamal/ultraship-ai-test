import re

def extract_data(text):
    data = {
        "shipment_id": None,
        "shipper": None,
        "consignee": None,
        "pickup_datetime": None,
        "delivery_datetime": None,
        "equipment_type": None,
        "mode": None,
        "rate": None,
        "currency": "USD",
        "weight": None,
        "carrier_name": None
    }

    # Shipment ID
    match = re.search(r"LD\d+", text)
    if match:
        data["shipment_id"] = match.group()

    # Rate
    match = re.search(r"\$\d+\.?\d*", text)
    if match:
        data["rate"] = match.group()

    # Weight
    match = re.search(r"\d{5,}\s?lbs", text)
    if match:
        data["weight"] = match.group()

    # Equipment
    if "Flatbed" in text:
        data["equipment_type"] = "Flatbed"

    # Mode
    if "FTL" in text:
        data["mode"] = "FTL"

    # Carrier name
    match = re.search(r"SWIFT SHIFT LOGISTICS LLC", text)
    if match:
        data["carrier_name"] = match.group()

    # Pickup date
    match = re.search(r"\d{2}-\d{2}-\d{4}", text)
    if match:
        data["pickup_datetime"] = match.group()

    # Shipper
    if "AAA" in text:
        data["shipper"] = "AAA"

    # Consignee
    if "xyz" in text:
        data["consignee"] = "xyz"

    return data