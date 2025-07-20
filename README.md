# 🍽️ RestCheck · Inteligência para Restaurantes

Painel com IA que transforma seu histórico de pedidos em previsões por prato.  
Feito para donos de restaurante que querem evitar desperdício, prever demanda e vender com precisão.

---

## 🚀 Como funciona

1. Envie seu arquivo `.csv` com colunas `data`, `prato`, `quantidade`
2. Clique em “Gerar Previsões” no painel
3. Visualize relatórios, estatísticas e exportações em Excel

---

## 🧠 Funcionalidades

- 🔮 Previsão por prato com IA
- 📊 Gráficos interativos
- 📈 Evolução da demanda ao longo do tempo
- 📋 Exportação em `.xlsx`
- 📁 Painel simples e responsivo

---

## 🛠️ Executando localmente

```bash
git clone https://github.com/seuusuario/restcheck.git
cd restcheck

python -m venv .venv
source .venv/bin/activate     # ou .venv\Scripts\activate no Windows

pip install -r requirements.txt
streamlit run painel_streamlit.py

🧬 Termos de uso
O RestCheck realiza previsões estatísticas com base nos dados fornecidos

Nenhuma informação é compartilhada ou armazenada externamente

Recomenda-se validação dos dados antes de tomar decisões comerciais

Política de privacidade (em breve)

Feito por Gabriel S. de Freitas com apoio do Copilot. Tecnologias usadas: Python · Streamlit · Machine Learning

📬 [restcheck.com.br/teste](https://gabrielsf476.github.io/SiteRestCheck/) | 📱 (21) 98243-8356 | 📷 @restcheckapp
