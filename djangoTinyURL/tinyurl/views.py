from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import MyUrl


class IndexView(generic.ListView):
    template_name = 'tinyurl/index.html'
    context_object_name = 'most_frequently_used'

    def get_queryset(self):
        return MyUrl.objects.order_by('-num_of_uses')[:5]


class DetailView(generic.DetailView):
    model = MyUrl
    template_name = 'tinyurl/detail.html'


class CreateView(generic.CreateView):
    model = MyUrl
    template_name = 'tinyurl/create.html'
    fields = ['original_url']
