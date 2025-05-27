from abc import ABCMeta, abstractmethod


class Transaction(metaclass=ABCMeta):
    """
    ВАЖНО:
    После коммита или ролбека транзакции нельзя больше с ней ничего делать,
    она закрытой становится, так что учитывайте это, когда будете писать юзкейсы
    """

    """
    Абстракция транзакции базы данных.

    Определяет базовый интерфейс для работы с транзакциями.
    После выполнения commit или rollback транзакция считается завершенной
    и не может быть использована повторно.
    """

    @abstractmethod
    async def commit(self): ...

    """
    Фиксирует изменения в базе данных.

    После успешного выполнения все изменения становятся видимыми
    для других транзакций.
    """

    @abstractmethod
    async def rollback(self): ...

    """
    Откатывает все изменения в рамках текущей транзакции.

    Возвращает базу данных в состояние, предшествующее началу транзакции.
    """


class TransactionsGateway(metaclass=ABCMeta):
    @abstractmethod
    async def __aenter__(self) -> Transaction: ...

    """
    Начинает новую транзакцию.

    Returns:
        Transaction: Объект активной транзакции
    """

    @abstractmethod
    def nested(self) -> "TransactionsGateway": ...

    """
    Создает новую вложенную транзакцию (savepoint).

    Returns:
        TransactionsGateway: Менеджер вложенной транзакции
    """

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb): ...

    """
    Завершает транзакцию в зависимости от наличия исключения.
    """
