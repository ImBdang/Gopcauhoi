from bs4 import BeautifulSoup as soup
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
    # s = "<link rel='stylesheet' href='style.css'>\n"
    s = get_style()
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
            s += f"Cau {stt}:{cauhoi}\n"
            s += "<form>\n"
            for ans in item["answer_option"]:
                dapan = ans['value']
                dapan = soup(dapan, "html.parser").text.strip()
                s += f"\t<div><input type='checkbox' name='answer' value='{dapan}'>{dapan}<br></div>\n"
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

def get_style():
    return '''
<style>
    :root {
    --primary-color: #4CAF50;
    --secondary-color: #2196F3;
    --accent-color: #FFC107;

    --text-color-dark: #333;
    --text-color-light: #666;
    --background-light: #f8f9fa;
    --background-card: #ffffff;
    --background-hover: #e9ecef;
    --border-color: #e0e0e0;
    --shadow-base: rgba(0, 0, 0, 0.04);
    --shadow-hover: rgba(0, 0, 0, 0.08);
    }

    body {
    font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    color: var(--text-color-dark);
    background-color: var(--background-light);
    line-height: 1.5;
    margin: 0;
    padding: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    }

    .cauhoi {
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background-color: var(--background-card);
    padding: 15px 20px;
    margin-bottom: 15px;
    box-shadow: 0 3px 6px var(--shadow-base);
    transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1);
    width: 100%;
    max-width: 600px; /* Giảm max-width thêm */
    box-sizing: border-box;
    }

    .cauhoi:hover {
    background-color: var(--background-hover);
    box-shadow: 0 5px 10px var(--shadow-hover);
    transform: translateY(-1px);
    }

    .cauhoi p:first-child {
    font-weight: 700;
    font-size: 1.1em;
    margin-bottom: 10px;
    color: var(--primary-color);
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 6px;
    line-height: 1.2;
    }

    .cauhoi p:not(:first-child) {
    margin: 6px 0;
    padding: 6px 10px;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.2s ease-in-out, padding-left 0.2s ease-in-out, color 0.2s ease-in-out;
    }

    .cauhoi p:not(:first-child):hover {
    background-color: var(--background-hover);
    padding-left: 14px;
    color: var(--secondary-color);
    }

    .drag_ans_zone,
    .grouping_ans_zone,
    .radio_zone {
    display: flex;
    flex-wrap: wrap;
    gap: 8px; /* Giảm khoảng cách giữa các mục */
    margin: 10px 0 15px 0;
    padding: 8px 10px;
    border-radius: 6px;
    background-color: var(--background-hover);
    box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.06);
    }

    .drag_ans,
    .grouping_ans,
    .radio_ans {
    border: 1px solid var(--primary-color);
    background-color: var(--background-card);
    color: var(--text-color-dark);
    padding: 6px 12px; /* Giảm padding */
    border-radius: 5px;
    cursor: grab;
    box-shadow: 0 1px 2px var(--shadow-base);
    transition: all 0.15s ease-in-out;
    }

    .drag_ans:hover,
    .grouping_ans:hover,
    .radio_ans:hover {
    background-color: #E8F5E9;
    border-color: #388E3C;
    box-shadow: 0 2px 4px var(--shadow-hover);
    transform: translateY(-0.5px);
    }

    .input_zone input,
    .grouping_zone input {
    width: calc(100% - 16px);
    padding: 8px; /* Giảm padding */
    margin: 6px 0;
    border: 1px solid var(--border-color);
    border-radius: 5px;
    font-size: 0.95em;
    color: var(--text-color-dark);
    transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    }

    .input_zone input:focus,
    .grouping_zone input:focus {
    border-color: var(--secondary-color);
    box-shadow: 0 0 0 2px rgba(33, 150, 243, 0.15);
    outline: none;
    }

    .drop_zone {
    border: 1.5px dashed var(--secondary-color); 
    border-radius: 5px;
    padding: 10px;
    margin: 6px 0;
    background-color: #e3f2fd;
    min-height: 40px; 
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.95em;
    color: var(--text-color-dark);
    text-align: center;
    }

    .drop_zone p {
    margin: 0;
    font-weight: 500;
    }

    .radio_zone {
        flex-direction: column;
        align-items: flex-start;
        padding: 10px;
    }

    .radio_zone > p {
        font-weight: 600;
        color: var(--text-color-dark);
        margin-bottom: 6px;
    }

    .radio_ans {
    border: 1px solid var(--border-color);
    background-color: var(--background-card);
    margin: 5px 0;
    padding: 8px 10px;
    border-radius: 5px;
    box-shadow: 0 1px 1px var(--shadow-light);
    width: calc(100% - 20px);
    box-sizing: border-box;
    }

    .radio_ans p {
        margin: 3px 0;
        font-weight: normal;
        color: var(--text-color-dark);
        cursor: pointer;
        padding: 3px 5px;
        border-radius: 3px;
        transition: background-color 0.15s ease-in-out;
    }

    .radio_ans p:hover {
        background-color: var(--background-hover);
    }

    form {
        margin-top: 10px;
    }

    form input[type="checkbox"],
    form input[type="radio"] {
        margin-right: 5px;
        transform: scale(1.0); 
        cursor: pointer;
    }

    form label {
        display: inline-block;
        margin-bottom: 5px;
        cursor: pointer;
        padding: 3px 0;
    }

    form br {
        display: none;
    }

    form input[type="checkbox"] + label,
    form input[type="radio"] + label {
        display: inline-flex;
        align-items: center;
        gap: 5px;
    }
</style>
'''

def tao_cauhoi(path, name, data):
    
    s = gen_string(data)

    try:
        with open(os.path.join(path, "Cauhoi", f"{name}.html"), "w", encoding="utf-8") as f:
            f.write(s)
    except Exception as e:
        print(f"Loi khi tao file cau hoi: {e}")
        return False
    return True
