import datetime

from hotel_booking_infrastructure.repositories import room_repository, customer_repository, booking_repository


class DbInitializer:
    def __init__(self):
        self.__rr = room_repository.RoomRepository()
        self.__cr = customer_repository.CustomerRepository()
        self.__br = booking_repository.BookingRepository()

        self.__date = datetime.datetime.now()
        self.__date_delta = self.__date + datetime.timedelta(14)

        booking_list = [
            {'start_date': self.__date, 'end_date': self.__date_delta, 'is_active': True, 'customer_id': 1, 'room_id': 1},
            {'start_date': self.__date, 'end_date': self.__date_delta, 'is_active': True, 'customer_id': 2, 'room_id': 2},
            {'start_date': self.__date, 'end_date': self.__date_delta, 'is_active': True, 'customer_id': 1, 'room_id': 3}
        ]

        customer_list = [
            {'name': 'John Smith', 'email': 'js@gmail.com'},
            {'name': 'Jane Doh', 'email': 'jd@gmail.com'}
        ]

        room_list = [
            {'id': 1, 'description': 'A'},
            {'id': 2, 'description': 'B'},
            {'id': 3, 'description': 'C'}
        ]

        if len(self.__rr.get_all()) == 0:
            for i in room_list:
                self.__rr.add(i)

        if len(self.__cr.get_all()) == 0:
            for i in customer_list:
                self.__cr.add(i)

        if len(self.__br.get_all()) == 0:
            for i in booking_list:
                self.__br.add(i)
