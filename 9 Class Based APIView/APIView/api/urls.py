
from django.urls import path

from .views import StudentAPI

urlpatterns = [
        path('student/', StudentAPI.as_view(), name='student'),
        path('student/<int:id>/', StudentAPI.as_view(), name='student'),
]

