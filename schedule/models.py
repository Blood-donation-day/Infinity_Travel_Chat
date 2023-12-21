# models.py

from django.db import models
from place.models import Places
from django.conf import settings

class Planners(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    public_flag = models.BooleanField(default=True) # 공개 여부 플래그 
    area = models
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 작성자 

    def __str__(self):
        return self.title

class PeriodEvents(models.Model):
    planner = models.ForeignKey(Planners, related_name='period_events', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

class DateEvents(models.Model):
    period_event = models.ForeignKey(PeriodEvents, related_name='date_events', on_delete=models.CASCADE)
    event_date = models.DateField()
    place = models.ManyToManyField(Places, related_name='date_events', blank=True)

    def __str__(self):
        return f"{self.period_event.title} - {self.event_date}"

class DateEventPlaces(models.Model):
    order = models.IntegerField()
    date_event = models.ForeignKey(DateEvents, related_name='date_event_places', on_delete=models.CASCADE)
    place = models.ForeignKey(Places, related_name='date_event_places', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.date_event} - {self.place}"