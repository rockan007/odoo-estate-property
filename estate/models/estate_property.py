from odoo import fields, models

class EstateProperty(models.Model):
    _name="estate.property"
    _description= "Estate property"

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
    user_id= fields.Many2one('res.users',string="Salesman",index=True,tracking=True, default=lambda self:self.env.user)
    partner_id = fields.Many2one('res.partner',string="Buyer",index= True,tracking=True,copy = False)