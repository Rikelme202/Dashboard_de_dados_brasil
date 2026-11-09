# Brasil em Dados 🇧🇷

Um dashboard pequeno e direto que cruza **indicadores econômicos do Banco Central** com **dados do IBGE**, usando só APIs públicas, sem cadastro e sem chave de acesso.

Eu queria ver, em uma única tela, como anda a economia do país e como os estados se comparam. Separei só o que achei mais interessante.

## O que ele mostra

- **4 números-chave:** dólar, Selic, inflação em 12 meses e PIB do país.
- **Como anda o dólar?** Série mensal, com filtro de 12 meses, 3 anos, 5 anos ou tudo.
- **Juros altos, inflação mais calma:** Selic e IPCA acumulado lado a lado, para ver o juro real na prática.
- **Quem produz mais por pessoa?** Ranking de PIB per capita dos 27 estados.

Os comentários abaixo de cada título são calculados a partir dos dados, então se atualizam sozinhos.

## De onde vêm os dados

| Fonte | Dado |
|---|---|
| Banco Central (SGS), séries 1, 432 e 433 | Dólar comercial, meta Selic e IPCA mensal |
| IBGE, agregado 4709 | População residente (Censo 2022) |
| IBGE, agregado 5938 | PIB a preços correntes (2023) |

## Como foi feito

1. `coletar.py` consulta as APIs, trata as respostas e gera o `dados.json`. Ele reduz dólar e Selic ao último valor de cada mês e calcula o IPCA acumulado em 12 meses.
2. `montar.py` embute os dados no `template.html` e gera o `dashboard.html`, um arquivo único.
3. O visual é HTML, CSS e JavaScript puros, com [Chart.js](https://www.chartjs.org/) nos gráficos.

## Como usar

Abra o `dashboard.html` no navegador (precisa de internet para carregar o Chart.js).

Para atualizar os dados:

```bash
python3 coletar.py && python3 montar.py
```

## Estrutura

```
├── coletar.py       # coleta e consolida os dados das APIs
├── montar.py        # gera o dashboard.html a partir do template
├── template.html    # layout e gráficos
├── dados.json       # dados consolidados (gerado)
└── dashboard.html   # dashboard final (gerado)
```

## Limitações

- População (2022) e PIB (2023) são de anos diferentes, então o PIB per capita mistura os dois.
- A Selic é a **meta** definida pelo Copom, não a taxa efetiva.
- O juro real é uma aproximação: Selic menos IPCA acumulado em 12 meses.

## Próximos passos

- Mapa por estado
- Mais séries (desemprego, PIB trimestral)
- Atualização automática dos dados
- Publicação online (GitHub Pages)

---

Feito por Rikelme Holanda, com dados abertos do governo brasileiro.
