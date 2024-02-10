from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from event_ticketing_system.common.forms import SearchForm
from event_ticketing_system.common.models import Like
from event_ticketing_system.events.models import Event


def index(request):
    events = Event.objects.all()

    context = {'events': events}
    return render(request, 'common/home_page.html', context)


@login_required
def like_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    existing_like = Like.objects.filter(user=user, event=event).first()

    if existing_like:
        existing_like.delete()
    else:
        new_like_object = Like.objects.create(user=user, event=event)
        new_like_object.save()

    return redirect(request.META.get('HTTP_REFERER', reverse('index')))


@login_required
def liked_events_view(request):
    liked_events = Like.objects.filter(user=request.user)
    context = {
        'liked_events': liked_events
    }
    return render(request, 'events/../../templates/accounts/user_liked_events.html', context)


def search_results(request):
    search_form = SearchForm(request.GET)

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_text')
        events = Event.objects.filter(title__icontains=search_query)
    else:
        search_query = None
        events = Event.objects.all()

    context = {'events': events, 'search_form': search_form, 'search_query': search_query}
    return render(request, 'common/search_results.html', context)
