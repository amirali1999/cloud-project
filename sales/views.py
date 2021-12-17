import json
from django.db.models import query
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView
from rest_framework.mixins import ListModelMixin , CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from sales.filters import ProductFilter
from django.db.models import F
from django.db.models import Q
from .models import sales
from .serializers import FindByRankSerializer , EuGtNaSerializer , CompareTwoGameSerializer
from sales import serializers
from django.http import JsonResponse


class FindByRank(APIView):
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination
    def get(self,request,rank):
        giverank = sales.objects.get(Rank=rank)
        serializer = FindByRankSerializer(giverank)
        return Response(serializer.data)

        
class FindByName(APIView):
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination
    def get(self,request,name):
        givename = sales.objects.filter(Name__icontains = name)
        serializer = FindByRankSerializer(givename,many=True)
        return Response(serializer.data)

class NPlatform(APIView):
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination
    def get(self,request,n,platform):
        nn = sales.objects.filter(Platform=platform).order_by('Rank')[:n]
        serializer = FindByRankSerializer(nn,many=True)
        return Response(serializer.data)

class NYear(APIView):
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination
    def get(self,request,n,year):
        nn = sales.objects.filter(Year=year).order_by('Rank')[:n]
        serializer = FindByRankSerializer(nn,many=True)
        return Response(serializer.data)

class NGenre(APIView):
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination
    def get(self,request,n,genre):
        nn = sales.objects.filter(Genre=genre).order_by('Rank')[:n]
        serializer = FindByRankSerializer(nn,many=True)
        return Response(serializer.data)

class TopFiveInYearAndPlatform(APIView):
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination
    def get(self,request,year,platform):
        nn = sales.objects.filter(Year=year).filter(Platform=platform).order_by('Rank')[:5]
        serializer = FindByRankSerializer(nn,many=True)
        return Response(serializer.data)


class EuGtNa(APIView):
    permission_classes = [IsAuthenticated]
    # pagination_class = PageNumberPagination
    def get(self,request):
        nn = sales.objects.filter(EU_Sales__gt = F('NA_Sales'))
        serializer = EuGtNaSerializer(nn,many=True)
        return Response(serializer.data)      

class CompareTwoGame(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,first_game,secend_game):
        first_queryset = sales.objects.filter(Name = first_game)

        secend_queryset = sales.objects.filter(Name = secend_game)
        name1= first_game
        NA_Sales_1=0
        EU_Sales_1=0
        JP_Sales_1=0
        Other_sales_1=0
        Global_sales_1=0
        NA_Sales_2=0
        EU_Sales_2=0
        JP_Sales_2=0
        Other_sales_2=0
        Global_sales_2=0
        for guery1 in first_queryset:
            NA_Sales_1 = NA_Sales_1 + guery1.NA_Sales
            EU_Sales_1 = EU_Sales_1 + guery1.EU_Sales
            JP_Sales_1 = JP_Sales_1 + guery1.JP_Sales
            Other_sales_1 = Other_sales_1 + guery1.Other_sales
            Global_sales_1 = Global_sales_1 + guery1.Global_sales
        
        for guery2 in secend_queryset:
            NA_Sales_2 = NA_Sales_2 + guery2.NA_Sales
            EU_Sales_2 = EU_Sales_2 + guery2.EU_Sales
            JP_Sales_2 = JP_Sales_2 + guery2.JP_Sales
            Other_sales_2 = Other_sales_2 + guery2.Other_sales
            Global_sales_2 = Global_sales_2 + guery2.Global_sales
        
        g1={
            'Name': first_game,
            'NA_Sales': NA_Sales_1,
            'EU_Sales': EU_Sales_1,
            'JP_Sales': JP_Sales_1,
            'Other_sales': Other_sales_1,
            'Global_sales': Global_sales_1,
        }
        g2={
            'Name': secend_game,
            'NA_Sales': NA_Sales_2,
            'EU_Sales': EU_Sales_2,
            'JP_Sales': JP_Sales_2,
            'Other_sales': Other_sales_2,
            'Global_sales': Global_sales_2,
        }
        Serializer_list = [g1,g2]

        return Response(Serializer_list)

class CompareSaleYear(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,year1,year2):
        queryset = sales.objects.filter(Year__range =(year1,year2))
        x=0
        num = year2-year1
        year = [0]*(num+1)
        na_sales=[0]*(num+1)
        eu_sales=[0]*(num+1)
        jp_sales=[0]*(num+1)
        other_sales=[0]*(num+1)
        global_sales=[0]*(num+1)
        dflt_year = year1
        for query in queryset:
            if query.Year == dflt_year :
                year[x] = query.Year
                na_sales[x] =na_sales[x]+ query.NA_Sales
                eu_sales[x] =eu_sales[x]+ query.EU_Sales
                jp_sales[x] =jp_sales[x]+ query.JP_Sales
                other_sales[x] =other_sales[x]+ query.Other_sales
                global_sales[x] =global_sales[x]+ query.Global_sales
            elif dflt_year != year2+1:
                dflt_year = dflt_year + 1
                x = x+1
                year[x] = query.Year
                na_sales[x] =na_sales[x]+ query.NA_Sales
                eu_sales[x] =eu_sales[x]+ query.EU_Sales
                jp_sales[x] =jp_sales[x]+ query.JP_Sales
                other_sales[x] =other_sales[x]+ query.Other_sales
                global_sales[x] =global_sales[x]+ query.Global_sales
        g = [0]*(num+1)
        for y in range(0,num+1):
            g[y] ={
            'Name': year[y],
            'NA_Sales': na_sales[y],
            'EU_Sales': eu_sales[y],
            'JP_Sales': jp_sales[y],
            'Other_sales': other_sales[y],
            'Global_sales': global_sales[y],
            }   
        Serializer_list = [g]
        return Response(Serializer_list)


class CompareSalePublisher(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,year1,year2,publisher1,publisher2):
        queryset1 = sales.objects.filter(Year__range =(year1,year2)).filter(Publisher=publisher1)
        queryset2 = sales.objects.filter(Year__range =(year1,year2)).filter(Publisher=publisher2)
        NA_Sales_1=0
        EU_Sales_1=0
        JP_Sales_1=0
        Other_sales_1=0
        Global_sales_1=0
        NA_Sales_2=0
        EU_Sales_2=0
        JP_Sales_2=0
        Other_sales_2=0
        Global_sales_2=0
        dflt_year = year1
        for query1 in queryset1:
            if query1.Year == dflt_year :
                NA_Sales_1 = NA_Sales_1 + query1.NA_Sales
                EU_Sales_1 = EU_Sales_1 + query1.EU_Sales
                JP_Sales_1 = JP_Sales_1 + query1.JP_Sales
                Other_sales_1 = Other_sales_1 + query1.Other_sales
                Global_sales_1 = Global_sales_1 + query1.Global_sales
            elif dflt_year != year2+1:
                dflt_year = dflt_year + 1
                NA_Sales_1 = NA_Sales_1 + query1.NA_Sales
                EU_Sales_1 = EU_Sales_1 + query1.EU_Sales
                JP_Sales_1 = JP_Sales_1 + query1.JP_Sales
                Other_sales_1 = Other_sales_1 + query1.Other_sales
                Global_sales_1 = Global_sales_1 + query1.Global_sales
        dflt_year = year1
        for query2 in queryset2:
            if query2.Year == dflt_year :
                NA_Sales_2 = NA_Sales_2 + query2.NA_Sales
                EU_Sales_2 = EU_Sales_2 + query2.EU_Sales
                JP_Sales_2 = JP_Sales_2 + query2.JP_Sales
                Other_sales_2 = Other_sales_2 + query2.Other_sales
                Global_sales_2 = Global_sales_2 + query2.Global_sales
            elif dflt_year != year2+1:
                dflt_year = dflt_year + 1
                NA_Sales_2 = NA_Sales_2 + query2.NA_Sales
                EU_Sales_2 = EU_Sales_2 + query2.EU_Sales
                JP_Sales_2 = JP_Sales_2 + query2.JP_Sales
                Other_sales_2 = Other_sales_2 + query2.Other_sales
                Global_sales_2 = Global_sales_2 + query2.Global_sales
        p1={
            'Name': publisher1,
            'NA_Sales': NA_Sales_1,
            'EU_Sales': EU_Sales_1,
            'JP_Sales': JP_Sales_1,
            'Other_sales': Other_sales_1,
            'Global_sales': Global_sales_1,
        }
        p2={
            'Name': publisher2,
            'NA_Sales': NA_Sales_2,
            'EU_Sales': EU_Sales_2,
            'JP_Sales': JP_Sales_2,
            'Other_sales': Other_sales_2,
            'Global_sales': Global_sales_2,
        }
        Serializer_list = [p1,p2]
        return Response(Serializer_list)


class CompareSaleGenre(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,year1,year2,genre1,genre2):
        queryset1 = sales.objects.filter(Year__range =(year1,year2)).filter(Genre=genre1)
        queryset2 = sales.objects.filter(Year__range =(year1,year2)).filter(Genre=genre2)
        NA_Sales_1=0
        EU_Sales_1=0
        JP_Sales_1=0
        Other_sales_1=0
        Global_sales_1=0
        NA_Sales_2=0
        EU_Sales_2=0
        JP_Sales_2=0
        Other_sales_2=0
        Global_sales_2=0
        dflt_year = year1
        for query1 in queryset1:
            if query1.Year == dflt_year :
                NA_Sales_1 = NA_Sales_1 + query1.NA_Sales
                EU_Sales_1 = EU_Sales_1 + query1.EU_Sales
                JP_Sales_1 = JP_Sales_1 + query1.JP_Sales
                Other_sales_1 = Other_sales_1 + query1.Other_sales
                Global_sales_1 = Global_sales_1 + query1.Global_sales
            elif dflt_year != year2+1:
                dflt_year = dflt_year + 1
                NA_Sales_1 = NA_Sales_1 + query1.NA_Sales
                EU_Sales_1 = EU_Sales_1 + query1.EU_Sales
                JP_Sales_1 = JP_Sales_1 + query1.JP_Sales
                Other_sales_1 = Other_sales_1 + query1.Other_sales
                Global_sales_1 = Global_sales_1 + query1.Global_sales
        dflt_year = year1
        for query2 in queryset2:
            if query2.Year == dflt_year :
                NA_Sales_2 = NA_Sales_2 + query2.NA_Sales
                EU_Sales_2 = EU_Sales_2 + query2.EU_Sales
                JP_Sales_2 = JP_Sales_2 + query2.JP_Sales
                Other_sales_2 = Other_sales_2 + query2.Other_sales
                Global_sales_2 = Global_sales_2 + query2.Global_sales
            elif dflt_year != year2+1:
                dflt_year = dflt_year + 1
                NA_Sales_2 = NA_Sales_2 + query2.NA_Sales
                EU_Sales_2 = EU_Sales_2 + query2.EU_Sales
                JP_Sales_2 = JP_Sales_2 + query2.JP_Sales
                Other_sales_2 = Other_sales_2 + query2.Other_sales
                Global_sales_2 = Global_sales_2 + query2.Global_sales
        p1={
            'Genre': genre1,
            'NA_Sales': NA_Sales_1,
            'EU_Sales': EU_Sales_1,
            'JP_Sales': JP_Sales_1,
            'Other_sales': Other_sales_1,
            'Global_sales': Global_sales_1,
        }
        p2={
            'Genre': genre2,
            'NA_Sales': NA_Sales_2,
            'EU_Sales': EU_Sales_2,
            'JP_Sales': JP_Sales_2,
            'Other_sales': Other_sales_2,
            'Global_sales': Global_sales_2,
        }
        Serializer_list = [p1,p2]
        return Response(Serializer_list)