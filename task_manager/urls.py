"""
URL configuration for task_manager project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path, include
from tasks.views import home_view
from tasks.views import about_us_view
from tasks.views import contact_us
from tasks import views  # додайте цей рядок



urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="index"),
    path("tasks/", include("tasks.urls")),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("about-us/", about_us_view, name="about-us"),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('author/', views.author_view, name='author'),
    path('presentation/', views.presentation_view, name='presentation'),
    path('page-header/', views.page_header_view, name='page_header'),
    path('features/', views.features_view, name='features'),
    path('navbar/', views.navbars, name='navbar'),
    path('nav-tabs/', views.nav_tabs, name='nav_tabs'),
    path('pagination/', views.pagination_view, name='pagination'),
    path('inputs/', views.inputs_view, name='inputs'),
    path('forms/', views.forms_view, name='forms'),
    path('avatars/', views.avatars_view, name='avatars'),
    path('badges/', views.badges_view, name='badges'),
    path('breadcrumbs/', views.breadcrumbs_view, name='breadcrumbs'),
    path('buttons/', views.buttons_view, name='buttons'),
    path('dropdowns/', views.dropdowns_view, name='dropdowns'),
    path('progress-bars/', views.progress_bars_view, name='progress_bars'),
    path('toggles/', views.toggles_view, name='toggles'),
    path('typography/', views.typography_view, name='typography'),
    path('alerts/', views.alerts_view, name='alerts'),
    path('modals/', views.modals_view, name='modals'),
    path('tooltips/', views.tooltips_view, name='tooltips'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
