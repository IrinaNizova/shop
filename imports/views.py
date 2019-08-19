from datetime import datetime, timezone
from collections import Counter
from imports.models import Person
from imports.serializers import PersonSerializer

from django.db.models import Max

from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail


class PersonLoad(APIView):
    queryset = Person.objects.all()

    def post(self, request, *args, **kwargs):
        import_id = self.get_import_id()
        if not isinstance(request.data, list):
            return Response("This method need list of objects. {} is not a valid data".format(request.data), status=status.HTTP_400_BAD_REQUEST)
        for person in request.data:
            if not isinstance(person, dict):
                return Response("Object must be a dict. {} is not a dict".format(request.data), status=status.HTTP_400_BAD_REQUEST)
            person["import_id"] = import_id
            serializer = PersonSerializer(data=person)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data": {"import_id": import_id}}, status=status.HTTP_201_CREATED)

    def get_import_id(self):
        if not Person.objects.all():
            return 1
        return Person.objects.all().aggregate(Max('import_id'))['import_id__max']+1


class PersonPatch(generics.GenericAPIView):

    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def patch(self, request, pk, citizen_pk, *args, **kwargs):
        if 'citizen_id' in request.data:
            return Response({'citizen_id': [ErrorDetail(string='Citizen id is not modified field', code='null')]}, status=status.HTTP_400_BAD_REQUEST)
        null_values = [r for r in request.data if request.data[r] is None]
        if any(null_values):
            error_dict = {}
            for null_value in null_values:
                error_dict[null_value] = [ErrorDetail(string='{} must be not null'.format(null_value), code='null')]
            return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.queryset = Person.objects.get(import_id=pk, citizen_id=citizen_pk)
        except Person.DoesNotExist:
            return Response("", status=status.HTTP_404_NOT_FOUND)
        serializer = PersonSerializer(self.queryset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            del data["import_id"]
            return Response({"data": data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonSet(mixins.ListModelMixin,
                  generics.GenericAPIView):

    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get(self, request, pk, *args, **kwargs):
        self.queryset = Person.objects.filter(import_id=pk)
        if not self.queryset:
            return Response('{} is not valid import id'.format(pk), status=status.HTTP_400_BAD_REQUEST)
        return self.list(request, *args, **kwargs)

class PresetnsStatistics(APIView):

    def get(self, request, pk, *args, **kwargs):
        month_dict = {}
        import_persons = Person.objects.filter(import_id=pk)
        for i in range(1, 13):
            month_dict[i] = []
            birth_in_month = [p['citizen_id'] for p in import_persons.filter(birth_date__month=i).values('citizen_id')]
            relatives_in_month = Counter()
            for birth_person in birth_in_month:
                byuers = [p['citizen_id'] for p in import_persons.filter(relatives__contains=[birth_person]).values('citizen_id')]
                relatives_in_month += Counter(byuers)
            for citizen, presents in relatives_in_month.items():
                month_dict[i].append({"citizen_id": citizen, "presents": presents})
        return Response(month_dict)



class TownStatistics(APIView):

    def get(self, request, pk, *args, **kwargs):
        import_persons = Person.objects.filter(import_id=pk)
        towns = import_persons.distinct('town').values('town')
        towns_dict = []
        for town in towns:
            town_person = import_persons.filter(town=town['town']).order_by('-birth_date')
            count_persons = town_person.count()-1
            get_persentile = lambda x: int((datetime.now(timezone.utc) - town_person[x].birth_date).days//365.25)
            p50 = get_persentile(round(count_persons//2))
            p75 = get_persentile(round(count_persons*0.75))
            p99 = get_persentile(round(count_persons*0.99))
            towns_dict.append(dict(town=town['town'], p50=p50, p75=p75, p99=p99))
        return Response(towns_dict)

