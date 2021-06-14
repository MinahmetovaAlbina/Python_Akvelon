from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy, reverse

from .models import MyUrl
from .hash import get_hash


class IndexView(generic.ListView):
    template_name = 'tinyurl/index.html'
    context_object_name = 'most_frequently_used'

    def get_queryset(self):
        return MyUrl.objects.order_by('-num_of_uses')[:20]


class DetailView(generic.DetailView):
    template_name = 'tinyurl/detail.html'
    model = MyUrl


def create(request):
    try:
        original_url = request.POST['original_url']
    except KeyError:
        return render(request, 'tinyurl/create.html', {
            'error_message': "You didn't right an url"
        })
    else:
        my_url = MyUrl.objects.create(original_url=original_url, hash=get_hash(original_url),
                                      pub_date=timezone.now(), last_us_date=timezone.now(), num_of_uses=0)
        my_url.save()
        return HttpResponseRedirect(reverse('tinyurl:detail', args=(my_url.id,)))


def tiny_url(request, my_hash):
    my_url = MyUrl.objects.filter(hash=my_hash).first()
    if my_url is None:
        raise Http404("Page does not exist")
    else:
        return HttpResponseRedirect(my_url.original_url)
