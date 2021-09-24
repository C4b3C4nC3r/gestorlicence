from django.db import models

# Create your models here.


class CodeLicence(models.Model):
    #manytomany
    #campos
    hash_licence = models.CharField(max_length=200)
    type_licence = models.IntegerField(null=True) #1-> 1 ano, NULL -> 6 meses
    create_at = models.DateTimeField(null=True) #fecha de la eliminacon => activo
    date_rem = models.DateTimeField(null=True) #fecha de la eliminacon => activo

    def __str__(self):
        return self.hash_licence

        
class Client(models.Model):
    #campos
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nci = models.CharField(max_length=10)
    number_phone = models.CharField(max_length=10)
    email = models.CharField(max_length=200)
    url_client = models.CharField(max_length=200)
    licences = models.ManyToManyField(CodeLicence,related_name='licences')
    def __str__(self):
            return self.name