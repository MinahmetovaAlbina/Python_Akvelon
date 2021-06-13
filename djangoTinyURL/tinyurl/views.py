from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import MyUrl


def index(request):
    most_frequently_used = MyUrl.objects.order_by('num_of_uses')[:5]
    context = {
        'most_frequently_used': most_frequently_used
    }
    return render(request, 'tinyurl/index.html', context)


def detail(request, myurl_id):
    myurl = get_object_or_404(MyUrl, pk=myurl_id)
    return render(request, 'tinyurl/detail.html', {'myurl': myurl})
