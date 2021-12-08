from odoo import models, fields, api


class FormaterModel(models.AbstractModel):
    _name = 'formater.model'

    @api.model
    def _get_fields_to_format(self):
        return [f for f in self._fields.values() if hasattr(f, 'format_func')]
    
    @api.model
    def _prepare_formated_values(self, values):
        fields_to_format = self._get_fields_to_format()
        formated_values = {}
        for field in fields_to_format:
            if field.name not in values:
                continue
            
            func = field.format_func
            if isinstance(func, str):
                func = getattr(self, func, None)
            
            if callable(func) is False:
                continue
            
            formated_values[field.name] = func(values[field.name])
        
        return formated_values

    def _valid_field_parameter(self, field, name):
        return (name == 'format_func' and field.store) or super()._valid_field_parameter(field, name)
    
    @api.model_create_multi
    def create(self, value_list):
        for values in value_list:
            values.update(self._prepare_formated_values(values))
        return super().create(value_list)
    
    def write(self, values):
        values.update(self._prepare_formated_values(values))
        return super().write(values)

