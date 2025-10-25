import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk


class CSVApp:
    def __init__(self, master):
        self.master = master
        master.title("ĐỌC & GHI FILE CSV")
        master.geometry("1000x700")
        master.resizable(True, True)

        # Nút đọc file CSV
        self.read_button = tk.Button(master, text="Đọc file",
                                     width=30, height=2, font=("Arial", 12),
                                     command=self.read_csv)
        self.read_button.pack(pady=10)

        # Nút ghi file CSV mới
        self.write_button = tk.Button(master, text="Ghi ra file CSV mới",
                                      width=30, height=2, font=("Arial", 12),
                                      command=self.write_csv)
        self.write_button.pack(pady=10)

        # Frame chứa bảng
        self.frame_table = tk.Frame(master)
        self.frame_table.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview để hiển thị bảng
        self.tree = ttk.Treeview(self.frame_table, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        # Scrollbar dọc
        self.vsb = ttk.Scrollbar(self.frame_table, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.vsb.set)

    def read_csv(self):
        input_file = "healthcare_dataset.csv"
        if not os.path.exists(input_file):
            messagebox.showerror("Lỗi", f"Không tìm thấy file {input_file} trong thư mục!")
            return

        try:
            with open(input_file, mode='r', encoding='utf-8', newline='') as file:
                reader = csv.reader(file)
                header = next(reader)  # tiêu đề cột
                # Cấu hình Treeview với các cột
                self.tree["columns"] = header
                for col in header:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=150, anchor="w")

                # Xóa dữ liệu hiện có
                for i in self.tree.get_children():
                    self.tree.delete(i)

                # Chèn các hàng
                for row in reader:
                    self.tree.insert("", "end", values=row)

            messagebox.showinfo("Thành công", "Đã đọc file healthcare_dataset.csv thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file!\n{e}")

    def write_csv(self):
        input_file = "healthcare_dataset.csv"
        if not os.path.exists(input_file):
            messagebox.showerror("Lỗi", f"Không tìm thấy file {input_file}!")
            return

        save_path = filedialog.asksaveasfilename(
            title="Lưu file CSV mới",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not save_path:
            return

        try:
            with open(input_file, mode='r', encoding='utf-8', newline='') as infile:
                reader = csv.reader(infile)
                rows = list(reader)

            with open(save_path, mode='w', encoding='utf-8', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(rows)

            messagebox.showinfo("Thành công", f"Đã sao chép dữ liệu ra file mới:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể ghi file!\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVApp(root)
    root.mainloop()
