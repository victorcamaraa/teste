# Caça Promoções de Hardware

Bot que procura promoções de **processadores, memória RAM, placas de vídeo e
armazenamento (SSD/HD)** em lojas brasileiras e mostra tudo numa página web com
filtros.

Lojas consultadas:

| Loja | Como os dados são obtidos |
|---|---|
| KaBuM! | API JSON do catálogo usada pelo próprio site |
| Pichau | JSON `__NEXT_DATA__` da página (com JSON-LD como plano B) |
| Terabyte | HTML da listagem (com JSON-LD como plano B) |
| Mercado Livre | API pública de busca (`ML_ACCESS_TOKEN` opcional) |

## Como rodar

```bash
cd bot-promocoes
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Abra **http://localhost:5000**. A primeira coleta começa sozinha ao iniciar e
leva cerca de 1 minuto. Depois disso o bot repete a busca a cada 30 minutos. O
botão **Buscar agora** força uma coleta na hora.

Para coletar uma vez só, sem a interface:

```bash
python -m promobot.collector
```

## Interface

- **Tipo de peça**: Processadores, Memória RAM, Placas de Vídeo, Armazenamento
  (dá para marcar vários; se nenhum estiver marcado, aparecem todos)
- **Busca por texto** (ex.: `rtx 4060`, `ddr5 32gb`, `nvme 1tb`)
- **Faixa de preço**, **desconto mínimo** e **lojas**
- **Só promoções** / **Só em estoque**
- Ordenação por maior desconto, menor ou maior preço e mais recentes
- Os filtros ficam na URL, então dá para salvar a busca nos favoritos
- **Status das lojas** mostra quantos produtos cada loja trouxe ou o erro que deu

### O que conta como promoção

Um produto aparece como promoção quando:

1. a loja mostra um preço "de/por" (preço antigo maior que o atual), **ou**
2. o preço caiu desde a coleta anterior (o bot guarda o histórico), **ou**
3. é uma oferta relâmpago com prazo (KaBuM!), que aparece com "Acaba em…"

O selo **Menor preço visto** aparece quando o preço atual é o menor já registrado.
Produtos que saíram da listagem da loja somem da página na coleta seguinte.

## Configuração (variáveis de ambiente)

| Variável | Padrão | Para que serve |
|---|---|---|
| `INTERVALO_MINUTOS` | `30` | Intervalo entre as coletas automáticas |
| `PROMOBOT_DB` | `promocoes.db` | Arquivo SQLite com ofertas e histórico |
| `HOST` / `PORT` | `127.0.0.1` / `5000` | Endereço da interface web |
| `TELEGRAM_BOT_TOKEN` e `TELEGRAM_CHAT_ID` | — | Ativam alertas no Telegram |
| `NOTIFY_MIN_DISCOUNT` | `15` | Desconto mínimo (%) para enviar alerta |
| `ML_ACCESS_TOKEN` | — | Token do Mercado Livre, se a busca anônima for bloqueada |

### Alertas no Telegram (opcional)

1. Fale com o [@BotFather](https://t.me/BotFather), crie um bot e copie o token.
2. Mande uma mensagem para o seu bot e pegue o seu `chat_id` em
   `https://api.telegram.org/bot<TOKEN>/getUpdates`.
3. Rode com `TELEGRAM_BOT_TOKEN=... TELEGRAM_CHAT_ID=... python app.py`.

Você recebe um alerta quando um produto novo aparece, ou quando um produto
baixa de preço, desde que o desconto seja de pelo menos `NOTIFY_MIN_DISCOUNT`%.

## Quando uma loja para de funcionar

As lojas mudam o layout de vez em quando. Se uma loja aparecer com erro ou com
0 produtos em **Status das lojas**:

- O endereço de cada categoria fica no topo do arquivo da loja, em
  `promobot/scrapers/<loja>.py` (`CATEGORY_PATHS`).
- Na Terabyte, os seletores CSS ficam em `CARD_SELECTORS`, `PRICE_SELECTORS` etc.
- Algumas lojas usam proteção anti-bot (Cloudflare) e podem bloquear por
  instantes. Nesse caso o bot mantém os últimos resultados que conseguiu e tenta
  de novo na próxima coleta.

Para adicionar outra loja, crie uma classe com `fetch(category) -> list[Deal]`
em `promobot/scrapers/` e coloque-a na lista `SCRAPERS` em
`promobot/scrapers/__init__.py`.

## Testes

```bash
pytest
```

## Estrutura

```
app.py                  interface web (Flask) + API
promobot/
  categories.py         tipos de peça e classificação por palavra-chave
  collector.py          roda os scrapers e agenda as coletas
  storage.py            SQLite: ofertas, histórico de preço, status das lojas
  notifier.py           alertas no Telegram
  scrapers/             um arquivo por loja
templates/, static/     página e estilo
tests/                  testes dos parsers e da API
```
