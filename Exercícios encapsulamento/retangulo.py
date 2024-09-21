class Retangulo:
    def __init__(self):
        self._largura = 0
        self._altura = 0

    def set_largura(self, largura):
        if largura > 0:
            self._largura = largura

    def set_altura(self, altura):
        if altura > 0:
            self._altura = altura

    def retorna_area(self):
        return self._largura * self._altura

    def retorna_perimetro(self):
        return 2 * (self._largura + self._altura)

class TestaRetangulo:
    @staticmethod
    def main():
        r = Retangulo()
        r.set_altura(5)
        r.set_largura(10)

        print("Área:", r.retorna_area())
        print("Perímetro:", r.retorna_perimetro())

TestaRetangulo.main()
