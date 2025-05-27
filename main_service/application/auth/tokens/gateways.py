from abc import ABCMeta, abstractmethod

from .dtos import PasswordDto, TokenInfoDto, TokenPairDto


class TokensGateway(metaclass=ABCMeta):
    """
        Абстрактный шлюз для работы с токенами аутентификации.
        Определяет интерфейс для генерации и верификации токенов.
        """
    @abstractmethod
    async def create_token_pair(self, subject: str) -> TokenPairDto: ...

    """
            Создает пару токенов (access и refresh) для указанного субъекта.
            """


    @abstractmethod
    async def extract_token_info(
        self, token: str, check_expires: bool = True
    ) -> TokenInfoDto: ...

    """
            Извлекает информацию из токена с возможностью проверки срока действия.
            """


class SecurityGateway(metaclass=ABCMeta):
    """
    Абстрактный шлюз для операций безопасности.
    Инкапсулирует логику работы с паролями и солями.
    """
    @abstractmethod
    def create_salt(self) -> str: ...

    """
    Генерирует криптографическую соль для хеширования паролей.
    """

    @abstractmethod
    def create_hashed_password(self, password: str) -> PasswordDto: ...

    """
    Создает защищенное представление пароля с использованием соли.
    """

    @abstractmethod
    def verify_passwords(
        self, plain_password: str, hashed_password: PasswordDto
    ) -> bool: ...

    """
    Проверяет соответствие введенного пароля сохраненному хешу.
    """
