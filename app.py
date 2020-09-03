import tkinter as tk
import logging
import datetime
from gui.gui import ApplicationGUI


if __name__ == "__main__":
    now = datetime.datetime.now()

    logging.basicConfig(filename='./logs/app.log', level=logging.WARNING)
    logging.debug(f'============================{now}===============================')
    logging.debug('Started')

    root = tk.Tk()
    ApplicationGUI(root)
    root.mainloop()

    logging.debug('Stopped')
    logging.debug('===============================================================')
