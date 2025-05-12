import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from cefpython3 import cefpython as cef
import sys
import os

from data_processor import DataProcessor
from visualizer import Visualizer

class GeoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Geoespacial Interativo")
        self.root.geometry("1000x700")

        self.processor = DataProcessor()

        self.setup_ui()

    def setup_ui(self):
        control_frame = tk.Frame(self.root, padx=10, pady=10)
        control_frame.pack(fill=tk.X)

        tk.Button(control_frame, text="Carregar CSV", command=lambda: self.load_file("csv")).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Carregar JSON", command=lambda: self.load_file("json")).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Carregar XML", command=lambda: self.load_file("xml")).pack(side=tk.LEFT, padx=5)

        self.browser_frame = tk.Frame(self.root, height=500)
        self.browser_frame.pack(fill=tk.BOTH, expand=True)

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

    def load_file(self, file_type):
        filetypes = {
            "csv": ("Arquivos CSV", "*.csv"),
            "json": ("Arquivos GeoJSON", "*.json"),
            "xml": ("Arquivos XML", "*.xml")
        }

        try:
            file_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[filetypes[file_type]])
            if not file_path:
                return

            if file_type == "csv":
                self.processor.load_csv(file_path)
            elif file_type == "json":
                self.processor.load_json(file_path)
            elif file_type == "xml":
                self.processor.load_xml(file_path)

            gdf = self.processor.get_data()

            html_path = Visualizer.plot_folium(gdf)

            self.embed_map(html_path)
            self.display_table(gdf)

        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar arquivo:\n{str(e)}")

    def embed_map(self, filepath):
        for widget in self.browser_frame.winfo_children():
            widget.destroy()

        window_info = cef.WindowInfo()
        window_info.SetAsChild(self.browser_frame.winfo_id(), [0, 0, 1000, 500])
        cef.CreateBrowserSync(window_info, url="file://" + filepath)
        self.browser_frame.update()

    def display_table(self, gdf):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(self.table_frame)
        tree["columns"] = list(gdf.columns)
        tree["show"] = "headings"

        for col in gdf.columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="w")

        for _, row in gdf.iterrows():
            values = [str(row[col]) for col in gdf.columns]
            tree.insert("", "end", values=values)

        tree.pack(fill=tk.BOTH, expand=True)

def main():
    sys.excepthook = cef.ExceptHook
    cef.Initialize()

    root = tk.Tk()
    app = GeoApp(root)

    def loop():
        cef.MessageLoopWork()
        root.after(10, loop)

    root.after(10, loop)
    root.mainloop()
    cef.Shutdown()

if __name__ == "__main__":
    main()