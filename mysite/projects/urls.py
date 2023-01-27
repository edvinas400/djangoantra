from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('manoprojektai/<int:pk>', views.ProjektaiDetailView.as_view(), name='projektas'),
    path('register/', views.register, name='register'),
    path('manoprojektai/', views.UserProjektaiListView.as_view(), name="manoprojektai"),
    path('projektai/', views.ProjektaiListView.as_view(), name="projektai"),
    path('projektai/<int:pk>', views.ProjektaiDetailView.as_view(), name='projektas'),
]