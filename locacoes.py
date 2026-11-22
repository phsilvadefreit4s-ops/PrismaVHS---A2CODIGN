from dados import locacoes, filmes, clientes
from clientes import listar_clientes, buscar_cliente_por_id
from filmes import listar_filmes, buscar_filme_por_id

def gerar_id_locacao():
    if not locacoes:
        return 1
    return max(l["id"] for l in locacoes) + 1

def alugar_filme():
    print("\n--- REGISTRAR NOVA LOCAÇÃO ---")
    if not clientes or not filmes:
        print("[ERRO] É necessário ter clientes e filmes cadastrados.")
        return

    listar_clientes()
    try:
        id_cliente = int(input("\nDigite o ID do Cliente: "))
    except ValueError:
        print("[ERRO] ID inválido.")
        return

    cliente = buscar_cliente_por_id(id_cliente)
    if not cliente:
        print("[ERRO] Cliente não encontrado.")
        return

    
    ativas_cliente = [l for l in locacoes if l["cliente_id"] == id_cliente and l["ativa"]]
    if len(ativas_cliente) >= 3:
        print("[ERRO] Limite atingido! Este cliente já possui 3 filmes alugados simultaneamente.")
        return

    listar_filmes(apenas_disponiveis=True)
    try:
        id_filme = int(input("\nDigite o ID do Filme desejado: "))
    except ValueError:
        print("[ERRO] ID inválido.")
        return

    filme = buscar_filme_por_id(id_filme)
    if not filme or filme["copias_disponiveis"] <= 0:
        print("[ERRO] Filme inexistente ou sem cópias disponíveis em estoque.")
        return

    
    if cliente["idade"] < filme["classificacao"]:
        print(f"[BLOQUEADO] O cliente tem {cliente['idade']} anos e o filme '{filme['titulo']}' tem classificação +{filme['classificacao']} anos.")
        return

    try:
        dias = int(input("Quantidade de dias de locação (1 a 7): "))
        if dias < 1 or dias > 7:
            print("[ERRO] O prazo de locação deve ser entre 1 e 7 dias.")
            return
    except ValueError:
        print("[ERRO] Informe um número válido de dias.")
        return

    subtotal = dias * filme["valor_diaria"]
    
    desconto = subtotal * 0.15 if len(ativas_cliente) >= 1 else 0.0
    total = subtotal - desconto

    
    filme["copias_disponiveis"] -= 1

    nova_locacao = {
        "id": gerar_id_locacao(),
        "cliente_id": cliente["id"],
        "cliente_nome": cliente["nome"],
        "filme_id": filme["id"],
        "filme_titulo": filme["titulo"],
        "dias": dias,
        "valor_total": total,
        "ativa": True
    }
    locacoes.append(nova_locacao)

    print("\n[SUCESSO] Locação registrada!")
    print(f"Contrato #{nova_locacao['id']} | Cliente: {cliente['nome']} | Filme: {filme['titulo']} ({dias} dia(s))")
    if desconto > 0:
        print(f"Desconto Combo (15% por múltiplas locações): -R$ {desconto:.2f}")
    print(f"Valor Total: R$ {total:.2f}")

def devolver_filme():
    print("\n--- DEVOLUÇÃO DE FILME ---")
    ativas = [l for l in locacoes if l["ativa"]]
    if not ativas:
        print("Não há locações ativas no momento.")
        return

    for l in ativas:
        print(f"Contrato ID: {l['id']} | Cliente: {l['cliente_nome']} | Filme: {l['filme_titulo']} | Prazo: {l['dias']} dia(s)")

    try:
        id_loc = int(input("\nDigite o ID do Contrato para devolução: "))
    except ValueError:
        print("[ERRO] ID inválido.")
        return

    locacao = next((l for l in ativas if l["id"] == id_loc), None)
    if not locacao:
        print("[ERRO] Contrato ativo não encontrado.")
        return

    filme = buscar_filme_por_id(locacao["filme_id"])
    try:
        dias_atraso = int(input("Houve dias de atraso na entrega? (0 se no prazo): "))
        if dias_atraso < 0:
            dias_atraso = 0
    except ValueError:
        dias_atraso = 0

    
    multa = 0.0
    if dias_atraso > 0 and filme:
        multa = dias_atraso * (filme["valor_diaria"] + 5.00)
        locacao["valor_total"] += multa
        print(f"[AVISO] Multa por atraso ({dias_atraso} dia(s)): R$ {multa:.2f}")

    locacao["ativa"] = False
    if filme:
        filme["copias_disponiveis"] += 1

    print(f"[SUCESSO] Filme devolvido ao estoque! Valor final acertado: R$ {locacao['valor_total']:.2f}")



def relatorio_resumo():
    print("\n--- RESUMO GERAL ---")
    copias_estoque = sum(f["copias_disponiveis"] for f in filmes)
    locacoes_ativas = sum(1 for l in locacoes if l["ativa"])
    faturamento = sum(l["valor_total"] for l in locacoes)

    print(f"Clientes Cadastrados          : {len(clientes)}")
    print(f"Títulos no Catálogo           : {len(filmes)}")
    print(f"Cópias Disponíveis na Loja    : {copias_estoque}")
    print(f"Filmes Atualmente Alugados    : {locacoes_ativas}")
    print(f"Total de Locações Realizadas  : {len(locacoes)}")
    print(f"Faturamento Total Acumulado   : R$ {faturamento:.2f}")

def relatorio_clientes():
    print("\n--- RELATÓRIO DE CLIENTES ---")
    if not clientes:
        print("Nenhum cliente cadastrado.")
        return
    for c in clientes:
        suas = [l for l in locacoes if l["cliente_id"] == c["id"]]
        ativas = sum(1 for l in suas if l["ativa"])
        gasto = sum(l["valor_total"] for l in suas)
        print(f"ID: {c['id']} | {c['nome']} | {c['idade']} anos | "
              f"Locações: {len(suas)} | Em aberto: {ativas} | Total gasto: R$ {gasto:.2f}")

def relatorio_catalogo():
    print("\n--- RELATÓRIO DO CATÁLOGO (DISPONÍVEIS x ALUGADAS) ---")
    if not filmes:
        print("Nenhum filme cadastrado.")
        return
    for f in filmes:
        alugadas = sum(1 for l in locacoes if l["filme_id"] == f["id"] and l["ativa"])
        vezes = sum(1 for l in locacoes if l["filme_id"] == f["id"])
        print(f"ID: {f['id']} | {f['titulo']} | Disponíveis: {f['copias_disponiveis']} | "
              f"Alugadas agora: {alugadas} | Vezes alugado: {vezes}")

def relatorio_historico():
    print("\n--- HISTÓRICO DE LOCAÇÕES ---")
    if not locacoes:
        print("Nenhuma locação registrada ainda.")
        return
    for l in locacoes:
        status = "ALUGADO" if l["ativa"] else "DEVOLVIDO"
        print(f"#{l['id']} | {l['cliente_nome']} -> '{l['filme_titulo']}' | "
              f"{l['dias']} dia(s) | R$ {l['valor_total']:.2f} | [{status}]")

def relatorio_faturamento():
    print("\n--- FATURAMENTO ---")
    recebido = sum(l["valor_total"] for l in locacoes if not l["ativa"])
    a_receber = sum(l["valor_total"] for l in locacoes if l["ativa"])
    print(f"Já recebido (devolvidos)      : R$ {recebido:.2f}")
    print(f"Em aberto (ainda alugados)    : R$ {a_receber:.2f}")
    print(f"Faturamento total             : R$ {recebido + a_receber:.2f}")

def exibir_relatorios():
    while True:
        print("\n=== RELATÓRIOS GERENCIAIS ===")
        print("1 - Resumo Geral")
        print("2 - Clientes")
        print("3 - Catálogo (disponíveis x alugadas)")
        print("4 - Histórico de Locações")
        print("5 - Faturamento")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            relatorio_resumo()
        elif opcao == "2":
            relatorio_clientes()
        elif opcao == "3":
            relatorio_catalogo()
        elif opcao == "4":
            relatorio_historico()
        elif opcao == "5":
            relatorio_faturamento()
        elif opcao == "0":
            break
        else:
            print("[ERRO] Opção inválida!")



def menu_locacoes():
    while True:
        print("\n=== GERENCIAR LOCAÇÕES ===")
        print("1 - Alugar Filme")
        print("2 - Devolver Filme")
        print("0 - Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            alugar_filme()
        elif opcao == "2":
            devolver_filme()
        elif opcao == "0":
            break
        else:
            print("[ERRO] Opção inválida!")