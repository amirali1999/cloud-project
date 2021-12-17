from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('findbyrank/<int:rank>/', views.FindByRank.as_view()),
    path('findbyname/<str:name>/', views.FindByName.as_view()),
    path('nplatform/<int:n>/<str:platform>/', views.NPlatform.as_view()),
    path('nyear/<int:n>/<int:year>/', views.NYear.as_view()),
    path('ngenre/<int:n>/<str:genre>/', views.NGenre.as_view()),
    path('topfive/<int:year>/<str:platform>/', views.TopFiveInYearAndPlatform.as_view()),
    path('eugtna/',views.EuGtNa.as_view()),
    path('comparetwogame/<str:first_game>/<str:secend_game>/',views.CompareTwoGame.as_view()),
    path('comparesaleyear/<int:year1>/<int:year2>/',views.CompareSaleYear.as_view()),
    path('comparesalepublisher/<int:year1>/<int:year2>/<str:publisher1>/<str:publisher2>/',views.CompareSalePublisher.as_view()),
    path('comparesalegenre/<int:year1>/<int:year2>/<str:genre1>/<str:genre2>',views.CompareSaleGenre.as_view()),
]
