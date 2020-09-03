import tkinter as tk
from tkinter import filedialog, messagebox
import calculator.main
from gui.parameters_panel import ParametersPanel
import logging


class ApplicationGUI(tk.Frame):
    """
    The graphical user interface.
    Run this file to start the app.
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parameters = dict()
        self.load_from_init_file()

        self.grid(padx=(10, 10), pady=(10, 10))

        self.app_font = ('helvetica', 16, 'bold')

        self.excel_text = tk.StringVar()
        self.excel_text.set('Excel Datei:')

        self.drawings_text = tk.StringVar()
        self.drawings_text.set('Pfad zu .GEO/.DXF Dateien')

        self.parent = parent
        self.parent.title('Kostenrechner')
        self.parent.columnconfigure(0, weight=1)

        self.excel_path = tk.StringVar()
        self.excel_path.set('')

        self.drawings_path = tk.StringVar()
        self.drawings_path.set('')

        self.cost_result = tk.StringVar()
        self.cost_result.set('')

        self.offset = tk.StringVar()
        value = self.parameters.get('Offset', 0)
        self.offset.set(value)

        self.material_cost_per_t = tk.StringVar()
        value = self.parameters.get('Materialkosten_euro_t', 0)
        self.material_cost_per_t.set(value)

        self.schnittgeschwindigkeit_mm_s = tk.StringVar()
        value = self.parameters.get('Schnittgeschwindigkeit_mm_s', 0)
        self.schnittgeschwindigkeit_mm_s.set(value)

        self.kosten_schnitt_euro_min = tk.StringVar()
        value = self.parameters.get('Kosten_Schnitt_euro_min', 0)
        self.kosten_schnitt_euro_min.set(value)

        self.materialgewicht_g_cm3 = tk.StringVar()
        value = self.parameters.get('Materialgewicht_g_cm3', 0)
        self.materialgewicht_g_cm3.set(value)

        self.gewinnmarge = tk.StringVar()
        value = self.parameters.get('Gewinnmarge')
        self.gewinnmarge.set(value)

        self.excel_ausgabespalte = tk.StringVar()
        value = self.parameters.get('Ausgabespalte', 'H')
        self.excel_ausgabespalte.set(value)

        self.excel_first_row = tk.StringVar()
        value = self.parameters.get('Nr_erste_Reihe_Daten', 3)
        self.excel_first_row.set(int(value))

        self.std_dicke_mm = tk.StringVar()
        value = '---'
        self.std_dicke_mm.set(value)

        self.use_excel = tk.IntVar()
        self.use_excel.set(1)

        # Excel file input
        checkbox = tk.Checkbutton(self, text='Excel Datei benutzen', variable=self.use_excel, onvalue=1, offvalue=0,
                                  fg='black', font=self.app_font, command=self.eval_checkbox)
        checkbox.grid(row=0, column=0, sticky='E')

        self.label_excel_path = tk.Label(self, textvariable=self.excel_text, fg='black', font=self.app_font)
        self.label_excel_path.grid(row=0, column=0, sticky='W')

        self.entry_excel_path = tk.Entry(self, width=65, textvariable=self.excel_path)
        self.entry_excel_path.focus()
        self.entry_excel_path.grid(row=1, column=0, sticky='W')

        self.button_open_filedialog_excel = tk.Button(self, text='Durchsuchen', command=self.open_filedialog_excel, bg='grey', fg='black', activebackground='azure3', font=self.app_font)
        self.button_open_filedialog_excel.grid(row=1, column=0, sticky='E')

        # Drawings path input
        self.label_drawings_path = tk.Label(self, textvariable=self.drawings_text, fg='black', font=self.app_font)
        self.label_drawings_path.grid(row=2, column=0, sticky='W', pady=(8, 0))

        self.entry_drawings_path = tk.Entry(self, width=65, textvariable=self.drawings_path)
        self.entry_drawings_path.grid(row=3, column=0, sticky='W')

        self.button_open_filedialog_drawings = tk.Button(self, text='Durchsuchen', command=self.open_filedialog_drawings, bg='grey', fg='black', activebackground='azure3', font=self.app_font)
        self.button_open_filedialog_drawings.grid(row=3, column=0, sticky='E')

        self.parameters_panel = ParametersPanel(self)

        # Buttons frame
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=7, column=0, pady=(10, 10))
        self.buttons_frame.columnconfigure(1, weight=1)

        self.button_close = tk.Button(self.buttons_frame, text='Beenden', command=self.close, bg='grey', fg='black', activebackground='azure3', font=self.app_font)
        self.button_close.grid(row=0, column=0, padx=(10, 10))

        self.button_compute = tk.Button(self.buttons_frame, text='Berechnen', command=self.calculate, bg='grey', fg='black', activebackground='azure3', font=self.app_font)
        self.button_compute.grid(row=0, column=2, padx=(10, 10))

        #
        self.label_result = tk.Label(self, textvariable=self.cost_result, fg='black', font=self.app_font)
        self.label_result.grid(row=6, column=0, pady=(30, 3))

    def open_filedialog_drawings(self):
        selected = self.use_excel.get()

        if selected:
            filename = tk.filedialog.askdirectory(initialdir="/", title="Verzeichnis auswählen")
            self.drawings_path.set(filename)
        else:
            filename = tk.filedialog.askopenfilename(initialdir="/", title="Datei auswählen", filetypes=(("Alle Dateien", "*"),))
            self.drawings_path.set(filename)

    def open_filedialog_excel(self):
        filename = tk.filedialog.askopenfilename(initialdir="/", title="Datei auswählen", filetypes=(("Excel Dateien", "*.xlsx"),))
        self.excel_path.set(filename)

    def calculate(self):
        error = self.parameters_panel.update_parameters()
        if error:
            return

        selected = self.use_excel.get()

        try:
            if selected:
                result = calculator.main.calculate(self.parameters, self.drawings_path.get(), self.excel_path.get())
            else:
                try:
                    float(self.std_dicke_mm.get())
                except ValueError:
                    raise ValueError('Bitte eine Zahl für die Dicke in mm eingeben.')
                result = calculator.main.calculate(self.parameters, self.drawings_path.get())

            cost = format(result, '.2f') + '€'
            msg = f'Berechnete Gesamtkosten: {cost}'
            self.cost_result.set(msg)
        except Exception as e:
            logging.error(e)
            messagebox.showerror('Berechnung abgebrochen!', f'Ein Fehler ist aufgetreten: {e}')

    def eval_checkbox(self):
        selected = self.use_excel.get()

        if selected:
            self.entry_excel_path.grid(row=1, column=0, sticky='W')
            self.button_open_filedialog_excel.grid(row=1, column=0, sticky='E')
            self.excel_text.set('Excel Datei:')
            self.drawings_text.set('Pfad zu .GEO/.DXF Dateien')
            self.entry_excel_path.focus()
            self.drawings_path.set('')
            self.std_dicke_mm.set('---')
        else:
            self.entry_excel_path.grid_remove()
            self.button_open_filedialog_excel.grid_remove()
            self.excel_text.set('Ohne Excel Datei')
            self.drawings_text.set('Einzelne .GEO/.DXF Datei auswählen:')
            self.entry_drawings_path.focus()
            self.drawings_path.set('')
            self.std_dicke_mm.set(self.parameters.get('Std_Dicke_mm', 20.0))

    def load_from_init_file(self):
        """
        Loads the values from the init file into a dictionary.
        The init file must be a textfile containing key=value pairs.
        """
        with open('./init.txt') as init_file:
            lines = init_file.readlines()
            for line in lines:
                if line.startswith('#'):
                    # skip comments
                    continue
                line = line.strip()
                key, value = line.split('=')
                try:
                    v = float(value)
                except:
                    v = value

                self.parameters[key] = v

    def close(self):
        self.parent.destroy()
