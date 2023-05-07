from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Event, Room, ScheduleEntry


def index(request):
    today = datetime.now().replace(hour=0, minute=0, second=0)

    return render(
        request,
        "schedule/index.html",
        context={
            "events": Event.objects.all(),
        },
    )


def schedule_html(request, slug):
    event = get_object_or_404(Event, acronym=slug)

    schedule = {}
    for day in range(0, event.duration_days):
        schedule[day] = {
            "day": day + 1,
            "start": event.start + timedelta(days=day),
            "end": event.start + timedelta(days=day + 1),
            "events": ScheduleEntry.objects.filter(
                start__date=event.start + timedelta(days=day)
            ).order_by("start"),
        }

    return render(
        request,
        "schedule/schedule.html",
        context={
            "event": event,
            "schedule": schedule,
        },
    )


def schedule_xml(request, slug):
    event = get_object_or_404(Event, acronym=slug)

    schedule = {}

    for day in range(0, event.duration_days):
        schedule[day] = {
            "day": day + 1,
            "start": event.start + timedelta(days=day),
            "end": event.start + timedelta(days=day + 1),
            "rooms": {},
        }

        for room in Room.objects.filter(event=event):
            entries = ScheduleEntry.objects.filter(
                room=room, start__date=event.start + timedelta(days=day)
            ).order_by("start")
            if entries.count():
                schedule[day]["rooms"][room] = {
                    "name": room.name,
                    "uuid": room.uuid,
                    "events": entries,
                }

    return render(
        request,
        "schedule/schedule.xml",
        context={
            "event": event,
            "schedule": schedule,
        },
        content_type="application/xml",
    )
