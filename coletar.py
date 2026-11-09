
import gzip
import json
import urllib.request
from datetime import datetime, date


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        raw = r.read()
    if raw[:2] == b"\x1f\x8b":  # resposta gzip
        raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8"))


def sgs(codigo, inicio="01/01/2020"):
    hoje = date.today().strftime("%d/%m/%Y")
    url = (f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"
           f"?formato=json&dataInicial={inicio}&dataFinal={hoje}")
    return [{"d": datetime.strptime(x["data"], "%d/%m/%Y").strftime("%Y-%m-%d"),
             "v": float(x["valor"])} for x in get(url)]


def mensal(serie):
    """Reduz série diária ao último valor de cada mês."""
    out = {}
    for p in serie:
        out[p["d"][:7]] = p["v"]
    return [{"d": k, "v": v} for k, v in sorted(out.items())]


def ibge(agregado, periodo, variavel):
    url = (f"https://servicodados.ibge.gov.br/api/v3/agregados/{agregado}"
           f"/periodos/{periodo}/variaveis/{variavel}?localidades=N3[all]")
    res = get(url.replace("[", "%5B").replace("]", "%5D"))[0]["resultados"][0]["series"]
    return {s["localidade"]["id"]: float(list(s["serie"].values())[0]) for s in res}


# --- Banco Central ---
dolar = mensal(sgs(1))               
selic = mensal(sgs(432))           
ipca = sgs(433)                    (
# IPCA acumulado em 12 meses
for i, p in enumerate(ipca):
    if i >= 11:
        acc = 1.0
        for q in ipca[i - 11:i + 1]:
            acc *= 1 + q["v"] / 100
        p["a12"] = round((acc - 1) * 100, 2)

# --- IBGE ---
estados = get("https://servicodados.ibge.gov.br/api/v1/localidades/estados?orderBy=nome")
pop = ibge(4709, 2022, 93)         # população Censo 2022
pib = ibge(5938, 2023, 37)         # PIB 2023 (mil reais)

ufs = []
for e in estados:
    i = str(e["id"])
    if i in pop and i in pib:
        ufs.append({
            "id": i, "uf": e["sigla"], "nome": e["nome"], "regiao": e["regiao"]["nome"],
            "pop": int(pop[i]), "pib": pib[i] * 1000,  # em reais
        })

dados = {"gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
         "dolar": dolar, "selic": selic, "ipca": ipca, "ufs": ufs}
with open("dados.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False)

print(f"dolar={len(dolar)} selic={len(selic)} ipca={len(ipca)} ufs={len(ufs)}")
print("último dólar:", dolar[-1], "| última selic:", selic[-1], "| último ipca:", ipca[-1])
