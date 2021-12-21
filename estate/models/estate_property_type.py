from odoo import fields,models

class EstatePropertyType(models.Model):
    _name ="estate.property.type"
    _description="type of estate property"
    
    name = fields.Char(required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the estate property type must be unique!'),
    ]
    