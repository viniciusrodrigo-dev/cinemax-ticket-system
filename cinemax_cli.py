# Projeto: Cinemax System
# Sistema de compra de ingresso de cinema

# importação das bibliotecas
import datetime
import random
import unicodedata

# ---------------------------------------------------------------
# DADOS DO SISTEMA
# ---------------------------------------------------------------

# Variável para controlar o sistema
sistema_ativo = True

# Fila de clientes
fila_clientes = []

# Lista (e não set) para manter a ordem fixa e sem duplicatas
filmes = ['Gente Grande', 'Toy Story', 'Bad Boys', 'Carros']

# Cada filme tem os seus próprios assentos
assentos_por_filme = {
    filme: ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
    for filme in filmes
}

# Preços dos ingressos
PRECOS = {'inteira': 50, 'meia': 25}

lista_desconto = [5, 10, 15]

# Credenciais do administrador (necessárias para finalizar o sistema)
ADMIN_LOGIN = 'admin123'
ADMIN_SENHA = 'teste123'


# ---------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ---------------------------------------------------------------

def normalizar(texto):
    """Remove espaços, acentos e deixa tudo em minúsculo.
    Assim 'NÃO', 'nao', ' Não ' viram todos 'nao'."""
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return texto.strip().lower()


def ler(mensagem):
    """input() que já devolve a resposta normalizada."""
    return normalizar(input(mensagem))


def ler_sim_nao(mensagem):
    """Pergunta até receber SIM/S ou NÃO/N. Devolve True ou False."""
    while True:
        resposta = ler(mensagem)
        if resposta in ('sim', 's'):
            return True
        if resposta in ('nao', 'n'):
            return False
        print('Digite apenas SIM ou NÃO.')


def ler_inteiro(mensagem):
    """Lê um número inteiro. Devolve None se o usuário digitar algo inválido."""
    try:
        return int(input(mensagem).strip())
    except ValueError:
        return None


def ler_valor(mensagem):
    """Lê um valor em reais (aceita vírgula). Devolve None se for inválido."""
    try:
        return float(input(mensagem).strip().replace(',', '.'))
    except ValueError:
        return None


def mostrar_assentos(assentos_livres):
    """Mostra o mapa de assentos. Assentos ocupados aparecem como [XX]."""
    for fileira in ('A', 'B', 'C'):
        linha = []
        for numero in ('1', '2', '3'):
            codigo = fileira + numero
            linha.append(codigo if codigo in assentos_livres else 'XX')
        print(' '.join(linha))


def calcular_ingressos(tipo, total):
    return total + PRECOS[tipo]


def pedir_nome_cliente():
    """Pede o nome do cliente até receber um nome não vazio."""
    nome = ''
    while not nome:
        nome = input('Digite seu nome e sobrenome para começarmos o atendimento. \n:').strip()
        if not nome:
            print('O nome não pode ficar vazio!')
    return nome


def finalizar_atendimento():
    """Encerra o atendimento do cliente atual (o sistema continua ligado)."""
    cliente_atendido = fila_clientes.pop(0)
    print(f"\nAtendimento do(a) {cliente_atendido} realizado!")


def finalizar_sistema():
    """Encerra o atendimento atual e desliga o sistema."""
    finalizar_atendimento()
    print("\n=====Sistema finalizado com sucesso!=====\n")


def autenticar_admin():
    """Pede login e senha do administrador.
    Devolve True se estiverem corretos ou False se o usuário desistir."""
    while True:
        print('\n=== ACESSO DO ADMINISTRADOR ===')
        login = ler('Login: ')              # login não diferencia maiúsculas/minúsculas
        senha = input('Senha: ').strip()    # senha diferencia maiúsculas/minúsculas

        if login == ADMIN_LOGIN and senha == ADMIN_SENHA:
            return True

        print('\nLogin ou senha incorretos! Verifique os dados digitados.')

        while True:
            escolha = ler('\n|1| TENTAR NOVAMENTE'
                          '\n|2| VOLTAR ÀS OPÇÕES'
                          '\n: ')
            if escolha == '1':
                break
            elif escolha == '2':
                return False
            else:
                print('Digite apenas 1 ou 2.')


# ---------------------------------------------------------------
# INÍCIO DO ATENDIMENTO
# ---------------------------------------------------------------

nome_cliente = pedir_nome_cliente()
fila_clientes.append(nome_cliente)

# ---------------------------------------------------------------
# LAÇO PRINCIPAL DO SISTEMA
# ---------------------------------------------------------------
while sistema_ativo:

    # Cabeçalho
    print('\n=====================')
    print('       CINEMAX   ')
    print('=====================')

    # Menu principal
    print('1 - Mostrar filmes')
    print('2 - Compra de ingresso')
    print('3 - Encerrar sistema')

    opcao = ler('Escolha uma opção: ')

    # EXIBIÇÃO DOS FILMES EM CARTAZ
    if opcao == '1':
        print('\n === FILMES EM CARTAZ ===')
        for filme in filmes:
            print(filme)

    # COMPRA DE INGRESSOS
    elif opcao == '2':
        print('\n === INGRESSOS ===')

        # Dicionário para achar o filme ignorando maiúsculas/minúsculas/acentos
        filmes_normalizados = {normalizar(f): f for f in filmes}

        selecao = ler('Qual filme você quer assistir? ')

        if selecao not in filmes_normalizados:
            print('Digite apenas filmes que estão na lista (OPÇÃO 1 DO MENU)')
            continue

        filme_escolhido = filmes_normalizados[selecao]
        assentos_livres = assentos_por_filme[filme_escolhido]
        disponiveis = len(assentos_livres)

        if disponiveis == 0:
            print(f'\nDesculpe, a sessão de {filme_escolhido} está esgotada!')
            continue

        # Quantidade de ingressos
        quantidade = ler_inteiro(
            f'Quantos ingressos deseja comprar? (disponíveis: {disponiveis}) '
        )

        if quantidade is None:
            print('Digite apenas números!')
            continue

        if quantidade <= 0:
            print('Quantidade inválida!')
            continue

        if quantidade > disponiveis:
            print(f'\nQuantidade inválida, existem apenas {disponiveis} assentos disponíveis!')
            continue

        total = 0
        lista_assentos = []

        # Trabalhamos em uma CÓPIA dos assentos. Só gravamos de verdade
        # quando o cliente confirmar a reserva (assim nada se perde ao cancelar).
        assentos_temporarios = list(assentos_livres)

        for numero in range(quantidade):
            print(f'\n ======= {filme_escolhido} =======')
            print('== ESCOLHA SEU ASSENTO ==')
            mostrar_assentos(assentos_temporarios)

            # Escolha do assento
            while True:
                assento_escolhido = ler(f'Escolha o assento {numero + 1}: ').upper()

                if assento_escolhido in assentos_temporarios:
                    assentos_temporarios.remove(assento_escolhido)
                    lista_assentos.append(assento_escolhido)
                    break
                else:
                    print('Assento inválido! '
                          '\nEscolha apenas os assentos que estão disponíveis\n')

            # Escolha do tipo de ingresso (mostrando os valores)
            while True:
                tipo = ler(
                    f'Selecione o tipo do ingresso {numero + 1} '
                    f'(Inteira R${PRECOS["inteira"]:.2f} / '
                    f'Meia R${PRECOS["meia"]:.2f}): '
                )

                if tipo in PRECOS:
                    break
                else:
                    print('Digite apenas (Inteira ou Meia)')

            total = calcular_ingressos(tipo, total)

        # Desconto
        desconto = random.choice(lista_desconto)

        print('\n ===== VALOR TOTAL ====='
              f'\n O valor total dos ingressos é de: R${total:.2f} '
              f'\n Parabéns! Você ganhou um desconto de {desconto}% ')

        valor_desconto = total * (desconto / 100)
        valor_final = total - valor_desconto

        print(f'\n Valor total com desconto aplicado = R${valor_final:.2f} ')

        # Gorjeta (agora é somada ao valor final da reserva)
        if ler_sim_nao('\nDeseja adicionar uma gorjeta aos funcionários do cinema? (SIM/NÃO)\n:'):
            while True:
                valor_gorjeta = ler_valor('Qual valor você quer adicionar de gorjeta: R$')

                if valor_gorjeta is None:
                    print('Digite apenas números!')
                elif valor_gorjeta < 0:
                    print('A gorjeta não pode ser negativa!')
                else:
                    break

            valor_final += valor_gorjeta
            print(f'\nObrigado pela sua gorjeta! O valor final agora é: R${valor_final:.2f} ')

        # Confirmação da reserva
        if ler_sim_nao('Confirmar reserva? (SIM/NÃO)\n: '):
            # Agora sim os assentos ficam ocupados
            assentos_por_filme[filme_escolhido] = assentos_temporarios

            agora = datetime.datetime.now()
            data_formatada = agora.strftime('%d/%m %H:%M')

            print(f'\n === RESERVA DE {nome_cliente} CONCLUÍDA ==='
                  f'\nFILME: {filme_escolhido}'
                  f'\nASSENTOS: {" ".join(lista_assentos)}'
                  f'\nVALOR: R${valor_final:.2f}'
                  f'\nHORÁRIO DA RESERVA: {data_formatada}')

            # Opções depois de concluir a reserva
            while True:
                proxima_acao = ler('\n== ESCOLHA A OPÇÃO ABAIXO: =='
                                   '\n|1| FAZER MAIS RESERVA'
                                   '\n|2| FINALIZAR ATENDIMENTO'
                                   '\n|3| FINALIZAR SISTEMA'
                                   '\n: ')

                # 1 - Volta ao menu para o mesmo cliente fazer outra reserva
                if proxima_acao == '1':
                    break

                # 2 - Encerra este atendimento e inicia o de outra pessoa
                elif proxima_acao == '2':
                    finalizar_atendimento()
                    print('\n=== NOVO ATENDIMENTO ===')
                    nome_cliente = pedir_nome_cliente()
                    fila_clientes.append(nome_cliente)
                    break

                # 3 - Finaliza o sistema (somente com login e senha do administrador)
                elif proxima_acao == '3':
                    if autenticar_admin():
                        finalizar_sistema()
                        sistema_ativo = False
                        break
                    # se o administrador desistiu, mostra as opções de novo

                else:
                    print('Digite apenas 1, 2 ou 3.')

        else:
            # Os assentos não foram gravados, então nada precisa ser devolvido
            print('\nReserva cancelada. Os assentos continuam disponíveis.')

    # SAÍDA DO SISTEMA
    elif opcao == '3':
        if autenticar_admin():
            finalizar_sistema()
            sistema_ativo = False

    # OPÇÃO ERRADA DO MENU
    else:
        print('Opção inválida! Escolha uma opção entre 1 e 3 (somente números!)')