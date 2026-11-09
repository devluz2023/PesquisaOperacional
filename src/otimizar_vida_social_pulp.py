"""
Otimização da Vida Social (Ana Paula e Sheila)
Resolução exata via PuLP e plotagem gráfica da região viável com isocurvas.
"""

import matplotlib.pyplot as plt
import numpy as np
import pulp


def resolver_vida_social():
    # Criação do modelo de Maximização
    prob = pulp.LpProblem("Vida_Social_Jovem", pulp.LpMaximize)

    # Variáveis de decisão (não-negativas)
    x1 = prob.add_variable("x1_AnaPaula", lowBound=0)
    x2 = prob.add_variable("x2_Sheila", lowBound=0)

    # Função-Objetivo
    prob += x1 + x2, "Max_Total_Saidas"

    # Restrições
    prob += 240.0 * x1 + 160.0 * x2 <= 960.0, "Restricao_Orcamento"
    prob += 3.0 * x1 + 3.0 * x2 <= 18.0, "Restricao_Tempo"
    prob += 5000.0 * x1 + 10000.0 * x2 <= 40000.0, "Restricao_Energia"

    solve_stats = prob.solve()

    x1_val = float(pulp.value(x1))
    x2_val = float(pulp.value(x2))
    z_val = float(pulp.value(prob.objective))

    # Cálculo dos recursos gastos e folgas
    gasto_orcamento = 240.0 * x1_val + 160.0 * x2_val
    gasto_tempo = 3.0 * x1_val + 3.0 * x2_val
    gasto_energia = 5000.0 * x1_val + 10000.0 * x2_val

    return {
        "status": solve_stats.status.name,
        "ana_paula": x1_val,
        "sheila": x2_val,
        "total_saidas": z_val,
        "folga_orcamento": 960.0 - gasto_orcamento,
        "folga_tempo": 18.0 - gasto_tempo,
        "folga_energia": 40000.0 - gasto_energia,
    }


def plotar_grafico(solucao):
    x1_opt = solucao["ana_paula"]
    x2_opt = solucao["sheila"]
    z_opt = solucao["total_saidas"]

    # Malha para o plano cartesiano
    x1_vals = np.linspace(0, 9, 1000)
    x2_vals = np.linspace(0, 7, 1000)
    X1, X2 = np.meshgrid(x1_vals, x2_vals)

    # Fronteiras isolando x2:
    r_orcamento = (960.0 - 240.0 * x1_vals) / 160.0
    r_tempo = 6.0 - x1_vals
    r_energia = (40000.0 - 5000.0 * x1_vals) / 10000.0

    fig, ax = plt.subplots(figsize=(11, 7.5))

    # Linhas de restrição
    ax.plot(
        x1_vals,
        np.maximum(0, r_orcamento),
        label=r"Orçamento: $240x_1 + 160x_2 \leq 960$ (Ativa)",
        color="royalblue",
        linewidth=2.2,
    )
    ax.plot(
        x1_vals,
        np.maximum(0, r_tempo),
        label=r"Tempo: $3x_1 + 3x_2 \leq 18$ (Folga: 3h)",
        color="darkorange",
        linestyle="--",
        linewidth=2,
    )
    ax.plot(
        x1_vals,
        np.maximum(0, r_energia),
        label=r"Energia: $5.000x_1 + 10.000x_2 \leq 40.000$ (Ativa)",
        color="forestgreen",
        linewidth=2.2,
    )

    # Região factível
    regiao_factivel = (
        (240.0 * X1 + 160.0 * X2 <= 960.0)
        & (3.0 * X1 + 3.0 * X2 <= 18.0)
        & (5000.0 * X1 + 10000.0 * X2 <= 40000.0)
        & (X1 >= 0)
        & (X2 >= 0)
    )

    ax.imshow(
        regiao_factivel.astype(int),
        extent=(0, 9, 0, 7),
        origin="lower",
        cmap="Greens",
        alpha=0.25,
    )

    # Retas da Função-Objetivo (x1 + x2 = Z => x2 = -x1 + Z)
    z_sub = 3.0
    ax.plot(
        x1_vals,
        -x1_vals + z_sub,
        color="crimson",
        linestyle=":",
        alpha=0.6,
        label=rf"F.O. Sub-ótima ($Z = {z_sub:.0f}$ saídas)",
    )
    ax.plot(
        x1_vals,
        -x1_vals + z_opt,
        color="crimson",
        linewidth=2.5,
        label=rf"F.O. Ótima ($Z^* = {z_opt:.0f}$ saídas)",
    )

    # Vértices (Pontos Extremos)
    vertices = {
        r"$V_1(0; 0)$": (0, 0),
        r"$V_2(0; 4)$": (0, 4),
        r"$V_4(4; 0)$": (4, 0),
    }

    for rotulo, (vx, vy) in vertices.items():
        z_v = vx + vy
        ax.plot(vx, vy, "ko", markersize=6)
        ax.annotate(
            f"{rotulo}\n[Z = {z_v}]",
            (vx, vy),
            textcoords="offset points",
            xytext=(8, 5),
            fontsize=9,
        )

    # Ponto Ótimo destacado
    ax.plot(
        x1_opt,
        x2_opt,
        "ro",
        markersize=10,
        label=rf"Ótimo $V_3({x1_opt:.0f};\, {x2_opt:.0f})$ [$Z^*={z_opt:.0f}$]",
    )
    ax.annotate(
        f"$V_3(2; 3)$ - ÓTIMO\n[Z* = {z_opt:.0f} saídas]",
        (x1_opt, x2_opt),
        textcoords="offset points",
        xytext=(10, 10),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    # Vetor de direção
    ax.annotate(
        "Sentido de Maximização (Crescimento de Z)",
        xy=(x1_opt, x2_opt),
        xytext=(x1_opt + 1.2, x2_opt + 1.2),
        arrowprops=dict(
            facecolor="crimson", shrink=0.08, width=1.5, headwidth=8
        ),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    ax.set_xlim(0, 7.5)
    ax.set_ylim(0, 6.5)
    ax.set_xlabel(r"Saídas com Ana Paula ($x_1$)", fontsize=12)
    ax.set_ylabel(r"Saídas com Sheila ($x_2$)", fontsize=12)
    ax.set_title(
        r"Planejamento de Vida Social via PuLP ($\max Z = x_1 + x_2$)",
        fontsize=13,
        pad=15,
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.92, fontsize=9)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    res = resolver_vida_social()
    print("=" * 52)
    print("     PLANEJAMENTO DE VIDA SOCIAL — PLANO ÓTIMO       ")
    print("=" * 52)
    print(f"Status da Solução          : {res['status']}")
    print(f"Saídas com Ana Paula (x1*) : {res['ana_paula']:.0f} vezes/mês")
    print(f"Saídas com Sheila    (x2*) : {res['sheila']:.0f} vezes/mês")
    print("-" * 52)
    print(f"Total Máximo de Saídas (Z*): {res['total_saidas']:.0f} saídas/mês")
    print("=" * 52)
    print("            DIAGNÓSTICO DE RECURSOS E FOLGAS        ")
    print("-" * 52)
    print(f"Folga no Orçamento         : R$ {res['folga_orcamento']:.2f} (Esgotado)")
    print(f"Folga na Energia           : {res['folga_energia']:.0f} cal (Esgotado)")
    print(f"Folga no Tempo             : {res['folga_tempo']:.1f} horas restantes")
    print("=" * 52)

    plotar_grafico(res)