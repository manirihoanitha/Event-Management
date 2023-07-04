from django.shortcuts import render, get_object_or_404
from events.models import Event, Speaker, Participant, Payment, Schedule
from django.utils import timezone
from django.db.models import Count
from django.db.models import Sum, Avg
from .utils import convert_usd_to_rwf
from django.core.paginator import Paginator


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
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/list.html', {'page_obj': page_obj})


def event_detail(request, title):
    event = get_object_or_404(Event, title=title)
    return render(request, 'events/detail.html', {'event': event})


def list_speakers(request):
    speakers = Speaker.objects.all()
    paginator = Paginator(speakers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'speakers/list.html', {'page_obj': page_obj})


def speaker_detail(request, email):
    speaker = get_object_or_404(Speaker, email=email)
    return render(request, 'speakers/detail.html', {'speaker': speaker})


def list_participants(request):
    participants = Participant.objects.all()
    paginator = Paginator(participants, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'participants/list.html', {'page_obj': page_obj})


def participant_detail(request, email):
    participant = get_object_or_404(Participant, email=email)
    return render(request, 'participants/detail.html', {'participant': participant})


def list_of_schedule(request):
    schedules = Schedule.objects.all()
    paginator = Paginator(schedules, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'schedules/list.html', {'page_obj': page_obj})


def schedule_detail(request, topic):
    schedule = get_object_or_404(Schedule, topic=topic)
    return render(request, 'schedules/detail.html', {'schedule': schedule})


def list_upcoming_events(request):
    events = Event.objects.filter(start_date__gte=timezone.now())
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/upcoming.html', {'page_obj': page_obj})


def list_free_events(request):
    events = Event.objects.filter(is_free=True)
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/free.html', {'page_obj': page_obj})


def list_paid_events(request):
    events = Event.objects.filter(is_free=False)
    paginator = Paginator(events, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/paid.html', {'page_obj': page_obj})


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
    total_amount = Payment.objects.filter(
        event__id=event_id).aggregate(total=Sum('amount'))
    return render(request, 'events/event_total_payment.html', {'total_amount': total_amount})

# 2. The average price of paid events


def average_paid_event_price(request):
    average_price = Payment.objects.filter(
        event__is_free=False).aggregate(average=Avg('amount'))
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
    speakers = [
        schedule.speaker for schedule in schedules if schedule.speaker is not None]
    return render(request, 'events/event_speakers.html', {'speakers': speakers})


def event_payment_processing(request, event_id):
    payments_list = Payment.objects.filter(
        event__id=event_id)  # get all Payment objects
    paginator = Paginator(payments_list, 5)  # Show 5 payments per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'events/single-event-payment.html', {'page_obj': page_obj})


def event_payment_detail(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    payment.amount_rwf = convert_usd_to_rwf(payment.amount)
    return render(request, 'events/single-event-payment-detail.html', {'payment': payment})


def metrics(request):
    event_participants = Event.objects.annotate(
        participant_count=Count('participants'))
    participant_events = Participant.objects.annotate(
        event_count=Count('events'))
    event_schedules = Event.objects.annotate(schedule_count=Count('schedules'))
    events_total_payment = Payment.objects.all().aggregate(total=Sum('amount'))
    average_paid_event_price = Payment.objects.filter(
        event__is_free=False).aggregate(average=Avg('amount'))

    return render(request, 'partials/metrics.html', {
        'event_participants': event_participants,
        'participant_events': participant_events,
        'event_schedules': event_schedules,
        'events_total_payment': events_total_payment,
        'average_paid_event_price': average_paid_event_price
    })


def events_payment_processing(request):
    payments = Payment.objects.all()
    paginator = Paginator(payments, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/event-payment-processing.html', {'page_obj': page_obj})
