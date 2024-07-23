from django.db import models

class RawData(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    edad = models.DateField()

class TransformedData(models.Model):
    nombre_completo = models.CharField(max_length=100)
    edad_nominal = models.IntegerField()
