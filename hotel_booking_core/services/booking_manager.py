import datetime


class BookingManager:
    def __init__(self, room_repository, booking_repository):
        self.__rr = room_repository
        self.__br = booking_repository

    def create_booking(self, booking):
        room_id = self.find_available_room(booking['start_date'], booking['end_date']);

        if room_id >= 0:
            booking['room_id'] = room_id
            booking['is_active'] = True
            self.__br.add(booking)
            return True

        else:
            return False

    def find_available_room(self, start_date, end_date):
        if start_date.date() <= datetime.date.today() or start_date > end_date:
            raise Exception('The start date cannot be in the past or later than the end date.')

        active_booking = []
        for i in self.__br.get_all():
            if i['is_active']:
                active_booking.append(i)

        for i in self.__rr.get_all():
            active_bookings_for_current_room = None

            for j in active_booking:
                if i['id'] == j['room_id']:
                    active_bookings_for_current_room = j

            if (start_date < active_bookings_for_current_room['start_date'] and
                    end_date < active_bookings_for_current_room['start_date'] or
                    start_date > active_bookings_for_current_room['end_date'] and
                    end_date > active_bookings_for_current_room['end_date']):
                return i['id']

        return -1

    def get_fully_occupied_dates(self, start_date, end_date):
        if start_date > end_date:
            raise Exception('The start date cannot be later than the end date.');

        fully_occupied_dates = []
        num_of_rooms = len(self.__rr.get_all())
        bookings = self.__br.get_all()

        if len(bookings) > 0:
            num_of_bookings = []

            while start_date <= end_date:
                for i in bookings:
                    if (i['is_active'] and
                            i['start_date'] <= start_date <= i['end_date']):
                        num_of_bookings.append(i)

                if len(num_of_bookings) >= num_of_rooms:
                    fully_occupied_dates.append(start_date)

                start_date += datetime.timedelta(1)

        return fully_occupied_dates
