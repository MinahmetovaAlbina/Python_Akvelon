from django.urls import path

from . import views

app_name = 'tinyurl'
urlpatterns = [
    # /tinyurl/
    path('', views.IndexView.as_view(), name='index'),
    # /tinyurl/4/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # /tinyurl/create/
    path('create/', views.create, name='create'),
    # /tinyurl/<3/some_hash
    path(':3/<my_hash>', views.tiny_url, name='tiny_url'),
]
