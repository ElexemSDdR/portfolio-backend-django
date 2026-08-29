from rest_framework.views import APIView as ApiView, Response
from experience.models import Experience
from experience.serializers import ExperienceSerializer

# Create your views here.
class ExperienceView(ApiView):
    def get(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

# Create your views here.
