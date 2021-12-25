from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description = "tag of estate property"
    _order="name"

    name=fields.Char(required=True)

    _sql_constraints=[
        ('name_uniq','unique (name)','A property tag name must be unique')
    ]
    