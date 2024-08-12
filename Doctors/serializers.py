from rest_framework import serializers
from Company.serializers import CompanySerializers
from Doctors.models import *
from DCRUser.serializers import CompanyUserRoleSerializers


class DoctorSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) 

    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorCategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = DoctorCategory
        fields = '__all__'


# class WorkingAreaSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = DoctorWorkingArea
#         fields = '__all__'


# class AreaWiseDoctorSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = AreaWiseDoctor
#         fields = '__all__'
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['doctor_name'] = DoctorSerializers(
#                                     instance.doctor_name).data
#         response['doctor_area'] = CompanyWiseAreaSerializer(
#                                     instance.doctor_area).data
#         return response


# class CategoryWiseDoctorSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = CategoryWiseDoctor
#         fields = [
#             'id',
#             'doctor_name',
#             'doctor_category'
#         ]
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['doctor_name'] = DoctorSerializers(
#                                     instance.doctor_name).data
#         response['doctor_category'] = CompanyDoctorSpecializationSerializer(
#                                     instance.doctor_category).data
#         return response



class CompanyWiseDoctorWithoutToRepresentation(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    class Meta:
        model = CompanyWiseDoctor
        fields = '__all__'

        
class CompanyWiseDoctorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False) 
    class Meta:
        model = CompanyWiseDoctor
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        try:
            response['company_name'] = CompanySerializers(
                                            instance.company_name).data
            response['doctor_name'] = DoctorSerializers(
                                            instance.doctor_name).data
            response['doctor_specialization'] = DoctorSerializers(
                                            instance.doctor_specialization).data
        except:
            response['company_name'] = CompanySerializers(
                                        instance['company_name']).data
            response['doctor_name'] = DoctorSerializers(
                                        instance['doctor_name']).data
            response['doctor_specialization'] = DoctorSerializers(
                                            instance.doctor_specialization).data
        return response


# class CompanyWiseAreaSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = DoctorCompanyArea
#         fields = '__all__'
#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['company_name'] = CompanySerializers(
#                                     instance.company_name).data
#         response['area_name'] = WorkingAreaSerializer(
#                                     instance.area_name).data
#         return response


class CompanyDoctorSpecializationSerializer(serializers.ModelSerializer):
    # category_name = DoctorCategorySerializers()
    class Meta:
        model = CompanyDoctorSpecialization
        fields = '__all__'
    
    # def create(self, validated_data):
    #     doctor_category_instance = DoctorCategory(
    #         category_name=validated_data['category_name']['category_name']
    #     )
    #     doctor_category_instance.save()
    #     instance = CompanyDoctorCategory(
    #         category_name=doctor_category_instance,
    #         company_name=validated_data['company_name']
    #     )
    #     instance.save()
    #     return instance
    
    # def update(self, instance, validated_data):
    #     doctor_category_instance = DoctorCategory.objects.get(
    #         id=instance.category_name.id)
    #     doctor_category_instance.category_name = validated_data['category_name']['category_name']
    #     doctor_category_instance.save()
    #     instance.category_name = doctor_category_instance
    #     instance.save()
    #     return instance
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['company_name'] = CompanySerializers(
    #                                 instance.company_name).data
    #     return response
    


class AddDoctorSerializer(serializers.ModelSerializer):
    # doctor_territory = serializers.CharField(max_length=200)
    company_name = serializers.CharField(max_length=150)
    mpo_name = serializers.CharField(max_length=10)
    is_investment = serializers.BooleanField()
    # doctor_category = serializers.CharField(max_length=200)

    class Meta:
        model = Doctor
        fields = ['doctor_name',
                    'doctor_address',
                    'doctor_gender',
                    'doctor_phone_number',
                    'company_name',
                    'doctor_territory',
                    'doctor_category',
                    'doctor_nmc_number',
                    'doctor_qualification',
                    'doctor_specialization',
                    'mpo_name',
                    'is_investment'
                    ]
        
    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return Doctor.objects.create_doctor_with_signal(
            doctor_name=validated_data['doctor_name'],
            doctor_gender=validated_data['doctor_gender'],
            doctor_phone_number=validated_data['doctor_phone_number'],
            company_name=validated_data['company_name'],
            doctor_address=validated_data['doctor_address'],
            # doctor_area=validated_data['doctor_area'],
            # =validated_data['category_name'],
            doctor_specialization=validated_data['doctor_specialization'],
            doctor_qualification=validated_data['doctor_qualification'],
            doctor_territory=validated_data['doctor_territory'],
            doctor_nmc_number=validated_data['doctor_nmc_number'],
            doctor_category=validated_data['doctor_category'],
            mpo_name=validated_data['mpo_name'],
            is_investment=validated_data['is_investment']
        )
    
    def update(self, instance, validated_data):
        instance.doctor_name = validated_data.get('doctor_name')
        instance.doctor_address = validated_data.get('doctor_address')
        instance.doctor_gender = validated_data.get('doctor_gender')
        instance.doctor_phone_number = validated_data.get('doctor_phone_number')
        instance.doctor_category = validated_data.get('doctor_category')
        instance.doctor_territory = validated_data.get('doctor_territory')
        instance.doctor_qualification = validated_data.get('doctor_qualification')
        instance.doctor_specialization = validated_data.get('doctor_specialization')
        instance.doctor_nmc_number = validated_data.get('doctor_nmc_number')
        instance.company_name = validated_data.get('company_name')
        instance.mpo_name = validated_data.get('mpo_name')
        instance.is_investment = validated_data.get('is_investment')
        instance.save()
        return instance


class DoctorSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'


class DoctorEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorEvents
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['mpo_id'] = CompanyUserRoleSerializers(
            instance.mpo_id
        ).data
        response['doctor_id'] = CompanyWiseDoctorSerializer(
            instance.doctor_id
        ).data
        return response
