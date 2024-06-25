## Written by TomCrey (tom.crey@ibs.fr)
"""
Program allowing to set up a graphical interface for the MemBrain pipeline

Features:
- Import tomograms to segment
- Import model for segmentation
- Run Prediction
"""

import tkinter as tk
from tkinter import messagebox, filedialog, Menu, Label, Button, ttk
import subprocess

class MemBrain_pipeline:

    def __init__(self, master):
        # Initialize application with main window as parameter
        self.master = master
        self.master.title("MemBrain - setup")
        self.create_widgets()
        self.create_menu()
        self.tomo_files = []
        self.model_files = []
        self.master.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        # Method to create user interface widgets
        self.create_title_label()
        self.create_tabs()

    def create_title_label(self):
        # Method to create the title label
        title_label = Label(self.master, text="MemBrain - SETUP", font=('Helvetica', 14, 'bold'), background='chartreuse2', foreground='white', pady=10, padx=10)
        title_label.grid(row=0, column=0, columnspan=2, sticky="ew")
        title_label.config(wraplength=500)
        tk.Label(self.master, text="").grid(row=1, column=0, columnspan=2, sticky="nsew")

    def create_tabs(self):
        # Method to create the tab for different actions
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=2, column=0, columnspan=3, rowspan=7, sticky="nsew")

        self.main_tab = tk.Frame(self.notebook)
        self.notebook.add(self.main_tab, text="MemBrain - pipeline")
        self.main_tab.grid_rowconfigure(0, weight=5)
        self.main_tab.grid_columnconfigure(0, weight=1)

        # List of buttons and their associated functions
        buttons_MemBrain = [
            ("Import Tomograms to segment", self.import_tomo),
            ("Import Model PATH", self.import_model_PATH),
            ("Segment with MemBrain", self.run_prediction),
        ]

        for i, (button_text, command) in enumerate(buttons_MemBrain):
            Button(self.main_tab, text=button_text, command=command,  font=('Helvetica', 10), padx=10, pady=5).grid(row=i+3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        # Labels to display selected tomograms and model
        self.odd_label = Label(self.main_tab, text="Tomograms Selected: ")
        self.odd_label.grid(row=len(buttons_MemBrain) + 4, column=0, columnspan=2)
        self.model_label = Label(self.main_tab, text="Model Selected: ")
        self.model_label.grid(row=len(buttons_MemBrain) + 5, column=0, columnspan=2)

    def on_resize(self, event):
        # Method called when resizing the window
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def create_menu(self):
        # Method to create the application menu
        menubar = Menu(self.master)
        about_menu = Menu(menubar, tearoff=0)
        about_menu.add_command(label="À propos", command=self.show_about)
        menubar.add_cascade(label="À propos", menu=about_menu)
        self.master.config(menu=menubar)

    def show_about(self):
        # Method to show "About" information in a dialog box
        about_text = '''Cette interface graphique a pour objectif de vous aider à configurer MemBrain. Elle a été réalisée par Tom CREY, stagiaire M1 à l'IBS et au LPCV.'''
        messagebox.showinfo("À propos", about_text)

    def import_tomo(self):
        # Method to import the tomogram to segment
        files = filedialog.askopenfilenames(title="Sélectionner le tomogramme à segmenter", filetypes=[("All files", "*.*")])
        if files:
            self.tomo_files = files
            self.odd_label.config(text=f"Tomogram Selected: {', '.join(files)}")

    def import_model_PATH(self):
        # Method to import the model
        files = filedialog.askopenfilenames(title="Sélectionner le modèle", filetypes=[("All files", "*.*")])
        if files:
            self.model_files = files
            self.model_label.config(text=f"Model Selected: {', '.join(files)}")

    def run_prediction(self):
        # Method to execute the prediction
        if self.tomo_files and self.model_files:
            tomo_path = " ".join(self.tomo_files)
            model_path = " ".join(self.model_files)
            subprocess.run(["membrain", "segment", "--tomogram-path", tomo_path, "--ckpt-path", model_path, "--store-connected-components"])
            print("Segmentation completed successfully.")

def main():
    # Create application instance
    root = tk.Tk()
    app = MemBrain_pipeline(root)

    # Start GUI main loop
    root.mainloop()

if __name__ == "__main__":
    main()
