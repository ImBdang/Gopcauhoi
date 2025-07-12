import json

def read_data(cauhoi):
    try:
        data = json.loads(cauhoi)
    except json.JSONDecodeError:
        return False
    return data

def add_question(data_root, data, danhsach):
    for item in data:
        if item['id'] not in danhsach:
            danhsach.append(item['id'])
            data_root.append(item)

    return data_root, danhsach

def tao_cauhoi(path, name, data):
    s = '<link rel="stylesheet" href="style.css">\n'

    for item in data:
        s += "<div class='cauhoi'>\n"
        cauhoi = item['question_direction']

        hint = ""
        if item["question_type"] == "checkbox":
            hint = f"(Chon {item['number_answer_correct']} dap an)"
        s += f"{cauhoi} {hint}\n"

        for ans in item["answer_option"]:
            dapan = ans['value']
            s += f"\t{dapan}\n\n"

        s += "</div>\n\n"

    with open(f"{path}/Cauhoi/{name}.html", "w", encoding="utf-8") as f:
        f.write(s)
    return True
