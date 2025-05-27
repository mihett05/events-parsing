from dataclasses import dataclass


@dataclass
class AuthenticateUserDto:
    email: str
    password: str


@dataclass
class RegisterUserDto:
    email: str
    password: str
    fullname: str = ""
    is_active: bool = False


@dataclass
class CreateUserWithPasswordDto:
    email: str
    fullname: str
    is_active: bool
    salt: str
    hashed_password: str
