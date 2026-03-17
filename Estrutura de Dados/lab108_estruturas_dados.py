#Interação com Estruturas de Dados usando Streamlit

import streamlit as st

# Título da aplicação
st.title("Simulador de Estruturas de Dados")

st.write(
    """
    Esta aplicação permite simular o comportamento de **Pilha**, **Fila** e **Lista**  
    de forma interativa, usando a mesma lógica básica da calculadora em Streamlit.
    """
)

# ------------------------------
# Inicializando estruturas na sessão
# ------------------------------
if "pilha" not in st.session_state:
    st.session_state.pilha = []

if "fila" not in st.session_state:
    st.session_state.fila = []

if "lista" not in st.session_state:
    st.session_state.lista = []

# ------------------------------
# Escolha da estrutura
# ------------------------------
estrutura = st.selectbox(
    "Escolha a estrutura de dados:",
    ("Pilha", "Fila", "Lista")
)

# ------------------------------
# Definindo operações conforme a estrutura
# ------------------------------
if estrutura == "Pilha":
    st.subheader("🧱 Pilha (LIFO - Last In, First Out)")
    st.caption("O último elemento que entra é o primeiro que sai.")

    operacao = st.selectbox(
        "Escolha a operação:",
        ("Empilhar (inserir)", "Desempilhar (remover topo)", "Visualizar pilha", "Limpar pilha")
    )

    # Campo de entrada só é usado na operação de inserir
    valor = st.text_input("Valor para inserir na pilha (push):", "")

    if st.button("Executar"):
        if operacao == "Empilhar (inserir)":
            if valor.strip() == "":
                st.error("Digite um valor para empilhar.")
            else:
                st.session_state.pilha.append(valor.strip())
                st.success(f"Valor **{valor}** empilhado com sucesso!")

        elif operacao == "Desempilhar (remover topo)":
            if st.session_state.pilha:
                removido = st.session_state.pilha.pop()
                st.success(f"Valor **{removido}** foi desempilhado (removido do topo).")
            else:
                st.error("A pilha está vazia. Não há o que desempilhar.")

        elif operacao == "Visualizar pilha":
            if st.session_state.pilha:
                st.info("Estado atual da pilha (base → topo):")
                st.code("Base -> " + " | ".join(st.session_state.pilha) + " <- Topo")
            else:
                st.info("A pilha está vazia.")

        elif operacao == "Limpar pilha":
            st.session_state.pilha.clear()
            st.success("Pilha esvaziada com sucesso!")

    # Mostra sempre o estado atual
    st.markdown("### Estado atual da pilha:")
    if st.session_state.pilha:
        st.code("Base -> " + " | ".join(st.session_state.pilha) + " <- Topo")
    else:
        st.write("Pilha vazia.")


elif estrutura == "Fila":
    st.subheader("🚶‍♀️ Fila (FIFO - First In, First Out)")
    st.caption("O primeiro elemento que entra é o primeiro que sai.")

    operacao = st.selectbox(
        "Escolha a operação:",
        ("Enfileirar (inserir no fim)", "Desenfileirar (remover do início)", "Visualizar fila", "Limpar fila")
    )

    valor = st.text_input("Valor para inserir na fila (enqueue):", "")

    if st.button("Executar"):
        if operacao == "Enfileirar (inserir no fim)":
            if valor.strip() == "":
                st.error("Digite um valor para enfileirar.")
            else:
                st.session_state.fila.append(valor.strip())
                st.success(f"Valor **{valor}** enfileirado com sucesso!")

        elif operacao == "Desenfileirar (remover do início)":
            if st.session_state.fila:
                removido = st.session_state.fila.pop(0)
                st.success(f"Valor **{removido}** foi desenfileirado (removido do início).")
            else:
                st.error("A fila está vazia. Não há o que desenfileirar.")

        elif operacao == "Visualizar fila":
            if st.session_state.fila:
                st.info("Estado atual da fila (início → fim):")
                st.code("Início -> " + " | ".join(st.session_state.fila) + " <- Fim")
            else:
                st.info("A fila está vazia.")

        elif operacao == "Limpar fila":
            st.session_state.fila.clear()
            st.success("Fila esvaziada com sucesso!")

    st.markdown("### Estado atual da fila:")
    if st.session_state.fila:
        st.code("Início -> " + " | ".join(st.session_state.fila) + " <- Fim")
    else:
        st.write("Fila vazia.")


elif estrutura == "Lista":
    st.subheader("📋 Lista (estrutura flexível)")
    st.caption("Permite acessar, inserir e remover elementos em qualquer posição.")

    operacao = st.selectbox(
        "Escolha a operação:",
        (
            "Adicionar no final",
            "Inserir em um índice",
            "Remover por índice",
            "Visualizar lista",
            "Limpar lista"
        )
    )

    valor = st.text_input("Valor para inserir na lista:", "")

    # Índice genérico usado para inserir ou remover
    indice = st.number_input(
        "Índice (quando necessário):",
        min_value=0,
        step=1,
        value=0
    )

    if st.button("Executar"):
        if operacao == "Adicionar no final":
            if valor.strip() == "":
                st.error("Digite um valor para adicionar na lista.")
            else:
                st.session_state.lista.append(valor.strip())
                st.success(f"Valor **{valor}** adicionado ao final da lista.")

        elif operacao == "Inserir em um índice":
            if valor.strip() == "":
                st.error("Digite um valor para inserir na lista.")
            else:
                # Garante que o índice não passe do tamanho da lista
                idx = min(indice, len(st.session_state.lista))
                st.session_state.lista.insert(idx, valor.strip())
                st.success(f"Valor **{valor}** inserido no índice **{idx}**.")

        elif operacao == "Remover por índice":
            if st.session_state.lista:
                if indice < len(st.session_state.lista):
                    removido = st.session_state.lista.pop(indice)
                    st.success(f"Valor **{removido}** removido do índice **{indice}**.")
                else:
                    st.error("Índice inválido para a lista atual.")
            else:
                st.error("A lista está vazia. Não há o que remover.")

        elif operacao == "Visualizar lista":
            if st.session_state.lista:
                st.info("Estado atual da lista (índice: valor):")
                for i, v in enumerate(st.session_state.lista):
                    st.write(f"[{i}] -> {v}")
            else:
                st.info("A lista está vazia.")

        elif operacao == "Limpar lista":
            st.session_state.lista.clear()
            st.success("Lista esvaziada com sucesso!")

    st.markdown("### Estado atual da lista:")
    if st.session_state.lista:
        for i, v in enumerate(st.session_state.lista):
            st.write(f"[{i}] -> {v}")
    else:
        st.write("Lista vazia.")
