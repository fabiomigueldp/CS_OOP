import math

class Quadrado:
    def __init__(self, lado):
        self._lado = lado

    def set_lado(self, lado):
        self._lado = lado

    def get_lado(self):
        return self._lado

    def area(self):
        return self._lado ** 2

    def perimetro(self):
        return 4 * self._lado

    def diagonal(self):
        return self._lado * math.sqrt(2)

class TestaQuadrado:
    @staticmethod
    def main():
        q = Quadrado(4)

        print("Lado:", q.get_lado())
        q.set_lado(5)
        print("Área:", q.area())
        print("Perímetro:", q.perimetro())
        print("Diagonal:", q.diagonal())

TestaQuadrado.main()
