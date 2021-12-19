from odoo import api, fields, models

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
    user_id= fields.Many2one('res.users',string="Salesman",index=True,default=lambda self:self.env.user)
    partner_id = fields.Many2one('res.partner',string="Buyer",index= True,copy = False)
    tag_ids = fields.Many2many('estate.property.tag',string="tags")
    offer_ids = fields.One2many('estate.property.offer',"property_id",string="Offers")

    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area= record.living_area+record.garden_area
    
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price= max(record.offer_ids.mapped('price'))

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation='north'
        else:
            self.garden_area = 0
            self.garden_orientation = ""