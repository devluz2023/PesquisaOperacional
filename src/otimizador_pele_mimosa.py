import matplotlib.pyplot as plt
import numpy as np


def plotar_grafico_pele_mimosa():
    # Malha de pontos para o plano cartesiano
    x1 = np.linspace(0, 200, 1000)  # Malas
    x2 = np.linspace(0, 220, 1000)  # Mochilas
    X1, X2 = np.meshgrid(x1, x2)

    # Fronteiras das restrições isolando x2:
    # 1. Corte: x1 <= 150
    # 2. Tingimento: x2 <= 180
    # 3. Costura: 2x1 + 2x2 <= 440  =>  x2 = 220 - x1
    r_costura = 220.0 - x1
    # 4. Embalagem: 1.2x1 + 1.5x2 <= 300  =>  x2 = (300 - 1.2*x1)/1.5 = 200 - 0.8*x1
    r_embalagem = (300.0 - 1.2 * x1) / 1.5

    fig, ax = plt.subplots(figsize=(11, 7.5))

    # Plot das fronteiras
    ax.axvline(
        150,
        color="royalblue",
        linewidth=2.2,
        label=r"Corte: $x_1 \leq 150$ (Ativa)",
    )
    ax.axhline(
        180,
        color="darkorange",
        linestyle="--",
        linewidth=1.8,
        label=r"Tingimento: $x_2 \leq 180$ (Redundante)",
    )
    ax.plot(
        x1,
        np.maximum(0, r_costura),
        color="forestgreen",
        linewidth=2.2,
        label=r"Costura: $x_1 + x_2 \leq 220$ (Ativa)",
    )
    ax.plot(
        x1,
        np.maximum(0, r_embalagem),
        color="purple",
        linestyle="-.",
        linewidth=1.8,
        label=r"Embalagem: $1{,}2x_1 + 1{,}5x_2 \leq 300$",
    )

    # Região factível conjunta (primeiro quadrante)
    regiao_factivel = (
        (X1 <= 150.0)
        & (X2 <= 180.0)
        & (X1 + X2 <= 220.0)
        & (1.2 * X1 + 1.5 * X2 <= 300.0)
        & (X1 >= 0)
        & (X2 >= 0)
    )

    ax.imshow(
        regiao_factivel.astype(int),
        extent=(0, 200, 0, 220),
        origin="lower",
        cmap="Greens",
        alpha=0.25,
    )

    # Retas da Função-Objetivo (Isolucro: 50*x1 + 40*x2 = Z => x2 = -1.25*x1 + Z/40)
    # 1. Reta da produção atual: Z = R$ 7.200 (120 malas e 30 mochilas)
    z_atual = 50.0 * 120.0 + 40.0 * 30.0  # 7.200
    ax.plot(
        x1,
        -1.25 * x1 + z_atual / 40.0,
        color="gray",
        linestyle=":",
        linewidth=2,
        label=rf"F.O. Produção Atual ($Z = \text{{R\$\,}}{z_atual:,.0f}$)",
    )

    # 2. Reta da produção ótima: Z* = R$ 10.300 (150 malas e 70 mochilas)
    z_opt = 50.0 * 150.0 + 40.0 * 70.0  # 10.300
    ax.plot(
        x1,
        -1.25 * x1 + z_opt / 40.0,
        color="crimson",
        linewidth=2.5,
        label=rf"F.O. Ótima ($Z^* = \text{{R\$\,}}{z_opt:,.0f}$)",
    )

    # Vértices da região factível
    vertices = {
        r"$V_1(0;\, 0)$": (0, 0),
        r"$V_2(0;\, 180)$": (0, 180),
        r"$V_3(40;\, 180)$": (40, 180),
        r"$V_5(150;\, 0)$": (150, 0),
    }
    for rotulo, (vx, vy) in vertices.items():
        ax.plot(vx, vy, "ko", markersize=5)
        ax.annotate(
            rotulo,
            (vx, vy),
            textcoords="offset points",
            xytext=(7, 5),
            fontsize=9,
        )

    # Ponto da produção atual
    ax.plot(120, 30, "bs", markersize=8, label=r"Atual $(120;\, 30)$ [$Z=\text{R\$\,7.200}$]")

    # Ponto da produção ótima destacado
    ax.plot(150, 70, "ro", markersize=10, label=r"Ótimo $V_4(150;\, 70)$ [$Z^*=\text{R\$\,10.300}$]")

    # Seta indicando o aumento de lucro (deslocamento ótimo)
    ax.annotate(
        "Aumento de Lucro\n(+R$ 3.100,00 ou +43,06%)",
        xy=(150, 70),
        xytext=(80, 110),
        arrowprops=dict(facecolor="crimson", shrink=0.08, width=1.5, headwidth=8),
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

    ax.set_xlim(0, 180)
    ax.set_ylim(0, 210)
    ax.set_xlabel(r"Malas ($x_1$)", fontsize=12)
    ax.set_ylabel(r"Mochilas ($x_2$)", fontsize=12)
    ax.set_title(
        r"Pele Mimosa Ltda. — Análise Gráfica ($\max Z = 50x_1 + 40x_2$)",
        fontsize=14,
        pad=15,
    )
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.92, fontsize=9)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plotar_grafico_pele_mimosa()