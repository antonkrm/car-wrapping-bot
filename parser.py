import re
import json
from datetime import datetime

PLATE_REGEX = r"\b[А-ЯA-ZЁё]{1}[А-ЯA-ZЁё0-9]{2,9}\b"

FIXED_COSTS = {
    # Пример: "полировка": 1000
}

def normalize(s):
    return " ".join(s.strip().lower().split())

def load_materials():
    with open("materials.json", encoding="utf-8") as f:
        materials_json = json.load(f)
    elements = {normalize(k): v for k, v in materials_json.get("elements", {}).items()}
    labor = {normalize(k): v for k, v in materials_json.get("labor", {}).items()}
    price_per_m2 = materials_json.get("pricing", {}).get("area_cost_per_m2", 360)
    return elements, labor, price_per_m2

def parse_report_text(text: str):
    elements, labor, price_per_m2 = load_materials()
    lines = text.strip().splitlines()

    result = []
    current_date = None
    current_plate = None
    current_description = ""

    DATE_REGEX = r"^\s*(\d{1,2})\.(\d{1,2})(?:\.(\d{4}))?\s*$"

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Проверка на дату
        date_match = re.match(DATE_REGEX, line)
        if date_match:
            day, month, year = date_match.groups()
            if not year:
                year = str(datetime.now().year)
            current_date = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
            continue

        # Проверка на номер машины
        plate_match = re.search(PLATE_REGEX, line, re.IGNORECASE)
        if plate_match:
            # Сохраняем предыдущую запись
            if current_plate and current_description.strip():
                result.append(
                    process_entry(current_plate, current_description, elements, labor, price_per_m2, current_date)
                )
            # Обновляем текущую машину
            current_plate = plate_match.group(0).upper()
            current_description = re.sub(PLATE_REGEX, "", line, count=1, flags=re.IGNORECASE).strip()
        else:
            # Продолжаем описание
            current_description += " " + line.strip()

    # Последняя запись
    if current_plate and current_description.strip():
        result.append(
            process_entry(current_plate, current_description, elements, labor, price_per_m2, current_date)
        )

    # Если дата не была найдена, подставим сегодняшнюю
    if not current_date:
        current_date = datetime.now().strftime("%Y-%m-%d")

    return result, current_date

def process_entry(plate, description, elements, labor, price_per_m2, date):
    parts = [normalize(p) for p in re.split(r'[,.;\n]|(?:\s+и\s+)|(?:\s+and\s+)|(?:\s*&\s*)', description) if p.strip()]
    print("DEBUG parts:", parts)

    total_area = 0.0
    total_labor = 0
    unknown_parts = []

    for part_norm in parts:
        labor_cost = labor.get(part_norm)
        area_val = elements.get(part_norm)
        print(f"DEBUG '{part_norm}': labor={labor_cost}, area={area_val}")
        if labor_cost is None and area_val is None:
            unknown_parts.append(part_norm)
        total_labor += labor_cost or 0
        total_area += area_val or 0

    # Логирование нераспознанных услуг
    if unknown_parts:
        with open("unrecognized_services.txt", "a", encoding="utf-8") as f:
            for unk in unknown_parts:
                f.write(f"{date}, {plate}, {unk}\n")

    # Фиксированные услуги
    fixed_cost = 0
    desc_lower = description.lower()
    for key, value in FIXED_COSTS.items():
        if key in desc_lower:
            fixed_cost += value

    material_cost = round(total_area * price_per_m2)
    total_cost = material_cost + fixed_cost

    return {
        "plate": plate,
        "description": description.strip(),
        "area": round(total_area, 2),
        "cost": total_cost,
        "labor_cost": total_labor,
        "date": date
    }

if __name__ == "__main__":
    sample_text = '''
    2.07
    О930ТР переднее крыло , половина бампера, латки
    ВН437 переднее крыло , половина бампера , латки
    3.07
    Е818ТР 8 элементов , переклейка бренда
    '''
    results, report_date = parse_report_text(sample_text)
    print('DEBUG:', results)
    print('Report date:', report_date)
