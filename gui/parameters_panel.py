import tkinter as tk


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

    def is_number(self, string):
        try:
            float(string)
            return True
        except:
            return False

    def update_parameters(self):
        # TODO: check number/string -> don't process invalid inputs
        self.parent.parameters['Offset'] = float(self.entry_offset.get())
        self.parent.parameters['Materialkosten_euro_t'] = float(self.entry_material_cost.get())
        self.parent.parameters['Schnittgeschwindigkeit_mm_s'] = float(self.entry_schnittgeschwindigkeit_mm_s.get())
        self.parent.parameters['Kosten_Schnitt_euro_min'] = float(self.entry_kosten_schnitt_euro_min.get())
        self.parent.parameters['Materialgewicht_g_cm3'] = float(self.entry_materialgewicht_g_cm3.get())
        self.parent.parameters['Gewinnmarge'] = float(self.entry_gewinnmarge.get())
        self.parent.parameters['Ausgabespalte'] = self.entry_excel_ausgabespalte.get()
        self.parent.parameters['Nr_erste_Reihe_Daten'] = int(self.entry_excel_first_row.get())

        value = self.entry_std_dicke_mm.get()
        if self.is_number(value):
            self.parent.parameters['Std_Dicke_mm'] = float(value)
        else:
            self.parent.parameters['Std_Dicke_mm'] = value