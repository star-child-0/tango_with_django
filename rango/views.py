from django.shortcuts import render
from rango.models import Category, Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    return render(request, 'rango/index.html', context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    urlpatterns = [
        path('', views.index, name='index'),
        path('about/', views.about, name='about'),
        path('category/<slug:category_name_slug>/',
             views.show_category, name='show_category'),
    ]
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context_dict)
