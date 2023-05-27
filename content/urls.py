from django.urls import path
from .views import ContentListView, ContentDetailView, ContentCreateView, ContentUpdateView, ContentDeleteView


urlpatterns = [
    path('content/', ContentListView.as_view(), name="content-list"),
    path('content/detail/<int:pk>/', ContentDetailView.as_view(), name="content-detail"),
]