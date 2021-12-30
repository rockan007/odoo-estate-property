from odoo import models

class EstateProperty(models.Model):
    _inherit ="estate.property"

    def action_sold(self):
        res = super().action_sold()
        if res:
            journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
            self.env['account.move'].create({
                'partner_id':self.partner_id,
                'move_type':'out_invoice',
                'journal_id': journal.id,
                'invoice_line_ids': [
                    (0,0,{
                        'name':'Available house',
                        'quantity': self.selling_price*0.06,
                        'price_unit':1
                    }),
                    (0,0,{
                        'name':'Administrative fees',
                        'quantity':100.00,
                        'price_unit':1
                    })
                ]
            })
        return res