from rest_framework.views import APIView as ApiView
from rest_framework.response import Response
from project.models import Project
from project.serializers import ProjectSerializer
from rest_framework.request import Request
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class ProjectView(ApiView):
    def get(self, _, id=''):
        if (not id):
            projects = Project.objects.all()

            if (len(projects) == 0):
                return Response({'message': 'No projects were found.'}, status=404)

            serialized_projects = ProjectSerializer(projects, many=True).data
            return Response(serialized_projects)
        else:
            try:
                project = Project.objects.get(id=id)
            except Project.DoesNotExist:
                return Response({'message': f'No project with id {id} was found.'}, status=404)

            serialized_project = ProjectSerializer(project).data

            return Response(serialized_project)


    def post(self, request: Request, format=None):
        body = request.data

        if (body is None):
            return Response({'message': 'The body must not be empty.'}, status=400)

        serialized_body = ProjectSerializer(data=body)

        if (not serialized_body.is_valid()):
            return Response({'message': 'The project is not valid.', 'errors': serialized_body.errors}, status=400)

        new_project = Project.objects.create(**serialized_body.data)
        parsed_new_project = ProjectSerializer(new_project).data

        return Response(parsed_new_project.get('id'), status=201)

    @csrf_exempt
    def delete(self, _, id=''):
        if (id == ''):
            return Response({'message': 'Missing project ID.'}, status=400)

        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            return Response({'message': f'No projects with id {id} were found.'}, status=404)
    
        deletion = project.delete()

        if (deletion.count == 0):
            return Response('The project could not be deleted.', status=500)

        return Response(status=204)

    def patch(self, request: Request, id=''):
        if (id == ''):
            return Response({'message': 'Missing project ID.'}, status=400)

        body = request.data

        if (body is None):
            return Response({'message': 'The body must not be empty.'}, status=400)

        if (type(body) is list):
            return Response({'message': 'The body has to be an object, not a list.'}, status=400)

        body = dict(body)

        try:
            project = Project.objects.get(id=id)
        except Project.DoesNotExist:
            return Response({'message': f'No projects with id {id} were found.'}, status=404)

        serialized_project = ProjectSerializer(project).data

        for key, value in body.items():
            if (not serialized_project.keys().__contains__(key)):
                return Response({'message': f'Could not update the project, "{key}" key does not exists in project object.'}, status=400)

            serialized_project[key] = value
            edited_project = ProjectSerializer(data=serialized_project)

            if (not edited_project.is_valid()):
                return Response({'message': f'Could not update the "{key}" value.', 'errors': edited_project.errors}, status=400)

            edited_project.update(project, edited_project.data)

        return Response(status=204)
