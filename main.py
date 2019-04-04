import os, pdfrw

TEMPLATE_NAME = 'IMX SHIP.pdf'

ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_AP_KEY = '/AP'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
'''
Filling a PDF form from python using only pdfrw

References:
github issue: https://github.com/pmaupin/pdfrw/issues/84
original posting: https://bostata.com/post/how_to_populate_fillable_pdfs_with_python/
'''

def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    annotations = template_pdf.pages[0][ANNOT_KEY]
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                    )
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


data_dict = {
    'LOT_1': 'ATR-153',
    'SN_1': 'TS1-175',
    'REF_1': 'LOJIC300',
    'DATE_1': '03/26/2019',
    'LOT_2': 'ATR-154',
    'SN_2': 'TS1-175',
    'REF_2': 'LOJIC300',
    'DATE_2': '03/26/2019',
}


def main():
    write_fillable_pdf(TEMPLATE_NAME, 'FILLED.PDF', data_dict)


if __name__ == '__main__':
    main()
