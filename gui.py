import os
import data_worker as worker
import tkinter as tk

root_path = os.getcwd()
danhsach_id = []
cauhoi_root = []


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
   

def button_clear_click(text_box):
    text_box.delete("1.0", tk.END)


def button_gen_click(text_box_name, label_trangthai):
    if ( len(danhsach_id) == 0):
        label_trangthai.config(text="Khong co cau hoi nao", fg="red")
        return
    name = text_box_name.get("1.0", tk.END).strip()
    if name == "":
        label_trangthai.config(text="Vui long nhap ten", fg="red")
        return
    if not os.path.exists("Cauhoi"):
        os.mkdir("Cauhoi")
    
    noti = worker.tao_cauhoi(root_path, name, cauhoi_root)
    if noti:
        label_trangthai.config(text="Tao thanh cong", fg="green")
    else:
        label_trangthai.config(text="Loi, khong tao duoc", fg="red")

    

def main():
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
    button_clear.config(command=lambda: button_clear_click(text_box))

    button_gen = tk.Button(root, text="Tao file cau hoi", font=("Arial", 14), cursor="hand2")
    button_gen.place(x=780, y=655, width=150, height=50)
    button_gen.config(command=lambda: button_gen_click(text_box_name, label_trangthai))

    root.mainloop()

main()