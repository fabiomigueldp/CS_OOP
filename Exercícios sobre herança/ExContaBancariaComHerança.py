# Classe base ContaBancaria
class ContaBancaria:
    def __init__(self, numeroDaConta, saldoInicial=0.0, contaAtiva=True):
        if saldoInicial < 0:
            raise ValueError("Saldo inicial não pode ser negativo")

        self.__numeroDaConta = numeroDaConta
        self.__saldo = saldoInicial
        self.__contaAtiva = contaAtiva
        self.__mesDaConta = 1

        self.__historico = []
        self.__historico.append(f'Conta {self.__numeroDaConta} criada com sucesso.')
        self.__historico.append(f'Saldo inicial: R$ {self.__saldo}')
        self.__historico.append(f'Conta ativa: {self.__contaAtiva}')

    # Getters e Setters
    def getNumeroDaConta(self):
        return self.__numeroDaConta

    def getSaldo(self):
        return self.__saldo

    def setSaldo(self, saldo):
        if saldo < 0:
            raise ValueError("Saldo não pode ser negativo")
        self.__saldo = saldo
        self.__historico.append(f'Saldo alterado para R$ {self.__saldo}')

    def getContaAtiva(self):
        return self.__contaAtiva

    def setContaAtiva(self, contaAtiva):
        self.__contaAtiva = contaAtiva
        self.__historico.append(f'Conta ativa: {self.__contaAtiva}')

    def setContaInativa(self):
        self.__contaAtiva = False
        self.__historico.append('Conta inativada com sucesso.')

    def getHistorico(self):
        return self.__historico

    # Métodos comuns
    def deposito(self, valor):
        if valor < 0:
            raise ValueError("Valor do depósito não pode ser negativo")
        self.__saldo += valor
        self.__historico.append(f'Depósito de R$ {valor} realizado com sucesso.')
        self.__historico.append(f'Saldo atual: R$ {self.__saldo}')

    def saque(self, valor):
        if valor < 0:
            raise ValueError("Valor do saque não pode ser negativo")
        if valor > self.__saldo:
            raise ValueError("Saldo insuficiente")
        self.__saldo -= valor
        self.__historico.append(f'Saque de R$ {valor} realizado com sucesso.')
        self.__historico.append(f'Saldo atual: R$ {self.__saldo}')

    def passarMes(self):
        self.__historico.append(f'Mês {self.__mesDaConta} passado com sucesso.')
        self.__mesDaConta += 1

    def extrato(self, n_meses=None):
        meses = []
        current_mes = {'mes': 1, 'transacoes': []}

        for entrada in self.__historico:
            if entrada.startswith('Mês') and 'passado com sucesso' in entrada:
                meses.append(current_mes)
                try:
                    mes_num = int(entrada.split()[1])
                except (IndexError, ValueError):
                    mes_num = current_mes['mes'] + 1
                current_mes = {'mes': mes_num, 'transacoes': []}
            else:
                current_mes['transacoes'].append(entrada)

        meses.append(current_mes)

        if n_meses is not None:
            if n_meses <= 0:
                raise ValueError("O número de meses deve ser positivo")
            meses = meses[-n_meses:]

        extrato_formatado = ""
        for mes in meses:
            extrato_formatado += f"\n--- Mês {mes['mes']} ---\n"
            for transacao in mes['transacoes']:
                extrato_formatado += transacao + "\n"

        return extrato_formatado.strip()

# Subclasse ContaCorrente
class ContaCorrente(ContaBancaria):
    _jurosChequeEspecial = 1.2

    def __init__(self, numeroDaConta, saldoInicial=0.0, limiteChequeEspecial=0.0, usoChequeEspecial=0.0, contaAtiva=True):
        super().__init__(numeroDaConta, saldoInicial, contaAtiva)
        if limiteChequeEspecial < 0 or usoChequeEspecial < 0:
            raise ValueError("Valores iniciais não podem ser negativos")
        self.__limiteChequeEspecial = limiteChequeEspecial
        self.__usoChequeEspecial = usoChequeEspecial
        self.getHistorico().append(f'Limite do cheque especial: R$ {self.__limiteChequeEspecial}')
        self.getHistorico().append(f'Uso inicial do cheque especial: R$ {self.__usoChequeEspecial}')

    # Getters e Setters específicos
    def getLimiteChequeEspecial(self):
        return self.__limiteChequeEspecial

    def setLimiteChequeEspecial(self, limiteChequeEspecial):
        if limiteChequeEspecial < self.__usoChequeEspecial:
            raise ValueError("Limite do cheque especial não pode ser menor que o uso do cheque especial")
        self.__limiteChequeEspecial = limiteChequeEspecial
        self.getHistorico().append(f'Limite do cheque especial alterado para R$ {self.__limiteChequeEspecial}')

    def getUsoChequeEspecial(self):
        return self.__usoChequeEspecial

    def setUsoChequeEspecial(self, usoChequeEspecial):
        if usoChequeEspecial > self.__limiteChequeEspecial:
            raise ValueError("Uso do cheque especial não pode ser maior que o limite do cheque especial")
        self.__usoChequeEspecial = usoChequeEspecial
        self.getHistorico().append(f'Uso do cheque especial alterado para R$ {self.__usoChequeEspecial}')

    # Métodos específicos
    def saque(self, valor):
        if valor < 0:
            raise ValueError("Valor do saque não pode ser negativo")
        saldo_disponivel = self.getSaldo() + self.__limiteChequeEspecial - self.__usoChequeEspecial
        if valor > saldo_disponivel:
            raise ValueError("Saldo insuficiente")

        valor_original = valor

        if valor > self.getSaldo():
            valor -= self.getSaldo()
            self.setSaldo(0)
            self.__usoChequeEspecial += valor
        else:
            self.setSaldo(self.getSaldo() - valor)

        self.getHistorico().append(f'Saque de R$ {valor_original} realizado com sucesso.')
        self.getHistorico().append(f'Saldo atual: R$ {self.getSaldo()}')
        self.getHistorico().append(f'Uso do cheque especial: R$ {self.__usoChequeEspecial}')

    def deposito(self, valor):
        if valor < 0:
            raise ValueError("Valor do depósito não pode ser negativo")

        valor_original = valor

        if self.__usoChequeEspecial > 0:
            if valor > self.__usoChequeEspecial:
                valor -= self.__usoChequeEspecial
                self.__usoChequeEspecial = 0
            else:
                self.__usoChequeEspecial -= valor
                valor = 0

        self.setSaldo(self.getSaldo() + valor)
        self.getHistorico().append(f'Depósito de R$ {valor_original} realizado com sucesso.')
        self.getHistorico().append(f'Saldo atual: R$ {self.getSaldo()}')
        self.getHistorico().append(f'Uso do cheque especial: R$ {self.__usoChequeEspecial}')

    def calcularJurosChequeEspecial(self):
        if self.__usoChequeEspecial > 0:
            saldo_anterior = self.__usoChequeEspecial
            self.__usoChequeEspecial *= ContaCorrente._jurosChequeEspecial
            self.getHistorico().append(f'Juros do cheque especial: R$ {self.__usoChequeEspecial - saldo_anterior}')
            self.getHistorico().append(f'Uso do cheque especial: R$ {self.__usoChequeEspecial}')

    def passarMes(self):
        super().passarMes()
        self.calcularJurosChequeEspecial()

    def transferencia(self, valor, contaDestino):
        if valor < 0:
            raise ValueError("Valor da transferência não pode ser negativo")

        saldo_disponivel = self.getSaldo() + self.__limiteChequeEspecial - self.__usoChequeEspecial
        if valor > saldo_disponivel:
            raise ValueError("Saldo insuficiente")

        valor_original = valor

        if valor > self.getSaldo():
            valor -= self.getSaldo()
            self.setSaldo(0)
            self.__usoChequeEspecial += valor
        else:
            self.setSaldo(self.getSaldo() - valor)

        contaDestino.deposito(valor_original)
        self.getHistorico().append(f'Transferência de R$ {valor_original} para a conta {contaDestino.getNumeroDaConta()} realizada com sucesso.')
        self.getHistorico().append(f'Saldo atual: R$ {self.getSaldo()}')
        self.getHistorico().append(f'Uso do cheque especial: R$ {self.__usoChequeEspecial}')

# Subclasse ContaPoupanca
class ContaPoupanca(ContaBancaria):
    _rendimentoPoupanca = 1.05

    def __init__(self, numeroDaConta, saldoInicial=0.0, contaAtiva=True):
        super().__init__(numeroDaConta, saldoInicial, contaAtiva)

    # Métodos específicos
    def calcularRendimentoPoupanca(self):
        saldo_anterior = self.getSaldo()
        self.setSaldo(self.getSaldo() * ContaPoupanca._rendimentoPoupanca)
        self.getHistorico().append(f'Rendimento da poupança: R$ {self.getSaldo() - saldo_anterior}')
        self.getHistorico().append(f'Saldo atual: R$ {self.getSaldo()}')

    def passarMes(self):
        super().passarMes()
        self.calcularRendimentoPoupanca()

    def transferencia(self, valor, contaDestino):
        if valor < 0:
            raise ValueError("Valor da transferência não pode ser negativo")
        if valor > self.getSaldo():
            raise ValueError("Saldo insuficiente")
        self.setSaldo(self.getSaldo() - valor)
        contaDestino.deposito(valor)
        self.getHistorico().append(f'Transferência de R$ {valor} para a conta {contaDestino.getNumeroDaConta()} realizada com sucesso.')
        self.getHistorico().append(f'Saldo atual: R$ {self.getSaldo()}')

# Classe Banco
class Banco:
    def __init__(self, nome):
        self.nome = nome
        self.contas = {}
        self.next_account_number = 1

    def abrir_conta_corrente(self, saldoInicial=0.0, limiteChequeEspecial=0.0, usoChequeEspecial=0.0):
        numeroDaConta = self.next_account_number
        self.next_account_number += 1
        conta = ContaCorrente(
            numeroDaConta=numeroDaConta,
            saldoInicial=saldoInicial,
            limiteChequeEspecial=limiteChequeEspecial,
            usoChequeEspecial=usoChequeEspecial
        )
        self.contas[numeroDaConta] = conta
        print(f"Conta Corrente {numeroDaConta} aberta com sucesso.")

    def abrir_conta_poupanca(self, saldoInicial=0.0):
        numeroDaConta = self.next_account_number
        self.next_account_number += 1
        conta = ContaPoupanca(
            numeroDaConta=numeroDaConta,
            saldoInicial=saldoInicial
        )
        self.contas[numeroDaConta] = conta
        print(f"Conta Poupança {numeroDaConta} aberta com sucesso.")

    def encerrar_conta(self, numeroDaConta):
        conta = self.contas.get(numeroDaConta)
        if not conta:
            raise ValueError(f"Conta {numeroDaConta} não encontrada.")
        if conta.getSaldo() != 0:
            raise ValueError("A conta deve estar com saldo zero para ser encerrada.")
        if isinstance(conta, ContaCorrente) and conta.getUsoChequeEspecial() != 0:
            raise ValueError("A conta corrente deve estar sem uso do cheque especial para ser encerrada.")
        conta.setContaInativa()
        del self.contas[numeroDaConta]
        print(f"Conta {numeroDaConta} encerrada com sucesso.")

    def listar_contas(self):
        if not self.contas:
            print("Nenhuma conta cadastrada.")
            return
        for numero, conta in self.contas.items():
            status = "Ativa" if conta.getContaAtiva() else "Inativa"
            tipo = "Corrente" if isinstance(conta, ContaCorrente) else "Poupança"
            print(f"Conta {numero} ({tipo}): Saldo=R$ {conta.getSaldo()}, Status={status}")

    def passar_mes(self):
        for conta in self.contas.values():
            conta.passarMes()
        print("Um mês passou. Rendimentos e juros atualizados.")

    def obter_conta(self, numeroDaConta):
        conta = self.contas.get(numeroDaConta)
        if not conta:
            raise ValueError(f"Conta {numeroDaConta} não encontrada.")
        return conta

    # Métodos para interagir com as contas
    def deposito(self, numeroDaConta, valor):
        conta = self.obter_conta(numeroDaConta)
        conta.deposito(valor)
        print(f"Depósito de R$ {valor} realizado na conta {numeroDaConta}.")

    def saque(self, numeroDaConta, valor):
        conta = self.obter_conta(numeroDaConta)
        conta.saque(valor)
        print(f"Saque de R$ {valor} realizado na conta {numeroDaConta}.")

    def transferencia(self, origem, destino, valor):
        conta_origem = self.obter_conta(origem)
        conta_destino = self.obter_conta(destino)
        conta_origem.transferencia(valor, conta_destino)
        print(f"Transferência de R$ {valor} da conta {origem} para a conta {destino} realizada com sucesso.")

    def extrato_conta(self, numeroDaConta, n_meses=None):
        conta = self.obter_conta(numeroDaConta)
        extrato = conta.extrato(n_meses)
        print(f"Extrato da conta {numeroDaConta}:")
        print(extrato)

# Classe Interface
class Interface:
    def __init__(self):
        self.banco = Banco("Banco")
        self.run()

    def run(self):
        while True:
            print("\nBem-vindo ao sistema do banco.")
            print("1. Abrir conta corrente")
            print("2. Abrir conta poupança")
            print("3. Encerrar conta")
            print("4. Listar contas")
            print("5. Depositar")
            print("6. Sacar")
            print("7. Transferir")
            print("8. Passar um mês")
            print("9. Ver extrato")
            print("10. Sair")
            choice = input("Escolha uma opção: ")

            if choice == '1':
                self.abrir_conta_corrente()
            elif choice == '2':
                self.abrir_conta_poupanca()
            elif choice == '3':
                self.encerrar_conta()
            elif choice == '4':
                self.banco.listar_contas()
            elif choice == '5':
                self.deposito()
            elif choice == '6':
                self.saque()
            elif choice == '7':
                self.transferencia()
            elif choice == '8':
                self.banco.passar_mes()
            elif choice == '9':
                self.extrato_conta()
            elif choice == '10':
                print("Obrigado por usar o sistema do banco.")
                break
            else:
                print("Opção inválida.")

    def abrir_conta_corrente(self):
        try:
            saldo_inicial = float(input("Digite o saldo inicial da conta corrente: "))
            limite_cheque_especial = float(input("Digite o limite do cheque especial: "))
            self.banco.abrir_conta_corrente(
                saldoInicial=saldo_inicial,
                limiteChequeEspecial=limite_cheque_especial
            )
        except ValueError as e:
            print(f"Erro ao abrir conta corrente: {e}")

    def abrir_conta_poupanca(self):
        try:
            saldo_inicial = float(input("Digite o saldo inicial da poupança: "))
            self.banco.abrir_conta_poupanca(
                saldoInicial=saldo_inicial
            )
        except ValueError as e:
            print(f"Erro ao abrir conta poupança: {e}")

    def encerrar_conta(self):
        try:
            numero_conta = int(input("Digite o número da conta a encerrar: "))
            self.banco.encerrar_conta(numero_conta)
        except ValueError as e:
            print(f"Erro ao encerrar conta: {e}")

    def deposito(self):
        try:
            numero_conta = int(input("Digite o número da conta: "))
            valor = float(input("Digite o valor a depositar: "))
            self.banco.deposito(numero_conta, valor)
        except ValueError as e:
            print(f"Erro ao depositar: {e}")

    def saque(self):
        try:
            numero_conta = int(input("Digite o número da conta: "))
            valor = float(input("Digite o valor a sacar: "))
            self.banco.saque(numero_conta, valor)
        except ValueError as e:
            print(f"Erro ao sacar: {e}")

    def transferencia(self):
        try:
            conta_origem = int(input("Digite o número da conta de origem: "))
            conta_destino = int(input("Digite o número da conta de destino: "))
            valor = float(input("Digite o valor a transferir: "))
            self.banco.transferencia(conta_origem, conta_destino, valor)
        except ValueError as e:
            print(f"Erro na transferência: {e}")

    def extrato_conta(self):
        try:
            numero_conta = int(input("Digite o número da conta: "))
            n_meses = input("Digite o número de meses (ou deixe em branco para todos): ")
            if n_meses == '':
                n_meses = None
            else:
                n_meses = int(n_meses)
            self.banco.extrato_conta(numero_conta, n_meses)
        except ValueError as e:
            print(f"Erro ao obter extrato: {e}")

if __name__ == "__main__":
    Interface()
