from django.urls import path

from . import views

app_name = 'tinyurl'
urlpatterns = [
    # /tinyurl/
    path('', views.index, name='index'),
    # /tinyurl/4/
    path('<int:myurl_id>/', views.detail, name='detail')
]
