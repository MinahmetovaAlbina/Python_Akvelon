from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic
from django.urls import reverse_lazy, reverse

from .models import MyUrl


class IndexView(generic.ListView):
    template_name = 'tinyurl/index.html'
    context_object_name = 'most_frequently_used'

    def get_queryset(self):
        return MyUrl.objects.order_by('-num_of_uses')[:5]


class DetailView(generic.DetailView):
    model = MyUrl
    template_name = 'tinyurl/detail.html'


def create(request):
    try:
        tiny_url_text = request.POST['original_url']
    except KeyError:
        return render(request, 'tinyurl/create.html', {
            'error_message': "You didn't right an url"
        })
    else:
        my_url = MyUrl.objects.create(original_url=tiny_url_text, tiny_url=tiny_url_text,
                                      pub_date=timezone.now(), last_us_date=timezone.now(), num_of_uses=0)
        my_url.save()
        return HttpResponseRedirect(reverse('tinyurl:detail', args=(my_url.id,)))
