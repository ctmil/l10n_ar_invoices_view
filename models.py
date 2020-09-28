# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime,date,timedelta
from dateutil import relativedelta
import base64

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _compute_printed_vat_amount(self):
        for rec in self:
            sign = 1
            if rec.type == 'out_refund':
                sign = -1
            rec.print_vat_amount_total = rec.amount_total * sign
            rec.print_vat_amount_untaxed = rec.amount_untaxed * sign
            rec.print_vat_amount_tax = (rec.amount_total - rec.amount_untaxed) * sign

    vat = fields.Char('CUIT',related='partner_id.vat')
    responsibility_type_id = fields.Many2one('l10n_ar.afip.responsibility.type',string='Responsabilidad Fiscal',related='partner_id.l10n_ar_afip_responsibility_type_id')
    print_vat_amount_total = fields.Float('Monto Total',compute=_compute_printed_vat_amount)
    print_vat_amount_tax = fields.Float('Monto IVA',compute=_compute_printed_vat_amount)
    print_vat_amount_untaxed = fields.Float('Monto Neto',compute=_compute_printed_vat_amount)

