from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_free = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Speaker(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField()
    photo = models.ImageField(upload_to='speakers/', null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    social_links = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

class Participant(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    events = models.ManyToManyField(Event)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    topic = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.topic

class Payment(models.Model):
    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
    ]

    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateTimeField()
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f'{self.participant.name} - {self.event.title}'

