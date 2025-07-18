from bs4 import BeautifulSoup as soup
import os
import json
from crc32 import return_signature
import requests
import base64

token1 = ""
label_trangthai = None

def fetch_img(name):
    url = f"https://apps.ictu.edu.vn:9087/ionline/api/aws/file/{name}"
    body = {}

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": f"Bearer {token1}",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Host": "apps.ictu.edu.vn:9087",
        "Origin": "https://lms.ictu.edu.vn",
        "Referer": "https://lms.ictu.edu.vn/",
        "Sec-CH-UA": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "X-App-Id": "7040BD38-0D02-4CBE-8B0E-F4115C348003",
        "X-Request-Signature": return_signature("POST", body)
    }

    response = requests.post(url, headers=headers, json=body)

    link_to_img = response.json().get("data")
    if link_to_img:
        res = requests.get(link_to_img)
        img = res.content
        image_base64 = base64.b64encode(img).decode("utf-8")
        mime_type = "image/png" 
        data_uri = f"data:{mime_type};base64,{image_base64}"
        return data_uri
    else:
        return False


def search_img(dulieu):
    soup_obj = soup(dulieu, "html.parser")
    img_tags = soup_obj.find_all("img")
    for img in img_tags:
        if img.has_attr("src"):
            img_beta = fetch_img(img["src"])
            if img_beta:
                img["src"] = img_beta
            else:
                label_trangthai.config(text="Token het han", fg="red")
                return False
            
    return soup_obj.prettify()


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
            cauhoi = search_img(cauhoi)
            if cauhoi == False:
                return False
            hint = ""
            if item["question_type"] == "checkbox":
                hint = f"(Chon {item['number_answer_correct']} dap an)"
            s += f"Cau {stt}:{cauhoi} {hint}\n"
     
            for ans in item["answer_option"]:
                dapan = ans['value']
                dapan = search_img(dapan)
                if dapan == False:
                    return False
                s += f"\t<div style='display: flex; align-items: center; gap: 2px; margin-bottom: 5px'><input type='checkbox' name='answer'>{dapan}</div>\n"
           
            s += "</div>\n\n"
        
        #drag_drop template
        elif item['question_type'] == "drag_drop":
            cauhoi = item['question_direction']
            cauhoi = search_img(cauhoi)
            if cauhoi == False:
                return False
            s += "<div>\n"
            s += f"Cau {stt}:{cauhoi}\n"

            #cac dap an co the keo
            s += "<p>(Cac dap an)</p>\n"
            s += "<div class='drag_ans_zone'>\n"
            for ans in item["answer_option"]:
                dapan =f"<div class='drag_ans'>{ans['value']}</div>"
                dapan = search_img(dapan)
                if cauhoi == False:
                    return False
                s += f"\t{dapan}\n\n"
            s += "</div>\n"
            s += "</div>\n"

            #khu vuc keo dap an vao
            s += "<div>\n"
            s += "<p>(Cac lua chon tuong duong voi dap an)</p>\n\n\n"
            s += "<div class='ans_to_drag'>\n"
            for jtem in data:
                if jtem['group_id'] == item['id']:
                    s += "<div class='drop_zone'>\n"
                    s += f"<p>{jtem['question_direction']}</p>\n"
                    s += "</div>\n"
            s += "</div>\n"
            s += "</div>\n"
            s += "</div>\n\n"

        #group-input template
        elif item['question_type'] == "group-input":
            cauhoi = item['question_direction']
            cauhoi = search_img(cauhoi)
            if cauhoi == False:
                return False
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
            cauhoi = search_img(cauhoi)
            if cauhoi == False:
                return False
            s += "<div>\n"
            s += f"Cau {stt}:{cauhoi}\n"
            s += "<div class='grouping_ans_zone'>\n"
            for ans in item["answer_option"]:
                dapan =f"<div class='grouping_ans'>{ans['value']}</div>"  
                dapan = search_img(dapan)
                if dapan == False:
                    return False
                s += f"\t{dapan}\n\n"
            s += "</div>\n"
            idx = 1
            s += "<div>\n"
            for jtem in data:
                if jtem['group_id'] == item['id']:
                    s += "<div class='grouping_zone'>\n"

                    s += f"<p>{idx}) {jtem['question_direction']}</p>\n"
                    s += "<input type='text' name='answer'>\n"

                    s += "</div>\n"
                    idx += 1
            s += "</div>\n"
            s += "</div>\n\n"


        #group-radio template
        elif item['question_type'] == "group-radio":
            cauhoi = item['question_direction']
            cauhoi = search_img(cauhoi)
            if cauhoi == False:
                return False
            s += f"Cau {stt}:{cauhoi}\n"
            idx = 1
            for jtem in data:
                if jtem['group_id'] == item['id']:
                    s += "<div class='radio_zone'>\n"

                    s += f"<p>{idx}) {jtem['question_direction']}</p>\n"

                    s += "<div class='radio_ans'>\n"
                    for ans in jtem["answer_option"]:
                        dapan = ans['value']
                        dapan = search_img(dapan)
                        if dapan == False:
                            return False
                        s += f"<p>{dapan}</p>\n"
           
                    s += "</div>\n\n"
                    s += "</div>\n"
                    idx += 1

            s += "</div>\n\n"

        #default template
        else:
            s += "<div>\n"
            cauhoi = item['question_direction']
            cauhoi = search_img(cauhoi)
            if cauhoi == False:
                return False
            s += f"Cau {stt}:{cauhoi}\n"
         
            s += "</div>\n"

            for ans in item["answer_option"]:
                dapan = ans['value']
                dapan = search_img(dapan)
                if dapan == False:
                    return False
                s += f"<div class='dapan'>{dapan}</div>\n\n"

        s += "</div>\n\n"
        stt += 1
    s += '''
    <script>
    document.querySelectorAll('.cauhoi').forEach(function(cauhoi) {
    cauhoi.querySelectorAll('.dapan').forEach(function(dapan) {
        dapan.addEventListener('click', function() {
    
        cauhoi.querySelectorAll('.dapan').forEach(function(item) {
            item.classList.remove('selected');
        });

        dapan.classList.add('selected');
        });
    });
    });
    </script>
    '''
    return s

def get_style():
    return '''
<style>
/* Root CSS Variables for Consistent Styling */
:root {
    --primary-color: #4CAF50;    /* Green */
    --secondary-color: #2196F3;  /* Blue */
    --accent-color: #FFC107;     /* Amber/Yellow */

    --text-color-dark: #222;     /* Dark grey for main text */
    --text-color-light: #555;    /* Lighter grey for secondary text */

    --background-light: #f0f4f8; /* Light greyish blue for general background */
    --background-card: #ffffff;  /* White for card backgrounds */
    --background-hover: #f1f8e9; /* Light green for hover states */
    --border-color: #d0d7de;     /* Light grey for borders */
    --shadow-base: rgba(0, 0, 0, 0.05); /* Subtle shadow */
    --shadow-hover: rgba(0, 0, 0, 0.1); /* Slightly more prominent shadow on hover */
}

/* Base Body Styles */
body {
    font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    color: var(--text-color-dark);
    line-height: 1.5;
    margin: 0;
    padding: 40px 20px; /* Increased padding for better spacing */
    min-height: 100vh; /* Ensures body takes full viewport height */

    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

    /* Dynamic Background Gradient */
    background: linear-gradient(
        135deg, /* Angle for the gradient */
        #ff7e5f, /* Peach/Orange */
        #feb47b, /* Orange-Yellow */
        #86a8e7, /* Light Blue */
        #91eae4  /* Teal/Aqua */
    );
    /* Fallback for browsers that don't support gradients */
    background-color: #ff7e5f;
}

/* --- Question Container Styling --- */
.cauhoi {
    border: 1px solid var(--border-color);
    border-radius: 12px;
    background-color: var(--background-card);
    padding: 20px 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px var(--shadow-base);
    transition: all 0.3s ease-in-out; /* Smooth transition for hover effects */
    width: 100%;
    max-width: 680px; /* Limits the overall width of the question box */
    box-sizing: border-box; /* Ensures padding and border are included in the width */
}

.cauhoi:hover {
    background-color: var(--background-hover);
    box-shadow: 0 6px 18px var(--shadow-hover);
    transform: translateY(-2px); /* Slight lift effect on hover */
}

/* Styling for the first paragraph (question text) within .cauhoi */
.cauhoi > p:first-of-type {
    font-weight: 700; /* Bold font for question */
    font-size: 1.2em; /* Slightly larger font size */
    margin-bottom: 14px;
    border-bottom: 2px solid var(--primary-color); /* Underline with primary color */
    padding-bottom: 8px;
    color: var(--primary-color);
}

/* Styling for other paragraphs (likely options) within .cauhoi */
.cauhoi p:not(:first-child) {
    margin: 6px 0;
    padding: 8px 12px;
    cursor: pointer;
    border-radius: 6px;
    transition: background-color 0.2s ease, color 0.2s ease;
}

.cauhoi p:not(:first-child):hover {
    background-color: #e8f5e9; /* Light green on hover */
    color: var(--secondary-color); /* Change text color on hover */
}

/* --- Answer Zones Styling --- */
.drag_ans_zone,
.grouping_ans_zone,
.radio_zone {
    display: flex;
    flex-wrap: wrap; /* Allows items to wrap to the next line */
    gap: 10px; /* Spacing between items */
    margin: 12px 0;
    padding: 12px;
    border-radius: 8px;
    background-color: #f5faff; /* Very light blue background */
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05); /* Inner shadow */
}

.radio_zone {
    flex-direction: column; /* Stacks radio options vertically */
    align-items: flex-start;
}

/* --- Individual Answer Block Styles (drag_ans, grouping_ans, radio_ans) --- */
.radio_ans,
.drag_ans,
.grouping_ans {
    border: 1px solid var(--border-color);
    background-color: #ffffff;
    color: var(--text-color-dark);
    padding: 8px 14px;
    border-radius: 6px;
    cursor: grab; /* Indicates draggable item */
    box-shadow: 0 1px 3px var(--shadow-base);
    transition: all 0.2s ease;
}

.radio_ans:hover,
.drag_ans:hover,
.grouping_ans:hover {
    background-color: #e3fcef; /* Lightest green on hover */
    border-color: var(--primary-color);
    box-shadow: 0 3px 6px var(--shadow-hover);
}

/* Paragraphs within radio answer blocks */
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
    background-color: #f1f8e9; /* Lightest green background on hover */
}

/* --- Input Field Styles --- */
.input_zone input,
.grouping_zone input {
    width: 100%; /* Full width of parent */
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
    box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.15); /* Blue glow on focus */
    outline: none; /* Removes default outline */
}

/* --- Drop Zone Styles --- */
.drop_zone {
    border: 2px dashed var(--secondary-color); /* Dashed blue border */
    border-radius: 6px;
    padding: 14px;
    margin: 8px 0;
    background-color: #e3f2fd; /* Very light blue background */
    min-height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color-dark);
    text-align: center;
    font-size: 1em;
}

/* --- Form Control Styles (Checkboxes, Radios, Labels) --- */
form input[type="checkbox"],
form input[type="radio"] {
    margin-right: 6px;
    transform: scale(1.1); /* Slightly larger checkboxes/radios */
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

/* Hides <br> tags used for spacing in forms, if any */
form br {
    display: none;
}

/* --- General Answer (dapan) Block Styles --- */
.dapan {
  padding: 5px;
  margin-bottom: 10px;
  background-color: #eee; /* Light grey background */
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.dapan p {
    padding-left: 10px;
}

.dapan:hover {
  background-color: #ddd; /* Darker grey on hover */
}

.dapan.selected {
  background-color: var(--accent-color); /* Amber/Yellow for selected answer */
  font-weight: bold;
  color: #000;
}

/* --- Crucial Additions for Image Responsiveness --- */
/* This ensures all images within .cauhoi and .dapan scale correctly */
.cauhoi img,
.dapan img {
    max-width: 100%; /* Images will never exceed the width of their container */
    height: auto;    /* Maintain the image's aspect ratio */
    display: block;  /* Helps with proper spacing and layout */
    border-radius: 8px; /* Optional: Adds rounded corners to images */
    margin: 10px 0;  /* Optional: Adds vertical spacing around images */
}

/* If images are nested inside paragraphs within .cauhoi or .dapan */
.cauhoi p img,
.dapan p img {
    max-width: 100%;
    height: auto;
    display: block;
    border-radius: 8px;
    margin-top: 5px;
    margin-bottom: 5px;
}
</style>
'''

def tao_cauhoi(path, name, data, token, label):
    global token1,label_trangthai
    token1 = token
    label_trangthai = label
    s = gen_string(data)
    if  s == False:
        return False
    try:
        with open(os.path.join(path, "Cauhoi", f"{name}.html"), "w", encoding="utf-8") as f:
            f.write(s)
    except Exception as e:
        label_trangthai.config(text="Khong the tao file", fg="red")
        return False
    return True
