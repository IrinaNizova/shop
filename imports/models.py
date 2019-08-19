from django.db import models
from django.contrib.postgres.fields import ArrayField

class Person(models.Model):
    class Meta:
        unique_together = (('import_id', 'citizen_id'),)

    GENDERS = (('male', 'male'), ('female', 'female'))
    import_id = models.IntegerField(null=False)
    citizen_id = models.IntegerField(null=False)
    town = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.CharField(max_length=50)
    appartement = models.SmallIntegerField()
    name = models.CharField(max_length=200, null=False)
    birth_date = models.DateTimeField()
    gender = models.CharField(max_length=10, choices=GENDERS, help_text="Male or Female")
    relatives = ArrayField(models.IntegerField(), size=20)

    def __str__(self):
        return " ".join((self.name, str(self.birth_date), self.town))