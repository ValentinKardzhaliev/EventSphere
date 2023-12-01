from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from event_ticketing_system.common.forms import SearchForm
from event_ticketing_system.common.models import Like
from event_ticketing_system.events.models import Event


def index(request):
    events = Event.objects.all()

    search_form = SearchForm(request.GET)

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search_text')

        if search_query:
            events = events.filter(title__icontains=search_query)
    else:
        # If the form is not valid, handle it accordingly (e.g., show an error message)
        search_query = None

    context = {'events': events, 'search_form': search_form, 'search_query': search_query}
    return render(request, 'common/home_page.html', context)


@login_required
def like_functionality(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    existing_like = Like.objects.filter(user=user, event=event).first()

    if existing_like:
        existing_like.delete()
    else:
        Like.objects.create(user=user, event=event)

    return redirect(request.META.get('HTTP_REFERER', reverse('index')))
