Projeto a 2ª Avaliação da Disciplina de Coding 

Grupo: 

Davi Da Rocha Cardoso - 03367865
Lucas Henrique Do Nascimento De Aquino - 03361343
Paulo Henrique Silva de Freitas - 03368584

# 🎬 PrismaVHS- Sistema de Gerenciamento de Locadora de Filmes

## 📋 Descrição e Objetivos
O PrismaVHS é um sistema de gerenciamento via terminal desenvolvido em Python puro para automatizar o controle de uma locadora de filmes. O projeto aplica conceitos de modularização, funções, estruturas de dados em memória (listas e dicionários), validações de regras de negócio e desenvolvimento colaborativo via Git/GitHub.

## ⚙️ Funcionalidades
- Gerenciamento de Clientes (CRUD): Cadastro com validação de CPF único e idade, listagem, atualização de dados e exclusão protegida.

- Gerenciamento de Filmes (CRUD): Cadastro de títulos com gênero, classificação indicativa, valor da diária e controle de cópias em estoque; consulta, edição e exclusão.

- Controle de Locações:  Empréstimo de filmes com baixa automática de estoque, validação de faixa etária e devolução com cálculo de multa por atraso.

- Relatórios Gerenciais: Resumo de clientes, catálogo, cópias disponíveis vs. alugadas, histórico de locações e faturamento total.

## 🛡️ Regras de Negócio Implementadas

1. Unicidade: Não permite cadastrar dois clientes com o mesmo CPF ou dois filmes com o mesmo título.

2. Classificação Indicativa: Bloqueia automaticamente a locação caso a idade do cliente seja inferior à classificação etária do filme (Livre, 10, 12, 14, 16 ou 18 anos).

3. Limite Simultâneo: Cada cliente pode manter no máximo 3 filmes alugados ao mesmo tempo.

4. Desconto Combo: Clientes que já possuem um filme alugado ganham 15% de desconto ao alugar títulos adicionais.

5. Multa por Atraso: Na devolução, cada dia de atraso gera multa de R$ 5,00 + o valor de 1 diária do filme.

6. Integridade de Dados: Impede excluir clientes com filmes pendentes ou filmes que possuam cópias alugadas no momento.

## 🗂️ Organização do Código
- `app.py`: Arquivo principal responsável pelo menu e navegação do sistema.
- `dados.py`: Listas em memória (`clientes`, `filmes`, `locacoes`) para armazenamento volátil dos dados.
- `clientes.py`: Módulo com funções de CRUD e validações de clientes.
- `filmes.py`: Módulo com funções de CRUD do catálogo e estoque de filmes.
- `locacoes.py`: Módulo com regras de negócio de aluguel, devolução, multas e relatórios.

