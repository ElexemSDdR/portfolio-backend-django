from django.urls import path
from experience.views import ExperienceView

urlpatterns = [
    path('experience/', ExperienceView.as_view()),
    path('experience/<uuid:id>', ExperienceView.as_view())
]
