import os,sys
import configparser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import subprocess
import platform
from pathlib import Path
 
 
 
# ---------- 持久化 ini 路径 ----------
def get_ini_path() -> Path:
    """
    返回一个可持久写入的 ini 文件路径。
    开发时放在脚本目录；打包后放在用户数据目录。
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后
        base = Path.home()  / 'PdfZipMerger' \
            if os.name == 'nt' else Path.home() / '.config' / 'PdfZipMerger'
    else:
        # 源码运行
        base = Path(__file__).parent
    base.mkdir(parents=True, exist_ok=True)
    return base / 'zipInPdfSettings.ini'
 
INI_FILE = get_ini_path()
# ---------- 配置 ----------
def load_output_dir() -> str:
    cfg = configparser.ConfigParser()
    cfg.read(INI_FILE, encoding="utf-8")
    return cfg.get("DEFAULT", "output_dir", fallback="")
 
def save_output_dir(path: str):
    cfg = configparser.ConfigParser()
    cfg["DEFAULT"] = {"output_dir": path}
    with open(INI_FILE, "w", encoding="utf-8") as f:
        cfg.write(f)
 
# ---------- 文件名 ----------
def auto_increment_filename(full_path: str) -> str:
    if not os.path.exists(full_path):
        return full_path
    base, ext = os.path.splitext(full_path)
    counter = 1
    while True:
        new_name = f"{base}{counter}{ext}"
        if not os.path.exists(new_name):
            return new_name
        counter += 1
 
# ---------- 拖拽 ----------
def drop_pdf(event):
    files = root.tk.splitlist(event.data)
    if files:
        pdf_var.set(files[0])
        if not out_dir_var.get():
            out_dir_var.set(os.path.dirname(files[0]))
 
def drop_zip(event):
    files = root.tk.splitlist(event.data)
    if files:
        zip_var.set(files[0])
 
# ---------- 浏览 ----------
def browse_pdf():
    path = filedialog.askopenfilename(title="选择 PDF 文件", filetypes=[("PDF files", "*.pdf")])
    if path:
        pdf_var.set(path)
        if not out_dir_var.get():
            out_dir_var.set(os.path.dirname(path))
 
def browse_zip():
    path = filedialog.askopenfilename(title="选择 ZIP 文件", filetypes=[("ZIP files", "*.zip")])
    if path:
        zip_var.set(path)
 
def browse_out_dir():
    path = filedialog.askdirectory(title="选择输出目录")
    if path:
        out_dir_var.set(path)
        save_output_dir(path)
 
# ---------- 合并 ----------
def merge():
    pdf_path = pdf_var.get().strip('"')
    zip_path = zip_var.get().strip('"')
    out_dir = out_dir_var.get().strip()
    base_name = out_name_var.get().strip() or "new"
    if not pdf_path or not zip_path:
        messagebox.showerror("错误", "请选择 PDF 和 ZIP 文件！")
        return
    if not out_dir:
        messagebox.showerror("错误", "请选择输出目录！")
        return
    full_out = auto_increment_filename(os.path.join(out_dir, base_name + ".pdf"))
    try:
        with open(full_out, "wb") as out_file:
            out_file.write(open(pdf_path, "rb").read())
            out_file.write(open(zip_path, "rb").read())
        messagebox.showinfo("成功", f"已合并为：{full_out}")
    except Exception as e:
        messagebox.showerror("合并失败", str(e))
 
# ---------- 快捷按钮 ----------
def open_out_dir():
 
    out_dir = out_dir_var.get().strip()
    print(out_dir)
    # messagebox.showwarning("提示", f"输出目录不存在：{out_dir}")
    if not out_dir:
        messagebox.showwarning("提示", "请先选择输出目录！")
        return
    
    # 规范化路径，处理斜杠和反斜杠问题
    out_dir = os.path.normpath(out_dir)
    
    if not os.path.exists(out_dir):
        messagebox.showerror("错误", f"输出目录不存在：{out_dir}")
        return
    
    try:
        # 使用更健壮的方式打开文件浏览器
        if platform.system() == "Windows":
            print("Windows")
            subprocess.run(["explorer", out_dir], check=True)
            # os.startfile(out_dir)  # Windows系统使用os.startfile
        elif platform.system() == "Darwin":
            print("macOS")
            subprocess.run(["open", out_dir], check=True)  # macOS使用open命令
        else:  # Linux
            print("Linux")
            subprocess.run(["xdg-open", out_dir], check=True)  # Linux使用xdg-open
    except Exception as e:
        print("错误", f"无法打开文件夹：{str(e)}")
        # messagebox.showerror("错误", f"无法打开文件夹：{str(e)}")
 
 
def clear_inputs():
    pdf_var.set("")
    zip_var.set("")
 
# ---------- GUI ----------
root = TkinterDnD.Tk()
root.title("PDF + ZIP 合并器")
root.geometry("600x290")
root.resizable(False, False)
 
style = ttk.Style()
style.theme_use("vista")
print(style.theme_names())
 
# 配置按钮样式
style.configure("Red.TButton", background="red", foreground="red")
style.configure("Green.TButton", background="green", foreground="green")
 
# 拖拽提示
drag_tip = ttk.Label(root, text="PDF 和 ZIP 文件可直接拖拽到对应输入框中",
                     foreground="RoyalBlue", anchor="center", font=("Segoe UI", 12 ))
drag_tip.grid(row=0, column=0, columnspan=3, pady=(6, 0), sticky="ew", padx=10)
 
# PDF
ttk.Label(root, text="PDF 文件：").grid(row=1, column=0, padx=10, pady=8, sticky="e")
pdf_var = tk.StringVar()
pdf_entry = ttk.Entry(root, textvariable=pdf_var, width=55)
pdf_entry.grid(row=1, column=1, padx=5, pady=8)
pdf_entry.drop_target_register(DND_FILES)
pdf_entry.dnd_bind("<<Drop>>", drop_pdf)
ttk.Button(root, text="浏览…", command=browse_pdf).grid(row=1, column=2, padx=5, pady=8)
 
# ZIP
ttk.Label(root, text="ZIP 文件：").grid(row=2, column=0, padx=10, pady=8, sticky="e")
zip_var = tk.StringVar()
zip_entry = ttk.Entry(root, textvariable=zip_var, width=55)
zip_entry.grid(row=2, column=1, padx=5, pady=8)
zip_entry.drop_target_register(DND_FILES)
zip_entry.dnd_bind("<<Drop>>", drop_zip)
ttk.Button(root, text="浏览…", command=browse_zip).grid(row=2, column=2, padx=5, pady=8)
 
# 输出目录
ttk.Label(root, text="输出目录：").grid(row=3, column=0, padx=10, pady=8, sticky="e")
out_dir_var = tk.StringVar(value=load_output_dir())
out_dir_entry = ttk.Entry(root, textvariable=out_dir_var, width=55)
out_dir_entry.grid(row=3, column=1, padx=5, pady=8)
ttk.Button(root, text="浏览…", command=browse_out_dir).grid(row=3, column=2, padx=5, pady=8)
 
# 输出文件名
ttk.Label(root, text="新文件名：").grid(row=4, column=0, padx=10, pady=8, sticky="e")
out_name_var = tk.StringVar(value="new")
out_name_entry = ttk.Entry(root, textvariable=out_name_var, width=55)
out_name_entry.grid(row=4, column=1, padx=5, pady=8, sticky="w")
ttk.Button(root, text="打开输出文件夹", command=open_out_dir).grid(row=4, column=2, padx=5, pady=8)
# ttk.Button(btn_frame, text="打开输出文件夹", command=open_out_dir).pack(side="left", padx=10)
 
# 按钮行
btn_frame = ttk.Frame(root)
btn_frame.grid(row=5, column=0, columnspan=3, pady=12)
# 使用Red.TButton样式
ttk.Button(btn_frame, text="清空数据", command=clear_inputs, style="Red.TButton").pack(side="left", padx=10)
# 使用Green.TButton样式
ttk.Button(btn_frame, text="合并", command=merge, style="Green.TButton").pack(side="left", padx=10)
 
drag_tip2 = ttk.Label(root, text=f"配置文件路径：{INI_FILE}",
                     foreground="RoyalBlue", font=("Segoe UI", 10))
drag_tip2.grid(row=6, column=0, columnspan=3, pady=(6, 0), sticky="w", padx=10)
root.mainloop()
