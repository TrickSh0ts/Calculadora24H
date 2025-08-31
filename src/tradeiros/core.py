from dataclasses import dataclass

def to_float(s) -> float:
    if s is None:
        return 0.0
    try:
        if isinstance(s, str):
            s = s.replace(',', '.').replace('%', '').strip()
        return float(s)
    except Exception:
        return 0.0

def to_pct01(x) -> float:
    """Aceita 0–1 ou 0–100% e devolve 0–1."""
    v = to_float(x)
    return v/100.0 if v > 1.0 else v

def fmt_money_usd(x: float) -> str:
    return f"$ {x:,.2f}"

def fmt_pct(x: float) -> str:
    return f"{x:.2f}%"

@dataclass
class Carteira24HInputs:
    pos_protecao_c1: float  # C1p
    total_c1: float         # C1t
    total_c2: float         # C2t
    A: float                # para mini calculadora
    B: float
    op_valor_c1: float      # OpC1

@dataclass
class Carteira24HOutputs:
    perc_c1_str: str
    capital_livre_c1_str: str
    c2_protecao_str: str
    capital_livre_c2_str: str
    mul_res_str: str
    op_valor_c2_str: str

def calcula_carteira_24h(i: Carteira24HInputs) -> Carteira24HOutputs:
    C1p, C1t, C2t, A, B, OpC1 = (
        i.pos_protecao_c1, i.total_c1, i.total_c2, i.A, i.B, i.op_valor_c1
    )
    perc = (C1p / C1t * 100.0) if C1t > 0 else 0.0
    capital_livre_c1 = max(C1t - C1p, 0.0)
    c2_protecao = C2t * (perc / 100.0)
    capital_livre_c2 = max(C2t - c2_protecao, 0.0)
    mul_res = A * B
    op_c2 = (OpC1 / C1t * C2t) if C1t > 0 else 0.0

    return Carteira24HOutputs(
        perc_c1_str=fmt_pct(perc),
        capital_livre_c1_str=fmt_money_usd(capital_livre_c1),
        c2_protecao_str=fmt_money_usd(c2_protecao),
        capital_livre_c2_str=fmt_money_usd(capital_livre_c2),
        mul_res_str=fmt_money_usd(mul_res),
        op_valor_c2_str=fmt_money_usd(op_c2),
    )

@dataclass
class PercentagemInputs:
    pos_protecao_c1: float  # P1
    total_c1: float         # T1
    total_c2: float         # T2
    percent_c2_0a1: float   # p2 (0–1)
    operacao_c1: float      # O1

@dataclass
class PercentagemOutputs:
    livre_c1_str: str
    prot_c2_str: str
    livre_c2_str: str
    operacao_c2_str: str

def calcula_percentagem(i: PercentagemInputs) -> PercentagemOutputs:
    T1 = i.total_c1
    P1 = i.pos_protecao_c1
    T2 = i.total_c2
    p2 = i.percent_c2_0a1
    O1 = i.operacao_c1

    L1 = max(T1 - P1, 0.0)
    r = (O1 / L1) if L1 > 0 else 0.0

    prot_c2 = T2 * p2
    L2 = T2 - prot_c2
    O2 = r * L2

    return PercentagemOutputs(
        livre_c1_str=fmt_money_usd(L1),
        prot_c2_str=fmt_money_usd(prot_c2),
        livre_c2_str=fmt_money_usd(L2),
        operacao_c2_str=fmt_money_usd(O2),
    )
