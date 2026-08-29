from rest_framework.views import APIView as ApiView
from rest_framework.response import Response
from project.models import Project
from project.serializers import ProjectSerializer
from rest_framework.request import Request
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class ProjectView(ApiView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None):
        body = request.data
        serialized_body = ProjectSerializer(data=body)

        if (not serialized_body.is_valid()):
            return Response({'message': 'El objeto no es válido', 'errors': serialized_body.errors}, status=400)

        new_project = Project.objects.create(**serialized_body.data)
        parsed_new_project = ProjectSerializer(new_project)

        return Response(parsed_new_project.data.get('id'), status=201)

    @csrf_exempt
    def delete(self, request: Request, id):
        projects = Project.objects.all()
        found_project = projects.get(id=id)
        
        if (not found_project):
            return Response('No se encontró ningún proyecto', status=404)
    
        deletion = found_project.delete()

        if (deletion.count == 0):
            return Response('No se pudo borrar el elemento', status=500)

        return Response(status=204)
