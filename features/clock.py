import datetime
from ui.constants import GAME_MINUTE_MS


class GameClock:
    def __init__(self, start_year=2050, start_month=10, start_day=25, start_hour=9):
        # Starts the game at: Oct 25, 2050, 9:00 AM
        self.current_time = datetime.datetime(start_year, start_month, start_day, start_hour, 0)
        self.ms_accumulator = 0

    def update(self, dt):
        """Updates clock based on delta time (milliseconds)."""
        self.ms_accumulator += dt
        minutes_passed = int(self.ms_accumulator // GAME_MINUTE_MS)

        if minutes_passed > 0:
            self.current_time += datetime.timedelta(minutes=minutes_passed)
            self.ms_accumulator %= GAME_MINUTE_MS

    def snapshot(self):
        """Return the current game datetime (for stamping news items)."""
        return self.current_time

    def get_relative_time(self, past_time):
        """
        Given a datetime snapshot taken earlier, return a human-readable
        relative string like 'Just Now', '3 mins ago', '2 hrs ago', etc.
        All times are in game-clock minutes.
        """
        delta = self.current_time - past_time
        total_minutes = int(delta.total_seconds() // 60)

        if total_minutes < 1:
            return "Just Now"
        elif total_minutes == 1:
            return "1 min ago"
        elif total_minutes < 60:
            return f"{total_minutes} mins ago"
        else:
            hours = total_minutes // 60
            if hours == 1:
                return "1 hr ago"
            return f"{hours} hrs ago"

    def get_date_string(self):
        """Returns format: FRI, OCT 25, 2050"""
        return self.current_time.strftime("%a, %b %d, %Y").upper()

    def get_time_string(self):
        """Returns format: xx:xx AM/PM"""
        return self.current_time.strftime("%I:%M %p").lstrip("0")