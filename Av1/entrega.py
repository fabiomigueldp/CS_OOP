from datetime import datetime

class Pessoa:
    def __init__(self, nome, documento):
        self.nome = nome
        self.documento = documento

class Funcionario(Pessoa):
    def __init__(self, nome, documento, cracha):
        super().__init__(nome, documento)
        self.cracha = cracha

class Visitante(Pessoa):
    def __init__(self, nome, documento):
        super().__init__(nome, documento)
        self.cracha = None
        self.empresa = None

class VisitantePessoaFisica(Visitante):
    pass

class VisitanteEmpresa(Visitante):
    def __init__(self, nome, documento, empresa):
        super().__init__(nome, documento)
        self.empresa = empresa

class Cracha:
    def __init__(self, id):
        self.id = id
        self.disponivel = True
        self.visitante = None

class LogAcesso:
    def __init__(self, visitante, tipo_acesso, data_hora):
        self.visitante = visitante
        self.tipo_acesso = tipo_acesso  # 'Entrada' ou 'Saída'
        self.data_hora = data_hora
        self.cracha_id = visitante.cracha.id if visitante.cracha else None

class ControleAcesso:
    def __init__(self):
        self.visitantes_no_predio = []
        self.historico_acessos = []
        self.crachas = [Cracha(id) for id in range(1, 101)]
        self.visitantes_registrados = []

    def registrar_entrada_visitante(self):
        print("\nRegistrar entrada de visitante")
        documento = input("Documento: ")
        if not documento:
            print("Documento não pode ser vazio.")
            return
        # Verifica se o visitante já está registrado
        visitante = None
        for v in self.visitantes_registrados:
            if v.documento == documento:
                visitante = v
                break
        if visitante:
            print(f"Visitante já registrado: {visitante.nome}")
        else:
            nome = input("Nome: ").strip()
            if not nome:
                print("Nome não pode ser vazio.")
                return
            tipo_visitante = input("Tipo de visitante (1 - Pessoa Física, 2 - Empresa): ").strip()
            if tipo_visitante == '1':
                visitante = VisitantePessoaFisica(nome, documento)
            elif tipo_visitante == '2':
                empresa = input("Nome da empresa: ").strip()
                if not empresa:
                    print("Nome da empresa não pode ser vazio.")
                    return
                visitante = VisitanteEmpresa(nome, documento, empresa)
            else:
                print("Tipo de visitante inválido.")
                return
            self.visitantes_registrados.append(visitante)
        # Verifica se o visitante já está no prédio
        for v in self.visitantes_no_predio:
            if v.documento == visitante.documento:
                print("Visitante já está no prédio.")
                return
        # Atribui um crachá disponível
        cracha_disponivel = None
        for cracha in self.crachas:
            if cracha.disponivel:
                cracha_disponivel = cracha
                break
        if cracha_disponivel is None:
            print("Não há crachás disponíveis no momento.")
            return
        # Atribui o crachá ao visitante
        cracha_disponivel.disponivel = False
        cracha_disponivel.visitante = visitante
        visitante.cracha = cracha_disponivel
        # Adiciona o visitante à lista de visitantes no prédio
        self.visitantes_no_predio.append(visitante)
        # Registra o acesso
        log = LogAcesso(visitante, 'Entrada', datetime.now())
        self.historico_acessos.append(log)
        print(f"Entrada registrada com sucesso. Crachá {cracha_disponivel.id} atribuído ao visitante.")

    def registrar_saida_visitante(self):
        print("\nRegistrar saída de visitante")
        documento = input("Documento do visitante: ").strip()
        if not documento:
            print("Documento não pode ser vazio.")
            return
        visitante = None
        for v in self.visitantes_no_predio:
            if v.documento == documento:
                visitante = v
                break
        if visitante is None:
            print("Visitante não encontrado no prédio.")
            return
        # Devolve o crachá
        cracha = visitante.cracha
        cracha.disponivel = True
        cracha.visitante = None
        visitante.cracha = None
        # Remove o visitante da lista
        self.visitantes_no_predio.remove(visitante)
        # Registra o acesso
        log = LogAcesso(visitante, 'Saída', datetime.now())
        self.historico_acessos.append(log)
        print(f"Saída registrada com sucesso. Crachá {cracha.id} devolvido.")

    def consultar_visitantes_no_predio(self):
        print("\nVisitantes atualmente no prédio:")
        if not self.visitantes_no_predio:
            print("Nenhum visitante no prédio no momento.")
            return
        for v in self.visitantes_no_predio:
            print(f"Nome: {v.nome}, Documento: {v.documento}, Crachá: {v.cracha.id}")

    def consultar_historico_visitantes(self):
        print("\nHistórico de acessos:")
        if not self.historico_acessos:
            print("Nenhum acesso registrado.")
            return
        for log in self.historico_acessos:
            data_hora = log.data_hora.strftime("%d/%m/%Y %H:%M:%S")
            print(f"{data_hora} - {log.tipo_acesso} - Nome: {log.visitante.nome}, Documento: {log.visitante.documento}, Crachá: {log.cracha_id}")

    def executar(self):
        while True:
            print("\nSistema de Controle de Acesso")
            print("1 - Registrar entrada de visitante")
            print("2 - Registrar saída de visitante")
            print("3 - Consultar visitantes no prédio")
            print("4 - Consultar histórico de acessos")
            print("5 - Sair")
            opcao = input("Selecione uma opção: ").strip()
            if opcao == '1':
                self.registrar_entrada_visitante()
            elif opcao == '2':
                self.registrar_saida_visitante()
            elif opcao == '3':
                self.consultar_visitantes_no_predio()
            elif opcao == '4':
                self.consultar_historico_visitantes()
            elif opcao == '5':
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    sistema = ControleAcesso()
    sistema.executar()
