from application.transactions import TransactionsGateway
from dishka import Provider, Scope, provide

from ..transactions import TransactionsMockGateway


class TransactionsProvider(Provider):
    scope = Scope.REQUEST

    gateway = provide(source=TransactionsMockGateway, provides=TransactionsGateway)
