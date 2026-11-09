# Pesquisa Operacional - Otimização Linear com SciPy

Projeto em Python para modelagem, resolução gráfica e computacional de problemas de **Programação Linear (PL)** via Pesquisa Operacional, utilizando o solver open-source **HiGHS** integrado ao `scipy.optimize` e suíte de testes com `pytest`.

---

## 📌 Formulação Matemática do Problema

$$\max Z = 4x_1 + 3x_2$$

**Sujeito a:**

$$x_1 + 3x_2 \le 7 \quad \text{(R1)}$$
$$2x_1 + 2x_2 \le 8 \quad \text{(R2, redundante)}$$
$$x_1 + x_2 \le 3 \quad \text{(R3)}$$
$$x_2 \le 2 \quad \text{(R4)}$$
$$x_1 \ge 0, \quad x_2 \ge 0$$

### Solução Ótima Analítica (Método Gráfico)

* **Vértice Ótimo:** $(x_1^*, x_2^*) = (3.0, 0.0)$
* **Valor Máximo da F.O.:** $Z^* = 4(3) + 3(0) = 12.0$

---

## 📁 Estrutura do Projeto

```text
PesquisaOperacional/
│
├── src/
│   ├── __init__.py
│   └── linear_problem.py       # Modelo matemático e função de otimização
│
├── tests/
│   ├── __init__.py
│   └── test_linear_problem.py  # Testes unitários de otimalidade e factibilidade
│
├── pytest.ini                  # Configuração do caminho raiz para imports
├── requirements.txt            # Dependências do projeto
└── README.md


educacao
seguranca
justica
moradia
alimentcao
trabalho
meio ambiente
animais
relacoes internacionais
musica
comercio exterior
filme
serie
anime
hq
livros
financas
orcamento
compras
vendas
pricing
cidade
estado
pais
saude
politica
familia
amigos
colegas
vizinhos
conjgete
empresas
trabalho
religioa
cultura 
sociedade