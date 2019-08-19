from django.urls import path, include
from imports.views import PersonLoad, PersonSet, PersonPatch, TownStatistics, PresetnsStatistics


urlpatterns = [
    path('', PersonLoad.as_view()),
    path('<int:pk>/citizens', PersonSet.as_view()),
    path('<int:pk>/citizens/<int:citizen_pk>', PersonPatch.as_view()),
    path('<int:pk>/citizens/towns/stat/percentile/age', TownStatistics.as_view()),
    path('<int:pk>/citizens/birthdays', PresetnsStatistics.as_view())
]
