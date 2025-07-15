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
            if item['group_id'] == 0:
                danhsach.append(item['id'])
            data_root.append(item)
    return data_root, danhsach


def gen_string(data):
    s = '<link rel="stylesheet" href="style.css">\n'
    stt = 1
    for item in data:
        if item["group_id"] != 0:
            continue
        s += "<div class='cauhoi'>\n"
        #checkbox template
        if item['question_type'] == "checkbox":
            cauhoi = item['question_direction']
            hint = ""
            if item["question_type"] == "checkbox":
                hint = f"(Chon {item['number_answer_correct']} dap an)"
            s += f"Cau {stt}:{cauhoi} {hint}\n"
            s += "<form>\n"
            for ans in item["answer_option"]:
                dapan = ans['value']
                s += f"\t<input type='checkbox' name='answer' value='{dapan}'>{dapan}<br>\n"
            s += "</form>\n"
            s += "</div>\n\n"
        
        #drag_drop template
        elif item['question_type'] == "drag_drop":
            cauhoi = item['question_direction']
            s += f"Cau {stt}:{cauhoi}\n"

            #cac dap an co the keo
            s += "<p>(Cac dap an)</p>\n"
            s += "<div class='drag_ans_zone'>\n"
            for ans in item["answer_option"]:
                dapan =f"<div class='drag_ans'>{ans['value']}</div>"
                s += f"\t{dapan}\n\n"
            s += "</div>\n"

            #khu vuc keo dap an vao
            s += "<p>(Cac lua chon tuong duong voi dap an)</p>\n\n\n"
            s += "<div class='ans_to_drag'>\n"
            for jtem in data:
                if jtem['group_id'] == item['id']:
                    s += "<div class='drop_zone'>\n"
                    s += f"<p>{jtem['question_direction']}</p>\n"
                    s += "</div>\n"
            s += "</div>\n"

            s += "</div>\n\n"

        #group-input template
        elif item['question_type'] == "group-input":
            cauhoi = item['question_direction']
            s += f"Cau {stt}:{cauhoi}\n"

      
            idx = 1
            for jtem in data:
                if jtem['group_id'] == item['id']:
                    s += "<div class='input_zone'>\n"

                    s += f"<p>{idx}) {jtem['question_direction']}</p>\n"
                    s += "<input type='text' name='answer'>\n"

                    s += "</div>\n"
                    idx += 1

            s += "</div>\n\n"

        #grouping template
        elif item['question_type'] == "grouping":
            cauhoi = item['question_direction']
            s += f"Cau {stt}:{cauhoi}\n"

            s += "<p>(Cac dap an)</p>\n"
            s += "<div class='grouping_ans_zone'>\n"
            for ans in item["answer_option"]:
                dapan =f"<div class='grouping_ans'>{ans['value']}</div>"
                s += f"\t{dapan}\n\n"

            idx = 1
            for jtem in data:
                if jtem['group_id'] == item['id']:
                    s += "<div class='grouping_zone'>\n"

                    s += f"<p>{idx}) {jtem['question_direction']}</p>\n"
                    s += "<input type='text' name='answer'>\n"

                    s += "</div>\n"
                    idx += 1

            s += "</div>\n\n"

        elif item['question_type'] == "group-radio":
            cauhoi = item['question_direction']
            s += f"Cau {stt}:{cauhoi}\n"

      
            idx = 1
            for jtem in data:
                if jtem['group_id'] == item['id']:
                    s += "<div class='radio_zone'>\n"

                    s += f"<p>{idx}) {jtem['question_direction']}</p>\n"
                    s += "<div class='radio_ans'>\n"
                    for ans in jtem["answer_option"]:
                        dapan = ans['value']
                        s += f"<p style='font-weight: normal'>{dapan}</p>\n"
                    s += "</div>\n\n"
                    s += "</div>\n"
                    idx += 1

            s += "</div>\n\n"

        #default template
        else:
  
            cauhoi = item['question_direction']
            s += f"Cau {stt}:{cauhoi}\n"

            for ans in item["answer_option"]:
                dapan = ans['value']
                s += f"\t{dapan}\n\n"

        s += "</div>\n\n"
        stt += 1
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
