import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque
from avl_tree import AVLTree

class HealthcareAVLApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Healthcare Dataset - Quản lý & Cây AVL")
        self.root.geometry("1200x760")

        self.data = []
        self.headers = []
        self.key_column = "Billing Amount"
        self.default_csv_path = "healthcare_dataset.csv"

        self.avl = AVLTree()
        self.root_node = None

        # Tạo vùng vẽ hình cây AVL (sẽ được nhúng vào giao diện Tkinter)
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.ax.axis('off')

        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill="both", expand=True)  # chiếm toàn bộ vùng cửa sổ

        self.tab1 = ttk.Frame(self.nb)
        self.tab2 = ttk.Frame(self.nb)

        self.nb.add(self.tab1, text="Quản lý dữ liệu")
        self.nb.add(self.tab2, text="Cây AVL")

        self.create_tab1()
        self.create_tab2()

        self.positions = {}  # dùng lưu toạ độ node khi vẽ

    def create_tab1(self):

        frame_top = tk.Frame(self.tab1)
        frame_top.pack(fill="x", pady=6, padx=6)
        tk.Button(frame_top, text="Đọc file CSV", command=self.on_read_csv).pack(side="left", padx=4)
        tk.Button(frame_top, text="Ghi file CSV", command=self.on_save_csv).pack(side="left", padx=4)
        tk.Button(frame_top, text="Thêm (form đầy đủ)", command=self.open_add_form).pack(side="left", padx=4)
        tk.Button(frame_top, text="Sửa dòng", command=self.open_edit_form).pack(side="left", padx=4)
        tk.Button(frame_top, text="Xóa dòng", command=self.delete_selected_row).pack(side="left", padx=4)
        search_frame = tk.Frame(self.tab1)
        search_frame.pack(fill="x", pady=6, padx=6)
        tk.Label(search_frame, text="Cột:").pack(side="left")
        self.search_col_cb = ttk.Combobox(search_frame, values=self.headers, state="readonly", width=30)
        self.search_col_cb.pack(side="left", padx=6)
        tk.Label(search_frame, text="Từ khóa:").pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=6)
        tk.Button(search_frame, text="Tìm", command=self.search_table).pack(side="left", padx=4)
        tk.Button(search_frame, text="Làm mới", command=self.refresh_table).pack(side="left", padx=4)
        table_frame = tk.Frame(self.tab1)
        table_frame.pack(fill="both", expand=True, padx=6, pady=6)
        self.treeview = ttk.Treeview(table_frame, show="headings")
        self.treeview.pack(side="left", fill="both", expand=True)
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.treeview.yview)
        vsb.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=vsb.set)
    def on_read_csv(self):
        path = filedialog.askopenfilename(
            title="Chọn file CSV",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return
        try:

            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.headers = reader.fieldnames if reader.fieldnames else []

                self.data = list(reader)

        except Exception as e:
            messagebox.showerror("Lỗi đọc file", str(e))
            return
        if self.key_column not in self.headers:
            if "Billing Amount" in self.headers:
                self.key_column = "Billing Amount"
            elif self.headers:
                self.key_column = self.headers[0]
        self.search_col_cb['values'] = self.headers
        if self.headers:
            try:
                self.search_col_cb.current(0)

            except:
                pass
        self.refresh_table()
        messagebox.showinfo("Đã đọc", f"Đã đọc {len(self.data)} dòng. Khóa chính: '{self.key_column}'")

    def on_save_csv(self):
        if not self.headers:
            messagebox.showwarning("Không có dữ liệu để lưu.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return
        try:
            # Ghi dữ liệu ra file CSV tại đường dẫn người dùng đã chọn.
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)

                writer.writeheader()
                writer.writerows(self.data)
            messagebox.showinfo("Đã lưu", f"Đã lưu {len(self.data)} dòng vào {path}")

        except Exception as e:
            messagebox.showerror("Lỗi lưu file", str(e))

    def refresh_table(self, filtered=None):
        for it in self.treeview.get_children():
            # get_children() trả về danh sách các item (dòng) hiện có trong bảng
            self.treeview.delete(it)
        self.treeview["columns"] = self.headers

        for col in self.headers:
            self.treeview.heading(col, text=col)
            # heading(): đặt tiêu đề (caption) cho cột
            self.treeview.column(col, width=140, anchor='w')
        rows = filtered if filtered is not None else self.data
        for r in rows:
            vals = [r.get(h, "") for h in self.headers]
            self.treeview.insert("", "end", values=vals)

    def search_table(self):
        col = self.search_col_cb.get()

        kw = self.search_entry.get().strip().lower()

        if not col or not kw:
            # Nếu người dùng chưa chọn cột hoặc chưa nhập từ khóa thì cảnh báo
            messagebox.showwarning("Cảnh báo", "Chọn cột và nhập từ khóa.")
            return  # Thoát khỏi hàm, không thực hiện tìm kiếm

        filtered = [r for r in self.data if kw in str(r.get(col, "")).lower()]

        self.refresh_table(filtered)
        messagebox.showinfo("Kết quả", f"Tìm thấy {len(filtered)} dòng khớp.")
    def open_add_form(self):
        if not self.headers:
            messagebox.showwarning("Bạn cần đọc file CSV trước.")
            return

        win = tk.Toplevel(self.root)
        # Toplevel(): tạo một cửa sổ con độc lập với cửa sổ chính (root)
        win.title("Thêm dòng mới (form đầy đủ)")
        entries = {}
        # entries sẽ chứa cặp {TênCột: ÔNhập}, giúp dễ dàng truy xuất sau này

        for i, col in enumerate(self.headers):
            # i: chỉ số hàng hiện tại trong form
            # col: tên cột dữ liệu (ví dụ: "Customer Name")

            tk.Label(win, text=col).grid(row=i, column=0, sticky='w', padx=6, pady=2)

            e = tk.Entry(win, width=80)
            e.grid(row=i, column=1, padx=6, pady=2)
            entries[col] = e
            # Lưu lại entry này vào dict để sau có thể lấy giá trị nhập theo tên cột

            def do_add():
                # Tạo một dict mới (1 dòng dữ liệu) bằng cách
                # lấy giá trị từ tất cả các ô nhập (entries)
                new = {col: entries[col].get() for col in self.headers}

                # Thêm dict mới vào danh sách dữ liệu gốc
                self.data.append(new)
                self.refresh_table()
                # Đóng cửa sổ nhập sau khi thêm xong
                win.destroy()

            tk.Button(win, text="Thêm", command=do_add).grid(
                row=len(self.headers), column=0, columnspan=2, pady=8
            )
            # Nút “Thêm” sẽ gọi hàm do_add() khi người dùng nhấn
            # columnspan=2 để nút chiếm hết 2 cột (đặt ở giữa)
            # pady=8 tạo khoảng cách phía trên/dưới

    def open_edit_form(self):
        sel = self.treeview.focus()
        # focus() trả về ID của dòng hiện đang được chọn trong bảng Treeview
        if not sel:
            messagebox.showwarning("Chọn 1 dòng để sửa.")
            return  # Thoát khỏi hàm, không làm gì thêm

        idx = self.treeview.index(sel)
        # Lấy chỉ số (vị trí) của dòng được chọn trong Treeview (tính từ 0)

        row = self.data[idx]
        # Lấy ra dictionary dữ liệu tương ứng từ danh sách self.data (chứa toàn bộ file CSV)
        # row là một dict như {"Name": "Alice", "Age": "25", "City": "Hanoi"}

        # TẠO CỬA SỔ CON (TOPLEVEL) ĐỂ SỬA DỮ LIỆU
        win = tk.Toplevel(self.root)
        # Toplevel(): tạo một cửa sổ mới, độc lập với cửa sổ chính (root)
        win.title("Sửa dòng")

        # TẠO TỪ ĐIỂN LƯU CÁC ENTRY (Ô NHẬP) THEO TÊN CỘT
        entries = {}
        # HIỂN THỊ TỪNG CỘT DỮ LIỆU LÊN FORM (CÓ LABEL + ENTRY)
        for i, col in enumerate(self.headers):
            # Duyệt qua danh sách các cột (header)
            # i là chỉ số dòng hiển thị, col là tên cột (ví dụ "Customer Name")

            tk.Label(win, text=col).grid(row=i, column=0, sticky='w', padx=6, pady=2)
            # Tạo label hiển thị tên cột ở cột đầu tiên (bên trái)
            # sticky='w' để căn trái, padx/pady là khoảng cách mép

            e = tk.Entry(win, width=80)
            # Tạo ô nhập (Entry) để người dùng chỉnh sửa nội dung cột
            e.grid(row=i, column=1, padx=6, pady=2)
            # Đặt Entry cạnh label, ở cột thứ 2

            e.insert(0, row.get(col, ""))
            # Chèn sẵn giá trị hiện tại của cột vào ô nhập
            # Nếu cột không tồn tại, thì để chuỗi rỗng ""

            entries[col] = e
            # Lưu lại đối tượng Entry này vào dict entries để sau có thể lấy giá trị ra

        def do_save():
            # Duyệt toàn bộ các cột, lấy giá trị mới nhập và cập nhật vào row
            for col in self.headers:
                row[col] = entries[col].get()

            # Cập nhật lại dòng này vào danh sách gốc (ghi đè dòng cũ)
            self.data[idx] = row

            # Cập nhật lại bảng hiển thị Treeview để hiển thị dữ liệu mới
            self.refresh_table()

            # Đóng cửa sổ chỉnh sửa
            win.destroy()

        tk.Button(win, text="Lưu", command=do_save).grid(
            row=len(self.headers), column=0, columnspan=2, pady=8
        )
    def delete_selected_row(self):

        selected = self.treeview.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn dòng", "Vui lòng chọn một dòng để xóa.")
            return

        # --- Lấy giá trị khóa của dòng được chọn ---
        row_values = self.treeview.item(selected[0], "values")
        key_index = self.treeview["columns"].index(self.key_column)
        key_value_raw = row_values[key_index].strip()

        try:
            key_value = round(float(key_value_raw), 2)
        except:
            key_value = key_value_raw  # giữ nguyên chuỗi nếu không ép được

        if not messagebox.askyesno("Xác nhận xóa",
                                   f"Bạn có chắc muốn xóa dòng có {self.key_column} = {key_value_raw}?"):
            return

        if self.root_node:
            try:
                self.root_node = self.avl.delete(self.root_node, key_value)
            except Exception as e:
                messagebox.showerror("Lỗi AVL", f"Lỗi khi xóa node trong AVL: {e}")
                return

        # --- Cập nhật danh sách dữ liệu (dataset) ---
        new_data = []
        for r in self.data:
            val = str(r.get(self.key_column, "")).strip()
            if val != key_value_raw:
                new_data.append(r)
        self.data = new_data

        self.treeview.delete(selected[0])

        self.clear_plot()
        if self.root_node:
            self.draw_avl_tree()

        messagebox.showinfo("Hoàn tất", f"Đã xóa dòng và node có {self.key_column} = {key_value_raw}.")

    # ---------------- Tab 2 ----------------
    def create_tab2(self):
        top_frame = tk.Frame(self.tab2, height=420)
        top_frame.pack(side="top", fill="both", expand=True, padx=6, pady=6)

        # Nhúng đồ thị matplotlib (self.fig) vào frame này
        self.canvas_fig = FigureCanvasTkAgg(self.fig, master=top_frame)
        self.canvas_fig.draw()  # Vẽ khung đồ thị rỗng ban đầu
        # Cho phép vùng vẽ co giãn theo cửa sổ
        self.canvas_fig.get_tk_widget().pack(fill="both", expand=True)

        # Frame chứa các nút và kết quả (không chiếm toàn bộ chiều cao)
        bottom_frame = tk.Frame(self.tab2, height=260)
        bottom_frame.pack(side="bottom", fill="x", expand=False, padx=6, pady=6)

        # Frame con chứa các nút điều khiển, đặt ở trên cùng vùng bottom
        ctrl_frame = tk.Frame(bottom_frame)
        ctrl_frame.pack(fill="x", pady=4)

        tk.Button(ctrl_frame, text="Tạo cây AVL (Billing Amount)",
                  command=self.build_avl).pack(side="left", padx=4)

        tk.Button(ctrl_frame, text="NLR (Preorder)",
                  command=self.show_preorder).pack(side="left", padx=4)

        tk.Button(ctrl_frame, text="LNR (Inorder)",
                  command=self.show_inorder).pack(side="left", padx=4)

        tk.Button(ctrl_frame, text="LRN (Postorder)",
                  command=self.show_postorder).pack(side="left", padx=4)

        tk.Button(ctrl_frame, text="Chiều cao cây",
                  command=self.show_tree_height).pack(side="left", padx=4)

        tk.Button(ctrl_frame, text="Đếm nút lá",
                  command=self.show_leaf_count).pack(side="left", padx=4)

        tk.Label(ctrl_frame, text=" K (số tầng muốn thấy):").pack(side="left", padx=6)

        # Ô nhập giá trị K (kiểu số nguyên)
        self.k_entry = tk.Entry(ctrl_frame, width=6)
        self.k_entry.pack(side="left", padx=2)

        tk.Button(ctrl_frame, text="Vẽ tầng K",
                  command=self.draw_up_to_k).pack(side="left", padx=4)

        tk.Button(ctrl_frame, text="Xóa vẽ",
                  command=self.clear_plot).pack(side="left", padx=4)

        # Ô văn bản hiển thị kết quả đầu ra (các giá trị duyệt, thống kê,…)
        self.output_text = tk.Text(bottom_frame, height=10)
        self.output_text.pack(fill="both", expand=True, pady=6)

        #tk.Button(ctrl_frame, text="Xuất tầng K", command=self.show_nodes_at_level).pack(side="left", padx=4)
        #tk.Button(ctrl_frame, text="Tạo AVL từ top10", command=self.build_avl_top10).pack(side="left", padx=4)
        #tk.Button(ctrl_frame, text="Tải 10 dòng & AVL", command=self.load_top10_from_file).pack(side="left", padx=4)
        tk.Button(ctrl_frame, text="Tải 10 dòng & AVL", command=self.load_top10_from_file).pack(side="left", padx=4)
        tk.Button(ctrl_frame, text="Xuất node đang hiển thị", command=self.show_nodes_button_clicked).pack(side="left", padx=4)


    def draw_avl_tree(self):
        # Dọn khu vực vẽ
        self.ax.clear()
        self.ax.axis('off')

        if not self.root_node:
            # Nếu cây rỗng, chỉ vẽ ô trống và return
            self.canvas_fig.draw()
            return

        # Hàm đệ quy vẽ node và cạnh; dùng tọa độ tương đối
        def draw_node(node, x, y, dx, level):
            if node is None:
                return
            label = str(node.record.get(self.key_column, node.key)) if hasattr(node, "record") else str(node.key)
            self.ax.text(x, y, label, ha='center', va='center',
                         bbox=dict(facecolor='lightblue', edgecolor='black', boxstyle='circle'))
            if node.left:
                self.ax.plot([x, x - dx], [y, y - 1], color='black')
                draw_node(node.left, x - dx, y - 1, dx / 1.6, level + 1)
            if node.right:
                self.ax.plot([x, x + dx], [y, y - 1], color='black')
                draw_node(node.right, x + dx, y - 1, dx / 1.6, level + 1)

        draw_node(self.root_node, 0.0, 0.0, 2.0, 0)
        self.fig.tight_layout()
        self.canvas_fig.draw()


    def delete_avl_node(self):

        key_input = self.delete_entry.get().strip()
        if not key_input:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập khóa cần xóa.")
            return

        if self.root_node is None:
            messagebox.showwarning("Cảnh báo", "Cây AVL hiện đang rỗng hoặc chưa được tạo.")
            return

        deleted = False
        try:
            key_num = round(float(key_input), 2)
            self.root_node, deleted = self.avl.delete_node(self.root_node, key_num)
        except Exception:
            deleted = False

        if not deleted:
            self.root_node, deleted = self.avl.delete_node(self.root_node, key_input)

        if deleted:
            self.clear_plot()
            self.draw_avl_tree()
            messagebox.showinfo("Thành công", f"Đã xóa node có khóa '{key_input}' khỏi cây AVL.")
        else:
            messagebox.showwarning("Không tìm thấy", f"Không tìm thấy node có khóa '{key_input}' trong cây AVL.")



    def clear_plot(self):
        self.ax.clear()
        self.ax.axis('off')
        self.canvas_fig.draw()

    def build_avl(self):
        if not self.data:
            messagebox.showwarning("Chưa có dữ liệu - bấm 'Đọc file CSV' ở Tab 1")
            return

        self.root_node = None
        skipped = 0  # Biến đếm số dòng dữ liệu bị lỗi không chèn được

        # Duyệt qua từng bản ghi trong danh sách dữ liệu (self.data)
        for r in self.data:
            # Lấy giá trị khóa chính (từ cột "Billing Account")
            raw = r.get(self.key_column, "")

            try:
                # Cố gắng chuyển khóa sang dạng số (float)
                key = round(float(raw), 2)  # làm tròn 2 chữ số thập phân

            except:
                # Nếu không thể chuyển sang số, giữ nguyên dạng chuỗi
                key = str(raw)

            try:
                # Thêm node mới vào cây AVL bằng hàm insert()
                self.root_node = self.avl.insert(self.root_node, key, r)
            except Exception:
                # Nếu có lỗi trong quá trình thêm node thì bỏ qua dòng đó
                skipped += 1

        self.clear_plot()
        messagebox.showinfo("Hoàn tất", f"Đã tạo cây AVL. Bỏ qua {skipped} dòng (nếu có).")


    def show_inorder(self):
        self.output_text.delete("1.0", tk.END)
        if not self.root_node:
            self.output_text.insert(tk.END, "Cây rỗng. Vui lòng tạo cây trước.\n")
            return

        # Tạo danh sách trống để lưu kết quả duyệt theo thứ tự Inorder
        out = []
        self.avl.inorder(self.root_node, out)

        # Trích lấy khóa chính (key_column) từ từng bản ghi trong danh sách kết quả
        # rồi chuyển thành chuỗi để dễ hiển thị
        keys = [str(r.get(self.key_column, "")) for r in out]
        self.output_text.insert(tk.END, "LNR (Inorder):\n" + " → ".join(keys) + "\n")

    def show_preorder(self):
        self.output_text.delete("1.0", tk.END)
        if not self.root_node:
            self.output_text.insert(tk.END, "Cây rỗng. Vui lòng tạo cây trước.\n")
            return

        # Danh sách lưu thứ tự duyệt Preorder
        out = []
        self.avl.preorder(self.root_node, out)

        # Lấy danh sách khóa của các node (key_column) để hiển thị
        keys = [str(r.get(self.key_column, "")) for r in out]

        # Ghi kết quả vào vùng hiển thị với định dạng đẹp mắt
        self.output_text.insert(tk.END, "NLR (Preorder):\n" + " → ".join(keys) + "\n")

    def show_postorder(self):
        self.output_text.delete("1.0", tk.END)
        if not self.root_node:
            self.output_text.insert(tk.END, "Cây rỗng. Vui lòng tạo cây trước.\n")
            return
        out = []
        self.avl.postorder(self.root_node, out)
        keys = [str(r.get(self.key_column, "")) for r in out]
        self.output_text.insert(tk.END, "LRN (Postorder):\n" + " → ".join(keys) + "\n")

    def show_tree_height(self):
        self.output_text.delete("1.0", tk.END)

        if not self.root_node:
            self.output_text.insert(tk.END, "Cây rỗng.\n")
            return
        h = self.avl.tree_height(self.root_node)
        self.output_text.insert(tk.END, f"Chiều cao cây (số tầng): {h}\n")

    def show_leaf_count(self):
        self.output_text.delete("1.0", tk.END)
        if not self.root_node:
            self.output_text.insert(tk.END, "Cây rỗng.\n")
            return
        cnt = self.avl.count_leaves(self.root_node)
        self.output_text.insert(tk.END, f"Số nút lá: {cnt}\n")

    def draw_up_to_k(self):
        if not self.root_node:
            messagebox.showwarning("Cây rỗng", "Tạo cây AVL trước khi vẽ.")
            return

        s = self.k_entry.get().strip()
        if not s:
            messagebox.showwarning("Nhập tầng K")
            return
        try:
            K = int(s)
            if K < 0:
                raise ValueError
        except:
            messagebox.showerror("K phải là số nguyên >= 0")
            return

        # BFS: chỉ lấy node ở tầng K
        q = deque()
        q.append((self.root_node, 0))
        nodes_at_k = []
        depths = {}
        while q:
            node, depth = q.popleft()
            depths[node] = depth
            if depth == K:
                nodes_at_k.append(node)
            elif depth < K:
                if node.left: q.append((node.left, depth + 1))
                if node.right: q.append((node.right, depth + 1))

        if not nodes_at_k:
            messagebox.showinfo("Thông báo", f"Không có node nào ở tầng {K}.")
            return

        # Xác định vị trí x chuẩn (theo Inorder) cho toàn bộ cây
        positions = {}
        cnt = 0

        def assign_x(node):
            nonlocal cnt
            if not node:
                return
            assign_x(node.left)
            positions[node] = {"x": cnt}
            cnt += 1
            assign_x(node.right)

        assign_x(self.root_node)

        # Chuẩn hóa tọa độ node tầng K
        minx = min(positions[n]['x'] for n in nodes_at_k)
        maxx = max(positions[n]['x'] for n in nodes_at_k)
        span = max(1, maxx - minx + 1)
        for n in nodes_at_k:
            positions[n]['sx'] = (positions[n]['x'] - minx) / span
            positions[n]['sy'] = -depths[n]

        # Xóa plot cũ
        self.ax.clear()
        self.ax.axis('off')

        # Vẽ node tầng K
        for n in nodes_at_k:
            sx, sy = positions[n]['sx'], positions[n]['sy']
            self.ax.text(sx, sy, str(n.key), ha='center', va='center',
                         bbox=dict(boxstyle='round', facecolor='#8fd18f', edgecolor='green'))

        self.ax.set_xlim(-0.05, 1.05)
        miny = min(positions[n]['sy'] for n in nodes_at_k)
        self.ax.set_ylim(miny - 0.5, 0.5)
        self.canvas_fig.draw()

        # Xuất ra output_text tối đa 10 node
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, f"Nodes ở tầng {K} (tối đa 10 node):\n")
        for i, n in enumerate(nodes_at_k):
            if i >= 10:
                break
            self.output_text.insert(tk.END, f"{n.key}\n")

    def load_top10_from_file(self):
        """Mở CSV, lấy 10 dòng đầu, build AVL và xuất node ra output_text"""
        path = filedialog.askopenfilename(
            title="Chọn file CSV",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return

        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.headers = reader.fieldnames if reader.fieldnames else []
                self.data = []
                for i, row in enumerate(reader):
                    if i >= 10:
                        break
                    self.data.append(row)

            if not self.headers:
                messagebox.showwarning("File rỗng hoặc không đúng định dạng CSV.")
                return

            # Chọn khóa chính
            if self.key_column not in self.headers:
                if "Billing Amount" in self.headers:
                    self.key_column = "Billing Amount"
                else:
                    self.key_column = self.headers[0]

            self.refresh_table()

            # Tạo AVL từ 10 dòng
            self.root_node = None
            for r in self.data:
                raw = r.get(self.key_column, "")
                try:
                    key = round(float(raw), 2)
                except:
                    key = str(raw)
                self.root_node = self.avl.insert(self.root_node, key, r)

            self.clear_plot()
            self.draw_avl_tree()

            # Xuất các node ra output_text
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Đã load {len(self.data)} dòng đầu và tạo AVL:\n")
            for n, r in enumerate(self.data):
                if n >= 10:
                    break
                self.output_text.insert(tk.END, f"{r}\n")

            messagebox.showinfo("Hoàn tất", f"Đã tải {len(self.data)} dòng đầu từ file và tạo AVL.")

        except Exception as e:
            messagebox.showerror("Lỗi đọc file", str(e))

    def load_csv_to_avl(self, file_path, key_index=0):
        self.root_node = None
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                key = row[key_index]
                self.root_node = self.avl.insert(self.root_node, key, row)

    def show_nodes_button_clicked(self):
        if not self.root_node:
            messagebox.showwarning("Cây rỗng", "Tạo cây AVL trước khi xuất node.")
            return

        s = self.k_entry.get().strip()
        if not s:
            messagebox.showwarning("Nhập tầng K")
            return
        try:
            K = int(s)
            if K < 0:
                raise ValueError
        except:
            messagebox.showerror("K phải là số nguyên >= 0")
            return

        # BFS lấy node chỉ ở tầng K
        q = deque()
        q.append((self.root_node, 0))
        nodes_at_k = []
        while q:
            node, depth = q.popleft()
            if depth == K:
                nodes_at_k.append(node)
            elif depth < K:
                if node.left: q.append((node.left, depth + 1))
                if node.right: q.append((node.right, depth + 1))

        # Xóa output_text cũ
        self.output_text.delete("1.0", tk.END)

        if not nodes_at_k:
            self.output_text.insert(tk.END, f"Không có node nào ở tầng {K}.\n")
            return

        self.output_text.insert(tk.END, f"Nodes ở tầng {K} (tối đa 10 node):\n")
        for i, n in enumerate(nodes_at_k):
            if i >= 10:  # giới hạn 10 node
                break
            self.output_text.insert(tk.END, f"{n.key}\n")
