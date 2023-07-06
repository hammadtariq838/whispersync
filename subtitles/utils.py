
def convert_seconds_to_hms(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    time_format = '{:02d}:{:02d}:{:02d}'.format(
        int(hours), int(minutes), int(seconds))
    return time_format
