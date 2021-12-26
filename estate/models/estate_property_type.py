from odoo import fields,models,api

class EstatePropertyType(models.Model):
    _name ="estate.property.type"
    _description="type of estate property"
    _order= 'sequence,name'
    
    sequence = fields.Integer('Sequence',default=1, help='Used to order stages.Lower is better.')
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id',string="Property Ids")
    offer_ids = fields.One2many('estate.property.offer','property_type_id',string="Type offer list")
    offer_count = fields.Integer(compute="_compute_offer_count")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the estate property type must be unique!'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count= len(record.offer_ids)
