import os
import re
import json
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from ddgs import DDGS
from google import genai
from google.genai import types

# Carrega automaticamente a GEMINI_API_KEY do arquivo .env
load_dotenv(override=True)
os.environ.pop("GOOGLE_API_KEY", None)

# =====================================================================
# 1. CONFIGURAÇÃO DA PÁGINA & CSS ESTILO LANDING PAGE (FANTASTIC PRINT)
# =====================================================================
st.set_page_config(
    page_title="Fantastic Print | Studio & Inteligência de Catálogo",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

.stApp {
    background-color: #09080E;
    color: #FFFFFF;
}

/* Remove barra superior preta e botão Deploy */
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu,
footer {
    display: none !important;
    visibility: hidden !important;
}

.block-container {
    padding-top: 1.2rem !important;
    max-width: 1240px !important;
    margin: 0 auto !important;
}

/* Slider em Roxo */
[data-testid="stSlider"] [role="slider"] {
    background-color: #9333EA !important;
    border: 2px solid #FFFFFF !important;
    box-shadow: 0 0 12px rgba(147, 51, 234, 0.8) !important;
}
[data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
    background: linear-gradient(90deg, #06B6D4 0%, #9333EA 50%, #EC4899 100%) !important;
}
[data-testid="stSliderThumbValue"] {
    color: #C084FC !important;
    font-weight: 700 !important;
}

/* 1. NAVBAR SUPERIOR */
.fp-navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 28px;
    background-color: #0E0C16;
    border: 1px solid #231D38;
    border-radius: 16px;
    margin-bottom: 22px;
}
.fp-logo-area {
    display: flex;
    align-items: center;
    gap: 12px;
}
.fp-logo-text {
    font-weight: 800;
    font-size: 1.25rem;
    line-height: 1.05;
    color: #FFFFFF;
    letter-spacing: 0.5px;
}
.fp-logo-sub {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 4.5px;
    background: linear-gradient(90deg, #A855F7, #EC4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.fp-nav-links {
    display: flex;
    gap: 28px;
    color: #D4D4D8;
    font-size: 0.9rem;
    font-weight: 600;
}
.fp-nav-cta {
    background: linear-gradient(90deg, #7C3AED 0%, #9333EA 100%);
    color: #FFFFFF !important;
    padding: 10px 22px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.88rem;
    box-shadow: 0 4px 20px rgba(147, 51, 234, 0.4);
}

/* 2. HERO SECTION */
.fp-hero {
    background: radial-gradient(circle at 80% 35%, rgba(124, 58, 237, 0.32) 0%, rgba(18, 14, 34, 0.95) 55%, #0D0B14 100%);
    border: 1px solid #2E244D;
    border-radius: 22px;
    padding: 44px 48px;
    margin-bottom: 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 32px;
    position: relative;
    overflow: hidden;
}
.fp-hero-left {
    flex: 1.2;
}
.fp-kicker {
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 2.5px;
    color: #22D3EE;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.fp-hero-title {
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.12;
    color: #FFFFFF;
    margin: 0 0 18px 0;
    letter-spacing: -1px;
}
.fp-gradient-text {
    background: linear-gradient(90deg, #38BDF8 0%, #A855F7 52%, #EC4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.fp-hero-desc {
    color: #A1A1AA;
    font-size: 1rem;
    line-height: 1.6;
    max-width: 480px;
    margin-bottom: 24px;
}
.fp-hero-badges {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}
.fp-btn-primary {
    background: linear-gradient(90deg, #7C3AED 0%, #A855F7 100%);
    color: #FFFFFF;
    padding: 11px 22px;
    border-radius: 10px;
    font-weight: 700;
    font-size: 0.9rem;
    box-shadow: 0 6px 24px rgba(168, 85, 247, 0.4);
}
.fp-btn-outline {
    background: rgba(255, 255, 255, 0.04);
    color: #E4E4E7;
    padding: 11px 22px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.9rem;
    border: 1px solid #3F3F46;
}
.fp-hero-right {
    flex: 0.8;
    position: relative;
    height: 260px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.fp-swoosh {
    position: absolute;
    width: 230px;
    height: 230px;
    border-radius: 50%;
    background: conic-gradient(from 140deg, #06B6D4, #7C3AED, #EC4899, transparent 75%);
    filter: blur(18px);
    opacity: 0.65;
}
.fp-card-main {
    position: relative;
    width: 195px;
    height: 225px;
    background: linear-gradient(145deg, #38BDF8 0%, #8B5CF6 48%, #EC4899 100%);
    border-radius: 18px;
    transform: rotate(-10deg);
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
    z-index: 2;
}
.fp-card-main-text {
    color: #09080E;
    font-weight: 900;
    font-size: 1.15rem;
    line-height: 1.05;
    text-transform: uppercase;
}
.fp-card-sub {
    position: absolute;
    bottom: 16px;
    right: 16px;
    width: 170px;
    height: 100px;
    background: linear-gradient(135deg, #110F1D 52%, #7C3AED 53%, #EC4899 100%);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 14px;
    transform: rotate(8deg);
    padding: 14px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.75);
    z-index: 3;
}

/* 3. SEÇÃO DE CATEGORIAS */
.fp-section-header {
    text-align: center;
    margin: 12px 0 22px 0;
}
.fp-section-kicker {
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 3px;
    color: #A855F7;
    text-transform: uppercase;
}
.fp-section-title {
    font-size: 1.9rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-top: 4px;
}
.cat-box {
    background-color: #13111C;
    border: 1px solid #26213B;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    transition: all 0.25s ease;
    margin-bottom: 10px;
}
.cat-box:hover {
    border-color: #9333EA;
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(147, 51, 234, 0.25);
}
.cat-art {
    height: 110px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.5rem;
    margin-bottom: 12px;
}
.cat-art-1 { background: linear-gradient(135deg, #1E1836 0%, #312159 100%); border: 1px solid #4C1D95; }
.cat-art-2 { background: linear-gradient(135deg, #102636 0%, #1B3B52 100%); border: 1px solid #0369A1; }
.cat-art-3 { background: linear-gradient(135deg, #2D162C 0%, #4A1D48 100%); border: 1px solid #9D174D; }
.cat-art-4 { background: linear-gradient(135deg, #181824 0%, #27273A 100%); border: 1px solid #4338CA; }
.cat-name {
    font-weight: 700;
    font-size: 1rem;
    color: #FFFFFF;
}

/* Botões Streamlit */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(90deg, #6D28D9 0%, #9333EA 100%);
    color: #FFFFFF;
    border: 1px solid #A855F7;
    border-radius: 10px;
    font-weight: 700;
    transition: all 0.2s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: linear-gradient(90deg, #7C3AED 0%, #EC4899 100%);
    border-color: #F472B6;
    box-shadow: 0 6px 20px rgba(168, 85, 247, 0.45);
}

/* Cards de Produto */
.product-card {
    background-color: #13111C;
    border: 1px solid #26213B;
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.25s ease;
    margin-top: 12px;
    margin-bottom: 16px;
}
.product-card:hover {
    border-color: #A855F7;
    box-shadow: 0 10px 28px rgba(147, 51, 234, 0.25);
}
.product-img {
    width: 100%;
    height: 210px;
    object-fit: cover;
    border-bottom: 1px solid #26213B;
    background-color: #181624;
}
.product-body {
    padding: 16px;
}
.product-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #C084FC;
    text-decoration: none;
    display: block;
    margin-bottom: 10px;
    line-height: 1.3;
}
.tech-pills {
    display: flex;
    gap: 8px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}
.pill {
    background-color: #1E1933;
    color: #E9D5FF;
    border: 1px solid #581C87;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
}
.price-box {
    background-color: #09080E;
    border: 1px solid #26213B;
    border-radius: 12px;
    padding: 12px 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.cost-label {
    font-size: 0.75rem;
    color: #A1A1AA;
    margin-bottom: 2px;
}
.cost-val {
    font-size: 1.05rem;
    font-weight: 700;
    color: #E4E4E7;
}
.sell-val {
    font-size: 1.22rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38BDF8, #C084FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.profit-tag {
    font-size: 0.75rem;
    color: #4ADE80;
    font-weight: 600;
}

/* Abas */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    background-color: #13111C;
    border-radius: 10px 10px 0 0;
    color: #A1A1AA;
    border: 1px solid #26213B;
}
.stTabs [aria-selected="true"] {
    background-color: #1F1836 !important;
    color: #FFFFFF !important;
    border-color: #9333EA !important;
}
</style>
""", unsafe_allow_html=True)

def obter_cliente_gemini():
    load_dotenv(override=True)
    os.environ.pop("GOOGLE_API_KEY", None)
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

# =====================================================================
# 2. LÓGICA DE CÁLCULO, BUSCA DE IMAGENS & RENDERIZAÇÃO DE CARDS
# =====================================================================

def calculo_interno_3d(
    peso_gramas: float,
    horas_impressao: float,
    preco_kg: float,
    insumos: float,
    taxa_pct: float,
    taxa_fixa: float,
    margem_pct: float
) -> dict:
    custo_filamento = (peso_gramas / 1000.0) * preco_kg * 1.05
    custo_maquina = horas_impressao * 0.85
    custo_total = custo_filamento + custo_maquina + insumos
    lucro_alvo = custo_total * (margem_pct / 100.0)
    divisor = max(0.10, 1.0 - (taxa_pct / 100.0))
    preco_venda = (custo_total + lucro_alvo + taxa_fixa) / divisor

    return {
        "custo_total": round(custo_total, 2),
        "lucro_liquido": round(lucro_alvo, 2),
        "preco_venda": round(preco_venda, 2)
    }


def buscar_foto_exata_makerworld(titulo_modelo: str, link_modelo: str, capa_direta: str = "") -> str:
    if capa_direta and capa_direta.startswith("http"):
        return capa_direta

    match_id = re.search(r"/models/(\d+)", link_modelo)
    modelo_id = match_id.group(1) if match_id else ""

    try:
        with DDGS() as ddgs:
            if modelo_id:
                imgs = list(ddgs.images(f'site:makerworld.com "{modelo_id}"', max_results=5))
                for img in imgs:
                    fonte_pagina = img.get("url", "")
                    url_img = img.get("image") or img.get("thumbnail")
                    if url_img and f"/models/{modelo_id}" in fonte_pagina:
                        return url_img
    except Exception:
        pass

    titulo_limpo = re.sub(r"[^a-zA-Z0-9 ]", "", titulo_modelo)[:26].strip().replace(" ", "+")
    return f"https://placehold.co/600x400/181624/C084FC?text={titulo_limpo or 'Modelo+3D'}"


def renderizar_grade_cards(cards: list):
    if not cards:
        return
    for i in range(0, len(cards), 3):
        cols = st.columns(3)
        for idx, card in enumerate(cards[i:i+3]):
            with cols[idx]:
                html_card = (
                    f'<div class="product-card">'
                    f'<a href="{card["link"]}" target="_blank">'
                    f'<img src="{card["foto"]}" class="product-img" alt="{card["titulo"]}">'
                    f'</a>'
                    f'<div class="product-body">'
                    f'<a href="{card["link"]}" target="_blank" class="product-title">{card["titulo"]} ↗</a>'
                    f'<div class="tech-pills">'
                    f'<span class="pill">🧵 {card["peso_g"]}g filamento</span>'
                    f'<span class="pill">⏱️ {card["horas"]}h impressão</span>'
                    f'</div>'
                    f'<div class="price-box">'
                    f'<div><div class="cost-label">Custo Produção</div><div class="cost-val">R$ {card["custo_R$"]:.2f}</div></div>'
                    f'<div style="text-align:right;"><div class="cost-label">Venda Sugerida</div><div class="sell-val">R$ {card["venda_R$"]:.2f}</div><div class="profit-tag">+R$ {card["lucro_R$"]:.2f} lucro líq.</div></div>'
                    f'</div></div></div>'
                )
                st.markdown(html_card, unsafe_allow_html=True)


# =====================================================================
# 3. FERRAMENTAS DO AGENTE (TOOLS)
# =====================================================================

def pesquisar_mercado_3d(nicho_ou_produto: str) -> str:
    """Pesquisa produtos impressos em 3D vendidos na Shopee, Mercado Livre e TikTok Shop no Brasil."""
    st.toast(f"📊 Pesquisando demanda na Shopee/ML: {nicho_ou_produto}...")
    resultados_texto = []
    queries = [
        f'site:shopee.com.br "{nicho_ou_produto}" 3d',
        f'site:mercadolivre.com.br "{nicho_ou_produto}" 3d',
    ]
    try:
        with DDGS() as ddgs:
            for q in queries:
                res = list(ddgs.text(q, region="br-pt", max_results=3))
                for r in res:
                    resultados_texto.append(
                        f"Anúncio Real: {r.get('title')}\nDetalhes: {r.get('body')}"
                    )
    except Exception as e:
        return f"Erro ao pesquisar marketplaces: {e}"

    return "\n---\n".join(resultados_texto) if resultados_texto else "Sem anúncios específicos indexados; use tendências populares do nicho."


def buscar_modelos_makerworld(termo_modelo: str) -> str:
    """Busca modelos 3D no MakerWorld ordenados pelos MAIS BAIXADOS."""
    st.toast(f"🏆 Buscando no MakerWorld: {termo_modelo}...")
    resultados_texto = []

    try:
        api_url = "https://makerworld.com/api/v1/search-service/select/design2"
        params = {
            "keyword": termo_modelo,
            "orderBy": "downloadCount",
            "limit": 8,
            "offset": 0
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Referer": "https://makerworld.com/en"
        }
        resp = requests.get(api_url, params=params, headers=headers, timeout=6)
        if resp.status_code == 200:
            dados = resp.json()
            hits = dados.get("hits", [])
            for item in hits:
                design_id = item.get("id")
                slug = item.get("slug", "")
                titulo = item.get("title", "Modelo 3D")
                downloads = item.get("downloadCount", 0)
                likes = item.get("likeCount", 0)
                capa = item.get("cover", "")
                link = f"https://makerworld.com/en/models/{design_id}-{slug}" if slug else f"https://makerworld.com/en/models/{design_id}"

                if downloads >= 10:
                    resultados_texto.append(
                        f"Título: {titulo}\nDownloads: {downloads} | Likes: {likes}\nLink: {link}\nCapa: {capa}"
                    )
    except Exception:
        pass

    if not resultados_texto:
        try:
            query_pop = f'site:makerworld.com/en/models {termo_modelo}'
            with DDGS() as ddgs:
                res = list(ddgs.text(query_pop, max_results=6))
                for r in res:
                    link = r.get("href", "")
                    if "makerworld.com" in link and "/models/" in link:
                        titulo_limpo = r.get("title", "").split("|")[0].split("- MakerWorld")[0].strip()
                        resultados_texto.append(
                            f"Título: {titulo_limpo}\nResumo: {r.get('body')}\nLink: {link}\nCapa: "
                        )
        except Exception as e:
            return f"Erro na busca: {e}"

    if not resultados_texto:
        return f"Nenhum modelo encontrado para '{termo_modelo}'. Tente buscar com palavras-chave mais curtas em inglês."

    return "\n---\n".join(resultados_texto[:6])


def atualizar_vitrine_produtos(modelos_json: str) -> str:
    """Gera e exibe os cards visuais dos produtos logo abaixo da resposta no chat."""
    st.toast("✨ Montando cards visuais na resposta...")
    try:
        lista_modelos = json.loads(modelos_json)
        p_filamento = st.session_state.get("cfg_filamento", 110.0)
        p_insumos = st.session_state.get("cfg_insumos", 1.50)
        p_taxa_pct = st.session_state.get("cfg_taxa_pct", 20.0)
        p_taxa_fixa = st.session_state.get("cfg_taxa_fixa", 4.00)
        p_margem = st.session_state.get("cfg_margem", 60.0)

        cards_prontos = []
        for item in lista_modelos[:6]:
            titulo = item.get("titulo", "Modelo 3D")
            link = item.get("link", "https://makerworld.com")
            capa_api = item.get("capa", "")
            peso = float(item.get("peso_gramas", 25.0))
            horas = float(item.get("horas_impressao", 1.0))

            calc = calculo_interno_3d(
                peso_gramas=peso,
                horas_impressao=horas,
                preco_kg=p_filamento,
                insumos=p_insumos,
                taxa_pct=p_taxa_pct,
                taxa_fixa=p_taxa_fixa,
                margem_pct=p_margem
            )
            foto_url = buscar_foto_exata_makerworld(titulo, link, capa_api)

            cards_prontos.append({
                "titulo": titulo,
                "link": link,
                "foto": foto_url,
                "peso_g": peso,
                "horas": horas,
                "custo_R$": calc["custo_total"],
                "venda_R$": calc["preco_venda"],
                "lucro_R$": calc["lucro_liquido"]
            })

        st.session_state["cards_rodada_atual"] = cards_prontos
        return f"Sucesso! {len(cards_prontos)} cards visuais anexados à resposta."
    except Exception as e:
        return f"Erro ao montar cards: {e}"


# =====================================================================
# 4. NAVBAR + HERO SECTION (HTML SEM INDENTAÇÃO PARA NÃO QUEBRAR MARKDOWN)
# =====================================================================
margem_atual_preview = st.session_state.get("cfg_margem", 60)
mkt_atual_preview = st.session_state.get("cfg_mkt_nome", "Shopee")

html_topo = f"""
<div class="fp-navbar">
<div class="fp-logo-area">
<svg width="38" height="38" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="fGradNav" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
<stop offset="0%" stop-color="#38BDF8"/>
<stop offset="100%" stop-color="#0284C7"/>
</linearGradient>
</defs>
<path d="M8 6H34L30 14H17V18H28L25 25H17V34H8V6Z" fill="url(#fGradNav)"/>
</svg>
<div>
<div class="fp-logo-text">FANTASTIC</div>
<div class="fp-logo-sub">PRINT</div>
</div>
</div>
<div class="fp-nav-links">
<span>Início</span>
<span>Catálogo IA</span>
<span>MakerWorld</span>
<span>Precificação</span>
</div>
<div class="fp-nav-cta">⚡ Bambu Lab A1 Mini</div>
</div>

<div class="fp-hero">
<div class="fp-hero-left">
<div class="fp-kicker">IMPRESSÃO 3D QUE TRANSFORMA</div>
<h1 class="fp-hero-title">Suas ideias.<br>Nossa impressão.<br><span class="fp-gradient-text">Resultados incríveis.</span></h1>
<p class="fp-hero-desc">Pesquisa inteligente de modelos validados, análise de mercado em tempo real e precificação automática para destacar a Fantastic Print.</p>
<div class="fp-hero-badges">
<span class="fp-btn-primary">🟣 Margem Ativa: {margem_atual_preview}%</span>
<span class="fp-btn-outline">🏪 {mkt_atual_preview}</span>
</div>
</div>
<div class="fp-hero-right">
<div class="fp-swoosh"></div>
<div class="fp-card-main">
<div class="fp-card-main-text">CRIE.<br>IMPRIMA.<br><span style="color:#FFFFFF;">SURPREENDA.</span></div>
</div>
<div class="fp-card-sub">
<div style="font-weight:800; font-size:0.95rem; color:#FFFFFF; letter-spacing:0.5px;">FANTASTIC</div>
<div style="font-size:0.65rem; font-weight:700; letter-spacing:3.5px; color:#38BDF8;">PRINT</div>
<div style="font-size:0.7rem; color:#E4E4E7; margin-top:8px;">PLA • PETG • NFC</div>
</div>
</div>
</div>
"""
st.markdown(html_topo, unsafe_allow_html=True)

# =====================================================================
# 5. PAINEL DE CONFIGURAÇÃO DE CUSTOS & CHAVE API
# =====================================================================
with st.expander("⚙️ Configurar Custos de Produção, Marketplace & Chave API", expanded=False):
    cfg1, cfg2, cfg3, cfg4 = st.columns([1, 1, 1.3, 1.2])
    preco_filamento = cfg1.number_input("Filamento (R$/kg)", value=110.0, step=5.0)
    custo_insumos = cfg2.number_input("Insumos (R$)", value=1.50, step=0.25)
    marketplace_alvo = cfg3.selectbox(
        "Marketplace",
        ["Shopee (20% + R$4 fixo)", "Mercado Livre Clássico (14% + R$6 fixo)", "TikTok Shop (15% + R$2 fixo)"]
    )
    margem_alvo = cfg4.slider("Margem Líquida (%)", min_value=20, max_value=200, value=60, step=10)

    if "Shopee" in marketplace_alvo:
        taxa_pct, taxa_fixa = 20.0, 4.00
    elif "Mercado Livre" in marketplace_alvo:
        taxa_pct, taxa_fixa = 14.0, 6.00
    else:
        taxa_pct, taxa_fixa = 15.0, 2.00

    st.session_state["cfg_filamento"] = preco_filamento
    st.session_state["cfg_insumos"] = custo_insumos
    st.session_state["cfg_taxa_pct"] = taxa_pct
    st.session_state["cfg_taxa_fixa"] = taxa_fixa
    st.session_state["cfg_margem"] = margem_alvo
    st.session_state["cfg_mkt_nome"] = marketplace_alvo.split("(")[0].strip()

    chave_atual = os.environ.get("GEMINI_API_KEY", "")
    if not chave_atual:
        nova_chave = st.text_input("🔑 Cole sua GEMINI_API_KEY aqui (ou salve no arquivo .env)", type="password")
        if nova_chave:
            os.environ["GEMINI_API_KEY"] = nova_chave.strip()
            st.success("Chave ativada para esta sessão!")

# =====================================================================
# 6. GRADE DE 4 CARDS DE CATEGORIA ("SOLUÇÕES PARA SUA LOJA")
# =====================================================================
st.markdown('<div class="fp-section-header"><div class="fp-section-kicker">SOLUÇÕES PARA SUA LOJA</div><div class="fp-section-title">Explore os nichos mais lucrativos</div></div>', unsafe_allow_html=True)

prompt_atalho = None
cat1, cat2, cat3, cat4 = st.columns(4)

with cat1:
    st.markdown('<div class="cat-box"><div class="cat-art cat-art-1">🏷️</div><div class="cat-name">Chaveiros & Tags NFC</div></div>', unsafe_allow_html=True)
    if st.button("Pesquisar Chaveiros", key="btn_cat1", use_container_width=True):
        prompt_atalho = "Pesquise chaveiros 3D e tags NFC que vendem bem no Brasil, busque os modelos mais baixados no MakerWorld e mostre os cards visuais."

with cat2:
    st.markdown('<div class="cat-box"><div class="cat-art cat-art-2">🎮</div><div class="cat-name">Setup Gamer & Suportes</div></div>', unsafe_allow_html=True)
    if st.button("Pesquisar Setup Gamer", key="btn_cat2", use_container_width=True):
        prompt_atalho = "Pesquise suportes gamers para controle e headset mais vendidos no Brasil, busque os mais baixados no MakerWorld e mostre os cards visuais."

with cat3:
    st.markdown('<div class="cat-box"><div class="cat-art cat-art-3">🎄</div><div class="cat-name">Decoração & Datas</div></div>', unsafe_allow_html=True)
    if st.button("Pesquisar Decoração", key="btn_cat3", use_container_width=True):
        prompt_atalho = "Pesquise itens de decoração e enfeites de Natal 3D mais vendidos no Brasil, busque os mais baixados no MakerWorld e mostre os cards visuais."

with cat4:
    st.markdown('<div class="cat-box"><div class="cat-art cat-art-4">🎁</div><div class="cat-name">Personalizados & Brindes</div></div>', unsafe_allow_html=True)
    if st.button("Pesquisar Personalizados", key="btn_cat4", use_container_width=True):
        prompt_atalho = "Pesquise lembrancinhas personalizadas e brindes criativos 3D com alta saída no Brasil, busque os mais baixados no MakerWorld e mostre os cards visuais."

st.markdown("<div style='text-align:center; color:#71717A; font-size:0.85rem; margin: 14px 0 24px 0;'>Qualidade • Precificação Inteligente • Criatividade • Alta Margem</div>", unsafe_allow_html=True)

# =====================================================================
# 7. ABAS PRINCIPAIS: AGENTE DE PESQUISA & GERADOR DE ANÚNCIOS
# =====================================================================
if "mensagens_3d" not in st.session_state:
    st.session_state.mensagens_3d = []
if "anuncios_salvos" not in st.session_state:
    st.session_state.anuncios_salvos = []

aba_chat, aba_anuncios = st.tabs(["🟣 Consultor de Catálogo & MakerWorld", "📦 Gerador de Anúncios SEO (CSV)"])

with aba_chat:
    for msg in st.session_state.mensagens_3d:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("cards"):
                renderizar_grade_cards(msg["cards"])

    entrada_usuario = st.chat_input("Digite qualquer ideia ou nicho 3D (ex: 'porta copos geek', 'organizador de cabos')...")
    prompt_final = prompt_atalho or entrada_usuario

    if prompt_final:
        client = obter_cliente_gemini()
        if not client:
            st.error("⚠️ Nenhuma chave API encontrada! Abra '⚙️ Configurar Custos de Produção, Marketplace & Chave API' acima e cole sua GEMINI_API_KEY.")
        else:
            st.session_state["cards_rodada_atual"] = []
            st.session_state.mensagens_3d.append({"role": "user", "content": prompt_final})
            with st.chat_message("user"):
                st.markdown(prompt_final)

            with st.chat_message("assistant"):
                with st.spinner("Consultando MakerWorld e calculando margens da Fantastic Print..."):
                    prompt_sistema = f"""
                    Você é o estrategista de catálogo da Fantastic Print (Bambu Lab A1 Mini).
                    Parâmetros ativos: Filamento R$ {preco_filamento}/kg | Insumos R$ {custo_insumos} | {marketplace_alvo} | Margem {margem_alvo}%.

                    FLUXO OBRIGATÓRIO:
                    1. Use 'buscar_modelos_makerworld' com termos curtos e objetivos em INGLÊS.
                    2. Assim que tiver os 3 melhores modelos reais (com link válido do MakerWorld), CHAME OBRIGATORIAMENTE 'atualizar_vitrine_produtos' passando a lista JSON com "titulo", "link", "capa", "peso_gramas" e "horas_impressao".
                    3. Na sua resposta escrita, faça apenas um comentário estratégico curto (3 a 4 linhas) com dicas de cores/filamentos e lembre de conferir a licença comercial no link. Nunca invente links ou nomes de modelos que não vieram da ferramenta.
                    """

                    modelos_reserva = [
                        "gemini-3.8-flash",
                        "gemini-3.5-flash-lite",
                        "gemini-3.7-flash",
                    ]
                    resposta_texto = None

                    for modelo in modelos_reserva:
                        try:
                            chat = client.chats.create(
                                model=modelo,
                                config=types.GenerateContentConfig(
                                    system_instruction=prompt_sistema,
                                    temperature=0.3,
                                    tools=[pesquisar_mercado_3d, buscar_modelos_makerworld, atualizar_vitrine_produtos],
                                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                                        maximum_remote_calls=15
                                    )
                                )
                            )
                            response = chat.send_message(prompt_final)
                            if response and response.text:
                                resposta_texto = response.text
                                break
                        except Exception as e:
                            st.warning(f"Erro em {modelo}: {e}")

                    if resposta_texto:
                        cards_gerados = st.session_state.get("cards_rodada_atual", [])
                        st.markdown(resposta_texto)
                        if cards_gerados:
                            renderizar_grade_cards(cards_gerados)
                        
                        st.session_state.mensagens_3d.append({
                            "role": "assistant",
                            "content": resposta_texto,
                            "cards": cards_gerados
                        })
                    else:
                        st.error("Os modelos não responderam agora. Verifique se sua GEMINI_API_KEY está válida no arquivo .env.")

with aba_anuncios:
    st.subheader("📦 Gerar Ficha Técnica & Anúncio Otimizado")
    with st.form("form_anuncio"):
        c1, c2, c3 = st.columns([2, 1, 1])
        nome_peca = c1.text_input("Nome do Produto 3D", placeholder="Ex: Chaveiro NFC Spotify Personalizado 3D")
        peso_peca = c2.number_input("Peso no Bambu Studio (g)", min_value=1.0, value=18.0)
        tempo_peca = c3.number_input("Tempo de Impressão (horas)", min_value=0.1, value=0.8, step=0.1)
        material_peca = st.selectbox("Filamento", ["PLA", "PLA Silk / Fosco", "PETG"])
        
        gerar_btn = st.form_submit_button("✨ Gerar Anúncio & Calcular Preço")

    if gerar_btn and nome_peca:
        client = obter_cliente_gemini()
        if not client:
            st.error("⚠️ Configure sua GEMINI_API_KEY antes de gerar o anúncio.")
        else:
            with st.spinner("Gerando ficha SEO..."):
                calc = calculo_interno_3d(
                    peso_gramas=peso_peca,
                    horas_impressao=tempo_peca,
                    preco_kg=preco_filamento,
                    insumos=custo_insumos,
                    taxa_pct=taxa_pct,
                    taxa_fixa=taxa_fixa,
                    margem_pct=margem_alvo
                )

                prompt_json = f"""
                Crie um anúncio de e-commerce para a loja Fantastic Print:
                Produto: {nome_peca} | Material: {material_peca} | Peso: {peso_peca}g
                Preço de Venda: R$ {calc['preco_venda']} | Canal: {marketplace_alvo}

                Retorne APENAS um JSON válido com as chaves:
                "titulo_seo" (máx 60 caracteres),
                "descricao_completa" (persuasiva com especificações, tópicos e quebra de linha),
                "tags_busca" (8 palavras-chave separadas por vírgula),
                "sugestao_foto_capa" (dica de cenário para foto).
                """

                modelos_anuncio = [
                    "gemini-3.8-flash",
                    "gemini-3.5-flash-lite",
                    "gemini-3.7-flash",
                ]
                dados_anuncio = None

                for modelo in modelos_anuncio:
                    try:
                        resp = client.models.generate_content(
                            model=modelo,
                            contents=prompt_json,
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json"
                            )
                        )
                        if resp and resp.text:
                            dados_anuncio = json.loads(resp.text)
                            break
                    except Exception:
                        continue

                if dados_anuncio:
                    dados_anuncio["preco_venda_R$"] = calc["preco_venda"]
                    dados_anuncio["custo_producao_R$"] = calc["custo_total"]
                    dados_anuncio["lucro_liquido_R$"] = calc["lucro_liquido"]

                    st.session_state.anuncios_salvos.insert(0, dados_anuncio)
                    st.success("✅ Ficha gerada com sucesso!")
                else:
                    st.error("⚠️ Os servidores da IA estão com alta demanda agora. Aguarde 5 segundos e clique novamente.")

    if st.session_state.anuncios_salvos:
        st.divider()
        top_bar_1, top_bar_2 = st.columns([3, 1])
        top_bar_1.markdown(f"### 📋 Catálogo Gerado ({len(st.session_state.anuncios_salvos)} {'ficha' if len(st.session_state.anuncios_salvos) == 1 else 'fichas'})")
        
        df = pd.DataFrame(st.session_state.anuncios_salvos)
        csv = df.to_csv(index=False).encode("utf-8-sig")
        top_bar_2.download_button(
            label="📥 Exportar Tudo (.CSV)",
            data=csv,
            file_name="catalogo_fantastic_print.csv",
            mime="text/csv",
            use_container_width=True
        )

        for idx, item in enumerate(st.session_state.anuncios_salvos):
            with st.container(border=True):
                custo_v = item.get("custo_producao_R$", 0.0)
                venda_v = item.get("preco_venda_R$", 0.0)
                lucro_v = item.get("lucro_liquido_R$", 0.0)

                # Painel financeiro completo sem truncar números
                html_fin = (
                    f'<div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:12px; '
                    f'background:#09080E; border:1px solid #26213B; border-radius:12px; padding:14px 18px; margin-bottom:16px;">'
                    f'<div><div style="font-size:0.78rem; color:#A1A1AA;">Custo de Produção</div>'
                    f'<div style="font-size:1.35rem; font-weight:800; color:#E4E4E7;">R$ {custo_v:.2f}</div></div>'
                    f'<div><div style="font-size:0.78rem; color:#A1A1AA;">Preço de Venda Sugerido</div>'
                    f'<div style="font-size:1.35rem; font-weight:800; color:#C084FC;">R$ {venda_v:.2f}</div></div>'
                    f'<div><div style="font-size:0.78rem; color:#A1A1AA;">Lucro Líquido Estimado</div>'
                    f'<div style="font-size:1.35rem; font-weight:800; color:#4ADE80;">+R$ {lucro_v:.2f}</div></div>'
                    f'</div>'
                )
                st.markdown(html_fin, unsafe_allow_html=True)

                st.markdown("**🏷️ Título SEO (clique no ícone à direita para copiar):**")
                st.code(item.get("titulo_seo", ""), language=None, wrap_lines=True)

                st.markdown("**📝 Descrição Completa do Anúncio:**")
                st.text_area(
                    label=f"desc_{idx}",
                    value=item.get("descricao_completa", ""),
                    height=180,
                    label_visibility="collapsed"
                )

                st.markdown("**🔍 Tags de Busca (Shopee / Mercado Livre):**")
                st.code(item.get("tags_busca", ""), language=None, wrap_lines=True)

                st.markdown("**📸 Sugestão de Foto de Capa:**")
                st.info(item.get("sugestao_foto_capa", ""))