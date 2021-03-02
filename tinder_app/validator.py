import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_date(value: datetime.date):
    valid_year = datetime.date.today().year - 16
    valid_date = datetime.date.today()
    valid_date = valid_date.replace(year=valid_year)
    if value > valid_date:
        raise ValidationError(
            _('Invalid date = %(date), you must be older to be on this site'),
            params={'date': value},
        )
