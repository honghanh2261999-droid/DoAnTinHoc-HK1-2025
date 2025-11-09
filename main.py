import tkinter as tk
from healthcare_gui import HealthcareAVLApp
from avl_tree import AVLTree
if __name__ == "__main__":
    root = tk.Tk()
    app = HealthcareAVLApp(root)
    root.mainloop()
