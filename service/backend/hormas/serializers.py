from rest_framework import serializers
from .models import RaraModel, RaraSurveyModel

class RaraModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaraModel
        fields = [
            "model",
            "inputText",
            "analysis_model",
            "response_method",
            "user_rating",
        ]
        extra_kwargs = {"user_rating": {"required": False}}


class CustomRaraModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaraModel
        fields = [
            "model",
            "inputText",
            "responder_name",
            "contact",
            "retrieval",
            "user_rating",
            "response_method",
            "analysis_model",
        ]
        extra_kwargs = {
            "responder_name": {"required": False},
            "contact": {"required": False},
            "retrieval": {"required": False},
            "user_rating": {"required": False},
        }


class RaraRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaraModel
        fields = [
            "model",
            "inputText",
            "response",
            "analysis_model",
            "response_method",
            "user_rating",
        ]


class RaraSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = RaraSurveyModel
        fields = [
            "name", 
            "organization", 
            "contact", 
            "email", 
            "dataidx", 
            "select_value"
        ]

        extra_kwargs = {
            "contact": {"required": False}, 
            "email": {"required": False}
        }
