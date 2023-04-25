from datetime import datetime


def get_present_time():
    now = datetime.now()
    return {'time_presence': now.strftime("%H:%M:%S")}
