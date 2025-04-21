from dataclasses import dataclass


@dataclass
class AuthenticateUserDto:
    email: str
    password: str
