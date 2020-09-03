from collections import namedtuple


"""
Import the Configuration NamedTuple to facilitate work with the calculator
"""
Configuration = namedtuple('Configuration',
                           (
                                'Offset',
                                'Schnittgeschwindigkeit_mm_s',
                                'Kosten_Schnitt_euro_min',
                                'Materialgewicht_g_cm3',
                                'Materialkosten_euro_t',
                                'Gewinnmarge',
                                'Ausgabespalte',
                                'Nr_erste_Reihe_Daten',
                                'Std_Dicke_mm',
                           )
                          )
Configuration.__new__.__defaults__ = (0.0,) * len(Configuration._fields)