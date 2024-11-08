from abc import ABC, abstractmethod
import math

class FormaGeometrica(ABC):
    @abstractmethod
    def calcular_perimetro(self):
        pass

    @abstractmethod
    def calcular_area(self):
        pass

class Quadrilatero(FormaGeometrica):
    def __init__(self, lado1, lado2, lado3, lado4):
        self.lado1 = lado1
        self.lado2 = lado2
        self.lado3 = lado3
        self.lado4 = lado4

    def calcular_perimetro(self):
        return self.lado1 + self.lado2 + self.lado3 + self.lado4

class Retangulo(Quadrilatero):
    def __init__(self, base, altura):
        super().__init__(base, altura, base, altura)
        self.base = base
        self.altura = altura

    def calcular_area(self):
        return self.base * self.altura

    def representar(self):
        print('*' * self.base)
        for _ in range(self.altura - 2):
            print('*' + ' ' * (self.base - 2) + '*')
        print('*' * self.base)

class Quadrado(Quadrilatero):
    def __init__(self, lado):
        super().__init__(lado, lado, lado, lado)
        self.lado = lado

    def calcular_area(self):
        return self.lado * self.lado

    def representar(self):
        print('*' * self.lado)
        for _ in range(self.lado - 2):
            print('*' + ' ' * (self.lado - 2) + '*')
        print('*' * self.lado)

class Circulo(FormaGeometrica):
    def __init__(self, raio):
        self.raio = raio

    def calcular_perimetro(self):
        return 2 * math.pi * self.raio

    def calcular_area(self):
        return math.pi * (self.raio ** 2)

def main():
    while True:
        print("\nEscolha uma forma geométrica para criar:")
        print("1 - Retângulo")
        print("2 - Quadrado")
        print("3 - Círculo")
        print("4 - Sair")
        opcao = input("Opção: ")

        if opcao == '1':
            base = int(input("Digite a base do retângulo: "))
            altura = int(input("Digite a altura do retângulo: "))
            retangulo = Retangulo(base, altura)
            print("\nRepresentação do Retângulo:")
            retangulo.representar()
            print(f"Área = {retangulo.calcular_area()}")
            print(f"Perímetro = {retangulo.calcular_perimetro()}")

        elif opcao == '2':
            lado = int(input("Digite o lado do quadrado: "))
            quadrado = Quadrado(lado)
            print("\nRepresentação do Quadrado:")
            quadrado.representar()
            print(f"Área = {quadrado.calcular_area()}")
            print(f"Perímetro = {quadrado.calcular_perimetro()}")

        elif opcao == '3':
            raio = float(input("Digite o raio do círculo: "))
            circulo = Circulo(raio)
            print(f"Área do Círculo = {circulo.calcular_area():.2f}")
            print(f"Perímetro do Círculo = {circulo.calcular_perimetro():.2f}")

        elif opcao == '4':
            print("Saindo...")
            break

        else:
            print("Opção inválida, tente novamente.")

main()

