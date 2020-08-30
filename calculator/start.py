import openpyxl
import logging
from calculator import costfunction
from collections import namedtuple


__author__ = 'lukas'


Configuration = namedtuple('Configuration', (
    'offset', 'material_cost_per_t', 'Schnittgeschwindigkeit_mm_s',
    'Kosten_Schnitt_euro_min', 'Materialgewicht_g_cm3', 'Materialkosten_euro_t',
    'Gewinnmarge', 'Ausgabespalte'
))
Configuration.__new__.__defaults__ = (0.0,) * len(Configuration._fields)


def load_from_init_file(file_path):
    """
    Loads the values from the init file into a dictionary.
    The init file must be a textfile containing key=value pairs.
    """
    init_values = {}
    with open(file_path) as init_file:
        lines = init_file.readlines()
        for line in lines:
            if line.startswith('#'):
                # skip comments
                continue
            line = line.strip()
            key, value = line.split('=')
            init_values[key] = float(value) if is_number(value) else value

    return init_values


def is_number(string):
    """
    Check if the string contains an integer of float number.
    string.isnumeric() only works for integers.
    """
    try:
        float(string)
        return True
    except:
        return False


def run():
    init_file_path = './init.txt'
    configuration = Configuration(**load_from_init_file(init_file_path))

    excel_file_path = './docs/Excel.xlsx'
    dxf_files_path = './docs/'

    try:
        xlsx = openpyxl.load_workbook(excel_file_path)
        sheet = xlsx.active
        values = sheet[str(sheet.dimensions)]
        is_header = True
        row_index = 1
        sum_of_all_cost = 0

        cell = configuration.Ausgabespalte + str(row_index)
        sheet[cell] = 'Kosten in €'

        # iterate over each line of the excel file
        for LfdNr, Liefermenge, ZeichnungsNr, Benennung, Dicke, Material in values:
            if is_header:
                # skip header line
                is_header = False
                continue

            row_index += 1
            file_path = dxf_files_path + 'Test2.dxf' #ZeichnungsNr.value
            cost = costfunction.compute_cost(
                Liefermenge.value,
                file_path,
                Dicke.value,
                configuration.Schnittgeschwindigkeit_mm_s,
                configuration.Kosten_Schnitt_euro_min,
                configuration.Materialgewicht_g_cm3,
                configuration.Materialkosten_euro_t,
                configuration.Gewinnmarge
            )

            sum_of_all_cost += cost
            cell = configuration.Ausgabespalte + str(row_index)
            sheet[cell] = format(cost, '.2f')
            logging.debug(configuration)
            logging.debug(f'Kosten für {Liefermenge.value} x {Benennung.value}: {round(cost, 2)}€')
            logging.debug("==============================================================")

        xlsx.save('./docs/output.xlsx')
        return sum_of_all_cost

    except Exception as e:
        print(f'Fehler -> {e}')
        raise e


