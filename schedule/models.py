from datetime import timedelta
from uuid import UUID

from django.db import models

from .utils import validate_acronym


class Language(models.Model):
    name = models.CharField(max_length=200)
    short = models.CharField("short code", max_length=10)

    def __str__(self):
        return self.name


class License(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    acronym = models.CharField(max_length=50, validators=[validate_acronym])
    start = models.DateField()
    duration_days = models.IntegerField("Duration (days)")
    license = models.ForeignKey(License, on_delete=models.RESTRICT)

    @property
    def last_day(self):
        return self.start + timedelta(days=self.duration_days - 1)

    class Meta:
        ordering = ["-start", "name"]

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=200)
    optout = models.BooleanField("Recording.Optout")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Room(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    optout = models.BooleanField("Recording.Optout")
    uuid = models.CharField("`uuidgen`", max_length=40, unique=True)

    class Meta:
        ordering = ["event", "name"]

    def __str__(self):
        return f"{self.name} [{self.event}]"


class ScheduleEntry(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start = models.DateTimeField()
    duration_minutes = models.IntegerField("Duration (minutes)")
    title = models.CharField(max_length=200)
    abstract = models.TextField(blank=True)
    optout = models.BooleanField("This event will not be recorded")
    persons = models.ManyToManyField(Person)
    slug = models.SlugField()
    uuid = models.CharField("`uuidgen`", max_length=40, unique=True)
    language = models.ForeignKey(Language, on_delete=models.RESTRICT)

    @property
    def duration_hhmm(self):
        return f"{int(self.duration_minutes/60)}:{self.duration_minutes%60}"

    @property
    def end(self):
        return self.start + timedelta(minutes=self.duration_minutes)

    @property
    def recording_optout(self):
        return self.optout or self.room.optout

    @property
    def full_slug(self):
        return f"{self.room.event.acronym}-{self.id}-{self.slug}"

    class Meta:
        ordering = ["start"]

    def __str__(self):
        return self.full_slug
