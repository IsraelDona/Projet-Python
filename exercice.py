
#Notre Projet
import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from tkinter import *
import datetime
from tkinter.simpledialog import askstring
root = tk.Tk()
class FileExplorer:
    def __init__(self, root):
        """Initialisation"""
        self.root = root
        self.root.title("Explorateur de Fichiers")
        self.root.geometry("900x600")
        self.current_path = os.getcwd()
        self.favorites = set()

        self.create_sidebar()
        self.create_main_area()
        self.load_directory(self.current_path)

    def create_sidebar(self):
        """Créer la barre latérale"""
        sidebar = tk.Frame(self.root, width=200)
        sidebar.pack(fill=tk.Y, side=tk.LEFT)

        sections = ["Recents", "Favoris", "Ordinateur", "Tags", "Accueil", "Images", "Téléchargements", "Musique", "Disque Local C", "Disque Local D"]
        for section in sections:
            btn = tk.Button(sidebar, text=section, relief=tk.FLAT, anchor="w", padx=10,
                            command=lambda sec=section: self.change_directory(sec))
            btn.pack(fill=tk.X, pady=2)

    def create_main_area(self):
        """Créer la zone principale"""
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Barre de chemin
        self.path_entry = tk.Entry(main_frame, bd=2)
        self.path_entry.pack(fill=tk.X, padx=5, pady=5)
        self.path_entry.insert(0, self.current_path)

        # Recherche
        search_frame = tk.Frame(main_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        self.search_entry = tk.Entry(search_frame, bd=2)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(search_frame, text="Rechercher", command=self.search_files).pack(side=tk.RIGHT)

        # Table des fichiers
        self.tree = ttk.Treeview(main_frame, columns=("Nom", "Taille", "Type", "Date"), show="headings", style="Treeview")
        for col in ("Nom", "Taille", "Type", "Date"):
            self.tree.heading(col, text=col, anchor="w")
            self.tree.column(col, width=150)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Boutons
        frame_buttons = tk.Frame(main_frame)
        frame_buttons.pack(fill=tk.X)
        tk.Button(frame_buttons, text="Actualiser", command=self.refresh).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_buttons, text="Créer dossier", command=self.create_folder).pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(frame_buttons, text="Créer fichier", command=self.create_file).pack(side=tk.LEFT, padx=5, pady=5)

        # Bindings
        self.tree.bind("<Double-1>", self.open_item)
        self.tree.bind("<Button-3>", self.show_context_menu)

        # Menu contextuel
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Ouvrir", command=self.open_item)
        self.context_menu.add_command(label="Renommer", command=self.rename_item)
        self.context_menu.add_command(label="Supprimer", command=self.delete_item)
        self.context_menu.add_command(label="Ajouter aux Favoris", command=self.add_to_favorites)

    def load_directory(self, path):
        """Charger les fichiers/dossiers"""
        self.tree.delete(*self.tree.get_children())
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(0, path)

        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                size = os.path.getsize(full_path)
                date = datetime.datetime.fromtimestamp(os.path.getmtime(full_path)).strftime("%Y-%m-%d %H:%M")
                type_item = "Dossier" if os.path.isdir(full_path) else "Fichier"

                self.tree.insert("", "end", values=(item, f"{size} octets", type_item, date))
        except PermissionError:
            messagebox.showerror("Erreur", "Accès refusé à ce dossier.")

    def change_directory(self, section):
        """Changer le répertoire à la sélection"""
        if section == "Ordinateur":
            self.load_directory("C:/")
        elif section == "Images":
            self.load_directory("C:/Users/Public/Pictures")
        elif section == "Téléchargements":
            self.load_directory("C:/Users/Public/Downloads")
        elif section == "Musique":
            self.load_directory("C:/Users/Public/Music")
        elif section == "Disque Local C":
            self.load_directory("C:/")
        elif section == "Disque Local D":
            self.load_directory("D:/")
        else:
            self.load_directory(self.current_path)

    def open_item(self, event=None):
        """Ouvrir un dossier ou un fichier"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_name = self.tree.item(selected_item, "values")[0]
        new_path = os.path.join(self.current_path, item_name)

        if os.path.isdir(new_path):
            self.current_path = new_path
            self.load_directory(new_path)
        else:
            os.startfile(new_path)  # Ouvrir le fichier avec l'application par défaut

    def rename_item(self):
        """Renommer un fichier ou un dossier"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_name = self.tree.item(selected_item, "values")[0]
        old_path = os.path.join(self.current_path, item_name)

        new_name = askstring("Renommer", f"Renommer {item_name} en :")
        if new_name:
            new_path = os.path.join(self.current_path, new_name)
            os.rename(old_path, new_path)
            self.refresh()

    def delete_item(self):
        """Supprimer un fichier ou un dossier"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_name = self.tree.item(selected_item, "values")[0]
        path = os.path.join(self.current_path, item_name)

        if messagebox.askyesno("Confirmation", f"Supprimer {item_name} ?"):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
            self.refresh()

    def create_folder(self):
        """Créer un nouveau dossier"""
        new_folder = filedialog.askstring("Créer dossier", "Nom du dossier :")
        if new_folder:
            os.mkdir(os.path.join(self.current_path, new_folder))
            self.refresh()

    def create_file(self):
        """Créer un fichier vide"""
        new_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])
        if new_file:
            with open(new_file, 'w') as file:
                file.write("")  # Créer un fichier vide
            self.refresh()

    def show_context_menu(self, event):
        """Afficher le menu contextuel"""
        selected_item = self.tree.selection()
        if selected_item:
            self.context_menu.post(event.x_root, event.y_root)

    def refresh(self):
        """Rafraîchir l'affichage"""
        self.load_directory(self.current_path)

    def add_to_favorites(self):
        """Ajouter un élément aux favoris"""
        selected_item = self.tree.selection()
        if selected_item:
            item_name = self.tree.item(selected_item, "values")[0]
            full_path = os.path.join(self.current_path, item_name)
            self.favorites.add(full_path)

    def show_favorites(self):
        """Afficher les favoris"""
        self.tree.delete(*self.tree.get_children())
        for path in self.favorites:
            item_name = os.path.basename(path)
            type_item = "Dossier" if os.path.isdir(path) else "Fichier"
            self.tree.insert("", "end", values=(item_name, "", type_item, ""))

    def search_files(self):
        """Rechercher un fichier"""
        query = self.search_entry.get().lower()
        if not query:
            return

        self.tree.delete(*self.tree.get_children())
        for item in os.listdir(self.current_path):
            if query in item.lower():
                self.tree.insert("", "end", values=(item, "", "Fichier/Dossier", ""))

# Lancement de l'application
root.title("Explorateur")
app = FileExplorer(root)
root.mainloop()
