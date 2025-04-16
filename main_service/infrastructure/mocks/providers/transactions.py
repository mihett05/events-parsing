from dishka import Provider, provide, Scope

from application.transactions import TransactionsGateway
from ..transactions import TransactionsMockGateway


class TransactionsProvider(Provider):
    scope = Scope.REQUEST

    gateway = provide(source=TransactionsMockGateway, provides=TransactionsGateway)
