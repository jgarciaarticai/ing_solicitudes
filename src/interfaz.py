import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from procesamiento import DocumentProcessor
from extraccion import DocumentExporter

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Preparación de Memoria Técnica")
        self.processor = None
        self.sections = []

        # Botón para cargar el archivo
        load_button = tk.Button(root, text="Cargar Documento", command=self.load_document)
        load_button.pack(pady=10)

        # Lista para mostrar secciones
        self.sections_list = tk.Listbox(root, selectmode=tk.MULTIPLE, width=80, height=10)
        self.sections_list.pack(pady=10)

        # Botón para exportar
        export_button = tk.Button(root, text="Exportar Secciones Seleccionadas", command=self.export_selected_sections)
        export_button.pack(pady=10)

    def load_document(self):
        """Permite al usuario cargar un documento Word y procesa las secciones."""
        file_path = filedialog.askopenfilename(filetypes=[("Word files", "*.docx")])
        if not file_path:
            return

        self.processor = DocumentProcessor(file_path)
        self.processor.load_document()

        # Aquí se define un conjunto de palabras clave, aunque podrían configurarse
        keywords = ["OBRA CIVIL"]  # Reemplazar por palabras clave adecuadas
        self.processor.identify_sections(keywords)
        self.sections = self.processor.get_sections()

        self.populate_sections_list()

    def populate_sections_list(self):
        """Llena la lista de secciones para que el usuario las revise."""
        self.sections_list.delete(0, tk.END)
        for i, section in enumerate(self.sections):
            self.sections_list.insert(tk.END, f"Sección {i + 1}")

    def export_selected_sections(self):
        """Exporta las secciones seleccionadas en la lista."""
        selected_indices = self.sections_list.curselection()
        selected_sections = [self.sections[i] for i in selected_indices]

        if not selected_sections:
            messagebox.showwarning("Advertencia", "No se han seleccionado secciones para exportar.")
            return

        exporter = DocumentExporter(selected_sections)
        exporter.export_sections()

        messagebox.showinfo("Exportación Completa", "Secciones exportadas con éxito.")

# Inicializar la aplicación
root = tk.Tk()
app = Application(root)
root.mainloop()
