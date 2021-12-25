from odoo import fields,models

class EstatePropertyType(models.Model):
    _name ="estate.property.type"
    _description="type of estate property"
    _order= 'sequence,name'
    
    sequence = fields.Integer('Sequence',default=1, help='Used to order stages.Lower is better.')
    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property','property_type_id',string="Property Ids")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the estate property type must be unique!'),
    ]
    