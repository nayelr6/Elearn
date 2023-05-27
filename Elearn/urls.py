"""
URL configuration for Elearn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from certification.views import CertificationListView, CertificationDetailView, CertificationCreateView, CertificationDeleteView, CertificationUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("course.urls")),
    path('home/', user_views.home, name='home'),
    path('contact/', user_views.contact, name='contact'),
    path('about/', user_views.about, name='about'),
    path('register/', user_views.register, name="register"),
    path('login/', LoginView.as_view(template_name="users/login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('enrolled/', include('enrollment.urls')),
    path('purchased/', include('coursePayment.urls')),
    path('profile/', user_views.profile, name='user-profile'),
    path('search/', include('search.urls')),
    path('instructor/<int:pk>/', user_views.instructorInfo, name="instructor-info"),
    path('certifications/', CertificationListView.as_view(),
         name="certification-list"),
    path('certifications/<int:pk>/', CertificationDetailView.as_view(),
         name="certification-detail"),
    path('certifications/new/', CertificationCreateView.as_view(),
         name="certification-new"),
    path('certifications/<int:pk>/update/',
         CertificationUpdateView.as_view(), name="certification-update"),
    path('certifications/<int:pk>/delete/',
         CertificationDeleteView.as_view(), name="certification-delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)