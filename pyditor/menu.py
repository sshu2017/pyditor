import tkinter as tk
from tkinter import messagebox, filedialog
import os


class MenuHandler:
    def __init__(self, root):
        self.root = root
        self.current_file = None
        self.text_widget = None

    def set_text_widget(self, text_widget):
        self.text_widget = text_widget

    def new_file(self):
        if self.text_widget:
            if self.text_widget.get("1.0", tk.END).strip():
                response = messagebox.askokcancel(
                    "Confirm",
                    "Unsaved changes will be lost. \
                                                  Click OK to Save it now or Cancel to discard.",
                )
                if response:
                    self.save_file()
                else:
                    self.text_widget.delete("1.0", tk.END)

            self.text_widget.delete("1.0", tk.END)
            self.current_file = None
            self.root.title("Untitled - Pyditor")
        else:
            messagebox.showinfo("Info", "No text widget set.")

    def save_file(self):
        """if current_file set, overwrite it. Otherwise ask for filename."""
        if not self.text_widget:
            messagebox.showinfo("Info", "No text widget set.")
            return

        if self.current_file:
            try:
                with open(self.current_file, "w", encoding="utf-8") as file:
                    file.write(self.text_widget.get("1.0", tk.END))
                messagebox.showinfo("Saved", f"File saved: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
        else:
            path = filedialog.asksaveasfilename(
                defaultextension=".py",
                filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
            )
            if path:
                try:
                    with open(path, "w") as file:
                        file.write(self.text_widget.get("1.0", tk.END))
                    self.current_file = path
                    self.root.title(f"{os.path.basename(path)} - Text Editor")
                    messagebox.showinfo("Success", f"File saved: {path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {e}")


def create_menu(root):
    menu_handler = MenuHandler(root)
    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Start Over", command=menu_handler.new_file)
    file_menu.add_command(label="Save", command=menu_handler.save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    root.config(menu=menubar)
    return menu_handler
