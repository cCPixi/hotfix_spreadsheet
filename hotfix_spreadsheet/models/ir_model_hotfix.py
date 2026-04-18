from odoo import models, api

class IrModel(models.Model):
    _inherit = 'ir.model'

    @api.model
    def has_searchable_parent_relation(self, model_names):
        """
c       Checks a list of model names to see if they have a searchable 
        parent-child relationship (parent_id).
        Restores the functionality of the 'child_of' operator in the spreadsheet dashboard.
        """
        result = {}
        for model_name in model_names:

            # Check whether the model exists in the system
            if model_name in self.env:
                model = self.env[model_name]
                
                parent_field_name = model._parent_name
                parent_field = model._fields.get(parent_field_name)
                
                if parent_field:
                    # getattr() catches any AttributeErrors that might occur if 
                    # the Odoo core field structure has changed in V19.
                    is_stored = getattr(parent_field, 'store', False)
                    has_search = getattr(parent_field, 'search', False)
                    is_searchable = bool(is_stored or has_search)
                else:
                    is_searchable = False
                
                result[model_name] = is_searchable
            else:
                # Fallback if an invalid model is requested
                result[model_name] = False
                
        return result