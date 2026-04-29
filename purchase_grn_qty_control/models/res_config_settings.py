from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    grn_over_receipt_tolerance = fields.Float(
        string='Over-Receipt Tolerance (%)',
        config_parameter='purchase_grn_qty_control.over_receipt_tolerance',
        default=0.0,
        help='Set 0 to block all over-receipts. Set 5 to allow up to 5% above PO qty.',
    )
