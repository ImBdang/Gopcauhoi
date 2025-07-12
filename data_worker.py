import os
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

    for item in data_root:
        if item['group_id'] != 0:
            if item['group_id'] in danhsach:
                for i in range(len(data_root)):
                    if data_root[i]['id'] == item['group_id']:
                        s =f"<p>{item['question_direction']}</p>\n\n"
                        data_root[i]['question_direction'] += s
                        data_root.remove(item)
                        break
                for i in danhsach:
                    if item['group_id'] == i:
                        danhsach.remove(i)
                        break


    return data_root, danhsach


def gen_string(data):
    s = '<link rel="stylesheet" href="style.css">\n'
    for item in data:
        if item['question_type'] == "checkbox":
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
        
        elif item['question_type'] == "drag_drop":
            s += "<div class='cauhoi'>\n"

            cauhoi = item['question_direction']
            s += f"{cauhoi}\n"

            for ans in item["answer_option"]:

                dapan =f"<p>{ans['value']}</p>"
                s += f"\t{dapan}\n\n"

            s += "</div>\n\n"

        else:
            s += "<div class='cauhoi'>\n"
            cauhoi = item['question_direction']
            s += f"{cauhoi}\n"

            for ans in item["answer_option"]:
                dapan = ans['value']
                s += f"\t{dapan}\n\n"

            s += "</div>\n\n"
    return s


def tao_cauhoi(path, name, data):
    
    s = gen_string(data)

    try:
        with open(os.path.join(path, "Cauhoi", f"{name}.html"), "w", encoding="utf-8") as f:
            f.write(s)
    except Exception as e:
        print(f"Loi khi tao file cau hoi: {e}")
        return False
    return True
