import logging
import datetime
import tkinter as tk
import tkinter.filedialog
from calculator.start import run


class MainApplication(tk.Frame):
    """
    The graphical user interface.
    Run this file to start the app.
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.excel_path = tk.StringVar()
        self.excel_path.set('Pfad zu Excel-Datei')

        self.drawings_path = tk.StringVar()
        self.drawings_path.set('Pfad zu .geo/.dxf Dateien')

        self.cost_result = tk.StringVar()
        self.cost_result.set('0€')

        self.canvas = tk.Canvas(root, width=800, height=400)
        self.canvas.pack()

        self.label_excel_path = tk.Label(root, textvariable=self.excel_path, fg='black', font=('helvetica', 16, 'bold'))
        self.canvas.create_window(400, 20, window=self.label_excel_path)

        self.label_drawings_path = tk.Label(root, textvariable=self.drawings_path, fg='black', font=('helvetica', 16, 'bold'))
        self.canvas.create_window(400, 70, window=self.label_drawings_path )

        self.label_result = tk.Label(root, textvariable=self.cost_result, fg='black', font=('helvetica', 16, 'bold'))
        self.canvas.create_window(400, 120, window=self.label_result)

        self.button_open_filedialog_excel = tk.Button(text='Excel auswählen', command=self.open_filedialog_excel, bg='grey', fg='black')
        self.canvas.create_window(400, 170, window=self.button_open_filedialog_excel)
        self.button_open_filedialog_excel.pack()

        self.button_open_filedialog_drawings = tk.Button(text='Pfad zu Zeichnungen auswählen', command=self.open_filedialog_drawings, bg='grey', fg='black')
        self.canvas.create_window(400, 220, window=self.button_open_filedialog_drawings)
        self.button_open_filedialog_drawings.pack()

        self.button_compute = tk.Button(text='Berechnen', command=self.compute, bg='grey', fg='black')
        self.canvas.create_window(400, 270, window=self.button_compute)
        self.button_compute.pack()

        self.button_close = tk.Button(text='Beenden', command=self.close, bg='grey', fg='black')
        self.canvas.create_window(400, 320, window=self.button_close)
        self.button_close.pack()

    def open_filedialog_drawings(self):
        filename = tk.filedialog.askopenfilename(initialdir="/", title="Datei auswählen", filetypes=(("DXF Dateien", "*.DXF"), ("GEO Dateien", "*.GEO")))
        self.drawings_path.set(filename)

    def open_filedialog_excel(self):
        filename = tk.filedialog.askopenfilename(initialdir="/", title="Datei auswählen", filetypes=(("Text Dateien", "*.txt"), ("Excel Dateien", "*.xlsx")))
        self.excel_path.set(filename)

    def compute(self):
        result = run()
        self.cost_result.set(format(result, '.2f') + '€')

    def close(self):
        self.parent.destroy()


if __name__ == "__main__":
    now = datetime.datetime.now()

    logging.basicConfig(filename='./logs/app.log', level=logging.DEBUG)
    logging.debug(f'============================{now}===============================')
    logging.debug('Started')

    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

    logging.debug('Stopped')
