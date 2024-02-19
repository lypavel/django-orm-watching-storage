from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render, get_object_or_404

from .storage_information_view import format_duration, is_visit_long


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard)

    this_passcard_visits = []

    for visit in visits:
        enteted_at = visit.entered_at
        duration = visit.get_duration()
        hours, minutes = format_duration(duration)
        is_strange = 'Да' if is_visit_long(duration) else 'Нет'

        this_passcard_visits.append(
            {
                'entered_at': enteted_at,
                'duration': f'{hours}ч {minutes}мин',
                'is_strange': is_strange
            }
        )

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
