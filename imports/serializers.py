from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'citizen_id', 'import_id', 'town', 'street', 'building', 'appartement', 'birth_date', 'gender', 'relatives']
