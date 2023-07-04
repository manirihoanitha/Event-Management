from django.shortcuts import render, get_object_or_404
from events.models import Event, Speaker, Participant, Payment
from django.utils import timezone
from django.db.models import Count
from django.db.models import Sum, Avg


def home(request):
    events = Event.objects.all()
    speakers = Speaker.objects.all()
    participants = Participant.objects.all()
    return render(request, 'home.html', {
        'events': events,
        'speakers': speakers,
        'participants': participants
    })

def list_events(request):
    events = Event.objects.all()
    return render(request, 'events/list.html', {'events': events})


def event_detail(request, title):
    event = get_object_or_404(Event, title=title)
    return render(request, 'events/detail.html', {'event': event})


def list_speakers(request):
    speakers = Speaker.objects.all()
    return render(request, 'speakers/list.html', {'speakers': speakers})


def speaker_detail(request, name):
    speaker = get_object_or_404(Speaker, name=name)
    return render(request, 'speakers/detail.html', {'speaker': speaker})


def list_participants(request):
    participants = Participant.objects.all()
    return render(request, 'participants/list.html', {'participants': participants})


def participant_detail(request, email):
    participant = get_object_or_404(Participant, email=email)
    return render(request, 'participants/detail.html', {'participant': participant})


def list_upcoming_events(request):
    events = Event.objects.filter(start_date__gte=timezone.now())
    return render(request, 'events/upcoming.html', {'events': events})

def list_free_events(request):
    events = Event.objects.filter(is_free=True)
    return render(request, 'events/free.html', {'events': events})

def list_paid_events(request):
    events = Event.objects.filter(is_free=False)
    return render(request, 'events/paid.html', {'events': events})

def event_participant_count(request):
    events = Event.objects.annotate(participant_count=Count('participants'))
    return render(request, 'events/event_participant_count.html', {'events': events})

def participant_event_count(request):
    participants = Participant.objects.annotate(event_count=Count('events'))
    return render(request, 'participants/participant_event_count.html', {'participants': participants})

def event_schedule_count(request):
    events = Event.objects.annotate(schedule_count=Count('schedules'))
    return render(request, 'events/event_schedule_count.html', {'events': events})

# 1. The total amount paid for a specific event
def event_total_payment(request, event_id):
    total_amount = Payment.objects.filter(event__id=event_id).aggregate(total=Sum('amount'))
    return render(request, 'events/event_total_payment.html', {'total_amount': total_amount})

# 2. The average price of paid events
def average_paid_event_price(request):
    average_price = Payment.objects.filter(event__is_free=False).aggregate(average=Avg('amount'))
    return render(request, 'events/average_paid_event_price.html', {'average_price': average_price})

# 3. The list of participants attending a specific event
def event_participants(request, event_id):
    event = Event.objects.get(id=event_id)
    participants = event.participants.all()
    return render(request, 'events/event_participants.html', {'participants': participants})

# 4. The list of speakers for a specific event
def event_speakers(request, event_id):
    event = Event.objects.get(id=event_id)
    schedules = event.schedules.all()
    speakers = [schedule.speaker for schedule in schedules if schedule.speaker is not None]
    return render(request, 'events/event_speakers.html', {'speakers': speakers})

