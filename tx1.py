import os

os.chdir(os.path.dirname(__file__))

class CustomFileNotFoundError(Exception):
    """Пользовательское исключение для случая, когда файл не найден."""
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return f"Файл '{self.filename}' не найден."


class AccessDeniedError(Exception):
    """Пользовательское исключение для случая, когда доступ к файлу запрещен."""
    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return f"Нет прав доступа к файлу '{self.filename}'."


class LogFile:
    """Класс для логирования операций с файлами."""
    def __init__(self, log_filename):
        self.log_filename = log_filename

    def __enter__(self):
        try:
            self.log_file = open(self.log_filename, 'a')
        except FileNotFoundError:
            raise CustomFileNotFoundError(self.log_filename)
        except PermissionError:
            raise AccessDeniedError(self.log_filename)
        return self

    def log(self, message):
        self.log_file.write(message + '\n')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.log_file:
            self.log_file.close()
        if exc_type is not None:
            return False  # Перебросить исключение дальше


class FileManager:
    """Класс для управления чтением и записью файлов."""
    def __init__(self, filename, mode='r'):
        self.filename = filename
        self.mode = mode

        # Проверка корректности режима доступа
        valid_modes = ['r', 'w', 'a', 'r+', 'w+', 'a+']
        if self.mode not in valid_modes:
            raise ValueError(f"Неверный режим доступа: '{self.mode}'")

    def __enter__(self):
        try:
            self.file = open(self.filename, self.mode)
        except FileNotFoundError:
            raise CustomFileNotFoundError(self.filename)
        except PermissionError:
            raise AccessDeniedError(self.filename)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        if exc_type is not None:
            return False  # Пробрасывать исключение дальше


# Пример использования

try:
    with FileManager('data.txt', 'r') as file:
        content = file.read()
        print(content)
except CustomFileNotFoundError as e:
    print(e)
except AccessDeniedError as e:
    print(e)

# Логирование операций
try:
    with LogFile('log.txt') as logger:
        logger.log("Операция с файлом успешно завершена.")
except CustomFileNotFoundError as e:
    print(e)
except AccessDeniedError as e:
    print(e)
