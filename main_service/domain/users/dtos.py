from dataclasses import dataclass


@dataclass
class ReadAllUsersDto:
    page: int
    page_size: int
