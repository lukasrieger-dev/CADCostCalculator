import tkinter as tk
from tkinter import messagebox
import string


class ParametersPanel:
    def __init__(self, parent):
        self.parent = parent
        entry_width = 5

        parameters_frame = tk.Frame(parent)
        parameters_frame.grid(row=5, column=0, pady=(20, 10))

        label_title = tk.Label(parameters_frame, text='Parameter', fg='black', font=parent.app_font)
        label_title.grid(row=0, column=0, sticky='W', pady=(5, 5))

        label_offset = tk.Label(parameters_frame, text='Offset [mm]:', fg='black', font=parent.app_font)
        label_offset.grid(row=1, column=0, sticky='W')

        self.entry_offset = tk.Entry(parameters_frame, textvariable=parent.offset, font=parent.app_font, width=entry_width)
        self.entry_offset.grid(row=1, column=1, sticky='W')

        label_material_cost = tk.Label(parameters_frame, text='Materialkosten [€/t]:', font=parent.app_font)
        label_material_cost.grid(row=1, column=2, padx=(10, 0), sticky='W')

        self.entry_material_cost = tk.Entry(parameters_frame, textvariable=parent.material_cost_per_t, font=parent.app_font, width=entry_width)
        self.entry_material_cost.grid(row=1, column=3, sticky='W')

        label_schnittgeschwindigkeit_mm_s = tk.Label(parameters_frame, text='Schnittgeschw. [mm/s]:', font=parent.app_font)
        label_schnittgeschwindigkeit_mm_s.grid(row=1, column=4, padx=(10, 0), sticky='W')

        self.entry_schnittgeschwindigkeit_mm_s = tk.Entry(parameters_frame, textvariable=parent.schnittgeschwindigkeit_mm_s, font=parent.app_font, width=entry_width)
        self.entry_schnittgeschwindigkeit_mm_s.grid(row=1, column=5, sticky='W')

        label_kosten_schnitt_euro_min = tk.Label(parameters_frame, text='Schnittkosten [€/min]:', font=parent.app_font)
        label_kosten_schnitt_euro_min.grid(row=2, column=0, sticky='W')

        self.entry_kosten_schnitt_euro_min = tk.Entry(parameters_frame, textvariable=parent.kosten_schnitt_euro_min, font=parent.app_font, width=entry_width)
        self.entry_kosten_schnitt_euro_min.grid(row=2, column=1, sticky='W')

        label_materialgewicht_g_cm3 = tk.Label(parameters_frame, text='Materialgew. [g/cm3]:', font=parent.app_font)
        label_materialgewicht_g_cm3.grid(row=2, column=2, padx=(10, 0), sticky='W')

        self.entry_materialgewicht_g_cm3 = tk.Entry(parameters_frame, textvariable=parent.materialgewicht_g_cm3, font=parent.app_font, width=entry_width)
        self.entry_materialgewicht_g_cm3.grid(row=2, column=3, sticky='W')

        label_gewinnmarge = tk.Label(parameters_frame, text='Gewinnmarge [>1.0]:', font=parent.app_font)
        label_gewinnmarge.grid(row=2, column=4, padx=(10, 0), sticky='W')

        self.entry_gewinnmarge = tk.Entry(parameters_frame, textvariable=parent.gewinnmarge, font=parent.app_font, width=entry_width)
        self.entry_gewinnmarge.grid(row=2, column=5, sticky='W')

        label_excel_ausgabespalte = tk.Label(parameters_frame, text='Ausgabespalte:', font=parent.app_font)
        label_excel_ausgabespalte.grid(row=3, column=0, sticky='W')

        self.entry_excel_ausgabespalte = tk.Entry(parameters_frame, textvariable=parent.excel_ausgabespalte, font=parent.app_font, width=entry_width)
        self.entry_excel_ausgabespalte.grid(row=3, column=1, sticky='W')

        label_excel_first_row = tk.Label(parameters_frame, text='Erste Zeile:', font=parent.app_font)
        label_excel_first_row.grid(row=3, column=2, padx=(10, 0), sticky='W')

        self.entry_excel_first_row = tk.Entry(parameters_frame, textvariable=parent.excel_first_row, font=parent.app_font, width=entry_width)
        self.entry_excel_first_row.grid(row=3, column=3, sticky='W')

        label_std_dicke_mm = tk.Label(parameters_frame, text='Einzelberech. Dicke [mm]', font=parent.app_font)
        label_std_dicke_mm.grid(row=3, column=4, padx=(10, 0), sticky='W')

        self.entry_std_dicke_mm = tk.Entry(parameters_frame, textvariable=parent.std_dicke_mm, font=parent.app_font, width=entry_width)
        self.entry_std_dicke_mm.grid(row=3, column=5, sticky='W')

    def update_parameters(self):
        def is_number(string):
            try:
                float(string)
                return True
            except:
                return False

        msg = 'Bitte korrigiere folgende Eingaben: '
        error = False

        value = self.entry_offset.get()
        if is_number(value):
            self.parent.parameters['Offset'] = float(value)
        else:
            msg += '\nOffset'
            error = True

        value = self.entry_material_cost.get()
        if is_number(value):
            self.parent.parameters['Materialkosten_euro_t'] = float(value)
        else:
            msg += '\nMaterialkosten'
            error = True

        value = self.entry_schnittgeschwindigkeit_mm_s.get()
        if is_number(value):
            self.parent.parameters['Schnittgeschwindigkeit_mm_s'] = float(value)
        else:
            msg += '\nSchnittgeschwindigkeit'
            error = True

        value = self.entry_kosten_schnitt_euro_min.get()
        if is_number(value):
            self.parent.parameters['Kosten_Schnitt_euro_min'] = float(value)
        else:
            msg += '\nSchnittkosten'
            error = True

        value = self.entry_materialgewicht_g_cm3.get()
        if is_number(value):
            self.parent.parameters['Materialgewicht_g_cm3'] = float(value)
        else:
            msg += '\nMaterialgewicht'
            error = True

        value = self.entry_gewinnmarge.get()
        if is_number(value):
            self.parent.parameters['Gewinnmarge'] = float(value)
        else:
            msg += '\nGewinnmarge'
            error = True

        value = self.entry_excel_ausgabespalte.get()
        if value in string.ascii_uppercase or value in string.ascii_lowercase:
            self.parent.parameters['Ausgabespalte'] = value
        else:
            msg += '\nAusgabespalte'
            error = True

        value = self.entry_excel_first_row.get()
        if is_number(value) and int(value) > 0:
            self.parent.parameters['Nr_erste_Reihe_Daten'] = int(value)
        else:
            msg += '\nErste Zeile in Excel'
            error = True

        value = self.entry_std_dicke_mm.get()
        if is_number(value):
            self.parent.parameters['Std_Dicke_mm'] = float(value)
        else:
            self.parent.parameters['Std_Dicke_mm'] = value

        if error:
            messagebox.showerror("Fehlerhafte Eingaben", msg)

        return error