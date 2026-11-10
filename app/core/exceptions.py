class AppError(Exception):
    """Parent of every error defined"""

class UserNotFound(AppError):
    pass

class InvalidToken(AppError):
    pass

class RoomInactive(AppError):
    pass

class RoomNameTaken(AppError):
    pass

class RoomNotFound(AppError):
    pass

class NotRoomOwner(AppError):
    pass

class ProductNotFound(AppError):
    pass

class EmailAlreadyRegistered(AppError):
    pass 

class InvalidCredentials(AppError):
    pass 