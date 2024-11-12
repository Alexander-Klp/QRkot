from datetime import timedelta


def format_timedelta(time: float) -> str:
    td = timedelta(days=time)
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{days}D, {hours}:{minutes}:{seconds}'
