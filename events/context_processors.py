from django.db.models import Count, Sum, Avg
from .models import Event, Participant, Payment
from .utils import add_commas

def metrics(request):
    event_participants_count = Event.objects.aggregate(participant_count=Count('participant'))
    participant_events_count = Participant.objects.aggregate(event_count=Count('events'))
    event_schedules_count = Event.objects.aggregate(schedule_count=Count('schedule'))
    events_total_payment = Payment.objects.all().aggregate(total=Sum('amount'))
    average_paid_event_price = Payment.objects.filter(event__is_free=False).aggregate(average=Avg('amount'))

    return {
        'event_participants': add_commas(event_participants_count['participant_count']),
        'participant_events': add_commas(participant_events_count['event_count']),
        'event_schedules': add_commas(event_schedules_count['schedule_count']),
        'events_total_payment': add_commas(events_total_payment['total']),
        'average_paid_event_price': add_commas(average_paid_event_price['average']),
    }

