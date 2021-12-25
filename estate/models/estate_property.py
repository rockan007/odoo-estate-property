from odoo import api, fields, models,exceptions,tools,_

from odoo.exceptions import ValidationError
from decimal import *

class EstateProperty(models.Model):
    _name="estate.property"
    _description= "Estate property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price= fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='garden_orientation',
        selection= [('north','North'),('south','South'),('east','East'),('west','West')],
        help="Orientation is used to info the orientation of the garden"

    )
    property_type_id= fields.Many2one("estate.property.type",string="Property type")
    user_id= fields.Many2one('res.users',string="Salesman",index=True,default=lambda self:self.env.user)
    partner_id = fields.Many2one('res.partner',string="Buyer",index= True,copy = False)
    tag_ids = fields.Many2many('estate.property.tag',string="tags")
    offer_ids = fields.One2many('estate.property.offer',"property_id",string="Offers")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    state = fields.Selection(
        string="State",
        copy=False,
        selection= [('new','NEW'),('received','OFFER RECEIVED'),('accepted','OFFER ACCEPTED'),('sold','SOLD'),('canceled','CANCELD')],
        default= 'new'
    )

    status = fields.Selection(
        string="Status",
        selection= [('new','New'),('canceled','Canceled'),('sold','Sold')],
        default = 'new'
    )

    _sql_constraints=[
        ('check_expected_price','CHECK (expected_price > 0)','A property expected price must be strictly positive'),
        ('check_selling_price','CHECK (selling_price >= 0)','A property selling price must be positive')
    ]

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area= record.living_area+record.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price= max(record.offer_ids.mapped('price')) if len(record.offer_ids)>0 else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation='north'
        else:
            self.garden_area = 0
            self.garden_orientation = ""
    
    def action_cancel(self):
        for record in self:
            if record.status == 'new':
                record.status = 'canceled'
                record.state = 'canceled'
                return True
            elif record.status == 'sold':
                raise exceptions.UserError("Sold properties can't be cancel!")
            else:
                raise exceptions.UserError("The property has been canceled!")
        
        return True

    def action_sold(self):
        for record in self:
            if record.status == 'new':
                record.status = 'sold'
                record.state = 'sold'
                return True
            elif record.status == 'canceled':
                raise exceptions.UserError("Canceled properties can't be sold!")
            else:
                raise exceptions.UserError("The property has been sold")
        
        return True
    
    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for record in self:
            min_selling_price= float(Decimal(record.expected_price)*Decimal(0.9)) 
            compared_result= tools.float_compare(record.selling_price,min_selling_price,precision_digits=3)
            print("record in self")
            if (not tools.float_is_zero(record.selling_price,precision_digits=3)) and (compared_result < 0):
                raise ValidationError(_('The selling price cannot be lower than 90 percent of the expected price.'))
    
    @api.onchange('offer_ids')
    def _onchange_state(self):
        state = "new"
        if self.status =='new':
            if tools.float_compare(self.selling_price,0,precision_digits=3)> 0:
                state="accepted"
            elif len(self.offer_ids)>0:
                state ="received"
            else:
                state = self.status

        self.state = state
                
            
            
