from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView as ApiView
from rest_framework.response import Response
from rest_framework.request import Request
from experience.models import Experience
from experience.serializers import ExperienceSerializer
import re

def validate_date(date: str):
    return True

# Create your views here.
class ExperienceView(ApiView):
    def get(self, _):
        experiences = Experience.objects.all()

        if (len(experiences) == 0):
            return Response({'message': 'No experiences were found.'}, status=404)

        serialized_experience = ExperienceSerializer(experiences, many=True).data
        return Response(serialized_experience)

    def post(self, request: Request, format=None):
        body = request.data

        if (body is None):
            return Response({'message': 'The body must not be empty.'}, status=400)

        serialized_body = ExperienceSerializer(data=body)

        if (type(body) is list):
            return Response({'message': 'The body has to be an object, not a list.'}, status=400)

        body = dict(request.data)

        if (not serialized_body.is_valid()):
            return Response({'message': 'The experience is not valid.', 'errors': serialized_body.errors}, status=400)

        date = str(body.get('date'))
        date_regex = re.search("^[0 -9]{4}\s-\s[0-9]{4}$|Actual$", date)

        if (date_regex is None):
            return Response({'message': 'Invalid date, it has to got a format like "2021 - 2022", "2021 - Actual" or similar'}, status=400)

        init_date = date.split(' - ')[0]
        end_date = date.split(' - ')[1]

        if (end_date != 'Actual' and int(init_date) > int(end_date)):
            return Response({'message': 'The initial year that becomes before the "-" must be lower than the year that becomes after that.'}, status=400)

        new_experience = Experience.objects.create(**serialized_body.data)
        parsed_new_experience = ExperienceSerializer(new_experience).data

        return Response(parsed_new_experience.get('id'), status=201)

    @csrf_exempt
    def delete(self, _, id=''):
        if (id == ''):
            return Response({'message': 'Missing experience ID.'}, status=400)

        try:
            experience = Experience.objects.get(id=id)
        except Experience.DoesNotExist:
            return Response({'message': f'No experiences with id {id} were found.'}, status=404)
    
        deletion = experience.delete()

        if (deletion.count == 0):
            return Response('The experience could not be deleted.', status=500)

        return Response(status=204)

    def patch(self, request: Request, id=''):
        if (id == ''):
            return Response({'message': 'Missing experience ID.'}, status=400)

        body = request.data

        if (body is None):
            return Response({'message': 'The body must not be empty.'}, status=400)

        if (type(body) is list):
            return Response({'message': 'The body has to be an object, not a list.'}, status=400)

        body = dict(request.data)

        try:
            experience = Experience.objects.get(id=id)
        except Experience.DoesNotExist:
            return Response({'message': f'No experiences with id {id} were found.'}, status=404)

        serialized_experience = ExperienceSerializer(experience).data

        for key, value in body.items():
            if (not serialized_experience.keys().__contains__(key)):
                return Response({'message': f'Could not update the experience, "{key}" key does not exists in experience object.'}, status=400)

            serialized_experience[key] = value
            edited_experience = ExperienceSerializer(data=serialized_experience)

            if (not edited_experience.is_valid()):
                return Response({'message': f'Could not update the "{key}" value.', 'errors': edited_experience.errors}, status=400)

            edited_experience.update(experience, edited_experience.data)

        return Response(status=204)

# Create your views here.
