"""
URL configuration for TestTick project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('results/', include('results.urls')),
#     path('analytics/', include('analytics.urls')),
#     path('api/analytics/', include('analytics.api_urls')),

# ]


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [

    path('admin/', admin.site.urls),

    
    # path('about/', TemplateView.as_view(template_name="pages/about.html"), name='about'),
    # path('contact/', TemplateView.as_view(template_name="pages/contact.html"), name='contact'),
    # path('event/', TemplateView.as_view(template_name="pages/event.html"), name='event'),
    # path('menu/', TemplateView.as_view(template_name="pages/menu.html"), name='menu'),
    # path('service/', TemplateView.as_view(template_name="pages/service.html"), name='service'),

    # App URLs
    path('', include('pages.urls')),
    path('users/', include('users.urls')),
    path('quiz/', include('quiz.urls')),
    path('results/', include('results.urls')),
    path('dashboard/', include('dashboard.urls')),



    # API URLs (if you're using DRF for APIs)
    # path('api/users/', include('users.api.urls')),       # example
    # path('api/quiz/', include('quiz.api.urls')),         # example
    # path('api/results/', include('results.api.urls')),   # example

    # Auth (optional if using dj-rest-auth, djoser, or custom APIs)
    # path('auth/', include('rest_framework.urls')),
]

# Static & Media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

