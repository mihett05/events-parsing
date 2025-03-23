from dataclasses import dataclass


@dataclass
class CreateUserDto:
    email: str
    fullname: str
    password: str


@dataclass
class ReadUsersDto:
    page: int
    page_size: int
