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
    # /tinyurl/create_post/
    path('create_post/', views.create_post, name='create_post'),
    # /tinyurl/:3/some_hash
    path(':3/<my_hash>', views.tiny_url, name='tiny_url'),
    # /tinyurl/delete/
    path('delete/', views.delete, name='delete'),
]
