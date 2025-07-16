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
    s += "<meta charset='UTF-8'>\n"
    s += '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'

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
                        s += f"<p>{dapan}</p>\n"
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

    --text-color-dark: #222;
    --text-color-light: #555;

    --background-light: #f0f4f8;
    --background-card: #ffffff;
    --background-hover: #f1f8e9;
    --border-color: #d0d7de;
    --shadow-base: rgba(0, 0, 0, 0.05);
    --shadow-hover: rgba(0, 0, 0, 0.1);
}

body {
    font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    color: var(--text-color-dark);
    background-color: var(--background-light);
    line-height: 1.5;
    margin: 0;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.cauhoi {
    border: 1px solid var(--border-color);
    border-radius: 12px;
    background-color: var(--background-card);
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px var(--shadow-base);
    transition: all 0.3s ease-in-out;
    width: 100%;
    max-width: 680px;
    box-sizing: border-box;
}

.cauhoi:hover {
    background-color: var(--background-hover);
    box-shadow: 0 6px 18px var(--shadow-hover);
    transform: translateY(-2px);
}

.cauhoi > p:first-of-type {
    font-weight: 700;
    font-size: 1.2em;
    margin-bottom: 14px;
    border-bottom: 2px solid var(--primary-color);
    padding-bottom: 8px;
    color: var(--primary-color);
}

.cauhoi p:not(:first-child) {
    margin: 6px 0;
    padding: 8px 12px;
    cursor: pointer;
    border-radius: 6px;
    transition: background-color 0.2s ease, color 0.2s ease;
}

.cauhoi p:not(:first-child):hover {
    background-color: #e8f5e9;
    color: var(--secondary-color);
}

/* Zones */
.drag_ans_zone,
.grouping_ans_zone,
.radio_zone {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin: 12px 0;
    padding: 12px;
    border-radius: 8px;
    background-color: #f5faff;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.radio_zone {
    flex-direction: column;
    align-items: flex-start;
}

/* Answer blocks */
.radio_ans,
.drag_ans,
.grouping_ans {
    border: 1px solid var(--border-color);
    background-color: #ffffff;
    color: var(--text-color-dark);
    padding: 8px 14px;
    border-radius: 6px;
    cursor: grab;
    box-shadow: 0 1px 3px var(--shadow-base);
    transition: all 0.2s ease;
}

.radio_ans:hover,
.drag_ans:hover,
.grouping_ans:hover {
    background-color: #e3fcef;
    border-color: var(--primary-color);
    box-shadow: 0 3px 6px var(--shadow-hover);
}

.radio_ans p {
    margin: 4px 0;
    font-weight: normal;
    color: var(--text-color-dark);
    cursor: pointer;
    padding: 4px 6px;
    border-radius: 4px;
    transition: background-color 0.2s ease-in-out;
}

.radio_ans p:hover {
    background-color: #f1f8e9;
}

/* Inputs */
.input_zone input,
.grouping_zone input {
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    font-size: 1em;
    background-color: #fff;
    transition: border-color 0.2s, box-shadow 0.2s;
}

.input_zone input:focus,
.grouping_zone input:focus {
    border-color: var(--secondary-color);
    box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.15);
    outline: none;
}

/* Drop zone */
.drop_zone {
    border: 2px dashed var(--secondary-color);
    border-radius: 6px;
    padding: 14px;
    margin: 8px 0;
    background-color: #e3f2fd;
    min-height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color-dark);
    text-align: center;
    font-size: 1em;
}

/* Form controls */
form input[type="checkbox"],
form input[type="radio"] {
    margin-right: 6px;
    transform: scale(1.1);
    cursor: pointer;
}

form label {
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    padding: 4px 0;
    gap: 6px;
    font-size: 0.95em;
}

form br {
    display: none;
}

body {
  font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
  color: var(--text-color-dark); /* Giữ màu chữ tối để dễ đọc trên nền sáng */
  line-height: 1.5;
  margin: 0;
  padding: 40px 20px;
  min-height: 100vh;

  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;

  /* BACKGROUND MỚI */
  background: linear-gradient(
    135deg, /* Góc chuyển màu: 135 độ */
    #ff7e5f, /* Màu 1: Cam đào */
    #feb47b, /* Màu 2: Vàng cam */
    #86a8e7, /* Màu 3: Xanh nhạt */
    #91eae4  /* Màu 4: Xanh ngọc */
  );
  /* Fallback nếu gradient không được hỗ trợ */
  background-color: #ff7e5f;
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
