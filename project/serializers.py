from rest_framework import serializers
from project.models import Project

MAX_URL_LENGTH = 255

class ProjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=5, required=True, allow_null=False, allow_blank=False)
    description = serializers.CharField(min_length=10, required=True, allow_null=False, allow_blank=False)
    url = serializers.URLField(max_length=MAX_URL_LENGTH, required=True, allow_null=False, allow_blank=False)
    technologies = serializers.ListField(required=True, allow_null=False, allow_empty=False, min_length=1, child=serializers.CharField(required=True, min_length=2))
    githubrepo = serializers.URLField(required=False, allow_null=False, allow_blank=True, max_length=MAX_URL_LENGTH)

    class Meta:
        model = Project
        fields = '__all__'
