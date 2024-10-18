from datetime import datetime

from options import sleep, life, work

time_0 = datetime.strptime("00:00", "%H:%M").time()
time_1 = datetime.strptime("07:00", "%H:%M").time()
time_2 = datetime.strptime("11:00", "%H:%M").time()
time_3 = datetime.strptime("15:00", "%H:%M").time()
time_4 = datetime.strptime("16:00", "%H:%M").time()
time_5 = datetime.strptime("20:00", "%H:%M").time()
time_6 = datetime.strptime("23:00", "%H:%M").time()
time_7 = datetime.strptime("23:59", "%H:%M").time()

time_ranges = [
    (time_0, time_1, sleep),
    (time_1, time_2, life),
    (time_2, time_3, work),
    (time_3, time_4, life),
    (time_4, time_5, work),
    (time_5, time_6, life),
    (time_6, time_7, sleep)
]

def get_time_status(default_staus=life):
    current_time = datetime.now().time()
    for start_time, end_time, status in time_ranges:
        if start_time <= current_time < end_time:
            return status
    return default_staus