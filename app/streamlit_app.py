import streamlit as st
from pathlib import Path
from tradeiros.core import (
    to_pct01,
    Carteira24HInputs, calcula_carteira_24h,
    PercentagemInputs, calcula_percentagem
)

ASSETS = Path(__file__).resolve().parents[1] / "assets"

st.set_page_config(
    page_title="HedgeModePro",
    page_icon=str(ASSETS / "tradeiros_ICON.ico"),
    layout="wide"
)

# =======================
# DENSIDADE / ESTILO
# =======================
MAX_WIDTH = 1100         # largura útil
COL_GAP = "1.6rem"       # espaço entre colunas
FS_TITLE = "1.08rem"     # H1
FS_H2 = "1.02rem"        # títulos dos cards
FS_LABEL = "0.84rem"     # labels dos inputs
FS_VAL = "1.02rem"       # valores à direita
PAD_BLOCK = "1.4rem"     # padding vertical global (↑ para "puxar" tudo para baixo)
PAD_CARD = "0.6rem"      # padding dos cards
INPUT_H = "2.0rem"       # altura dos inputs

st.markdown(f"""
<style>
/* largura e paddings globais */
.block-container {{
  padding-top: {PAD_BLOCK}; padding-bottom: 0.4rem;
  max-width: {MAX_WIDTH}px;
}}
/* gap lateral extra entre colunas */
div[data-testid="column"] {{
  padding-left: {COL_GAP};
  padding-right: {COL_GAP};
}}
/* títulos compactos */
h1 {{ font-size: {FS_TITLE}; margin: .2rem 0 .5rem 0 }}
h2 {{ font-size: {FS_H2}; margin: .2rem 0 .3rem 0 }}

/* inputs compactos */
label {{ font-size: {FS_LABEL} !important; margin-bottom: .15rem !important; }}
input, textarea {{
  height: {INPUT_H} !important; padding-top: .25rem !important; padding-bottom: .25rem !important;
}}

/* esconder botões +/− dos number_input do Streamlit */
div[data-testid="stNumberInput"] button {{ display: none !important; }}
/* esconder spinners nativos */
input[type=number]::-webkit-outer-spin-button,
input[type=number]::-webkit-inner-spin-button {{ -webkit-appearance: none; margin: 0; }}
input[type=number] {{ -moz-appearance: textfield; appearance: textfield; }}

/* containers com menos ar */
div[data-testid="stVerticalBlock"] > div:has(>.stContainer) {{ margin-bottom: .45rem !important; }}
.stContainer {{ padding: {PAD_CARD} !important; }}

/* tipografia dos valores à direita */
.tradeiros-cap {{ color: var(--text-color-secondary); font-size: {FS_LABEL}; }}
.tradeiros-val {{ font-weight: 600; font-size: {FS_VAL}; text-align: right; margin-top: .1rem; }}

/* header: evitar corte + dar margem superior extra */
.tradeiros-header {{ margin-top: .6rem; }}
.tradeiros-header-title {{ white-space: nowrap; }}
</style>
""", unsafe_allow_html=True)

# =======================
# HEADER
# =======================
c1, c2, c3 = st.columns([1, 6, 1])
with c1:
    logo = ASSETS / "tradeiros_logo.png"
    if logo.exists():
        st.image(str(logo), width=92)
with c2:
    st.markdown('<div class="tradeiros-header"><h1 class="tradeiros-header-title">HedgeModePro</h1></div>', unsafe_allow_html=True)
with c3:
    st.caption("")

tab1, tab2 = st.tabs(["Carteira 24H", "Define a tua Proteção (%)"])

# =======================================================
# TAB 1 — grelha 2×2, compacto e com mais espaço lateral
# =======================================================
with tab1:
    # Linha 1: [Carteira 24H] [Minha Carteira]
    colL, colR = st.columns(2)

    # --------- CARD: Carteira 24H
    with colL:
        st.markdown("## Carteira 24H")
        with st.container(border=True):
            c11, c12 = st.columns(2)
            C1p = c11.number_input("Posição em Proteção", min_value=0.0, value=0.0, step=100.0, key="t1_c1p")
            C1t = c12.number_input("Total da Carteira", min_value=0.0, value=0.0, step=100.0, key="t1_c1t")

            t_out = calcula_carteira_24h(Carteira24HInputs(C1p, C1t, 0.0, 0.0, 0.0, 0.0))
            r1a, r1b = st.columns([1, 1])
            r1a.markdown('<div class="tradeiros-cap">Percentagem de Proteção</div>', unsafe_allow_html=True)
            r1b.markdown(f'<div class="tradeiros-val">{t_out.perc_c1_str}</div>', unsafe_allow_html=True)

            r2a, r2b = st.columns([1, 1])
            r2a.markdown('<div class="tradeiros-cap">Capital Livre</div>', unsafe_allow_html=True)
            r2b.markdown(f'<div class="tradeiros-val">{t_out.capital_livre_c1_str}</div>', unsafe_allow_html=True)

    # --------- CARD: Minha Carteira
    with colR:
        st.markdown("## Minha Carteira")
        with st.container(border=True):
            C2t = st.number_input("Total da Minha Carteira", min_value=0.0, value=0.0, step=100.0, key="t1_c2t")

            t_out = calcula_carteira_24h(Carteira24HInputs(C1p, C1t, C2t, 0.0, 0.0, 0.0))
            r3a, r3b = st.columns([1, 1])
            r3a.markdown('<div class="tradeiros-cap">Proteção (mesma % da Carteira 24H)</div>', unsafe_allow_html=True)
            r3b.markdown(f'<div class="tradeiros-val">{t_out.c2_protecao_str}</div>', unsafe_allow_html=True)

            r4a, r4b = st.columns([1, 1])
            r4a.markdown('<div class="tradeiros-cap">Capital livre</div>', unsafe_allow_html=True)
            r4b.markdown(f'<div class="tradeiros-val">{t_out.capital_livre_c2_str}</div>', unsafe_allow_html=True)

    # Linha 2: [Mini Calculadora] [Operação]
    colL2, colR2 = st.columns(2)

    # --------- CARD: Mini Calculadora
    with colL2:
        st.markdown("## Mini Calculadora")
        with st.container(border=True):
            ca, cb = st.columns(2)
            A = ca.number_input("A", value=0.0, key="t1_A")
            B = cb.number_input("B", value=0.0, key="t1_B")
            mul = A * B

            m1a, m1b = st.columns([1, 1])
            m1a.markdown('<div class="tradeiros-cap">Resultado=A × B</div>', unsafe_allow_html=True)
            m1b.markdown(f'<div class="tradeiros-val">$ {mul:,.2f}</div>', unsafe_allow_html=True)

            # botão que copia para a operação (guardamos em session_state["t1_op"])
            if "t1_op" not in st.session_state:
                st.session_state["t1_op"] = 0.0
            st.button("Copiar Valor para Operação", key="t1_copy",
                      on_click=lambda: st.session_state.__setitem__("t1_op", mul))

    # --------- CARD: Operação
    with colR2:
        st.markdown("## Operação")
        with st.container(border=True):
            # gerir valor da operação sem conflito de keys
            if "t1_op" not in st.session_state:
                st.session_state["t1_op"] = 0.0
            OpC1_in = st.number_input("Valor da Operação (Carteira 24H)",
                                      min_value=0.0,
                                      value=float(st.session_state["t1_op"]),
                                      step=100.0, key="t1_op_in")
            st.session_state["t1_op"] = OpC1_in

            out1 = calcula_carteira_24h(Carteira24HInputs(C1p, C1t, C2t, A, B, st.session_state["t1_op"]))
            o1a, o1b = st.columns([1, 1])
            o1a.markdown('<div class="tradeiros-cap">Operação Equivalente na<br>Minha Carteira (mesma %)</div>',
                         unsafe_allow_html=True)
            o1b.markdown(f'<div class="tradeiros-val">{out1.op_valor_c2_str}</div>', unsafe_allow_html=True)

# ===================================
# TAB 2 — também compacto em grelha
# ===================================
with tab2:
    st.markdown("## ⚠️ Confirmação necessária")
    if "t2_on" not in st.session_state:
        st.session_state["t2_on"] = False
    if not st.session_state["t2_on"]:
        st.warning("Ao usar esta aba, sai do fluxo padrão dos Tradeiros e assume total responsabilidade.")
        if st.checkbox("Tenho consciência e quero continuar", key="t2_chk"):
            st.session_state["t2_on"] = True
        st.stop()

    L, R = st.columns(2)

    # --------- CARD: Carteira 24H
    with L:
        st.markdown("## Carteira 24H")
        with st.container(border=True):
            c1, c2 = st.columns(2)
            P1 = c1.number_input("Posição em Proteção", min_value=0.0, value=0.0, step=100.0, key="t2_p1")
            T1 = c2.number_input("Total da Carteira", min_value=0.0, value=0.0, step=100.0, key="t2_t1")
            L1 = max(T1 - P1, 0.0)
            a, b = st.columns([1, 1])
            a.markdown('<div class="tradeiros-cap">Capital Livre</div>', unsafe_allow_html=True)
            b.markdown(f'<div class="tradeiros-val">$ {L1:,.2f}</div>', unsafe_allow_html=True)

    # --------- CARD: Minha Carteira
    with R:
        st.markdown("## Minha Carteira")
        with st.container(border=True):
            t2c1, t2c2 = st.columns(2)
            T2 = t2c1.number_input("Total da Minha Carteira", min_value=0.0, value=0.0, step=100.0, key="t2_t2")
            p2_raw = t2c2.text_input("Percentagem de Proteção (0–100%)", value="0", key="t2_p2")
            p2 = to_pct01(p2_raw)
            prot = T2 * p2
            L2 = T2 - prot
            c, d = st.columns([1, 1])
            c.markdown('<div class="tradeiros-cap">Proteção da Minha Carteira</div>', unsafe_allow_html=True)
            d.markdown(f'<div class="tradeiros-val">$ {prot:,.2f}</div>', unsafe_allow_html=True)
            e, f = st.columns([1, 1])
            e.markdown('<div class="tradeiros-cap">Capital Livre</div>', unsafe_allow_html=True)
            f.markdown(f'<div class="tradeiros-val">$ {L2:,.2f}</div>', unsafe_allow_html=True)

    # --------- CARD: Operação
    L2, R2 = st.columns(2)
    with L2:
        st.markdown("## Operação")
        with st.container(border=True):
            O1 = st.number_input("Valor da operação", min_value=0.0, value=0.0, step=100.0, key="t2_o1")
            out2 = calcula_percentagem(PercentagemInputs(P1, T1, T2, p2, O1))
            g, h = st.columns([1, 1])
            g.markdown('<div class="tradeiros-cap">Operação Equivalente na<br>Minha Carteira (em %)</div>',
                       unsafe_allow_html=True)
            h.markdown(f'<div class="tradeiros-val">{out2.operacao_c2_str}</div>', unsafe_allow_html=True)

st.caption("© Tradeiros — versão Streamlit")
