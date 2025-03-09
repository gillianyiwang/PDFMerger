import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
from PIL import Image, ImageTk


class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("650x550")
        self.root.resizable(True, True)
        self.center_window(650, 550)

        self.file_list = []

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.instruction_label = tk.Label(
            root, text="👆👇 Drag files around to adjust the order", font=("Arial", 14)
        )
        self.instruction_label.pack(pady=5)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(
            self.frame,
            selectmode=tk.SINGLE,
            width=60,
            height=15,
            yscrollcommand=self.scrollbar.set,
        )
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.bind("<B1-Motion>", self.drag_item)
        self.listbox.bind("<ButtonRelease-1>", self.drop_item)

        self.add_button = tk.Button(
            root, text="Add PDFs", command=self.add_files, height=1
        )
        self.add_button.pack(pady=2)

        self.remove_button = tk.Button(
            root, text="Remove Selected", command=self.remove_selected, height=1
        )
        self.remove_button.pack(pady=2)

        self.merge_button = tk.Button(
            root, text="Merge PDFs", command=self.merge_pdfs, height=1
        )
        self.merge_button.pack(pady=10)

        self.version_label = tk.Label(root, text="Version 1.0.0", font=("Arial", 10))
        self.version_label.place(x=600, y=530, anchor='se')  # Positioning it at the bottom right

        self.dragged_item = None

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def add_files(self):
        self.root.attributes("-topmost", False)
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        self.root.lift()
        for file in files:
            if file not in self.file_list:
                self.file_list.append(file)
                self.listbox.insert(tk.END, file)

    def drag_item(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.dragged_item = selected_index[0]

    def drop_item(self, event):
        if self.dragged_item is not None:
            new_index = self.listbox.nearest(event.y)
            self.file_list.insert(new_index, self.file_list.pop(self.dragged_item))
            self.listbox.delete(0, tk.END)
            for file in self.file_list:
                self.listbox.insert(tk.END, file)
            self.listbox.select_set(new_index)
            self.dragged_item = None

    def remove_selected(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.file_list[index]
            self.listbox.delete(index)

    def merge_pdfs(self):
        if not self.file_list:
            messagebox.showerror("Error", "No PDF files selected.")
            return

        self.root.attributes("-topmost", False)
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
        )
        self.root.lift()  # Bring main window back to front

        if not output_path:
            return

        merger = PdfMerger()
        for pdf in self.file_list:
            merger.append(pdf)

        merger.write(output_path)
        merger.close()

        self.root.lift()  # Ensure success message is visible
        messagebox.showinfo("Success", "PDFs merged successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
