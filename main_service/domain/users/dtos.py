from dataclasses import dataclass


@dataclass
class CreateUserDto:
    email: str
    password: str
    fullname: str = ""
    is_active: bool = True


@dataclass
class ReadAllUsersDto:
    page: int
    page_size: int
