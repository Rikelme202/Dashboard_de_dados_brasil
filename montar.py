
dados = open("dados.json", encoding="utf-8").read()
html = open("template.html", encoding="utf-8").read()
open("dashboard.html", "w", encoding="utf-8").write(html.replace("/*DADOS*/null", dados))
print("dashboard.html gerado")
