DEFAULT_FIELD = "-"

sex_mapper = {DEFAULT_FIELD: "Undefined", 1: "Women", 2: "Men"}


class UserInfo:
    def __init__(self, first_name, last_name, sex, bdate, city):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.bdate = bdate
        self.city = city


class FriendInfo:
    def __init__(self, first_name, last_name, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex


class AlbumInfo:
    def __init__(self, id, title, size, description):
        self.id = id
        self.title = title
        self.size = size
        self.description = description