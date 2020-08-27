import tkinter as tk
from calculator import start


def run():
    root = tk.Tk()

    canvas1 = tk.Canvas(root, width=300, height=300)
    canvas1.pack()

    def compute_cost():
        result = start.run()
        costs = format(result, '.2f')
        msg = f'Kosten aller Teile: {costs}€'
        label1 = tk.Label(root, text=msg, fg='green', font=('helvetica', 16, 'bold'))
        canvas1.create_window(150, 200, window=label1)

    button1 = tk.Button(text='Berechne Kosten', command=compute_cost, bg='grey', fg='black')
    canvas1.create_window(150, 150, window=button1)

    root.mainloop()




