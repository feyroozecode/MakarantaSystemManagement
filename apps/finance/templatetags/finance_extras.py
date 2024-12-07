from django import template
from datetime import datetime

register = template.Library()

FRENCH_MONTHS = {
    1: 'Janvier',
    2: 'Février',
    3: 'Mars',
    4: 'Avril',
    5: 'Mai',
    6: 'Juin',
    7: 'Juillet',
    8: 'Août',
    9: 'Septembre',
    10: 'Octobre',
    11: 'Novembre',
    12: 'Décembre'
}

@register.filter
def french_date(value):
    """Convert a date to French format."""
    if not value:
        return ''
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return value
    
    day = value.day
    month = FRENCH_MONTHS[value.month]
    year = value.year
    time = value.strftime('%H:%M')
    
    return f"{day} {month} {year} {time}"
