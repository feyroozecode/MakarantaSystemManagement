from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

FRENCH_MONTHS = {
    'January': 'Janvier',
    'February': 'Février',
    'March': 'Mars',
    'April': 'Avril',
    'May': 'Mai',
    'June': 'Juin',
    'July': 'Juillet',
    'August': 'Août',
    'September': 'Septembre',
    'October': 'Octobre',
    'November': 'Novembre',
    'December': 'Décembre'
}

@register.filter
def french_date(value):
    """Convert a date to French format."""
    if not value:
        return '-'
    
    # If it's a method, call it
    if callable(value):
        value = value()
        
    # Handle string dates
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            try:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return value
    
    # Format date as "18 April 2024"
    try:
        english_date = value.strftime('%-d %B %Y')
    except:
        english_date = timezone.template_localtime(value).strftime('%-d %B %Y')
    
    # Replace English month with French month
    for eng_month, fr_month in FRENCH_MONTHS.items():
        if eng_month in english_date:
            return english_date.replace(eng_month, fr_month)
    
    return english_date
