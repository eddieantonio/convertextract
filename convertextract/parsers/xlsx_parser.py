import xlrd
from openpyxl import load_workbook 
from openpyxl.styles import Font, Fill, Color
from openpyxl.cell import Cell


from .utils import BaseParser
from ..cors import processCors


class Parser(BaseParser):
    """Extract text from Excel files (.xls/xlsx).
    """

    def extract(self, filename, **kwargs):
        converted_filename = filename[:-5] + '_converted.xlsx'
        wb = load_workbook(filename)
        new_output = []
        output = ""
        for ws in wb:
            if not isinstance(kwargs["language"], type(None)):
                cors = processCors(kwargs["language"]).cor_list
                cors.sort(key=lambda x: len(x["from"]), reverse=True)
                for row in ws:
                    for col in row:
                        value = col.value
                        if value != None:
                            if isinstance(value, (int, float, long)):
                                value = unicode(value)
                                for kv in cors:
                                    value = value.replace(kv["from"],kv["to"])
                            elif not isinstance(value, str):
                                for kv in cors:
                                    value = value.replace(kv["from"],kv["to"])
                            new_output.append(value)
                            col.value = value
                wb.save(converted_filename)
            else:
                for row in ws:
                    for col in row:
                        value = col.value
                        if isinstance(value, (int, float, long)):
                            value = unicode(value)
                        if value != None:
                            new_output.append(value)

        if new_output:
            output += u' '.join(new_output) + u'\n'
        return output
