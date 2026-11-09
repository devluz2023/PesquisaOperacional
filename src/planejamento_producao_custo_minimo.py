import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


def resolver_alumilaminas():
    # Custos em milhares de R$ para evitar instabilidade numérica
    c = [100.0, 200.0]

    # Restrições de demanda (>= convertidas para <= via multiplicação por -1)
    A_ub = [
        [-8.0, -2.0],  # Finas:  -8x1 - 2x2 <= -16
        [-1.0, -1.0],  # Médias: -1x1 - 1x2 <= -6
        [-2.0, -7.0],  # Grossas: -2x1 - 7x2 <= -28
    ]
    b_ub = [-16.0, -6.0, -28.0]
    bounds = [(0.0, None), (0.0, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    return {
        "x1": res.x[0],
        "x2": res.x[1],
        "custo_total": res.fun * 1000,  # Converte de volta para R$
    }


def plotar_grafico(solucao):
    x1_opt = solucao["x1"]
    x2_opt = solucao["x2"]
    z_min_milhar = solucao["custo_total"] / 1000

    # Malha de pontos
    x1 = np.linspace(0, 16, 1000)
    x2 = np.linspace(0, 10, 1000)
    X1, X2 = np.meshgrid(x1, x2)

    # Equações das fronteiras (isolando x2)
    # Finas:  8x1 + 2x2 >= 16 => x2 >= 8 - 4x1
    r_finas = 8 - 4 * x1
    # Médias: x1 + x2 >= 6     => x2 >= 6 - x1
    r_medias = 6 - x1
    # Grossas: 2x1 + 7x2 >= 28 => x2 >= (28 - 2x1)/7
    r_grossas = (28 - 2 * x1) / 7

    plt.figure(figsize=(11, 7))

    # Linhas de restrição
    plt.plot(
        x1,
        np.maximum(0, r_finas),
        label=r"Finas: $8x_1 + 2x_2 \geq 16$",
        color="royalblue",
        linewidth=2,
    )
    plt.plot(
        x1,
        np.maximum(0, r_medias),
        label=r"Médias: $x_1 + x_2 \geq 6$",
        color="darkorange",
        linewidth=2,
    )
    plt.plot(
        x1,
        np.maximum(0, r_grossas),
        label=r"Grossas: $2x_1 + 7x_2 \geq 28$",
        color="forestgreen",
        linewidth=2,
    )

    # Região viável conjunta
    factivel = (
        (8 * X1 + 2 * X2 >= 16)
        & (X1 + X2 >= 6)
        & (2 * X1 + 7 * X2 >= 28)
        & (X1 >= 0)
        & (X2 >= 0)
    )

    plt.imshow(
        factivel.astype(int),
        extent=(0, 16, 0, 10),
        origin="lower",
        cmap="Blues",
        alpha=0.2,
    )

    # Retas da Função-Objetivo (Isocusto: x2 = -0.5*x1 + Z/200)
    # Reta com custo mais alto
    plt.plot(
        x1,
        -0.5 * x1 + 1400 / 200,
        "crimson",
        linestyle="--",
        alpha=0.6,
        label=r"F.O. Sub-ótima ($Z = \text{R\$\,1.400.000}$)",
    )
    # Reta no ponto ótimo
    plt.plot(
        x1,
        -0.5 * x1 + z_min_milhar / 200,
        "crimson",
        linewidth=2.5,
        label=rf"F.O. Ótima ($Z^* = \text{{R\$\,}}{solucao['custo_total']:,.2f}$)",
    )

    # Vértices da fronteira
    vertices = {
        r"$V_1(0; 8)$": (0, 8),
        r"$V_2(0.67; 5.33)$": (2 / 3, 16 / 3),
        r"$V_4(14; 0)$": (14, 0),
    }
    for label, (vx, vy) in vertices.items():
        plt.plot(vx, vy, "ko", markersize=6)
        plt.annotate(
            label,
            (vx, vy),
            textcoords="offset points",
            xytext=(10, 5),
            fontsize=9,
        )

    # Ponto ótimo destacado
    plt.plot(
        x1_opt,
        x2_opt,
        "ro",
        markersize=9,
        label=rf"Ótimo $V_3({x1_opt:.1f}; {x2_opt:.1f})$",
    )

    # Seta indicando o sentido de minimização
    plt.annotate(
        "Sentido de Minimização (menor custo)",
        xy=(2.8, 3.2),
        xytext=(6.5, 6.0),
        arrowprops=dict(
            facecolor="crimson", shrink=0.08, width=1.5, headwidth=8
        ),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    plt.xlim(0, 15)
    plt.ylim(0, 9)
    plt.xlabel(r"Dias em São Paulo ($x_1$)", fontsize=12)
    plt.ylabel(r"Dias no Rio de Janeiro ($x_2$)", fontsize=12)
    plt.title(
        "Alumilâminas S.A. — Otimização de Custos de Produção",
        fontsize=14,
        pad=15,
    )
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="upper right", framealpha=0.9, fontsize=9)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    solucao = resolver_alumilaminas()
    print("=" * 50)
    print("       RESULTADO — ALUMILÂMINAS S.A.       ")
    print("=" * 50)
    print(f"Dias de operação em São Paulo (x1*) : {solucao['x1']:.2f} dias")
    print(f"Dias de operação no Rio de Jan. (x2*) : {solucao['x2']:.2f} dias")
    print(f"Custo Mínimo Total (Z*)              : R$ {solucao['custo_total']:,.2f}")
    print("=" * 50)

    plotar_grafico(solucao)