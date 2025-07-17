import os
import sys
import data_worker as worker
import tkinter as tk

danhsach_id = []
cauhoi_root = []
token = ""

def get_dir():
    path = ""
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.path.dirname(os.path.abspath(__file__))
    return path

root_path = get_dir()



def button_import_click(text_box, label_trangthai, text_box_name, label_soluong):
    global danhsach_id, cauhoi_root
    if text_box_name.get("1.0", tk.END).strip() == "":
        label_trangthai.config(text="Vui long nhap ten", fg="red")
        return
    text = text_box.get("1.0", tk.END).strip()
    data = worker.read_data(text)
    if data == False:
        label_trangthai.config(text="Loi, du lieu khong hop le", fg="red")
        text_box.delete("1.0", tk.END)
        return

    cauhoi = data["data"][0]["test"]

    cauhoi_root, danhsach_id = worker.add_question(cauhoi_root, cauhoi, danhsach_id)
    label_soluong.config(text=f"So luong cau hoi: {len(danhsach_id)}", fg="black")
    text_box.delete("1.0", tk.END)
   

def button_clear_click(text_box, label_soluong):
    global danhsach_id, cauhoi_root
    text_box.delete("1.0", tk.END)
    label_soluong.config(text="So luong cau hoi: 0", fg="black")
    danhsach_id = []
    cauhoi_root = []
  

def button_gen_click(text_box_name, label_trangthai, token):
    if ( len(danhsach_id) == 0):
        label_trangthai.config(text="Khong co cau hoi nao", fg="red")
        return
    name = text_box_name.get("1.0", tk.END).strip()
    if name == "":
        label_trangthai.config(text="Vui long nhap ten", fg="red")
        return
    if not os.path.exists(os.path.join(root_path, "Cauhoi")):
        os.mkdir("Cauhoi")
    
    noti = worker.tao_cauhoi(root_path, name, cauhoi_root, token, label_trangthai)
    if noti:
        label_trangthai.config(text="Tao thanh cong", fg="green")


def read_token():
    global token
    try:
        with open(os.path.join(root_path, "token.txt"), "r") as f:
            token = f.read().strip()
    except FileNotFoundError:
        token = ""
        with open(os.path.join(root_path,"token.txt"), "w") as f:
            f.write("")
    return token

def write_token(token):
    with open(os.path.join(root_path, "token.txt"), "w") as f:
        f.write(token)

def write_token_click(text_box, label_trangthai, window):
    global token
    t = text_box.get("1.0", tk.END).strip()
    write_token(t)
    label_trangthai.config(text="Da them token", fg="green")
    token = read_token()
    window.destroy()



def button_import_token_click(label_trangthai):
    global token

    window = tk.Toplevel()
    window.title("Nhap token")
    window.geometry("400x270")
    window.configure(bg="gray")
    text_box = tk.Text(window, wrap=tk.WORD, width=90, height=24,  font=("Arial", 14))
    text_box.place(x=10, y=10, width=370, height=170) 

    button_import = tk.Button(window, text="Them du lieu", font=("Arial", 14), cursor="hand2")
    button_import.place(x=125, y=200, width=150, height=50)
    button_import.config(command=lambda: write_token_click(text_box, label_trangthai, window))




def main():
    global token
    token = read_token()

    soluong = 0
    root = tk.Tk()
    root.title("Tong hop cau hoi")
    root.geometry("1280x720")
    root.configure(bg="gray")

    #text box data
    text_box = tk.Text(root, wrap=tk.WORD, width=80, height=24,  font=("Arial", 14))
    text_box.place(x=25, y=25, width=550, height=600) 

    text_box_name = tk.Text(root, wrap=tk.WORD, width=80, height=24,  font=("Arial", 22))
    text_box_name.place(x=780, y=55, width=350, height=59) 

    #label hiem thi
    label_soluong = tk.Label(root, text=f"So luong cau hoi: {soluong}", font=("Arial", 24), fg="black")
    label_soluong.place(x=780, y=155)

    label_name = tk.Label(root, text=f"Name: ", font=("Arial", 24), fg="black", bg="gray")
    label_name.place(x=660, y=55, height=59)

    label_trangthai = tk.Label(root, text="", font=("Arial", 24), fg="black", bg="gray")
    label_trangthai.place(x=780, y=255)


    #button 
    button_import = tk.Button(root, text="Them du lieu", font=("Arial", 14), cursor="hand2")
    button_import.place(x=25, y=655, width=150, height=50)
    button_import.config(command=lambda: button_import_click(text_box, label_trangthai, text_box_name, label_soluong))

    button_clear = tk.Button(root, text="Clear du lieu", font=("Arial", 14), cursor="hand2")
    button_clear.place(x=225, y=655, width=150, height=50)
    button_clear.config(command=lambda: button_clear_click(text_box, label_soluong))

    button_gen = tk.Button(root, text="Tao file cau hoi", font=("Arial", 14), cursor="hand2")
    button_gen.place(x=780, y=655, width=150, height=50)
    button_gen.config(command=lambda: button_gen_click(text_box_name, label_trangthai, token))

    button_token = tk.Button(root, text="Import token", font=("Arial", 14), cursor="hand2")
    button_token.place(x=1100, y=655, width=150, height=50)
    button_token.config(command=lambda: button_import_token_click(label_trangthai))


    root.mainloop()

main()