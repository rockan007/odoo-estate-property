from odoo import api, fields, models
import datetime

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

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline",inverse="_inverse_date_deadline")


    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date if record.create_date else datetime.date.today()) +datetime.timedelta(days = record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline-record.create_date.date()).days

