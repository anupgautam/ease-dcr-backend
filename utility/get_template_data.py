def get_template_data(original_model, original_serializer, data):
    data_return = {}
    data_return['original_data'] = {'model': original_model,
                                    'serializer': original_serializer}
    this_data = [{'model': i.get('model'),
                  'mapped_model': i.get('mapped_model'),
                  'fk_original': i.get('fk_original'),
                  'fk_map': i.get('fk_map'),
                  'serializer': i.get('serializer'),
                  'mapped_serializer': i.get('mapped_serializer'),
                  'model_field_name': i.get('model_field_name')} for i in data]
    data_return['repeated_data'] = this_data
    return data_return