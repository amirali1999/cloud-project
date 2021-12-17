from django_filters.rest_framework import FilterSet
from .models import sales

class ProductFilter(FilterSet):
    class Meta:
        model = sales
        fields = {
            'Name':['exact'],
            'Rank':['exact','lt'],
            'Year':['exact'],
            'Platform':['exact'],
            'Genre':['exact'],

        }