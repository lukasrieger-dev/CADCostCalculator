import openpyxl
import logging
from calculator import costfunction
from converter.converter import to_dxf_file
from calculator import config


__author__ = 'lukas'


def calculate(parameters, drawings_path, excel_file_path=None):
    tmp_file_path = './tmp.DXF'
    configuration = config.Configuration(**parameters)

    if not excel_file_path:
        try:
            to_dxf_file(drawings_path, './tmp.DXF')
            drawings_path = './tmp.DXF'
        except:
            pass

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
                try:
                    to_dxf_file(file_path, tmp_file_path)
                except:
                    # file is already .dxf
                    pass

                cost = costfunction.compute_cost(
                    Liefermenge.value,
                    tmp_file_path,
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
            logging.WARNING(f'Fehler -> {e}')
            raise e


