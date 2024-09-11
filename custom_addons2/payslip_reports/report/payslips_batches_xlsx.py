""" Initialize Payslips Batches Xlsx """

from odoo import _, models


def set_report_header(format_header, row_pos, sheet):
    sheet.write_string(row_pos, 0, _('Branch'), format_header)
    sheet.write_string(row_pos, 1, _('Bank Id'), format_header)
    sheet.write_string(row_pos, 2, _('Account#'), format_header)
    sheet.write_string(row_pos, 3, _('Name'), format_header)
    sheet.write_string(row_pos, 4, _('Code'), format_header)
    sheet.write_string(row_pos, 5, _('Reason'), format_header)
    sheet.write_string(row_pos, 6, _('Amount'), format_header)
    # Set column width
    sheet.set_column(0, 3, 30)
    sheet.set_column(4, 6, 15)
    return row_pos + 2


def _get_report_name():
    return _('Bank template')


def set_report_content(format_content, format_header, lines, sheet, row_pos):
    for line in lines:
        # Report Header
        row_pos = set_report_header(format_header, row_pos, sheet)
        # report Data
        slip_ids = line.slip_ids.filtered(
            lambda r: r.employee_id.journal_id.type == 'bank')
        for rec in slip_ids:
            sheet.write(row_pos, 0, rec.employee_id.branch, format_content)
            sheet.write(row_pos, 1, rec.employee_id.bank_id, format_content)
            sheet.write(row_pos, 2, rec.employee_id.bank_account,
                        format_content)
            sheet.write(row_pos, 3, rec.employee_id.name, format_content)
            sheet.write(row_pos, 4, "Code", format_content)
            sheet.write(row_pos, 5, "Salary", format_content)
            sheet.write(row_pos, 6, rec.net_wage, format_content)
            row_pos += 1
        row_pos += 3


class BankXLSX(models.AbstractModel):
    _name = 'report.payslip_reports.bank_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        sheet = workbook.add_worksheet(_get_report_name()[:31])
        format_header = workbook.add_format({
            'bold': True,
            'align': 'center',
            'border': True
        })
        format_content = workbook.add_format({
            'align': 'center',
            'font_size': 12,
            'border': False
        })
        set_report_content(format_content, format_header, lines, sheet,
                           row_pos=0)
