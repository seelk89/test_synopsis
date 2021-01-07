import unittest
import datetime

from unittest.mock import Mock
from hotel_booking_core.services import booking_manager


class BookingManagerTests(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__date = datetime.datetime.now()
        self.__start = self.__date + datetime.timedelta(10)
        self.__end = self.__date + datetime.timedelta(20)

        self.booking_list = [
            {'start_date': self.__date + datetime.timedelta(9), 'end_date': self.__end, 'is_active': True, 'customer_id': 1,
             'room_id': 1},
            {'start_date': self.__start, 'end_date': self.__end, 'is_active': True, 'customer_id': 2, 'room_id': 2}
        ]

        self.room_list = [
            {'id': 1, 'description': '1'},
            {'id': 2, 'description': '2'},
        ]

        self.room_repository = Mock()
        self.booking_repository = Mock()

        self.room_repository.get_all.return_value = self.room_list
        self.booking_repository.get_all.return_value = self.booking_list

        self.fake_booking_manager = booking_manager.BookingManager(self.room_repository, self.booking_repository)

    def test_create_booking(self):
        # Case create_booking in occupied time
        # Arrange
        booking = {'start_date': self.__start, 'end_date': self.__end, 'is_active': False, 'customer_id': 1, 'room_id': 1}

        # Act
        # Assert
        self.assertFalse(self.fake_booking_manager.create_booking(booking))

        # Case create_booking before occupied time
        # Arrange
        booking = {'start_date': self.__date + datetime.timedelta(8), 'end_date': self.__date + datetime.timedelta(9),
                   'is_active': True, 'customer_id': 1, 'room_id': 1}

        # Act
        # Assert
        self.assertTrue(self.fake_booking_manager.create_booking(booking))

        # Case create_booking after occupied time
        # Arrange
        booking = {'start_date': self.__date + datetime.timedelta(21), 'end_date': self.__date + datetime.timedelta(22),
                   'is_active': True, 'customer_id': 1, 'room_id': 1}

        # Act
        # Assert
        self.assertTrue(self.fake_booking_manager.create_booking(booking))

        # Case create_booking start before, end in occupied time
        # Arrange
        booking = {'start_date': self.__date + datetime.timedelta(8), 'end_date': self.__date + datetime.timedelta(19),
                   'is_active': True, 'customer_id': 1, 'room_id': 1}

        # Act
        # Assert
        self.assertFalse(self.fake_booking_manager.create_booking(booking))

        # Case create_booking start in occupied time, end after
        # Arrange
        booking = {'start_date': self.__date + datetime.timedelta(11), 'end_date': self.__date + datetime.timedelta(21),
                   'is_active': True, 'customer_id': 1, 'room_id': 1}

        # Act
        # Assert
        self.assertFalse(self.fake_booking_manager.create_booking(booking))

        # Case create_booking start before occupied time, end after
        # Arrange
        booking = {'start_date': self.__date + datetime.timedelta(8), 'end_date': self.__date + datetime.timedelta(21),
                   'is_active': True, 'customer_id': 1, 'room_id': 1}

        # Act
        # Assert
        self.assertFalse(self.fake_booking_manager.create_booking(booking))

        # Case create_booking in available room
        # Arrange
        booking = {'start_date': self.__date + datetime.timedelta(8), 'end_date': self.__date + datetime.timedelta(22),
                   'is_active': False, 'customer_id': 1, 'room_id': 1}

        # Act
        # Assert
        self.assertFalse(self.fake_booking_manager.create_booking(booking))

    def test_find_available_room(self):
        # Case no available rooms
        # Arrange
        # Act
        # Assert
        self.assertFalse(self.fake_booking_manager.find_available_room(self.__start, self.__end) > -1)

        # Case has available room
        # Arrange
        start = self.__date + datetime.timedelta(7)
        end = self.__date + datetime.timedelta(8)

        # Act
        # Assert
        self.assertTrue(self.fake_booking_manager.find_available_room(start, end) > -1)

        # Case start date out of occupied end date in occupied
        # Arrange
        start = self.__date + datetime.timedelta(9)
        end = self.__date + datetime.timedelta(19)

        # Act
        # Assert
        self.assertFalse(self.fake_booking_manager.find_available_room(start, end) > -1)

        # Case start date before occupied end date after occupied
        # Arrange
        start = self.__date + datetime.timedelta(7)
        end = self.__date + datetime.timedelta(22)

        # Act
        # Assert
        self.assertFalse(self.fake_booking_manager.find_available_room(start, end) > -1)

    def test_get_fully_occupied_dates(self):
        # Case is occupied = {start, end, true};
        # Arrange
        # Act
        # Assert
        self.assertTrue(len(self.fake_booking_manager.get_fully_occupied_dates(self.__start, self.__end)) > 0)

        # Case is not occupied = {start.AddDays(-3), start.AddDays(-2), false};
        # Arrange
        start = self.__date + datetime.timedelta(7)
        end = self.__date + datetime.timedelta(8)

        # Act
        # Assert
        self.assertFalse(len(self.fake_booking_manager.get_fully_occupied_dates(start, end)) > 0)

        # Case is not fully occupied = {start.AddDays(-3), end, true};
        # Arrange
        start = self.__date + datetime.timedelta(7)

        # Act
        # Assert
        self.assertTrue(len(self.fake_booking_manager.get_fully_occupied_dates(start, self.__end)) > 0)


if __name__ == '__main__':
    unittest.main()
