from abc import ABCMeta, abstractmethod

from .dtos import PasswordDto, TokenInfo, TokenPairDto


class TokensGateway(metaclass=ABCMeta):
    @abstractmethod
    async def create_token_pair(self, subject: str) -> TokenPairDto: ...

    @abstractmethod
    async def extract_token_info(
        self, token: str, check_expires: bool = True
    ) -> TokenInfo: ...


class SecurityGateway(metaclass=ABCMeta):
    @abstractmethod
    def create_salt(self) -> str: ...

    @abstractmethod
    def create_hashed_password(self, password: str) -> PasswordDto: ...

    @abstractmethod
    def verify_passwords(
        self, plain_password: str, hashed_password: PasswordDto
    ) -> bool: ...
