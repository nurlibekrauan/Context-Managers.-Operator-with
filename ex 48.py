# Менеджеры контекстов. Оператор with


# fp = None
# try:
#     with open("stepik 48/myfile.txt") as fp:
#         for t in fp:
#             print(t)
# except Exception as e:
#     print(e)
class DefenerVector:
    def __init__(self, v):
        self.__v = v

    def __enter__(self):  # в момент инициализации менеджера контекста
        self.__temp = self.__v[:]  # делаем копию вектора v
        return self.__temp

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.__v[:] = self.__temp
        return False


v1 = [1, 2, 3]
v2 = [1, 2, 3]
try:
    with DefenerVector(v1) as dv:
        for i, a in enumerate(dv):
            dv[i] += v2[i]
except:
    print("Ошибка внутри менеджера контекста")

print(v1)
