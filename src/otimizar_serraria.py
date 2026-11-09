"""
Otimização da Produção de Compensados (Serra Serra Serrador)
Resolução exata via SciPy (HiGHS).

Problema:
    Max Z = 40*x1 + 30*x2 + 20*x3
    sujeito a:
        2*x1 + 5*x2 + 10*x3 <= 900  (Operação I)
        2*x1 + 5*x2 +  3*x3 <= 400  (Operação II)
        4*x1 + 2*x2 +  2*x3 <= 600  (Operação III)
        x1, x2, x3 >= 0
"""

from scipy.optimize import linprog


def resolver_serraria():
    # Coeficientes da F.O. (linprog minimiza, portanto multiplicamos por -1)
    c = [-40.0, -30.0, -20.0]

    A_ub = [
        [2.0, 5.0, 10.0],  # Operação I
        [2.0, 5.0, 3.0],   # Operação II
        [4.0, 2.0, 2.0],   # Operação III
    ]
    b_ub = [900.0, 400.0, 600.0]

    bounds = [(0.0, None), (0.0, None), (0.0, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

    if not res.success:
        raise RuntimeError(f"Erro na otimização: {res.message}")

    return {
        "x1": float(res.x[0]),
        "x2": float(res.x[1]),
        "x3": float(res.x[2]),
        "lucro_max": float(-res.fun),
        "folga_op1": float(res.slack[0]),
        "folga_op2": float(res.slack[1]),
        "folga_op3": float(res.slack[2]),
    }


if __name__ == "__main__":
    resultado = resolver_serraria()
    print("=" * 52)
    print("    SERRA SERRA SERRADOR — PLANO ÓTIMO DE PRODUÇÃO  ")
    print("=" * 52)
    print(f"Placas Tipo A (x1*) : {resultado['x1']:>8.1f} unidades")
    print(f"Placas Tipo B (x2*) : {resultado['x2']:>8.1f} unidades")
    print(f"Placas Tipo C (x3*) : {resultado['x3']:>8.1f} unidades")
    print("-" * 52)
    print(f"Lucro Máximo Total  : R$ {resultado['lucro_max']:>6.2f}")
    print("=" * 52)
    print("            UTILIZAÇÃO DAS OPERAÇÕES (HORAS)        ")
    print("-" * 52)
    print(f"Folga Operação I    : {resultado['folga_op1']:>8.1f} h (de 900 h)")
    print(f"Folga Operação II   : {resultado['folga_op2']:>8.1f} h (de 400 h)")
    print(f"Folga Operação III  : {resultado['folga_op3']:>8.1f} h (de 600 h)")
    print("=" * 52)