from datacenter.models import Visit
from django.shortcuts import render


def format_duration(duration: float) -> str:
    seconds_in_hour = 3600
    seconds_in_minute = 60

    hours = int(duration // seconds_in_hour)
    minutes = int((duration % seconds_in_hour) // seconds_in_minute)

    return hours, minutes


def is_visit_long(duration: float, max_minutes_allowed: int = 60) -> bool:
    seconds_in_minute = 60

    total_minutes = duration // seconds_in_minute

    return total_minutes > max_minutes_allowed


def storage_information_view(request):

    active_visits = Visit.objects.filter(leaved_at=None)

    non_closed_visits = []

    for visitor in active_visits:
        owner_name = visitor.passcard.owner_name
        enteted_at = visitor.entered_at
        duration = visitor.get_duration()
        hours, minutes = format_duration(duration)
        is_strange = 'Да' if is_visit_long(duration) else 'Нет'

        non_closed_visits.append(
            {
                'who_entered': owner_name,
                'entered_at': enteted_at,
                'duration': f'{hours}ч {minutes}мин',
                'is_strange': is_strange
            }
        )

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
