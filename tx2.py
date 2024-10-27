import os
import datetime

# Пользовательское исключение для недостатка средств
class InsufficientFundsError(Exception):
    def __init__(self, message=None):
        if message is None:
            self.message = "Insufficient funds"
        self.message = message        

    def __str__(self):
        return self.message

# Пользовательское исключение для превышения лимита транзакций
class TransactionLimitError(Exception):
    def __init__(self, message=None):
        if message is None:
            self.message = "Transaction limit exceeded"
        self.message = message

    def __str__(self):
        return self.message

# Класс для логирования всех транзакций
class TransactionLog:
    def __init__(self, log_file="log.txt") -> None:
        self.log_file = log_file

    def __enter__(self):
        self.file = open(self.log_file, "a+", encoding="utf-8")
        return self

    def write_log(self, message):
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.file.write(f"{time_now} - {message}\n")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.write_log(f"Ошибка: {exc_val}")
        self.file.close()

# Основной класс для управления транзакциями
class Transaction:
    def __init__(self, account, balance, limit=10) -> None:
        self.account = account
        self.balance = balance
        self.transaction_count = 0
        self.transaction_limit = limit  # Устанавливаем дневной лимит транзакций
    
    # Проверка корректности суммы
    @staticmethod
    def validate_amount(amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

    # Проверка дневного лимита
    def validate_limit(self):
        if self.transaction_count >= self.transaction_limit:
            raise TransactionLimitError()

    # Депозит средств
    def deposit(self, amount):
        self.validate_amount(amount)
        self.balance += amount
        with TransactionLog("transaction_log.txt") as log:
            log.write_log(f"Успешно: Депозит {amount} на счет {self.account}. Баланс: {self.balance}")

    # Выполнение транзакции
    def execute(self, amount):
        self.validate_amount(amount)
        if self.balance >= amount:
            self.validate_limit()
            self.balance -= amount
            self.transaction_count += 1
            with TransactionLog("transaction_log.txt") as log:
                log.write_log(f"Успешно: Перевод {amount} со счета {self.account}. Баланс: {self.balance}")
        else:
            raise InsufficientFundsError(f'Недостаточно средств для снятия {amount}. Текущий баланс: {self.balance}')

    # Начало транзакции (контекстный менеджер)
    def __enter__(self):
        return self

    # Завершение транзакции (контекстный менеджер)
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            with TransactionLog("transaction_log.txt") as log:
                log.write_log(f"Ошибка: {exc_val}. Транзакция для {self.account} не выполнена.")
