from events import views
from django.urls import path
urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.list_events, name='list-events'),
    path('events/<str:title>/', views.event_detail, name='event-detail'),
    path('speakers/', views.list_speakers, name='list-speakers'),
    path('speakers/<str:name>/', views.speaker_detail, name='speaker-detail'),
    path('participants/', views.list_participants, name='list-participants'),
    path('participants/<str:email>/',
         views.participant_detail, name='participant-detail'),
    path('event/<int:event_id>/total-payment/',
         views.event_total_payment, name='event-total-payment'),
    path('average-paid-event-price/', views.average_paid_event_price,
         name='average-paid-event-price'),
    path('event/<int:event_id>/participants/',
         views.event_participants, name='event-participants'),
    path('event/<int:event_id>/speakers/',
         views.event_speakers, name='event-speakers'),
]
