class FoundItem:

    def __init__(self, found_id, lost_id, finder_user_id, found_date, found_location, status):
        self.__found_id = found_id
        self.__lost_id = lost_id
        self.__finder_user_id = finder_user_id
        self.__found_date = found_date
        self.__found_location = found_location
        self.__status = status

    def get_found_id(self):
        return self.__found_id

    def get_lost_id(self):
        return self.__lost_id

    def get_finder_user_id(self):
        return self.__finder_user_id

    def get_found_date(self):
        return self.__found_date

    def get_found_location(self):
        return self.__found_location

    def get_status(self):
        return self.__status
