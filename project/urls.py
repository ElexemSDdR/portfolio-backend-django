from django.urls import path
from project.views import ProjectView

urlpatterns = [
        path('project/', ProjectView.as_view()),
        path('project/<uuid:id>', ProjectView.as_view())
]
