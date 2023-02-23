from django.contrib import admin
from django.urls import path, include, reverse
from rango import views
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView

urlpatterns = [
	path('', views.index, name='index'),
	path('rango/', include('rango.urls')),
	path('admin/', admin.site.urls),
	path('accouts/register/', MyRegistrationViews.as_view(),
		 name='registration_register'),
	path('accounts/', include('registration.backends.simple,urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


class MyRegistrationView(RegistrationView):
	def get_success_url(self, user):
		return reverse('index')
