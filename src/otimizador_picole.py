"""
Otimização da Produção de Picolés (Picolé Lelé Ltda.)
Resolução exata via Programação Linear com SciPy (HiGHS).

Problema:
    Max Z = 1.00*x1 + 0.90*x2 + 0.95*x3
    sujeito a:
        0.45*x1 + 0.50*x2 + 0.40*x3 <= 200  (Leite)
        0.50*x1 + 0.40*x2 + 0.40*x3 <= 150  (Açúcar)
        0.10*x1 + 0.15*x2 + 0.20*x3 <= 60   (Polpa de fruta)
        x1, x2, x3 >= 0
"""

from scipy.optimize import linprog


def resolver_picole_lele():
    # Max Z <=> Min -Z
    c = [-1.00, -0.90, -0.95]

    A_ub = [
        [0.45, 0.50, 0.40],  # Leite
        [0.50, 0.40, 0.40],  # Açúcar
        [0.10, 0.15, 0.20],  # Polpa
    ]
    b_ub = [200.0, 150.0, 60.0]

    bounds = [(0.0, None), (0.0, None), (0.0, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not res.success:
        raise RuntimeError(f"Erro na otimização: {res.message}")

    x1, x2, x3 = [float(val) for val in res.x]
    lucro_max = float(-res.fun)
    folgas = [float(s) for s in res.slack]

    return {
        "morango": x1,
        "uva": x2,
        "limao": x3,
        "lucro_max": lucro_max,
        "folga_leite": folgas[0],
        "folga_acucar": folgas[1],
        "folga_polpa": folgas[2],
    }


if __name__ == "__main__":
    resultado = resolver_picole_lele()
    print("=" * 52)
    print("      PICOLÉ LELÉ LTDA. — PROGRAMAÇÃO DE PRODUÇÃO   ")
    print("=" * 52)
    print(f"Picolés de Morango (x1*) : {resultado['morango']:>8.0f} unidades")
    print(f"Picolés de Uva     (x2*) : {resultado['uva']:>8.0f} unidades")
    print(f"Picolés de Limão   (x3*) : {resultado['limao']:>8.0f} unidades")
    print("-" * 52)
    print(f"Lucro Máximo Total (Z*)  : R$ {resultado['lucro_max']:>6.2f}")
    print("=" * 52)
    print("             USO DE RECURSOS E FOLGAS               ")
    print("-" * 52)
    print(f"Sobra de Leite           : {resultado['folga_leite']:>8.1f} litros")
    print(f"Sobra de Açúcar          : {resultado['folga_acucar']:>8.1f} unidades (100g)")
    print(f"Sobra de Polpa           : {resultado['folga_polpa']:>8.1f} litros")
    print("=" * 52)