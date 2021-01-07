from singleton_decorator import singleton


@singleton
class BookingRepository:
    def __init__(self):
        self.__db_set = []

    def add(self, json):
        self.__db_set.append(json)

    def get(self, json):
        return self.__db_set.insert(json)

    def get_all(self):
        return self.__db_set

    def edit(self, json):
        self.__db_set.insert(json, json)

    def remove(self, json):
        self.__db_set.remove(json, json)
