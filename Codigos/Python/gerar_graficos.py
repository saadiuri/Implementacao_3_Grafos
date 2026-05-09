# Script Python para Gerar Tabelas e Gráficos
# (Grafos Densos e Esparsos)

import os
import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt

# =====================================================
# PASTAS
# =====================================================

PASTA_TESTES = "Testes"
PASTA_RESULTADOS = "Resultados"

# Cria a pasta Resultados automaticamente
os.makedirs(PASTA_RESULTADOS, exist_ok=True)

# =====================================================
# LISTA DE RESULTADOS
# =====================================================

resultados = []

arquivos = sorted(os.listdir(PASTA_TESTES))

# =====================================================
# EXECUÇÃO DOS TESTES
# =====================================================

for arquivo in arquivos:

    caminho_arquivo = os.path.join(PASTA_TESTES, arquivo)

    if not os.path.isfile(caminho_arquivo):
        continue

    print(f"\nExecutando {arquivo}")

    # =====================================================
    # COMANDO JAVA
    # =====================================================

    comando = f"java -cp . Codigos.Java.Main {caminho_arquivo}"

    resultado = subprocess.run(
        comando,
        shell=True,
        capture_output=True,
        text=True
    )

    # =====================================================
    # SAÍDA
    # =====================================================

    saida = resultado.stdout

    print(saida)

    # Mostra erros do Java se existirem
    if resultado.stderr:
        print("ERRO JAVA:")
        print(resultado.stderr)

    # =====================================================
    # EXTRAÇÃO DOS DADOS
    # =====================================================

    distancia = re.search(
        r"Distancia \(comprimento\): (\d+)",
        saida
    )

    arestas = re.search(
        r"Numero de arestas: (\d+)",
        saida
    )

    tempo = re.search(
        r"Tempo: ([\d.]+) ms",
        saida
    )

    # =====================================================
    # CONVERSÃO DOS DADOS
    # =====================================================

    if distancia:
        distancia = int(distancia.group(1))
    else:
        distancia = None

    if arestas:
        arestas = int(arestas.group(1))
    else:
        arestas = None

    if tempo:
        tempo = float(tempo.group(1))
    else:
        tempo = None

    # =====================================================
    # IDENTIFICA O TIPO
    # =====================================================

    tipo = "outro"

    if "denso" in arquivo:
        tipo = "denso"

    elif "sparse" in arquivo:
        tipo = "esparso"

    # =====================================================
    # EXTRAI NÚMERO DE VÉRTICES
    # =====================================================

    tamanho = re.search(r"_(\d+)\.txt", arquivo)

    if tamanho:
        tamanho = int(tamanho.group(1))
    else:
        tamanho = 0

    # =====================================================
    # SALVA RESULTADOS
    # =====================================================

    resultados.append({
        "arquivo": arquivo,
        "tipo": tipo,
        "vertices": tamanho,
        "distancia": distancia,
        "arestas": arestas,
        "tempo_ms": tempo
    })

# =====================================================
# DATAFRAME
# =====================================================

df = pd.DataFrame(resultados)

print("\n===== TABELA COMPLETA =====")
print(df)

# =====================================================
# EXPORTA CSV
# =====================================================

df.to_csv(
    os.path.join(PASTA_RESULTADOS, "resultados.csv"),
    index=False
)

print("\nArquivo resultados.csv gerado!")

# =====================================================
# SEPARAÇÃO DOS DADOS
# =====================================================

df_denso = df[df["tipo"] == "denso"]
df_esparso = df[df["tipo"] == "esparso"]

# =====================================================
# REMOVE LINHAS INVÁLIDAS
# =====================================================

df_denso = df_denso.dropna(subset=["tempo_ms"])
df_esparso = df_esparso.dropna(subset=["tempo_ms"])

# =====================================================
# ORDENAÇÃO
# =====================================================

df_denso = df_denso.sort_values(by="vertices")
df_esparso = df_esparso.sort_values(by="vertices")

# =====================================================
# GRÁFICO - DENSOS
# =====================================================

plt.figure(figsize=(10, 6))

plt.plot(
    df_denso["vertices"],
    df_denso["tempo_ms"],
    marker='o'
)

plt.title("Tempo de Execução - Grafos Densos")
plt.xlabel("Número de Vértices")
plt.ylabel("Tempo (ms)")
plt.grid(True)

for i, tempo in enumerate(df_denso["tempo_ms"]):

    plt.text(
        df_denso["vertices"].iloc[i],
        tempo,
        f"{tempo:.2f}"
    )

plt.savefig(
    os.path.join(PASTA_RESULTADOS, "grafico_densos.png")
)

plt.close()

print("grafico_densos.png gerado!")

# =====================================================
# GRÁFICO - ESPARSOS
# =====================================================

plt.figure(figsize=(10, 6))

plt.plot(
    df_esparso["vertices"],
    df_esparso["tempo_ms"],
    marker='o'
)

plt.title("Tempo de Execução - Grafos Esparsos")
plt.xlabel("Número de Vértices")
plt.ylabel("Tempo (ms)")
plt.grid(True)

for i, tempo in enumerate(df_esparso["tempo_ms"]):

    plt.text(
        df_esparso["vertices"].iloc[i],
        tempo,
        f"{tempo:.2f}"
    )

plt.savefig(
    os.path.join(PASTA_RESULTADOS, "grafico_esparsos.png")
)

plt.close()

print("grafico_esparsos.png gerado!")

# =====================================================
# GRÁFICO COMPARATIVO
# =====================================================

plt.figure(figsize=(12, 6))

plt.plot(
    df_denso["vertices"],
    df_denso["tempo_ms"],
    marker='o',
    label='Densos'
)

plt.plot(
    df_esparso["vertices"],
    df_esparso["tempo_ms"],
    marker='o',
    label='Esparsos'
)

plt.title("Comparação de Tempos")
plt.xlabel("Número de Vértices")
plt.ylabel("Tempo (ms)")
plt.legend()
plt.grid(True)

plt.savefig(
    os.path.join(PASTA_RESULTADOS, "grafico_comparativo.png")
)

plt.close()

print("grafico_comparativo.png gerado!")

# =====================================================
# TABELA COMPLETA EM IMAGEM
# =====================================================

fig, ax = plt.subplots(figsize=(14, 7))

ax.axis('tight')
ax.axis('off')

tabela = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    loc='center'
)

tabela.auto_set_font_size(False)
tabela.set_fontsize(10)
tabela.scale(1.2, 1.5)

plt.title("Tabela Completa de Resultados")

plt.savefig(
    os.path.join(PASTA_RESULTADOS, "tabela_completa.png"),
    bbox_inches='tight'
)

plt.close()

print("tabela_completa.png gerada!")

# =====================================================
# TABELA DENSOS
# =====================================================

fig, ax = plt.subplots(figsize=(12, 5))

ax.axis('tight')
ax.axis('off')

tabela_denso = ax.table(
    cellText=df_denso.values,
    colLabels=df_denso.columns,
    loc='center'
)

tabela_denso.auto_set_font_size(False)
tabela_denso.set_fontsize(10)
tabela_denso.scale(1.2, 1.5)

plt.title("Tabela - Grafos Densos")

plt.savefig(
    os.path.join(PASTA_RESULTADOS, "tabela_densos.png"),
    bbox_inches='tight'
)

plt.close()

print("tabela_densos.png gerada!")

# =====================================================
# TABELA ESPARSOS
# =====================================================

fig, ax = plt.subplots(figsize=(12, 5))

ax.axis('tight')
ax.axis('off')

tabela_esparso = ax.table(
    cellText=df_esparso.values,
    colLabels=df_esparso.columns,
    loc='center'
)

tabela_esparso.auto_set_font_size(False)
tabela_esparso.set_fontsize(10)
tabela_esparso.scale(1.2, 1.5)

plt.title("Tabela - Grafos Esparsos")

plt.savefig(
    os.path.join(PASTA_RESULTADOS, "tabela_esparsos.png"),
    bbox_inches='tight'
)

plt.close()

print("tabela_esparsos.png gerada!")

# =====================================================
# FINALIZAÇÃO
# =====================================================

print("\n===== FINALIZADO =====")

print("\nArquivos gerados dentro da pasta 'Resultados':")

print("- resultados.csv")
print("- grafico_densos.png")
print("- grafico_esparsos.png")
print("- grafico_comparativo.png")
print("- tabela_completa.png")
print("- tabela_densos.png")
print("- tabela_esparsos.png")