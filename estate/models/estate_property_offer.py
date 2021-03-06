from odoo import api, exceptions, fields, models,tools
import datetime

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description = "offer of estate property"
    _order =  'price desc'

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

    property_type_id = fields.Many2one(related='property_id.property_type_id', store = True)
    """约束"""
    _sql_constraints=[
        ('check_price','CHECK (price > 0)','An offer price must be strictly positive')
    ]

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date if record.create_date else datetime.date.today()) +datetime.timedelta(days = record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline-record.create_date.date()).days

    def action_accept(self):
        for record in self:
            self._reset_offers_status(record.property_id)
            record.status = 'accepted'
            record.property_id.selling_price= record.price
            record.property_id.partner_id = record.partner_id
            record.property_id.state = 'accepted'
        return True
    
    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                self._reset_property_id(record)
            record.status = 'refused'
            record.property_id.state= 'received'
        return True

    def _reset_offers_status(self,property_id):
        for record in property_id.offer_ids:
            if record.status == 'accepted':
                record.status = 'refused'
    
    def _reset_property_id(self,record):
        record.property_id.selling_price= 0
        record.property_id.partner_id = None
    
    @api.model
    def create(self,vals):
        estate_property = self.env['estate.property'].browse(vals['property_id'])
        if tools.float_compare(estate_property.best_price,vals['price'],precision_digits=3)>=0:
            raise exceptions.UserError("The offer must be higher than $%.2f" % estate_property.best_price)
        estate_property.state='received'
        return super().create(vals)


   