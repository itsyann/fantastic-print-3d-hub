# 🟣 Fantastic Print 3D — Catálogo Inteligente & Precificação com IA

Aplicação web desenvolvida em **Python** e **Streamlit** integrada à **Google Gemini API (`google-genai`)** para automação de pesquisa de produtos, validação de demanda em marketplaces e precificação dinâmica para impressão 3D.

## 🚀 Funcionalidades
- **Agente de Pesquisa de Catálogo (Function Calling):** Busca modelos validados no MakerWorld ordenados por popularidade (`downloadCount`) e cruza com anúncios reais da Shopee e Mercado Livre.
- **Calculadora de Precificação & Margem:** Calcula automaticamente custo de filamento (PLA/PETG com fator de perda), hora-máquina, insumos e taxas de marketplaces (Shopee, Mercado Livre, TikTok Shop).
- **Gerador de Anúncios SEO:** Cria títulos otimizados (até 60 caracteres), descrições persuasivas, tags de busca e sugestões de foto de capa com exportação direta para `.CSV`.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.13
- **IA & SDK:** Google GenAI SDK (`gemini-3.8-flash` / `gemini-3.5-flash-lite`) com *Automatic Function Calling*
- **Interface:** Streamlit (CSS customizado estilo SaaS)
- **Dados & Busca:** Pandas, Requests, DDGS

## ⚙️ Como Executar Localmente
1. Clone o repositório:
   ```bash
   git clone [https://github.com/itsyann/fantastic-print-3d-hub.git](https://github.com/itsyann/fantastic-print-3d-hub.git)
   cd fantastic-print-3d-hub