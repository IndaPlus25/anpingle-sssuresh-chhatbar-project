import datetime
from ui.constants import GAME_MINUTE_MS

class GameClock:
    def __init__(self, start_year=2050, start_month=10, start_day=25, start_hour=9):
        # Starts the game at: Oct 25, 2050, 9:00 AM
        self.current_time = datetime.datetime(start_year, start_month, start_day, start_hour, 0)
        self.ms_accumulator = 0


    def update(self, dt):
        #updates clock based on delta clock
        self.ms_accumulator += dt
        minutes_passed = int(self.ms_accumulator // GAME_MINUTE_MS)

        if minutes_passed > 0:
            # Advance the actual calendar time
            self.current_time += datetime.timedelta(minutes=minutes_passed)
            # Keep the leftover milliseconds for the next frame
            self.ms_accumulator %= GAME_MINUTE_MS

    def get_date_string(self):
        # Returns format: FRI, OCT 25, 2024
        return self.current_time.strftime("%a, %b %d, %Y").upper()

    def get_time_string(self):
        # Returns format: xx:xx AM/PM
        return self.current_time.strftime("%I:%M %p").lstrip("0")