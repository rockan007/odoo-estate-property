from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description = "offer of estate property"

    price=fields.Float()
    status = fields.Selection(
        string="offer status",
        selection=[('accepted','Accepted'),('refused','Refused')],
        help="Offer status is uesed to show the offer's status",
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner",required=True)
    property_id = fields.Many2one('estate.property',required=True)


