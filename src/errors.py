class MyBarError(Exception):
    pass


class DoesNotExistError(MyBarError):
    pass


class NotInBarError(MyBarError):
    pass


class AlreadyInBarError(MyBarError):
    pass
