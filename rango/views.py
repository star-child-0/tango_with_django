from typing import no_type_check_decorator
from django.core.files.base import ContentFile
from django.forms import renderers
from django.http import request, response
from django.shortcuts import render, resolve_url
#from rango.admin import CategoryAdmin
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from datetime import datetime
from rango.bing_search import run_query, read_bing_key
from django.contrib.auth.decorators import login_required
from django import HttpResponse


def index(request):
	request.session.set_cookie()
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list, 'pages': page_list}
	visitor_cookie_handler(request)
	context_dict['visits'] = request.session['visits']
	response = render(request, 'rango/index.html', context_dict)
	return response


def about(request):
	if request.session.test_cookie_worked():
		print("Test cookie worked")
		request.session.delete_test_cookie()
	return render(request, 'rango/about.html')


def show_category(request, category_name_slug):
	context_dict = {}

	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category

	except Category.DoesNotExist:
		context_dict['pages'] = None
		context_dict['category'] = None
	return render(request, 'rango/category.html', context_dict)


def add_category(request):
	form = CategoryForm()

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)

		else:
			print(form.errors)

	return render(request, 'rango/add_category.html', {'form': form})


def add_page(requst, category_name_slug):
	try:
		category = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
		category = None

	form = PageForm()
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			if category:
				page = form.save(commit=False)
				page.category = category
				page.views = 0
				page.save()
				return show_category(request, category_name_slug)
		else:
			print(form.errors)

	context_dict = {'from': form, 'category': category}
	return render(request, 'rango/add_page.html', context_dict)


def get_server_side_cookie(request, cookie, default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val


def visitor_cookie_handler(request):
	visits = int(get_server_side_cookie(request, 'visits', '1'))
	last_visit_cookie = get_server_side_cookie(
		request, 'last_visit', str(datetime.now()))
	last_visit_time = datetime.strptime(
		last_visit_cookie[:-7], '%Y-%m-%d %H-%M-%S')

	if (datetime.now() - last_visit_time).days > 0:
		visits = visits + 1
		request.session['last_visit'] = str(datetime.now())
	else:
		request.session['last_visit'] = last_visit_cookie
	response.session['visits'] = visits


def search(request):
	result_list = []

	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			result_list = run_query(query)
	return render(request, 'rango/search.html', {'result_list': result_list})


@login_required
def like_category(request):
	cat_id = None
	if request.method == 'GET':
		cat_id = request.GET['category_id']
		likes = 0
	if cat_id:
		cat = Category.objects.get(id=int(cat_id))
		if cat:
			likes = cat.likes + 1
			cat.likes = likes
			cat.save()
	return HttpResponse(likes)


def get_category_list(max_results=0, starts_with=''):
	cat_list = []
	if starts_with:
		cat_list = Category.objects.filter(name__istartswith=starts_with)

	if max_results > 0:
		if len(cat_list) > max_results:
			cat_list = cat_list[:max_results]
	return cat_list


def suggest_category(request):
	cat_list = []
	starts_with = ''

	if request.method == 'GET':
		starts_with = request.GET['suggestion']

	cat_list = get_category_list(8, starts_with)
	if len(cat_list) == 0:
		cat_list = Category.objects.order_by('-likes')


@login_required
def auto_add_page(request):
	cat_id = None
	url = None
	titl = None
	context_dict = {}
	if request.method == 'GET':
		cat_id = request.GET['category_id']
		url = request.GET['URL']
		title = request.GET['title']
		if cat_id:
			category = Category.objects.get(id=int(cat_id))
			p = Page.objects.get_or_create(
				category=category, title=title, url=url)
			pages = Page.objects.filter(category=category).order_by('-views')
			context_dict['pages'] = pages
	return render(request, 'rango/page_list.html')
