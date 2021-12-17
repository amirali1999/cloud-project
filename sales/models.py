from django.db import models

# Create your models here.
class sales (models.Model):
    Rank = models.IntegerField()
    Name = models.CharField(max_length=255)
    Platform = models.CharField(max_length=255)
    Year = models.IntegerField()
    Genre = models.CharField(max_length=255)
    Publisher = models.CharField(max_length=255)
    NA_Sales = models.DecimalField(max_digits=4,decimal_places=2)
    EU_Sales = models.DecimalField(max_digits=4,decimal_places=2)
    JP_Sales = models.DecimalField(max_digits=4,decimal_places=2)
    Other_sales = models.DecimalField(max_digits=4,decimal_places=2)
    Global_sales = models.DecimalField(max_digits=4,decimal_places=2)

    def __str__(self) -> str:
        return self.Name
    
    class Meta:
        ordering = ['Year']