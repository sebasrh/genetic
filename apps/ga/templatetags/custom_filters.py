from django import template
from django.utils.timesince import timesince
from django.utils import timezone

register = template.Library()


@register.filter
def floater(value):
    return float(value)


@register.filter
def inter(value):
    return int(value)


@register.filter
def replace_comma_with_dot(value):
    return str(value).replace(',', '.')


@register.filter
def replace_underscore_with_space(value):
    # la primera letra mayuscula y luego reemplazar los guiones por espacios
    # Tambien traducir 'melody' a 'melodía'
    return str(value).replace('melody', 'melodía').capitalize().replace('_', ' ')


@register.filter
def durationformat(duration):
    # Convierte la duración de segundos a minutos y segundos
    int_duration = int(duration)
    minutes, seconds = divmod(int_duration, 60)
    return f"{int(minutes)}:{int(seconds)}"


@register.filter
def durationformat2(duration):
    # Convierte la duración de segundos a minutos y segundos
    int_duration = int(duration)
    minutes, seconds = divmod(int_duration, 60)
    return f"{int(minutes)} min {int(seconds)} s"


@register.filter
def ordinal(value):
    if 10 <= value % 100 <= 20:
        suffix = 'º'
    else:
        suffix = {1: 'º', 2: 'º', 3: 'º'}.get(value % 10, 'º')
    return f"{value}{suffix}"


@register.filter
def custom_date(value):

    now = timezone.localtime(timezone.now()) # Hora actual
    value = timezone.localtime(value)
    delta = now - value # Diferencia entre la hora actual y la hora del post

    # Si es menos de un día, muestra la hora en formato '4:38 PM'
    if delta.days == 0 and now.day == value.day:
        formatted_time = value.astimezone(
            timezone.get_current_timezone()).strftime('%I:%M %p')
    else:
        # Si es más de un día, muestra la fecha completa en formato '4:38 PM - 3/11/23'
        formatted_time = value.astimezone(
            timezone.get_current_timezone()).strftime('%I:%M %p - %m/%d/%y')

    return formatted_time
