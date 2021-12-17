from rest_framework import serializers

from sales.models import sales

class FindByRankSerializer(serializers.ModelSerializer):
    class Meta:
        model = sales
        fields = ['Rank','Name','Platform','Year','Genre','Publisher','NA_Sales','EU_Sales','JP_Sales','Other_sales','Global_sales']

        def eugtna(self,sales:sales):
            if sales.EU_Sales > sales.NA_Sales :
                return True
            else:
                return False

class EuGtNaSerializer(serializers.ModelSerializer):
    class Meta:
        model = sales
        fields = ['Name','NA_Sales','EU_Sales']

class CompareTwoGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = sales
        fields = ['Name','NA_Sales','EU_Sales','JP_Sales','Other_sales','Global_sales']
