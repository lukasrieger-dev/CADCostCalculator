import logging
import datetime
import tkinter as tk
import tkinter.filedialog
from calculator.start import run


class CustomButton(tk.Button):
    def __init__(self, parent, *args, **kwargs):
        tk.Button.__init__(self, parent, *args, **kwargs)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(bg='green')
        self.grid()
        self.update_idletasks()
        print('On_Enter')

    def on_leave(self, e):
        self.configure(bg='white')
        self.grid()
        print('On_Leave')


class ParametersPanel:
    def __init__(self, parent):
        entry_width = 5

        parameters_frame = tk.Frame(parent)
        parameters_frame.grid(row=5, column=0, pady=(20, 10))

        label_title = tk.Label(parameters_frame, text='Parameter', fg='black', font=parent.app_font)
        label_title.grid(row=0, column=0, sticky='W', pady=(5, 5))

        label_offset = tk.Label(parameters_frame, text='Offset [mm]:', fg='black', font=parent.app_font)
        label_offset.grid(row=1, column=0, sticky='W')

        entry_offset = tk.Entry(parameters_frame, textvariable=parent.offset, font=parent.app_font, width=entry_width)
        entry_offset.grid(row=1, column=1, sticky='W')

        label_material_cost = tk.Label(parameters_frame, text='Materialkosten [€/t]:', font=parent.app_font)
        label_material_cost.grid(row=1, column=2, padx=(10, 0), sticky='W')

        entry_material_cost = tk.Entry(parameters_frame, textvariable=parent.material_cost_per_t, font=parent.app_font, width=entry_width)
        entry_material_cost.grid(row=1, column=3, sticky='W')

        label_schnittgeschwindigkeit_mm_s = tk.Label(parameters_frame, text='Schnittgeschw. [mm/s]:', font=parent.app_font)
        label_schnittgeschwindigkeit_mm_s.grid(row=1, column=4, padx=(10, 0), sticky='W')

        entry_schnittgeschwindigkeit_mm_s = tk.Entry(parameters_frame, textvariable=parent.schnittgeschwindigkeit_mm_s, font=parent.app_font, width=entry_width)
        entry_schnittgeschwindigkeit_mm_s.grid(row=1, column=5, sticky='W')

        label_kosten_schnitt_euro_min = tk.Label(parameters_frame, text='Schnittkosten [€/min]:', font=parent.app_font)
        label_kosten_schnitt_euro_min.grid(row=2, column=0, sticky='W')

        entry_kosten_schnitt_euro_min = tk.Entry(parameters_frame, textvariable=parent.kosten_schnitt_euro_min, font=parent.app_font, width=entry_width)
        entry_kosten_schnitt_euro_min.grid(row=2, column=1, sticky='W')

        label_materialgewicht_g_cm3 = tk.Label(parameters_frame, text='Materialgew. [g/cm3]:', font=parent.app_font)
        label_materialgewicht_g_cm3.grid(row=2, column=2, padx=(10, 0), sticky='W')

        entry_materialgewicht_g_cm3 = tk.Entry(parameters_frame, textvariable=parent.materialgewicht_g_cm3, font=parent.app_font, width=entry_width)
        entry_materialgewicht_g_cm3.grid(row=2, column=3, sticky='W')

        label_gewinnmarge = tk.Label(parameters_frame, text='Gewinnmarge [>1.0]:', font=parent.app_font)
        label_gewinnmarge.grid(row=2, column=4, padx=(10, 0), sticky='W')

        entry_gewinnmarge = tk.Entry(parameters_frame, textvariable=parent.gewinnmarge, font=parent.app_font, width=entry_width)
        entry_gewinnmarge.grid(row=2, column=5, sticky='W')

        label_excel_ausgabespalte = tk.Label(parameters_frame, text='Ausgabespalte:', font=parent.app_font)
        label_excel_ausgabespalte.grid(row=3, column=0, sticky='W')

        entry_excel_ausgabespalte = tk.Entry(parameters_frame, textvariable=parent.excel_ausgabespalte, font=parent.app_font, width=entry_width)
        entry_excel_ausgabespalte.grid(row=3, column=1, sticky='W')

        label_excel_first_row = tk.Label(parameters_frame, text='Erste Zeile:', font=parent.app_font)
        label_excel_first_row.grid(row=3, column=2, padx=(10, 0), sticky='W')

        entry_excel_first_row = tk.Entry(parameters_frame, textvariable=parent.excel_first_row, font=parent.app_font, width=entry_width)
        entry_excel_first_row.grid(row=3, column=3, sticky='W')


class MainApplication(tk.Frame):
    """
    The graphical user interface.
    Run this file to start the app.
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
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
        self.offset.set('7')

        self.material_cost_per_t = tk.StringVar()
        self.material_cost_per_t.set('650')

        self.schnittgeschwindigkeit_mm_s = tk.StringVar()
        self.schnittgeschwindigkeit_mm_s.set('50')

        self.kosten_schnitt_euro_min = tk.StringVar()
        self.kosten_schnitt_euro_min.set('0.25')

        self.materialgewicht_g_cm3 = tk.StringVar()
        self.materialgewicht_g_cm3.set('7.9')

        self.gewinnmarge = tk.StringVar()
        self.gewinnmarge.set('1.4')

        self.excel_ausgabespalte = tk.StringVar()
        self.excel_ausgabespalte.set('H')

        self.excel_first_row = tk.StringVar()
        self.excel_first_row.set('3')

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

        self.button_open_filedialog_excel = CustomButton(self, text='Durchsuchen', command=self.open_filedialog_excel, bg='grey', fg='black', font=self.app_font)
        self.button_open_filedialog_excel.grid(row=1, column=0, sticky='E')

        # Drawings path input
        self.label_drawings_path = tk.Label(self, textvariable=self.drawings_text, fg='black', font=self.app_font)
        self.label_drawings_path.grid(row=2, column=0, sticky='W', pady=(8, 0))

        self.entry_drawings_path = tk.Entry(self, width=65, textvariable=self.drawings_path)
        self.entry_drawings_path.grid(row=3, column=0, sticky='W')

        self.button_open_filedialog_drawings = tk.Button(self, text='Durchsuchen', command=self.open_filedialog_drawings, bg='grey', fg='black', font=self.app_font)
        self.button_open_filedialog_drawings.grid(row=3, column=0, sticky='E')

        ParametersPanel(self)

        # Buttons frame
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=7, column=0, pady=(10, 10))
        self.buttons_frame.columnconfigure(1, weight=1)

        self.button_close = tk.Button(self.buttons_frame, text='Beenden', command=self.close, bg='grey', fg='black', font=self.app_font)
        self.button_close.grid(row=0, column=0, padx=(10, 10))

        self.button_compute = tk.Button(self.buttons_frame, text='Berechnen', command=self.compute, bg='grey', fg='black', font=self.app_font)
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
            filename = tk.filedialog.askopenfilename(initialdir="/", title="Datei auswählen", filetypes=(("DXF Dateien", "*.DXF"), ("GEO Dateien", "*.GEO")))
            self.drawings_path.set(filename)

    def open_filedialog_excel(self):
        filename = tk.filedialog.askopenfilename(initialdir="/", title="Datei auswählen", filetypes=(("Excel Dateien", "*.xlsx"),))
        self.excel_path.set(filename)

    def compute(self):
        result = run()
        cost = format(result, '.2f') + '€'
        msg = f'Berechnete Gesamtkosten: {cost}'
        self.cost_result.set(msg)

    def eval_checkbox(self):
        selected = self.use_excel.get()

        if selected:
            self.entry_excel_path.grid(row=1, column=0, sticky='W')
            self.button_open_filedialog_excel.grid(row=1, column=0, sticky='E')
            self.excel_text.set('Excel Datei:')
            self.drawings_text.set('Pfad zu .GEO/.DXF Dateien')
            self.entry_excel_path.focus()
            self.drawings_path.set('')
        else:
            self.entry_excel_path.grid_remove()
            self.button_open_filedialog_excel.grid_remove()
            self.excel_text.set('Ohne Excel Datei')
            self.drawings_text.set('Einzelne .GEO/.DXF Datei auswählen:')
            self.entry_drawings_path.focus()
            self.drawings_path.set('')

    def close(self):
        self.parent.destroy()


if __name__ == "__main__":
    now = datetime.datetime.now()

    logging.basicConfig(filename='./logs/app.log', level=logging.DEBUG)
    logging.debug(f'============================{now}===============================')
    logging.debug('Started')

    root = tk.Tk()
    MainApplication(root) #.pack(side="top", fill="both", expand=True)
    root.mainloop()

    logging.debug('Stopped')
