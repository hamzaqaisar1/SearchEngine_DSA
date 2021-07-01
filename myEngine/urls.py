from django.urls import path

from . import views

app_name = 'myEngine'
# Setting up urls for the app
urlpatterns = [

    path('', views.index, name='index'),
    path('buildIndex',views.buildIndex,name="buildIndex"),

]