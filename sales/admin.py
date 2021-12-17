from django.contrib import admin
from . import models

class ProductAdmin(admin.ModelAdmin):
    list_display = ['Rank','Name','Platform','Year','Genre','Publisher','NA_Sales','EU_Sales','JP_Sales','Other_sales','Global_sales']

    list_per_page = 300
    search_fields = ['Rank','Name']


    
    

# admin.site.register(models.sales)
# Register your models here.
admin.site.register(models.sales,ProductAdmin)