# 🎬 Cinemax System

Sistema de compra de ingressos de cinema feito em Python, executado no terminal.
O cliente escolhe o filme, os assentos e o tipo de ingresso, recebe um desconto
e confirma a reserva. Vários clientes podem ser atendidos na mesma execução.

## Funcionalidades

- **Lista de filmes em cartaz** com ordem fixa.
- **Compra de ingressos** com escolha de assento para cada ingresso.
- **Mapa de assentos por filme**: cada filme tem os seus próprios assentos, e os ocupados aparecem como `XX`.
- **Tipos de ingresso** com o valor exibido antes da escolha:
  - Inteira: R$ 50,00
  - Meia: R$ 25,00
- **Desconto sorteado** de 5%, 10% ou 15% sobre o total.
- **Gorjeta opcional** para os funcionários, somada ao valor final.
- **Confirmação da reserva**: os assentos só ficam ocupados depois que o cliente confirma. Se cancelar, continuam livres.
- **Comprovante** com cliente, filme, assentos, valor final e horário da reserva.
- **Vários atendimentos** na mesma execução, sem precisar reiniciar o sistema.
- **Encerramento protegido** por login e senha de administrador.

## Requisitos

- Python 3.6 ou superior
- Nenhuma biblioteca externa (usa apenas `datetime`, `random` e `unicodedata`, que já vêm com o Python)

## Como executar

```bash
python cinemax_projeto2.py
```

## Como usar

1. Digite seu nome e sobrenome para iniciar o atendimento.
2. No menu principal, escolha uma opção:

   | Opção | Ação |
   |-------|------|
   | `1` | Mostrar filmes em cartaz |
   | `2` | Comprar ingresso |
   | `3` | Encerrar o sistema (exige login de administrador) |

3. Na compra de ingresso:
   1. Digite o nome do filme (conforme a opção 1 do menu).
   2. Informe a quantidade de ingressos.
   3. Para cada ingresso, escolha o assento (ex.: `A1`) e o tipo (`Inteira` ou `Meia`).
   4. Veja o total e o desconto aplicado.
   5. Informe se deseja deixar gorjeta.
   6. Confirme ou cancele a reserva.

### Depois da reserva concluída

| Opção | Ação |
|-------|------|
| `1` - Fazer mais reserva | Volta ao menu para o mesmo cliente fazer outro pedido |
| `2` - Finalizar atendimento | Encerra o atendimento atual, pede o nome de outra pessoa e volta ao menu. Os assentos já reservados continuam ocupados |
| `3` - Finalizar sistema | Pede login e senha de administrador e, se estiverem corretos, desliga o sistema |

Se o login ou a senha estiverem errados, o sistema avisa e oferece
**tentar novamente** ou **voltar às opções**.

### Acesso do administrador

Os dados ficam nas constantes `ADMIN_LOGIN` e `ADMIN_SENHA`, no início do código:

| Campo | Valor |
|-------|-------|
| Login | `admin123` |
| Senha | `teste123` |

O login não diferencia maiúsculas de minúsculas, mas a senha diferencia.

### As respostas não diferenciam maiúsculas, minúsculas ou acentos

`MEIA`, `meia` e ` Meia ` funcionam igual. Nas perguntas de sim/não,
`SIM`, `sim` e `s` valem como sim, e `NÃO`, `nao` e `n` valem como não.

## Exemplo de execução

```
Digite seu nome e sobrenome para começarmos o atendimento.
:Maria Souza

=====================
       CINEMAX
=====================
1 - Mostrar filmes
2 - Compra de ingresso
3 - Encerrar sistema
Escolha uma opção: 2

 === INGRESSOS ===
Qual filme você quer assistir? toy story
Quantos ingressos deseja comprar? (disponíveis: 9) 1

 ======= Toy Story =======
== ESCOLHA SEU ASSENTO ==
A1 A2 A3
B1 B2 B3
C1 C2 C3
Escolha o assento 1: a1
Selecione o tipo do ingresso 1 (Inteira R$50.00 / Meia R$25.00): meia
```

## Estrutura do código

| Parte | Descrição |
|-------|-----------|
| `filmes` | Lista dos filmes em cartaz |
| `assentos_por_filme` | Dicionário com os assentos livres de cada filme |
| `PRECOS` | Valores da inteira e da meia |
| `lista_desconto` | Percentuais possíveis de desconto |
| `ADMIN_LOGIN` / `ADMIN_SENHA` | Credenciais do administrador |
| `normalizar()` | Tira espaços e acentos e converte para minúsculo |
| `ler()` | `input()` que já devolve a resposta normalizada |
| `ler_sim_nao()` | Repete a pergunta até receber sim ou não |
| `ler_inteiro()` / `ler_valor()` | Leitura segura de números, sem travar o programa |
| `mostrar_assentos()` | Exibe o mapa de assentos |
| `calcular_ingressos()` | Soma o valor do ingresso ao total |
| `pedir_nome_cliente()` | Pede o nome do cliente até receber um nome válido |
| `finalizar_atendimento()` | Encerra o atendimento do cliente atual |
| `finalizar_sistema()` | Encerra o atendimento atual e desliga o sistema |
| `autenticar_admin()` | Confere login e senha do administrador |

## Como personalizar

- **Adicionar um filme:** inclua o nome na lista `filmes`. Os assentos dele são criados automaticamente.
- **Alterar preços:** edite o dicionário `PRECOS`.
- **Alterar descontos:** edite a lista `lista_desconto`.
- **Alterar login e senha:** edite `ADMIN_LOGIN` e `ADMIN_SENHA`.
- **Alterar assentos:** edite a lista de assentos dentro de `assentos_por_filme`. Se mudar o número de fileiras ou colunas, ajuste também `mostrar_assentos()`.

## Limitações conhecidas

- Os dados não são salvos em arquivo ou banco: ao encerrar o programa, as reservas e os assentos ocupados são perdidos.
- Existe uma única sessão por filme.
- O desconto é sorteado, sem relação com regras reais de promoção.
- O login e a senha ficam escritos no código, o que serve para um projeto de demonstração, mas não para um sistema real.

## Sobre o projeto

Projeto pessoal desenvolvido para portfólio.
