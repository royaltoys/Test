from odoo import models, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for picking in self:
            if picking.picking_type_code != 'incoming':
                continue
            if not picking.purchase_id:
                continue

            tolerance_raw = self.env['ir.config_parameter'].sudo().get_param(
                'purchase_grn_qty_control.over_receipt_tolerance', default='0'
            )
            try:
                tolerance_pct = float(tolerance_raw) / 100.0
            except (ValueError, TypeError):
                tolerance_pct = 0.0

            over_lines = []
            for move in picking.move_ids.filtered(
                lambda m: m.state not in ('done', 'cancel')
            ):
                done_qty = move.quantity
                demand_qty = move.product_uom_qty

                if demand_qty <= 0:
                    continue

                max_allowed = demand_qty * (1 + tolerance_pct)

                if done_qty > max_allowed:
                    over_lines.append(
                        "• %s:  Done: %g %s  |  Max Allowed: %g %s  |  PO Ordered: %g %s"
                        % (
                            move.product_id.display_name,
                            done_qty, move.product_uom.name,
                            max_allowed, move.product_uom.name,
                            demand_qty, move.product_uom.name,
                        )
                    )

            if over_lines:
                raise ValidationError(
                    _("Over-Receipt Blocked!\n\n"
                      "These products exceed the PO ordered quantity:\n\n%s\n\n"
                      "Correct the received quantities before validating.")
                    % "\n".join(over_lines)
                )

        return super().button_validate()
