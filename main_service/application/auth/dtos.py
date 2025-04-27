from dataclasses import dataclass


@dataclass
class AuthenticateUserDto:
    email: str
    password: str


@dataclass
class RegisterUserDTO:
    email: str
    password: str
    fullname: str = ""
    is_active: bool = True
