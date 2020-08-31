import openpyxl
import logging
from calculator import costfunction
from collections import namedtuple


__author__ = 'lukas'

# TODO: global config dict/tuple
Configuration = namedtuple('Configuration', (
    'Offset', 'Schnittgeschwindigkeit_mm_s',
    'Kosten_Schnitt_euro_min', 'Materialgewicht_g_cm3', 'Materialkosten_euro_t',
    'Gewinnmarge', 'Ausgabespalte', 'Nr_erste_Reihe_Daten', 'Std_Dicke_mm'
))
Configuration.__new__.__defaults__ = (0.0,) * len(Configuration._fields)


def calculate(parameters, drawings_path, excel_file_path=None):
    configuration = Configuration(**parameters)

    if not excel_file_path:
        return costfunction.compute_cost(
            1,
            drawings_path,
            configuration.Std_Dicke_mm,
            configuration.Schnittgeschwindigkeit_mm_s,
            configuration.Kosten_Schnitt_euro_min,
            configuration.Materialgewicht_g_cm3,
            configuration.Materialkosten_euro_t,
            configuration.Gewinnmarge,
            configuration.Offset
        )
    else:
        try:
            xlsx = openpyxl.load_workbook(excel_file_path)
            sheet = xlsx.active
            min_dimension = 'A' + str(int(configuration.Nr_erste_Reihe_Daten))
            max_dimension = sheet.dimensions.split(':')[1]
            working_dimensions = min_dimension + ':' + max_dimension
            values = sheet[working_dimensions]
            row_index = int(configuration.Nr_erste_Reihe_Daten-1)
            sum_of_all_cost = 0

            cell = configuration.Ausgabespalte + str(row_index)
            sheet[cell] = 'Kosten in €'

            # iterate over each line of the excel file
            for LfdNr, Liefermenge, ZeichnungsNr, Benennung, Dicke, Material in values:
                row_index += 1
                file_path = drawings_path + '/' + ZeichnungsNr.value
                cost = costfunction.compute_cost(
                    Liefermenge.value,
                    file_path,
                    Dicke.value,
                    configuration.Schnittgeschwindigkeit_mm_s,
                    configuration.Kosten_Schnitt_euro_min,
                    configuration.Materialgewicht_g_cm3,
                    configuration.Materialkosten_euro_t,
                    configuration.Gewinnmarge,
                    configuration.Offset
                )

                sum_of_all_cost += cost
                cell = configuration.Ausgabespalte + str(row_index)
                sheet[cell] = format(cost, '.2f')
                logging.debug(configuration)
                logging.debug(f'Kosten für {Liefermenge.value} x {Benennung.value}: {round(cost, 2)}€')
                logging.debug("==============================================================")

            xlsx.save('./output.xlsx')
            return sum_of_all_cost

        except Exception as e:
            print(f'Fehler -> {e}')
            raise e


