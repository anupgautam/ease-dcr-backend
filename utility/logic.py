from abc import ABC, abstractmethod
from django.core.exceptions import FieldError
from django.db.models import Model
from utility.string_to_image_conversion import Base64ToImageConversion
# from utility.string_to_image_conversion


class RetrieveLogic(ABC):

    def __init__(self, data, pk) -> None:
        self.data = data
        self.pk = pk

    @abstractmethod
    def retrieve():
        pass


class RetrieveLogicID(RetrieveLogic):

    def __init__(self, data, pk) -> None:
        self.data = data
        self.pk = pk

    def retrieve(self):
        package_data = self.data['original_data']['model'].objects.get(pk=self.pk)
        serializer = self.data['original_data']['serializer'](instance=package_data)
        data_dict = {}
        for i in self.data['repeated_data']:
            field_instance = i['fk_original']
            mapped_data = i['mapped_model'].objects.filter(**{field_instance:self.pk})
            filter_list_tuple = mapped_data.values_list(i['fk_map'])
            filter_list = [j[0] for j in filter_list_tuple]
            filtered_data = i['serializer'](
                                    i['model'].objects.filter(id__in=filter_list),
                                    many=True)
            data_dict[i['model_field_name']] = filtered_data.data
        data_dict.update(serializer.data)
        return data_dict
    
class RetrieveLogicIDSelect(RetrieveLogic):
    def __init__(self, data, pk, select_fields) -> None:
        self.data = data
        self.pk = pk
        self.select_fields = select_fields

    def retrieve(self):
        package_data = self.data['original_data']['model'].objects.get(pk=self.pk)
        
        
        serializer = self.data['original_data']['serializer'](instance=package_data)
        
        looped_serializer = serializer.data.copy()
        # for key, value in serializer.data.items():
        #     if(key in self.select_fields):
        #         looped_value = value.copy()
                
        #         for key1, value1 in value.items():
        #             if isinstance(value1, dict):
        #                 looped_value[key1] = value1.get('id')
        #             else:
        #                 looped_value[key1] = value1
        #         looped_serializer[key] = value
        data_dict = {}
        for i in self.data['repeated_data']:
            field_instance = i['fk_original']
            mapped_data = i['mapped_model'].objects.filter(**{field_instance:self.pk})
            filter_list_tuple = mapped_data.values_list(i['fk_map'])
            filter_list = [j[0] for j in filter_list_tuple]
            filtered_data = i['serializer'](
                                    i['model'].objects.filter(id__in=filter_list),
                                   many=True)
            data_dict[i['model_field_name']] = filtered_data.data
            data_dict.update(serializer.data)
            # final_data = filtered_data.data.copy()
            # if len(filtered_data.data)>0:
            #     for index in range(0, len(filtered_data.data)):
            #         inside_serialized_data = filtered_data.data[index].copy()
            #         for key, value in filtered_data.data[index].items():
            #             if isinstance(value, dict):
            #                 if key == "company_name":
            #                     inside_serialized_data[key] =  value.get('company_id')
            #                 elif key == "role_name":
            #                     inside_serialized_data[key] = value.get("role_id")
            #                 else:
            #                     inside_serialized_data[key] = value.get('id')
            #                 final_data[index] = inside_serialized_data
            # data_dict[i['model_field_name']] = final_data
        # data_dict.update(looped_serializer)
        return data_dict


class RetrieveLogicUUID(RetrieveLogic):

    def __init__(self, data, pk) -> None:
        self.data = data
        self.pk = pk

    def retrieve(self):
        package_data = self.data['original_data']['model'].objects.get(pk=self.pk)
        serializer = self.data['original_data']['serializer'](instance=package_data)
        data_dict = {}
        for i in self.data['repeated_data']:
            field_instance = i['fk_original']
            mapped_data = i['mapped_model'].objects.filter(**{field_instance:self.pk})
            filter_list_tuple = mapped_data.values_list(i['fk_map'])
            filter_list = [j[0] for j in filter_list_tuple]
            filtered_data = i['serializer'](
                                    instance=i['model'].objects.filter(uuid__in=filter_list),
                                    many=True)
            data_dict[i['model_field_name']] = filtered_data.data
        data_dict.update(serializer.data)
        return data_dict
        

class CreateArray(ABC):

    @abstractmethod
    def return_json(self):
        pass

    @abstractmethod
    def return_json_empty(self):
        pass


class CreateArrayInsideDictionaryWithQuerySet(CreateArray):

    def __init__(self, dict_field_name=None, array_value=None, return_dict=None):
        self.dict_field_name = dict_field_name
        self.array_value = array_value
        self.return_dict = return_dict

    def return_json(self):
        if self.return_dict.get(self.dict_field_name):
            self.return_dict[self.dict_field_name].append(self.array_value)
        else:
            self.return_dict[self.dict_field_name] = [self.array_value]
        return self.return_dict

    def return_json_empty(self):
        self.return_dict[self.dict_field_name] = []
        return self.return_dict


class CreateArrayInsideDictionaryWithoutQuerySet(CreateArray):

    def __init__(self, dict_field_name=None, array_value=None, return_dict=None):
        self.dict_field_name = dict_field_name
        self.array_value = array_value
        self.return_dict = return_dict

    def return_json(self):
        if self.return_dict.get(self.dict_field_name):
            self.return_dict[self.dict_field_name].append(self.array_value.values())
        else:
            self.return_dict[self.dict_field_name] = [self.array_value.values()]
        return self.return_dict

    def return_json_empty(self):
        self.return_dict[self.dict_field_name] = []
        return self.return_dict


class CreateLogic(ABC):

    def __init__(self, data, original_model, validated_data) -> None:
        self.data = data
        self.original_model = original_model
        self.validated_data = validated_data

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def create_return(self):
        pass


class CreateLogicID(CreateLogic):

    def __init__(
        self,
        data,
        original_model,
        validated_data: dict,
        create_array: CreateArray) -> None:
        self.data = data
        self.original_model = original_model
        self.validated_data = validated_data
        self.create_array = create_array

    def create(self):
        for i in self.data:
            this_data = []
            if(self.validated_data.get(i.get('model_field_name'))):
                this_data = self.validated_data[i.get('model_field_name')]
            if len(this_data)>0:
                for j in this_data:
                    if j.get('id'):
                        if i.get('model').objects.filter(pk=j.get('id')).exists():
                            if  not i.get('mapped_model').objects.filter(**{
                                    i.get('fk_original'): self.validated_data.get('id'),
                                    i.get('fk_map'): j.get('id')}).exists():
                                i.get('mapped_model').objects.create(
                                    **{
                                        i.get('fk_original')+'_id': self.validated_data.get('id'),
                                        i.get('fk_map')+'_id': j.get('id')
                                        })
                            else:
                                raise FieldError("Your value has already been added to this relationshop!!!")
                        else:
                            instance = i.get('model')(**j)
                            instance.save()
                            i.get('mapped_model').objects.create(
                                **{
                                    i.get('fk_original')+'_id': self.validated_data.get('id'),
                                    i.get('fk_map')+'_id': instance.id})
                    else:
                        instance = i.get('model')(**j)
                        instance.save()
                        i.get('mapped_model').objects.create(
                                **{
                                    i.get('fk_original')+'_id': self.validated_data.get('id'),
                                    i.get('fk_map')+'_id': instance.id})


    def create_return(self):
        returning_instance = {}
        for data in self.data:
            filtered_values = data.get('mapped_model').objects.filter(
                    **{data.get('fk_original'): self.validated_data.get('id')})
            ids = filtered_values.values(data.get('fk_map')).all()
            all_repeated_id = [id[data.get('fk_map')] for id in ids]
            if(len(all_repeated_id))>0:
                for id in all_repeated_id:
                    self.create_array(
                        dict_field_name=data.get('model_field_name'),
                        array_value=data.get('model').objects.get(pk=id),
                        return_dict=returning_instance).return_json()
            else:
                self.create_array(
                    dict_field_name=data.get('model_field_name'),
                    return_dict=returning_instance
                ).return_json_empty()
        original_data = self.original_model.objects.get(
                            id=self.validated_data.get('id')).__dict__
        field_names = [key for key, value in returning_instance.items()]
        for field in field_names:
            original_data[field] = returning_instance[field]
        return original_data
        
        
class UpdateLogic(ABC):

    def __init__(self, data, original_model, validated_data):
        self.data = data
        self.original_model = original_model
        self.validated_data = validated_data

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def update_return(self):
        pass


# class UpdateLogicID(UpdateLogic):

    def __init__(
        self,
        data,
        original_model,
        validated_data,
        instance,
        context,
        create_array: CreateArray):
        self.data = data
        self.original_model = original_model
        self.validated_data = validated_data
        self.create_array = create_array
        self.context = context
        self.instance = instance

    def update(self):
        editable_data = self.validated_data.copy()
        for data in self.data:
            del editable_data[data.get('model_field_name')]
        for key , value in editable_data.copy().items():
            if isinstance(value, dict):
                editable_data.pop(key, None)
                for key1, values in value.items():
                    if(key1 == "id"):
                        editable_data[f'{key}_id'] = values
        (self.original_model.
            objects.filter(
                pk=self.instance.id)
                .update(**editable_data))
        for i in self.data:
            this_data = self.validated_data[i.get('model_field_name')]
            if self.context[i.get('model_field_name')] == "normal":
                if len(this_data)>0:
                    for j in this_data:
                        i.get('model').objects.filter(pk=j.get('id')).update(**j)
            if self.context[i.get('model_field_name')] == "select":
                if len(this_data)>0:
                    i.get('mapped_model').objects.filter(
                                    **{
                                        i.get('fk_original'): self.validated_data.get('id')
                                    }).delete()
                    final_list = []
                    for data in self.validated_data[i.get('model_field_name')]:
                        final_list.append(i.get('mapped_model')(**{
                            i.get('fk_original')+"_id": self.validated_data.get('id'),
                            i.get('fk_map')+"_id": data.get('id')
                        }))
                    i.get('mapped_model').objects.bulk_create(final_list)
                    
    def update_return(self):
        returning_instance = {}
        for data in self.data:
            filtered_values = data.get('mapped_model').objects.filter(
                    **{data.get('fk_original'): self.validated_data.get('id')})
            ids = filtered_values.values(data.get('fk_map')).all()
            all_repeated_id = [id[data.get('fk_map')] for id in ids]
            if(len(all_repeated_id))>0:
                for id in all_repeated_id:
                    self.create_array(
                        dict_field_name=data.get('model_field_name'),
                        array_value=data.get('model').objects.get(pk=id),
                        return_dict=returning_instance).return_json()
            else:
                self.create_array(
                    dict_field_name=data.get('model_field_name'),
                    return_dict=returning_instance
                ).return_json_empty()
        original_data = self.original_model.objects.get(
                            id=self.validated_data.get('id')).__dict__
        field_names = [key for key, value in returning_instance.items()]
        for field in field_names:
            original_data[field] = returning_instance[field]
        return original_data


class UpdateLogic(ABC):
    def __init__(self, data, original_model, validated_data):
        self.data = data
        self.original_model = original_model
        self.validated_data = validated_data
    @abstractmethod
    def update(self):
        pass
    @abstractmethod
    def update_return(self):
        pass
class UpdateLogicID(UpdateLogic):
    def __init__(
        self,
        data,
        original_model,
        validated_data,
        instance,
        context,
        create_array: CreateArray):
        self.data = data
        self.original_model = original_model
        self.validated_data = validated_data
        self.create_array = create_array
        self.context = context
        self.instance = instance

    def delete_repeatable_field(self, data_dict):
        for data in self.data:
            del data_dict[data.get('model_field_name')]

    def get_original_model_instance(self):
        return self.original_model.objects.get(pk=self.instance.id)
    
    def update_blob_image_field_original(self, key, value):
        obj = self.get_original_model_instance()
        setattr(
            obj,
            key,
            Base64ToImageConversion(value).convert())
        obj.save()

    def update_image_return_image_field_original(self, data_dict):
        image_field_list = []
        for key, value in data_dict.items():
            if isinstance(value, str):
                if value.__contains__('http'):
                    image_field_list.append(key)
                elif value.__contains__('image'):
                    self.update_blob_image_field_original(key, value)
                    image_field_list.append(key)
                else:
                    image_field_list = image_field_list
        return image_field_list
    
    def update_original_model(self, data_dict):
        self.original_model.objects.filter(
            pk=self.instance.id).update(**data_dict)
        
    def get_repeatable_model_instance(self, model_instance, pk_value):
        return model_instance.objects.get(pk=pk_value)
    
    def update_blob_image_field_map(self, model_instance, pk_value, key, value):
        inner_obj = self.get_repeatable_model_instance(
            model_instance, pk_value)
        setattr(
            inner_obj,
            key,
            Base64ToImageConversion(value).convert())
        inner_obj.save()

    def update_image_return_image_field_map(self, data_dict, meta_data, loop_data):
        image_field_list = []
        for key, value in data_dict.items():
            if isinstance(value, str):
                if value.__contains__('image'):
                    self.update_blob_image_field_map(
                        meta_data.get('model'),
                        loop_data.get('id'),
                        key,
                        value)
                    image_field_list.append(key)
                elif value.__contains__('http'):
                    image_field_list.append(key)
                else:
                    image_field_list = image_field_list
        return image_field_list
    
    def update_repeatable_model(self, editable_data, meta_data, loop_data):
        meta_data.get('model').objects.filter(
            pk=loop_data.get('id')).update(**editable_data)
        
    def delete_existing_mapping(self, meta_data):
        meta_data.get('mapped_model').objects.filter(
            **{
            meta_data.get('fk_original'): self.validated_data.get('id')
            }
        ).delete()

    def bulk_create_mapping(self, meta_data):
        final_list = []
        for data in self.validated_data[meta_data.get('model_field_name')]:
            final_list.append(meta_data.get('mapped_model')(**{
                            meta_data.get('fk_original')+"_id": self.validated_data.get('id'),
                            meta_data.get('fk_map')+"_id": data.get('id')
                        }))
        meta_data.get('mapped_model').objects.bulk_create(final_list)

    def update_normal_mapped_total(self, meta_data, model_field_data):
        if len(model_field_data)>0:
            for j in model_field_data:
                editable_loop_data = j.copy()
                inner_image_list = self.update_image_return_image_field_map(
                    editable_loop_data, meta_data, j)
                for image in inner_image_list:
                    del editable_loop_data[image]
                self.update_repeatable_model(editable_loop_data, meta_data, j)
                
    def update_select_mapped_total(self, meta_data, model_field_data):
        if len(model_field_data)>0:
            self.delete_existing_mapping(meta_data)
            self.bulk_create_mapping(meta_data)

    def update(self):
        editable_data = self.validated_data.copy()
        self.delete_repeatable_field(editable_data)
        image_field_list = self.update_image_return_image_field_original(editable_data)
        for data in image_field_list:
            del editable_data[data]
        self.update_original_model(editable_data)
        for i in self.data:
            this_data = self.validated_data[i.get('model_field_name')]
            if self.context[i.get('model_field_name')] == "normal":
                self.update_normal_mapped_total(i, this_data)
            if self.context[i.get('model_field_name')] == "select":
                self.update_select_mapped_total(i, this_data)

    def update_return(self):
        returning_instance = {}
        for data in self.data:
            filtered_values = data.get('mapped_model').objects.filter(
                    **{data.get('fk_original'): self.validated_data.get('id')})
            ids = filtered_values.values(data.get('fk_map')).all()
            all_repeated_id = [id[data.get('fk_map')] for id in ids]
            if(len(all_repeated_id))>0:
                for id in all_repeated_id:
                    self.create_array(
                        dict_field_name=data.get('model_field_name'),
                        array_value=data.get('model').objects.get(pk=id),
                        return_dict=returning_instance).return_json()
            else:
                self.create_array(
                    dict_field_name=data.get('model_field_name'),
                    return_dict=returning_instance
                ).return_json_empty()
        original_data = self.original_model.objects.get(
                            id=self.validated_data.get('id')).__dict__
        field_names = [key for key, value in returning_instance.items()]
        for field in field_names:
            original_data[field] = returning_instance[field]
        return original_data

class DeleteLogic(ABC):

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def delete_return(self):
        pass


class DeleteLogicID(DeleteLogic):

    def __init__(
        self,
        data,
        original_model,
        validated_data,
        create_array: CreateArray,
        context):

        self.data = data
        self.original_model = original_model
        self.validated_data = validated_data
        self.create_array = create_array
        self.context = context

    def delete(self):
        for data in self.data:
            this_data = self.validated_data.get(data.get('model_field_name'))
            if self.context[data.get('model_field_name')] == "normal":
                if this_data:
                    for input in this_data:
                        data.get('mapped_model').objects.filter(
                            **{
                                data.get('fk_original'): self.validated_data.get('id'),
                                data.get('fk_map'): input.get('id')}).delete()
                        data.get('model').objects.filter(
                            **{
                                'id': input.get('id')
                            }
                        ).delete()
            if self.context[data.get('model_field_name')] == "select":
                if this_data:
                    for input in this_data:
                        data.get('mapped_model').objects.filter(
                            **{
                                data.get('fk_original'): self.validated_data.get('id'),
                                data.get('fk_map'): input.get('id')}).delete()

                

    def delete_return(self):
        returning_instance = {}
        for data in self.data:
            filtered_values = data.get('mapped_model').objects.filter(
                    **{data.get('fk_original'): self.validated_data.get('id')})
            ids = filtered_values.values(data.get('fk_map')).all()
            all_repeated_id = [id[data.get('fk_map')] for id in ids]
            if(len(all_repeated_id))>0:
                for id in all_repeated_id:
                    self.create_array(
                        dict_field_name=data.get('model_field_name'),
                        array_value=data.get('model').objects.filter(pk=id).values().first(),
                        return_dict=returning_instance).return_json()
            else:
                self.create_array(
                    dict_field_name=data.get('model_field_name'),
                    return_dict=returning_instance
                ).return_json_empty()
        original_data = self.original_model.objects.get(
                            id=self.validated_data.get('id')).__dict__
        field_names = [key for key, value in returning_instance.items()]
        for field in field_names:
            original_data[field] = returning_instance[field]
        return original_data


class StringToDictionary(ABC):

    @abstractmethod
    def convert(self):
        pass

class DictionaryInsideArray(StringToDictionary):

    def __init__(self, key_array, value, dict) -> None:
        self.key_array = key_array
        self.value = value
        self.dict = dict
        
    def convert_zero_index(self):
        if(self.dict.get(self.key_array[0])):
            self.dict[self.key_array[0]][int(self.key_array[1])].update(
                    {self.key_array[2]:self.value}) 
        else: 
            self.dict[self.key_array[0]] = [{self.key_array[2]: self.value}]
    
    def convert_other_index(self):
        if(len(self.dict.get(self.key_array[0])) == (int(self.key_array[1])+1)):
            self.dict[self.key_array[0]][int(self.key_array[1])].update(
                    {self.key_array[2]:self.value}) 
        else:
            self.dict[self.key_array[0]].append(
                    {self.key_array[2]: self.value})

    def convert(self):
        if(int(self.key_array[1]) == 0):
            self.convert_zero_index()
        else:
            self.convert_other_index()


class DictionaryInsideDictionary(StringToDictionary):

    def __init__(self, key_array, value, dict) -> None:
        self.key_array = key_array
        self.value = value
        self.dict = dict

    def convert(self):
        if self.dict.get(self.key_array[0]):
            self.dict[self.key_array[0]].update({self.key_array[1]: self.value})
        else:
            self.dict.update({self.key_array[0]:{ self.key_array[1]: self.value}})



#not completed
def change_string_to_dict(
    dict_to_return,
    key,
    value):
        if key.find('[') == -1:
            dict_to_return[key] = value
        else:
            key_without_brac = key.replace("]", '', 2)
            key_array = key_without_brac.split('[', 2)
            if len(key_array) < 3:
                DictionaryInsideDictionary(key_array, value, dict_to_return).convert()   
            
            else:
                if key_array[2].find('[') == -1:
                    if key_array[1].isdigit():
                        DictionaryInsideArray(key_array, value, dict_to_return).convert()

                else:
                    if key_array[1].isdigit():
                        change_string_to_dict(dict_to_return[key_array[0]][int(key_array[1])], key_array[2], value)
                    else:
                        change_string_to_dict(dict_to_return[key_array[0]][key_array[1]], key_array[2], value)


def formdata_application_json(data):
    dict_to_return = {}
    for key, value in data.items():
        change_string_to_dict(
            dict_to_return=dict_to_return,
            key=key,
            value=value)
    return dict_to_return






        