import logging
from gui import gui
import datetime


def main():
    now = datetime.datetime.now()

    logging.basicConfig(filename='./logs/app.log', level=logging.DEBUG)
    logging.debug(f'============================{now}===============================')
    logging.debug('Started')
    gui.run()
    logging.debug('Finished')


if __name__ == '__main__':
    main()
