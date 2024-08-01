from rest_framework import serializers
from Chemist.serializers import CompanyWiseChemistSerializer
from DCRUser.serializers import CompanyUserRoleSerializers
from Doctors.serializers import CompanyWiseDoctorSerializer
from Stat.models import CompanyDCRTourPlanValidity, MPOMissedCallModel


class CompanyDCRTourPlanValiditySerializers(serializers.ModelSerializer):

    class Meta:
        model = CompanyDCRTourPlanValidity
        fields = "__all__"


class MPOMissedCallSerializers(serializers.ModelSerializer):

    class Meta:
        model = MPOMissedCallModel
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['mpo_name'] = CompanyUserRoleSerializers(instance.mpo_name).data
        response['doctor'] = CompanyWiseDoctorSerializer(instance.doctor).data
        response['chemist'] = CompanyWiseChemistSerializer(instance.chemist).data
        return response
