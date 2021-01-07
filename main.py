from hotel_booking_infrastructure import db_initializer
from hotel_booking_infrastructure.repositories import room_repository, customer_repository, booking_repository

if __name__ == '__main__':
    db_init = db_initializer.DbInitializer()

    rr = room_repository.RoomRepository()
    cr = customer_repository.CustomerRepository()
    br = booking_repository.BookingRepository()

    print(rr.get_all())
    print(cr.get_all())
    print(br.get_all())
