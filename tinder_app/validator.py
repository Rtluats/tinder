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



def validate_update_cords(user):
    valid_hours = datetime.datetime.now().hour - 2
    valid_datetime = datetime.datetime.now()
    valid_datetime = valid_datetime.replace(hour=valid_hours)
    if user.last_cords_update is not None and user.last_cords_update > valid_datetime:
        raise ValidationError(
            _("User can't update his cords, because 2 hours have not passed yet"),
        )


def validate_counter_swipes(user):
    if user.group.number_of_allowed_swipes != - 1 and user.group.number_of_allowed_swipes <= user.counter_swipes:
        raise ValidationError(
            _("the user can't make more likes"),
        )
