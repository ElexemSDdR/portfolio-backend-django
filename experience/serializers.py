from rest_framework import serializers
from experience.models import Experience

class ExperienceSerializer(serializers.ModelSerializer):
    jobname = serializers.CharField(min_length=5, required=True, allow_null=False, allow_blank=False)
    date = serializers.CharField(min_length=11, required=True, allow_null=False, allow_blank=False)
    jobposition = serializers.CharField(min_length=10, required=True, allow_null=False, allow_blank=False)

    class Meta:
        model = Experience
        fields = '__all__'
