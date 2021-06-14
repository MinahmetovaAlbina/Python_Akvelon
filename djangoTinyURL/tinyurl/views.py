from django.db.models import F
from django.http import HttpResponseRedirect, Http404, HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import generic
from django.urls import reverse

from .models import MyUrl
from .hash import get_hash


def get_most_frequently_used():
    return MyUrl.objects.order_by('-num_of_uses')


class IndexView(generic.ListView):
    template_name = 'tinyurl/index.html'
    context_object_name = 'most_frequently_used'

    # set of all MyUrls sorted by number of uses
    def get_queryset(self):
        return get_most_frequently_used()


def index(request):
    return render(request, 'tinyurl/index.html', {'most_frequently_used':  get_most_frequently_used()})


def delete(request):
    try:
        deleted_id = request.POST['deleted_my_url']
    except KeyError:
        return render(request, 'tinyurl/index.html', {
            'most_frequently_used': get_most_frequently_used(),
            'error_message': "You haven't selected anything to delete"
        })
    else:
        try:
            MyUrl.objects.filter(id=deleted_id)
        except MyUrl.DoesNotExist:
            return render(request, 'tinyurl/index.html', {
                'most_frequently_used': get_most_frequently_used(),
                'error_message': "You haven't selected anything to delete"
            })
        else:
            MyUrl.objects.filter(id=deleted_id).delete()
            return render(request, 'tinyurl/index.html', {
                'most_frequently_used':  get_most_frequently_used(),
                'success_message': 'Tiny URL has been deleted successfully'
            })


class DetailView(generic.DetailView):
    template_name = 'tinyurl/detail.html'
    model = MyUrl


def create(request):
    try:
        original_url = request.POST['original_url']
    except KeyError:
        return render(request, 'tinyurl/create.html', {
                'error_message': "Key error"
            })
    else:
        # if the original url is empty
        if original_url is None or original_url is '':
            return render(request, 'tinyurl/create.html', {
                'error_message': "You didn't give me any url ;("
            })
        else:
            # find this original url in DB
            duplicate_url = MyUrl.objects.filter(original_url=original_url).first()
            # if MyUrl with this original_url already exists
            if duplicate_url is not None:
                return render(request, 'tinyurl/create.html', {
                    'error_message': "I already made a tiny url for this one"
                })
            else:
                # generate a MyUrl
                my_url = MyUrl.objects.create(original_url=original_url, hash=get_hash(original_url),
                                              pub_date=timezone.now(), last_us_date=timezone.now(), num_of_uses=0)
                # save the changes in DB
                my_url.save()
                # redirect to the detail page
                return redirect(reverse('tinyurl:detail', args=(my_url.id,)))


# redirects to the original url from the tiny url
def tiny_url(request, my_hash):
    my_url = MyUrl.objects.filter(hash=my_hash).first()
    # if MyUrl with the given hash doesn't exist
    if my_url is None:
        raise Http404("Page does not exist")
    else:
        # increase number of uses
        my_url.num_of_uses = F('num_of_uses') + 1
        # update the last use date
        my_url.last_us_date = timezone.now()
        # save the changes in DB
        my_url.save()
        return redirect(my_url.original_url, permanent=True)
