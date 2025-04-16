from application.transactions import TransactionsGateway, Transaction


class MockTransaction(Transaction):
    async def commit(self):
        pass

    async def rollback(self):
        pass


class TransactionsMockGateway(TransactionsGateway):
    async def __aenter__(self) -> Transaction:
        return MockTransaction()

    def nested(self) -> "TransactionsMockGateway":
        return TransactionsMockGateway()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
