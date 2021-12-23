from django.shortcuts import render
from django.urls import path
from rango import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/',
         views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('like$', views.like_category, name='like_category'),
    path('suggest/', views.suggest_category, name='suggest_category'),
    path('add/', views.auto_add_page, name='auto_add_page'),
]


def about(request):
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', {})
