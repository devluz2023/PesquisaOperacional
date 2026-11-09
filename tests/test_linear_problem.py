import pytest
from src.linear_problem import solve_lp_problem


def test_solucao_otima():
    """Valida se a função retorna a solução analítica correta (x1=3, x2=0, Z=12)."""
    resultado = solve_lp_problem()

    assert resultado["status"] == "Optimal"
    assert pytest.approx(resultado["x1"], rel=1e-5) == 3.0
    assert pytest.approx(resultado["x2"], rel=1e-5) == 0.0
    assert pytest.approx(resultado["z"], rel=1e-5) == 12.0


def test_viabilidade_das_restricoes():
    """Garante que o ponto ótimo encontrado respeita todas as restrições originais."""
    resultado = solve_lp_problem()
    x1 = resultado["x1"]
    x2 = resultado["x2"]

    # Não-negatividade
    assert x1 >= 0.0
    assert x2 >= 0.0

    # Restrições funcionais (com tolerância numérica de ponto flutuante)
    tol = 1e-7
    assert (x1 + 3 * x2) <= 7.0 + tol
    assert (2 * x1 + 2 * x2) <= 8.0 + tol
    assert (x1 + x2) <= 3.0 + tol
    assert x2 <= 2.0 + tol