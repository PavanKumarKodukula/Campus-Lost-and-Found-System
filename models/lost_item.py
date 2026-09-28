class LostItem:

    def __init__(self, lost_id, user_id, item_name, category, description, location, date, status):
        self.__lost_id = lost_id
        self.__user_id = user_id
        self.__item_name = item_name
        self.__category = category
        self.__description = description
        self.__location = location
        self.__date = date
        self.__status = status

    def get_lost_id(self):
        return self.__lost_id

    def get_user_id(self):
        return self.__user_id

    def get_item_name(self):
        return self.__item_name

    def get_category(self):
        return self.__category

    def get_description(self):
        return self.__description

    def get_location(self):
        return self.__location

    def get_date(self):
        return self.__date

    def get_status(self):
        return self.__status
