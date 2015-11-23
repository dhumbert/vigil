from datetime import timedelta
from vigil import app


def bracketing_days(day_datetime):
    prev_day = day_datetime - timedelta(days=1)
    next_day = day_datetime + timedelta(days=1)

    return prev_day.strftime(app.config['DATE_FORMAT']), next_day.strftime(app.config['DATE_FORMAT'])