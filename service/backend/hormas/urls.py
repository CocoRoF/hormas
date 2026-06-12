from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RaraModelView, CustomRaraModelView, RaraRatingView, RaraSurveyView

urlpatterns = [
    path("basic/", RaraModelView.as_view(), name="Basic_Response_Model"),
    path("custom/", CustomRaraModelView.as_view(), name="Custom_Response_Model"),
    path("rating/", RaraRatingView.as_view(), name="Response_Rating_Save"),
    path("survey/", RaraSurveyView.as_view(), name="Response_Survey_Save"),
]
