from django.db import models

# Create your models here.


class RaraModel(models.Model):
    model = models.CharField(max_length=30)
    analysis_model = models.CharField(max_length=30, null=True, blank=True)
    response_method = models.CharField(max_length=20)
    responder_name = models.CharField(max_length=50, null=True, blank=True)
    contact = models.CharField(max_length=1000, null=True, blank=True)
    retrieval = models.CharField(max_length=100000, null=True, blank=True)
    inputText = models.CharField(max_length=5000)
    response = models.CharField(max_length=5000, null=True, blank=True)
    user_rating = models.IntegerField(null=True, blank=True)
    time = models.DateTimeField()

    def __str__(self):
        return self.model

class RaraSurveyModel(models.Model):
    name = models.CharField(max_length=30)
    organization = models.CharField(max_length=30)
    contact = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    dataidx = models.IntegerField()
    select_value = models.IntegerField()
    time = models.DateTimeField()

    def __str__(self):
        return self.name
