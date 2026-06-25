#!/usr/bin/env python3
"""
Generate Reino Animal study notes as a styled HTML file.
Can be opened in any browser and printed/saved as PDF.
"""

# Color palette
C = {
    "cnidaria":      "#2E86AB",
    "ctenophora":    "#A23B72",
    "platy":         "#F18F01",
    "rhyncho":       "#C73E1D",
    "nematoda":      "#3B1F2B",
    "annelida":      "#44BBA4",
    "mollusca":      "#E94F37",
    "arthropoda":    "#393E41",
    "deutero":       "#6B4226",
    "hemicorda":     "#7B2D8B",
    "chordata":      "#1B998B",
    "anfibia":       "#5C8001",
    "reptilia":      "#8B5E3C",
    "aves":          "#E7B800",
    "mammalia":      "#D62246",
}

def banner(title, color, subtitle=""):
    sub_html = f'<div class="banner-sub">{subtitle}</div>' if subtitle else ""
    return f'<div class="banner" style="background:{color}">{title}{sub_html}</div>'


def info_card(rows, border_color):
    rows_html = ""
    for label, val in rows:
        rows_html += f'<div class="card-row"><span class="card-label">{label.upper()}:</span> {val}</div>\n'
    return f'<div class="info-card" style="border-left:5px solid {border_color}">{rows_html}</div>'

def table(headers, rows, col_color):
    th = "".join(f'<th style="background:{col_color};color:#fff">{h}</th>' for h in headers)
    body = ""
    for i, row in enumerate(rows):
        bg = "#f9f9f9" if i % 2 else "#fff"
        tds = "".join(f'<td>{c}</td>' for c in row)
        body += f'<tr style="background:{bg}">{tds}</tr>\n'
    return f'<table><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table>'

def bul(text):
    return f'<li>{text}</li>'

def dis(text):
    return f'<li class="disease">{text}</li>'

def extra(text):
    return f'<div class="extra">[EXTRA] {text}</div>'

def h2(text):
    return f'<h2>{text}</h2>'

def body_p(text):
    return f'<p>{text}</p>'


HTML_HEAD = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Reino Animal - Apuntes de clase</title>
<style>
"""


CSS = """
@page { size: A4; margin: 1.5cm; }
* { box-sizing: border-box; }
body {
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 9pt;
    line-height: 1.5;
    color: #222;
    max-width: 21cm;
    margin: 0 auto;
    padding: 1.5cm;
}
.cover {
    text-align: center;
    padding-top: 8cm;
    page-break-after: always;
}
.cover h1 {
    font-size: 36pt;
    color: #1A1A2E;
    margin-bottom: 0.3cm;
}
.cover .sub {
    font-size: 14pt;
    color: #444;
}
.cover hr {
    width: 80%;
    margin: 1cm auto;
    border: none;
    border-top: 2px solid #1B998B;
}
.banner {
    color: #fff;
    font-weight: bold;
    font-size: 12pt;
    padding: 8px 16px;
    border-radius: 6px;
    margin: 18px 0 10px 0;
    page-break-inside: avoid;
}
.banner-sub {
    font-size: 8pt;
    font-weight: normal;
    margin-top: 2px;
}
.info-card {
    background: #F5F5F5;
    border: 1px solid #DDD;
    border-radius: 4px;
    padding: 8px 12px;
    margin: 8px 0;
    page-break-inside: avoid;
}
.card-row {
    padding: 2px 0;
    font-size: 8.5pt;
}
.card-label {
    font-weight: bold;
    color: #555;
}
h2 {
    font-size: 10.5pt;
    color: #333;
    margin: 12px 0 4px 0;
    border-bottom: 1px solid #eee;
    padding-bottom: 2px;
}
ul {
    margin: 4px 0;
    padding-left: 18px;
}
li {
    margin: 2px 0;
    font-size: 8.5pt;
}
li.disease {
    color: #CC0000;
    background: #FFE5E5;
    padding: 2px 6px;
    border-radius: 3px;
    list-style-type: none;
    margin-left: -18px;
    padding-left: 18px;
}
li.disease::before {
    content: "\\1F534 ";
}
.extra {
    background: #FFFDE7;
    color: #E65100;
    padding: 4px 8px;
    border-radius: 3px;
    font-size: 8pt;
    margin: 6px 0;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 7.5pt;
    page-break-inside: avoid;
}
th, td {
    padding: 4px 6px;
    border: 0.4px solid #CCC;
    vertical-align: middle;
}
th {
    font-weight: bold;
}
p {
    margin: 4px 0;
    font-size: 8.5pt;
}
.page-break {
    page-break-before: always;
}
"""


def build_content():
    parts = []
    add = parts.append

    # COVER
    add('<div class="cover">')
    add('<h1>REINO ANIMAL</h1>')
    add('<p class="sub">Biolog\u00eda \u00b7 Apuntes de clase</p>')
    add('<hr>')
    add('<p class="sub">Phylum Cnidaria \u2192 Mammalia</p>')
    add('</div>')

    # 1. CNIDARIA
    add(banner("PHYLUM CNIDARIA (Celent\u00e9reos)", C["cnidaria"]))
    add(info_card([
        ("Tambi\u00e9n llamados", "Celent\u00e9rados (por tener cavidad)"),
        ("Ambiente",         "Exclusivamente acu\u00e1ticos"),
        ("Organizaci\u00f3n",     "Dibl\u00e1sticos: Ectodermo + Mesoglea + Endodermo"),
        ("Formas",           "P\u00f3lipo (s\u00e9sil) o Medusa (nadadora)"),
        ("Digestivo",        "Cavidad gastrovascular \u2014 \u00f3sculo de entrada y salida"),
        ("Epitelio interno", "Gastrodermis"),
        ("Circulatorio",     "NO TIENEN \u2014 usan sus c\u00e9lulas"),
        ("Respiratorio",     "NO TIENEN \u2014 difusi\u00f3n celular"),
        ("Reproductor",      "Sexual y asexual (gemaci\u00f3n) \u2014 hermafroditas"),
    ], C["cnidaria"]))
    add(h2("Caracter\u00edsticas clave"))
    add('<ul>')
    add(bul("Distinguidos por sus <b>cnidocitos</b> (c\u00e9lulas urticantes)"))
    add(bul("Cnidocitos poseen <b>nematocisto</b> (arp\u00f3n) para atrapar presas o defenderse"))
    add(bul("<b>Primeros animales en tener tejidos</b>"))
    add(bul("<b>Primeros en tener sistema nervioso y muscular</b>"))
    add(bul("Sistema nervioso: plexo nervioso bajo la dermis (neuronas simples)"))
    add(bul("Sistema muscular: <b>mionemas</b> (c\u00e9lulas ricas en actina y miosina)"))
    add('</ul>')
    add(h2("Clases del Phylum Cnidaria"))
    add(table(
        ["Clase", "Ejemplos", "Forma dominante", "Reproducci\u00f3n asexual"],
        [
            ["Hydrozoa",  "Hidras, Obelia, Physalia", "P\u00f3lipo (hidras) / ambas (Obelia)", "Gemaci\u00f3n"],
            ["Scyphozoa", "Aguamalas / aguavivas",    "Medusa",                            "Gemaci\u00f3n \u2192 Efira"],
            ["Anthozoa",  "Corales, an\u00e9monas",         "Solo p\u00f3lipo",                       "Gemaci\u00f3n, divisi\u00f3n, fragmentaci\u00f3n"],
        ],
        C["cnidaria"]
    ))
    add(body_p("<b>Efira:</b> etapa creciente de la medusa. <b>Pl\u00e1nula:</b> larva que viaja y se incrusta para originar adulto."))

    # 2. CTENOPHORA
    add(banner("PHYLUM CTENOPHORA (Nueces de mar)", C["ctenophora"]))
    add(info_card([
        ("H\u00e1bitat",       "Planct\u00f3nicos, marinos"),
        ("Caracter\u00edstica","Bioluminiscentes \u2014 hileras de cilios"),
        ("Digestivo",     "Cavidad gastrovascular (similar a medusas)"),
        ("Alimentaci\u00f3n",  "Tent\u00e1culos pegajosos"),
        ("Reproductor",   "Sexual hermafrodita \u2014 cigoto \u2192 larva \u2192 adulto"),
    ], C["ctenophora"]))

    # SIMETRIAS
    add(banner("COMPARACI\u00d3N DE SIMETR\u00cdAS Y TRIBL\u00c1STICOS", "#607D8B"))
    add('<ul>')
    add(bul("Cnidarios y Cten\u00f3foros: <b>simetr\u00eda radial</b>"))
    add(bul("De aqu\u00ed en adelante: <b>simetr\u00eda bilateral</b> (mayor movilidad y complejidad)"))
    add(bul("Excepci\u00f3n: <b>Equinodermos</b> \u2014 larvaria bilateral \u2192 adulto radial"))
    add(bul("Todos los bilaterales son <b>tribl\u00e1sticos</b> (ectodermo, mesodermo, endodermo)"))
    add('</ul>')
    add(table(
        ["Tipo", "Cavidad", "Ejemplos"],
        [
            ["Acelomados",      "Sin celoma (mesodermo s\u00f3lido)",       "Platelmintos, Nemertinos"],
            ["Pseudocelomados", "Pseudoceloma (no revestido del todo)", "Nematodos"],
            ["Celomados",       "Celoma verdadero (en mesodermo)",      "An\u00e9lidos, Moluscos, Artr\u00f3podos, Cordados"],
        ],
        "#607D8B"
    ))

    return parts


def build_content_2():
    parts = []
    add = parts.append

    # 3. PLATYHELMINTHES
    add(banner("PHYLUM PLATYHELMINTHES (Gusanos planos)", C["platy"]))
    add(info_card([
        ("Organizaci\u00f3n",  "Acelomados tribl\u00e1sticos \u2014 invertebrados"),
        ("H\u00e1bitat",       "Acu\u00e1ticos o par\u00e1sitos de vertebrados"),
        ("Digestivo",     "Algunos por piel / otros con faringe (sin ano)"),
        ("Respiratorio",  "NO TIENEN \u2014 difusi\u00f3n celular"),
        ("Circulatorio",  "NO TIENEN \u2014 difusi\u00f3n celular"),
        ("Nervioso",      "Ganglios, axones e interneuronas \u2014 centralizaci\u00f3n"),
        ("Muscular",      "Mionemas o movimientos perist\u00e1lticos"),
        ("Excretor",      "Protonefridios (c\u00e9lula flama) \u2014 secretan amoniaco"),
        ("Reproductor",   "Hermafroditas \u2014 fecundaci\u00f3n interna \u2014 fragmentaci\u00f3n en algunas sp."),
    ], C["platy"]))

    add(h2("Clase Turbellaria (Planarias)"))
    add('<ul>')
    add(bul("<b>Primera vez sistema renal</b> (protonefridios / c\u00e9lula flama)"))
    add(bul("Carn\u00edvoras \u2014 desplazamiento por cilios \u2014 hermafroditas"))
    add('</ul>')

    add(h2("Clase Trematoda (Duelas)"))
    add('<ul>')
    add(bul("Par\u00e1sitos de vertebrados"))
    add(bul("Capa externa resistente a jugos g\u00e1stricos del hu\u00e9sped"))
    add(dis("Fasciola hepatica \u2014 par\u00e1sito del humano por consumo de berros o caracoles"))
    add('</ul>')

    add(h2("Clase Cestoda (Tenias / Solitarias)"))
    add('<ul>')
    add(bul("Sin tubo digestivo \u2014 hermafroditas \u2014 capa externa resistente a jugos g\u00e1stricos"))
    add(bul("Transmisi\u00f3n: quiste o huevo. Fijaci\u00f3n: ganchos y ventosas en mucosa intestinal"))
    add(bul("Formas: gusano (adulto), cisticerco y huevo"))
    add(bul("Progl\u00f3tidos: inmaduros (cerca del esc\u00f3lex) \u2192 maduros (medio) \u2192 gr\u00e1vidos (final). Todo el cuerpo = <b>estr\u00f3bilo</b>"))
    add(bul("<b>T. saginata</b> (res) \u2014 <b>T. solium</b> (puerco, tiene ganchos)"))
    add(dis("Cisticercosis \u2014 solo por ingerir HUEVO de T. solium \u2192 va a tejidos, m\u00fasculo, cerebro"))
    add(dis("Teniasis \u2014 por ingerir cisticercos (carne mal cocida)"))
    add(dis("S\u00edndrome de mala absorci\u00f3n"))
    add('</ul>')

    add(h2("Phylum Rhynchocoela (Nemertinos / Gusano cinta)"))
    add('<ul>')
    add(bul("Acelomados marinos"))
    add(bul("<b>Primeros en tener sistema circulatorio cerrado</b> \u2014 2 vasos laterales + 1 dorsal (sangre incolora)"))
    add(bul("Tubo digestivo con boca y ano \u2014 poseen prob\u00f3scide"))
    add('</ul>')

    add(h2("Phylum Gnathostomulida (Gusanos mandibulados)"))
    add('<ul>')
    add(bul("Acelomado marino y diminuto \u2014 vive en arena y lodo de costas litorales"))
    add(bul("Poseen mand\u00edbulas duras (gnathos = mand\u00edbula, stomos = boca)"))
    add('</ul>')

    return parts


def build_content_3():
    parts = []
    add = parts.append

    # 4. NEMATODA
    add(banner("PHYLUM NEMATODA (Nemathelmintos \u2014 Pseudocelomados)", C["nematoda"]))
    add(info_card([
        ("Organizaci\u00f3n",  "Pseudocelomados \u2014 gusanos cil\u00edndricos (hilo/filamento)"),
        ("Pseudoceloma",  "Tubo sellado que incrementa efectividad de contracciones musculares"),
        ("Digestivo",     "Unidireccional \u2014 faringe + boca con estiletes + ano"),
        ("Respiratorio",  "NO TIENEN \u2014 todo por piel"),
        ("Circulatorio",  "NO TIENEN \u2014 tama\u00f1o peque\u00f1o"),
        ("Nervioso",      "Ganglios y somas"),
        ("Excretor",      "Secretan NH4 (amoniaco)"),
        ("Reproductor",   "Solo fecundaci\u00f3n sexual"),
        ("Transmisi\u00f3n",   "Ciclo ano-boca (ingesta de huevos)"),
    ], C["nematoda"]))
    add(h2("Par\u00e1sitos importantes"))
    add('<ul>')
    add(dis("Enterobius vermicularis \u2014 forma infectante: huevo (ciclo ano-boca)"))
    add(dis("Ascaris lumbricoides \u2014 principal parasitosis de M\u00e9xico \u2014 solo etapa larvaria, huevos con mameloides"))
    add(dis("Filarias / Ancylostoma / Necator / Strongyloides \u2014 penetran por piel en lugares h\u00famedos \u2192 v\u00eda linf\u00e1tica \u2192 coraz\u00f3n. Produce saba\u00f1\u00f3n en punto de entrada"))
    add(dis("Trichinella trichiura \u2014 sin huevo, se reproducen en larvas \u2014 atraviesan mucosas \u2192 m\u00fasculo (carne porcina)"))
    add('</ul>')

    # 5. ANNELIDA
    add(banner("PHYLUM ANNELIDA (Gusanos anillados)", C["annelida"]))
    add(info_card([
        ("Organizaci\u00f3n",  "Celomados protostomos \u2014 segmentados (met\u00e1meros)"),
        ("H\u00e1bitat",       "Tierra y agua dulce/salada"),
        ("Digestivo",     "Tubular con boca y ano"),
        ("Circulatorio",  "CERRADO \u2014 lombriz: 5 corazones en anillo, sin eritrocitos, solo plasma"),
        ("Respiratorio",  "Por epidermis"),
        ("Nervioso",      "Centralizado \u2014 receptores t\u00e1ctiles, gustativos, fotorreceptores"),
        ("Excretor",      "Metanefridios en hileras a lo largo del cuerpo"),
        ("Reproductor",   "Hermafroditas \u2014 sin fragmentaci\u00f3n"),
        ("Muscular",      "Circular + longitudinal (circular hace avanzar)"),
    ], C["annelida"]))
    add(body_p("<b>\u00a1Primera vez que hay coraz\u00f3n en animales!</b>"))
    add(table(
        ["Clase", "H\u00e1bitat", "Caracter\u00edsticas clave"],
        [
            ["Oligoqueta", "Terrestre",        "Amoniot\u00e9licos \u2014 hacen t\u00faneles \u2014 cl\u00edtelo en apareamiento \u2014 partenog\u00e9nesis posible"],
            ["Poliqueta",  "Marina",           "Tent\u00e1culos y antenas \u2014 parapodios (locomoci\u00f3n + respiraci\u00f3n) \u2014 tagmosis \u2014 larva troc\u00f3fora"],
            ["Hirudinea",  "Dulce/pantanosa",  "Sanguijuelas \u2014 2 ventosas \u2014 enzima hirudinea (anticoagulante) \u2014 tratamiento de aterosclerosis"],
        ],
        C["annelida"]
    ))

    return parts


def build_content_4():
    parts = []
    add = parts.append

    # 6. MOLLUSCA
    add(banner("PHYLUM MOLLUSCA", C["mollusca"]))
    add(info_card([
        ("Etimolog\u00eda",    "Mollus = blando \u2014 ~100,000 especies \u2014 f\u00f3siles desde el C\u00e1mbrico"),
        ("Organizaci\u00f3n",  "Celomados protostomos tribl\u00e1sticos"),
        ("Cuerpo",        "Cefalopi\u00e9 + masa visceral + manto"),
        ("Cavidad paleal","Entre manto y masa visceral \u2014 desechos digestivos, urinarios, reproductores y respiraci\u00f3n"),
        ("Digestivo",     "R\u00e1dula (dientes) excepto bivalvos. Cefal\u00f3podos tambi\u00e9n tienen pico de perico"),
        ("Circulatorio",  "Abierto (hemoceloma) EXCEPTO cefal\u00f3podos (cerrado) \u2014 coraz\u00f3n 3 c\u00e1maras"),
        ("Sangre",        "Hemolinfa \u2014 bivalvos incolora \u2014 gaster\u00f3podos/cefal\u00f3podos AZUL-VERDOSA (hemocianina con cobre)"),
        ("Excretor",      "Metanefridios \u2192 cavidad paleal"),
        ("Reproductor",   "Sexual \u2014 bivalvos fecundaci\u00f3n externa / cefal\u00f3podos: sexos sep. / gaster\u00f3podos: hermafroditas"),
    ], C["mollusca"]))
    add(table(
        ["Clase", "Ejemplos", "Caracter\u00edsticas especiales"],
        [
            ["Bivalva (Lamelibranquios)", "Mejillones, ostiones, almejas, vieiras", "Sin r\u00e1dula \u2014 m\u00fasculos aductores \u2014 alimentaci\u00f3n por filtraci\u00f3n \u2014 vieiras: >100 ojos \u2014 estatocistos"],
            ["Gastropoda",               "Caracoles, babosas",                       "\u00danico animal asim\u00e9trico del reino \u2014 quimiorreceptores \u2014 ojos detectan luz \u2014 SN: 6 ganglios"],
            ["Cephalopoda",              "Pulpos (8), calamares (10), jibias (10), nautilos (90)", "3 corazones \u2014 SN cerrado \u2014 cerebro con ganglios \u2014 ojos especializados \u2014 defensa: tinta, camuflaje, mimetismo \u2014 PRIMER CEREBRO PROPIAMENTE DICHO"],
        ],
        C["mollusca"]
    ))

    # 7. ARTHROPODA
    add(banner("PHYLUM ARTHROPODA", C["arthropoda"]))
    add(info_card([
        ("Organizaci\u00f3n",   "Celomados protostomos esquizocel\u00f3micos"),
        ("Clasificaci\u00f3n",  "Por ap\u00e9ndices, segmentaci\u00f3n, exoesqueleto y \u00f3rganos sensoriales"),
        ("Exoesqueleto",   "Quitina (todos) \u2014 crust\u00e1ceos: quitina + calcio"),
        ("Muda",           "Ap\u00f3lisis (apoptosis para soltar exoesqueleto) \u2192 Ecdisis (salida) \u2192 Esclerotizaci\u00f3n"),
        ("Circulatorio",   "Abierto \u2014 hemolinfa (azul, verde o incolora) \u2014 coraz\u00f3n tubular dorsal de 1 c\u00e1mara \u2014 hemocitos"),
        ("Digestivo",      "Unidireccional \u2014 estomodeo + mesenteron + proctodeo \u2014 cut\u00edcula quitinizada"),
        ("Excretor",       "T\u00fabulos de Malpighi (ri\u00f1ones) \u2014 cristales de \u00e1cido \u00farico o guanina con heces"),
        ("Respiratorio",   "Tr\u00e1queas ramificadas con espir\u00e1culos \u2014 ar\u00e1cnidos: filobranquias/filotraqueas"),
        ("Nervioso",       "3 pares de ganglios dorsales fusionados en cabeza \u2014 tagmosis: puede moverse sin cabeza"),
        ("Reproductor",    "Sexos separados \u2014 metamorfosis: ametabolismo / hemimetabolismo / holometabolismo"),
    ], C["arthropoda"]))

    add(h2("Comparaci\u00f3n de clases principales"))
    add(table(
        ["Caracter\u00edstica",  "Insecta",          "Crustacea",             "Arachnida"],
        [
            ["\u00bfVuelan?",        "Mayor\u00eda s\u00ed",       "NO",                    "NO"],
            ["Antenas",         "1 par (2)",         "2 pares (4)",           "Ninguna"],
            ["Patas",           "3 pares (6)",       "5 pares (10)",          "4 pares (8)"],
            ["Segmentaci\u00f3n",    "Cabeza+T\u00f3rax+Abd.", "Cabeza+T\u00f3rax+Abd.",     "Cefalot\u00f3rax+Abd."],
            ["Exoesqueleto",    "Solo quitina",      "Quitina + calcio",      "Solo quitina"],
            ["H\u00e1bitat",         "Terrestre/a\u00e9reo",   "Acu\u00e1tico",              "Terrestre"],
            ["Ap\u00e9ndice bucal",  "Mand\u00edbulas",        "Mand\u00edbulas",            "Quel\u00edceros (colmillos)"],
        ],
        C["arthropoda"]
    ))

    return parts


def build_content_5():
    parts = []
    add = parts.append

    add(h2("Quelicerados"))
    add('<ul>')
    add(bul("Incluye: Merostomata (cangrejo cacerola/l\u00edmulos), Pycnogonida (ara\u00f1as de mar), Arachnida"))
    add(bul("Sin antenas ni mand\u00edbulas \u2014 1er ap\u00e9ndice: quel\u00edceros (pinzas/colmillos) \u2014 2do: pedipalpos"))
    add(bul("Solo escorpiones tienen abdomen segmentado \u2014 excepto \u00e1caros: todos carn\u00edvoros"))
    add(bul("Merostomata: su sangre se usa para detectar contaminaci\u00f3n bacteriana en medicamentos"))
    add(dis("Latrodectus mactans \u2014 Ara\u00f1a viuda negra (SLP)"))
    add(dis("Loxosceles laeta \u2014 Ara\u00f1a violinista venenosa"))
    add(dis("Enfermedad de Lyme \u2014 Borrelia burgdorferi (garrapata)"))
    add(dis("Fiebre de las Monta\u00f1as Rocosas \u2014 Rickettsia (garrapata)"))
    add(dis("Babesiosis \u2014 Babesia bigemina (garrapata)"))
    add('</ul>')

    add(h2("Metamorfosis en insectos"))
    add(table(
        ["Tipo", "Nombre", "Etapas"],
        [
            ["Sin metamorfosis",      "Ametabolismo",    "Huevo \u2192 Ninfa \u2192 Adulto (cambios m\u00ednimos)"],
            ["Metamorfosis incompleta","Hemimetabolismo", "Huevo \u2192 Ninfas sucesivas \u2192 Adulto"],
            ["Metamorfosis completa",  "Holometabolismo", "Huevo \u2192 Larva \u2192 Pupa/Cris\u00e1lida (capullo) \u2192 Adulto"],
        ],
        C["arthropoda"]
    ))
    add(body_p("<b>\u00d3rdenes de insectos:</b> \u00c1ptera (piojos, pulgas) \u00b7 Odonata (lib\u00e9lulas) \u00b7 Blattodea (cucarachas) \u00b7 Isoptera (termitas) \u00b7 Orthoptera (saltamontes, grillos) \u00b7 Diptera (moscas, mosquitos) \u00b7 Lepidoptera (mariposas, polillas) \u00b7 Hymenoptera (abejas, avispas, hormigas) \u00b7 Coleoptera (escarabajos, luci\u00e9rnagas)"))

    add(h2("Subclase Myriapoda"))
    add('<ul>')
    add(bul("Quil\u00f3podos (100 pies) y Dipl\u00f3podos (1000 pies, herb\u00edvoros) \u2014 1 par de antenas \u2014 excreci\u00f3n por t\u00fabulos de Malpighi"))
    add('</ul>')

    # 8. DEUTEROSTOMOS
    add(banner("DEUTEROSTOMOS \u2014 Generalidades", C["deutero"]))
    add(info_card([
        ("Incluye",       "Equinodermos, Hemicordados, Precordados, Cordados"),
        ("Desarrollo",    "Primero se forma el ANO, despu\u00e9s la boca"),
        ("Celoma",        "Enterocel\u00f3mico (invaginaciones del endodermo)"),
        ("Simetr\u00eda",      "Bilateral \u2014 excepci\u00f3n: equinodermos adultos (radial)"),
        ("Reproducci\u00f3n",  "Predomina la asexual"),
    ], C["deutero"]))

    add(h2("Equinodermos \u2014 Grupo Ambulacraria"))
    add('<ul>')
    add(bul("Se mueven mediante <b>pies ambulacrales hidr\u00e1ulicos</b> \u2014 sin sangre \u2014 agua de mar por placa cribosa (madreporita)"))
    add(bul("Digestivo: <b>\u00fanicos que sacan su est\u00f3mago fuera del cuerpo</b> para digerir la presa"))
    add(bul("Reproductor: sexos separados, fecundaci\u00f3n externa \u2014 asexual por fragmentaci\u00f3n"))
    add(bul("Nervioso: anillo nervioso central del que parten ramas a cada brazo"))
    add('</ul>')
    add(table(
        ["Clase", "Ejemplos"],
        [
            ["Asteroidea",   "Estrellas de mar"],
            ["Echinoidea",   "Erizos de mar"],
            ["Crinoidea",    "Lirios de mar"],
            ["Holothuroidea","Pepinos de mar"],
        ],
        C["deutero"]
    ))

    add(h2("Phylum Hemicordata (Gusanos bellota)"))
    add('<ul>')
    add(bul("Aspecto de gusano \u2014 sistema nervioso central \u2014 <b>sin notocorda ni esqueleto</b>"))
    add(bul("Clases: Pterobranchia y Enteropneusta"))
    add('</ul>')

    return parts


def build_content_6():
    parts = []
    add = parts.append

    add(banner("PRECORDADOS", C["hemicorda"]))
    add('<ul>')
    add(bul("<b>Notocorda:</b> cord\u00f3n cartilaginoso delante de la m\u00e9dula \u2014 soporte y protecci\u00f3n del SN \u2014 en vertebrados se convierte en columna vertebral"))
    add('</ul>')
    add(table(
        ["Subphylum", "Nombre com\u00fan", "Datos clave"],
        [
            ["Quetognata",    "Gusanos flecha",       "Planct\u00f3nicos marinos"],
            ["Cephalocordata","Lancetas / Anfioxos",   "Parecidos a peces sin aletas \u2014 PRIMEROS en tener notocorda \u2014 viven enterrados en arena \u2014 respiran/comen por filtraci\u00f3n de agua \u2014 el agua sale por el atrioporo"],
            ["Urochordata",   "Tunicados / Papas de mar","Larva: SN + notocorda \u2014 adulto: involuciona a 1 ganglio cerebral \u2014 fisiolog\u00eda similar a cefalocordados"],
        ],
        C["hemicorda"]
    ))

    # 9. PECES
    add(banner("SUBPHYLUM CHORDATA \u2014 PECES (Superclase Gnatostomata)", C["chordata"]))
    add(info_card([
        ("Agnathos",      "Peces sin mand\u00edbula \u2014 boca en ventosa \u2014 notocorda NO reemplazada (Mixines, Lampreas)"),
        ("Circulatorio",  "Cerrado \u2014 1 aur\u00edcula + 1 ventr\u00edculo \u2014 eritrocitos el\u00edpticos con n\u00facleo"),
        ("Tegumentario",  "Escamas (reducen fricci\u00f3n del agua)"),
        ("Respiratorio",  "Branquias (hendiduras far\u00edngeas) \u2014 ox\u00edgeno captado por mucosa branquial"),
        ("Digestivo",     "Unidireccional \u2014 cloaca posterior (mezcla orina + heces)"),
        ("Nervioso",      "PRIMER CEREBRO \u2014 arquicorteza + m\u00e9dula espinal protegidas por sistema \u00f3seo"),
        ("Reproductor",   "Sexos separados \u2014 fecundaci\u00f3n externa mayoritaria \u2014 tiburones/rayas: interna \u2014 pterig\u00f3podos (\u00f3rganos copuladores en tiburones)"),
    ], C["chordata"]))
    add(table(
        ["Clase", "Esqueleto", "Ejemplos"],
        [
            ["Placodermi",  "Placas \u00f3seas (EXTINTOS)",       "\u2014"],
            ["Condrictia",  "Cartilaginoso",                  "Tiburones, rayas, pez torpedo (20V, usado en Grecia para dolor)"],
            ["Osteictia",   "\u00d3seo calcificado",               "Acrinopterigios (aletas con rayos) \u00b7 Sarcopterigios (peces pulmonares, aletas carnosas \u2014 Celacanto f\u00f3sil viviente)"],
        ],
        C["chordata"]
    ))

    # 10. ANFIBIOS
    add(banner("SUPERCLASE TETRAPODA \u2014 CLASE ANFIBIA", C["anfibia"]))
    add(info_card([
        ("Origen",        "Derivados de los Sarcopterigios"),
        ("Tegumentario",  "Piel sin escamas \u2014 tambi\u00e9n respiran por piel \u2014 queratina delgada \u2014 susceptibles a desecaci\u00f3n \u2014 algunas sp. liberan sustancias t\u00f3xicas"),
        ("Respiratorio",  "Cut\u00e1neo (piel vascularizada) y pulmonar"),
        ("Circulatorio",  "Sangre fr\u00eda \u2014 2 aur\u00edculas + 1 ventr\u00edculo \u2014 eritrocitos el\u00edpticos con n\u00facleo \u2014 cerrado"),
        ("Digestivo",     "Unidireccional \u2014 cloaca (huevos tambi\u00e9n salen por aqu\u00ed)"),
        ("Excretor",      "Ri\u00f1ones \u2014 amoniaco o urea seg\u00fan especie"),
        ("Nervioso",      "Similar al de los peces"),
        ("Reproductor",   "Anuros: fecundaci\u00f3n externa \u2014 renacuajos (larvas con branquias) \u2192 metamorfosis / Apodos: fecundaci\u00f3n interna (cloaca) / Caudata: evitan etapa larvaria"),
    ], C["anfibia"]))
    add(table(
        ["Orden", "Nombre com\u00fan", "Caracter\u00edsticas"],
        [
            ["Gymnophiona (Apoda)", "Cecilias",                 "Sin patas \u2014 fecundaci\u00f3n interna"],
            ["Caudata",             "Salamandras \u2014 AJOLOTE MX", "Siempre con cola \u2014 evitan etapa larvaria"],
            ["Anura",               "Ranas y sapos",            "Sin cola de adultos \u2014 renacuajos \u2014 fecundaci\u00f3n externa"],
        ],
        C["anfibia"]
    ))

    return parts


def build_content_7():
    parts = []
    add = parts.append

    # 11. REPTILIA
    add(banner("CLASE REPTILIA", C["reptilia"]))
    add(info_card([
        ("Origen",        "Derivados de anfibios \u2014 adaptados a la vida completamente terrestre"),
        ("Tegumentario",  "Escamas \u2014 evitan p\u00e9rdida de l\u00edquidos"),
        ("Respiratorio",  "Pulmonados"),
        ("Circulatorio",  "Cerrado \u2014 3 c\u00e1maras \u2014 sangre fr\u00eda \u2014 eritrocitos el\u00edpticos con n\u00facleo"),
        ("Digestivo",     "Unidireccional \u2014 cloaca (orina como \u00e1cido \u00farico + heces + semen)"),
        ("Nervioso",      "Cerebro con arquicorteza \u2014 \u00f3rgano de Jacobson/vomeronasal (par craneal 0, detecta olores) \u2014 roseta loreal en serpientes (visi\u00f3n t\u00e9rmica)"),
        ("Excretor",      "Ri\u00f1ones \u2014 amoniaco, \u00e1cido \u00farico o urea"),
        ("Reproductor",   "Sexos separados \u2014 huevo amniota con cascar\u00f3n c\u00e1lcico \u2014 membranas: alb\u00famina (agua+prote\u00ednas), saco amni\u00f3tico (embri\u00f3n), saco vitelino (carbohidratos+l\u00edpidos), alantoides (intercambio gaseoso)"),
    ], C["reptilia"]))
    add(table(
        ["Subclase/Infraclase", "Ejemplos"],
        [
            ["Anapsida",            "Tortugas (quel\u00f3nidos) \u2014 \u00fanicas que quedan de este grupo"],
            ["Dyapsida",            "Todos los reptiles actuales excepto tortugas"],
            ["Archosauromorpha",    "Dinosaurios (extintos)"],
            ["Lepidosauria",        "Serpientes y lagartos"],
            ["Terapsida",           "Reptiles mam\u00edferos \u2014 ancestros de los mam\u00edferos"],
        ],
        C["reptilia"]
    ))

    # 12. AVES
    add(banner("CLASE AVES", C["aves"]))
    add(info_card([
        ("Origen",         "Derivadas de reptiles especializados en vuelo \u2014 Archaeopteryx: primer volador"),
        ("Tegumentario",   "Plumas (termorregulaci\u00f3n + vuelo) \u2014 cera en algunas sp. \u2014 gl\u00e1ndula urop\u00edgea"),
        ("Respiratorio",   "Sacos a\u00e9reos (menor peso + O\u2082 extra en espiraci\u00f3n) \u2014 huesos huecos conectados al SR \u2014 siringe (producci\u00f3n de sonidos)"),
        ("Digestivo",      "Buche (almacenar) \u2192 Molleja (moler) \u2192 Est\u00f3mago (digerir) \u2192 Intestinos \u2192 Cloaca \u2014 Bolsa de Fabricio (hematopoyesis)"),
        ("Circulatorio",   "4 c\u00e1maras \u2014 eritrocitos nucleares y el\u00edpticos \u2014 homeot\u00e9rmicas (40\u00b0-43\u00b0C) \u2014 algunas poiquilot\u00e9rmicas"),
        ("Excretor",       "Uricot\u00e9licas \u2014 \u00e1cido \u00farico \u2192 cloaca (junto con heces)"),
        ("Reproductor",    "Sexos separados \u2014 huevo amniota \u2014 1 trompa uterina + 1 ovario \u2014 LA HEMBRA determina el sexo"),
        ("Nervioso",       "Grande en relaci\u00f3n al cuerpo \u2014 hemisferios: comportamiento, orientaci\u00f3n, apareamiento, construcci\u00f3n del nido"),
    ], C["aves"]))
    add(extra("El halc\u00f3n peregrino alcanza 290 km/h en picada con 90 aleteos/segundo. El ave m\u00e1s grande: avestruz. La m\u00e1s peque\u00f1a: Mellisuga helenae (zunzuncito)."))

    return parts


def build_content_8():
    parts = []
    add = parts.append

    # 13. MAMMALIA
    add(banner("CLASE MAMMALIA", C["mammalia"]))
    add(info_card([
        ("Origen",         "Derivados de reptiles Ter\u00e1psidos \u2014 principios del Tri\u00e1sico (~200 Ma)"),
        ("Especies",       "~5,486 \u2014 5 monotremas, 272 marsupiales, 5,209 placentarios"),
        ("Sinapomorf\u00edas",  "PELO y GL\u00c1NDULAS MAMARIAS"),
        ("Tegumentario",   "Piel y pelaje \u2014 camuflaje, comunicaci\u00f3n, protecci\u00f3n, termorregulaci\u00f3n, excreci\u00f3n"),
        ("Respiratorio",   "Pulmonar"),
        ("Circulatorio",   "Endot\u00e9rmicos \u2014 cerrado \u2014 4 c\u00e1maras \u2014 eritrocitos bic\u00f3ncavos SIN n\u00facleo \u2014 FC: musara\u00f1a 1200 lpm / ballena azul 6 lpm"),
        ("Digestivo",      "Especializado + gl\u00e1ndulas complementarias \u2014 clasificados por dieta: carn\u00edvoros, herb\u00edvoros, insect\u00edvoros, omn\u00edvoros"),
        ("Excretor",       "Renal con nefronas + vejiga urinaria \u2014 forma UREA (excepto d\u00e1lmata: \u00e1cido \u00farico)"),
        ("Nervioso",       "Arquicorteza (hipocampo+l\u00edmbico) + Paleocorteza (olfatoria) = Alocorteza \u2014 Neocorteza: solo bien desarrollada en primates y H. sapiens (lenguaje, comprensi\u00f3n, emoci\u00f3n, memoria)"),
        ("Reproductor",    "Viv\u00edparos placentarios o marsupiales \u2014 excepto monotremas (huevo amniota) \u2014 gestaci\u00f3n: elefante 24 meses / zarig\u00fceya 12 d\u00edas"),
    ], C["mammalia"]))
    add(table(
        ["Subclase", "Caracter\u00edsticas", "Ejemplos"],
        [
            ["Prototheria (Monotremas)", "Nacen de huevo amniota \u2014 gl\u00e1ndulas mamarias que sudan la leche \u2014 espolones venenosos", "Ornitorrinco, Equidna"],
            ["Theria: Marsupialia",      "Viv\u00edparos \u2014 cr\u00eda nace prematura y completa desarrollo en marsupio (bolsa)",           "Canguro, koala, zarig\u00fceya"],
            ["Theria: Placentalia",      "Viv\u00edparos \u2014 desarrollo completo en \u00fatero con placenta",                                "La gran mayor\u00eda de los mam\u00edferos"],
        ],
        C["mammalia"]
    ))
    add(table(
        ["Orden (Placentalia)", "Caracter\u00edstica", "Ejemplos"],
        [
            ["Perissodactyla",  "Dedos impares",                 "Caballos, rinocerontes, tapires"],
            ["Artiodactyla",    "Dedos pares",                   "Vacas, cerdos, jirafas, camellos"],
            ["Sirenia",         "Mam\u00edferos acu\u00e1ticos herb\u00edvoros", "Manat\u00edes, dugongos"],
            ["Chiroptera",      "Vuelan con las manos",          "Murci\u00e9lagos"],
            ["Primates",        "Manos pr\u00e9nsiles, neocorteza desarrollada", "Monos, simios, humanos"],
            ["Lagomorpha",      "Incisivos grandes, herb\u00edvoros", "Conejos, liebres"],
            ["Proboscidea",     "Con trompa",                    "Elefantes"],
            ["Carnivora",       "Dientes carnasiales",           "Perros, gatos, osos, leones"],
            ["Rodentia",        "Roedores \u2014 capibara: el m\u00e1s grande", "Ratas, ardillas, capibara"],
            ["Cetacea",         "Mam\u00edferos acu\u00e1ticos",           "Ballenas, delfines"],
        ],
        C["mammalia"]
    ))

    return parts


def build_content_9():
    parts = []
    add = parts.append

    # TABLA COMPARATIVA VERTEBRADOS
    add('<div class="page-break"></div>')
    add(banner("TABLA COMPARATIVA \u2014 VERTEBRADOS", "#37474F"))
    add(table(
        ["Caracter\u00edstica", "Peces", "Anfibios", "Reptiles", "Aves", "Mam\u00edferos"],
        [
            ["Temperatura",   "Fr\u00eda",        "Fr\u00eda",        "Fr\u00eda",        "Caliente",     "Caliente"],
            ["Eritrocitos",   "El\u00edpticos+n\u00facleo","El\u00edpticos+n\u00facleo","El\u00edpticos+n\u00facleo","El\u00edpticos+n\u00facleo","Bic\u00f3ncavos sin n\u00facleo"],
            ["Coraz\u00f3n",       "1A + 1V",     "2A + 1V",     "3 c\u00e1maras",   "4 c\u00e1maras",    "4 c\u00e1maras"],
            ["Respiraci\u00f3n",   "Branquias",   "Piel+pulm\u00f3n", "Pulmones",    "Pulmones+sacos","Pulmones"],
            ["Tegumento",     "Escamas",     "Piel desnuda","Escamas",     "Plumas",       "Pelo"],
            ["Reproducci\u00f3n",  "Ext./Int.",   "Ext./Int.",   "Interna",     "Interna",      "Interna"],
            ["Huevo",         "Sin cascar\u00f3n","Sin cascar\u00f3n","Amniota c\u00e1lcico","Amniota c\u00e1lcico","Viv\u00edparos (mayor\u00eda)"],
            ["Excreci\u00f3n",     "Amoniaco",    "Amoniaco/Urea","\u00c1c.\u00farico/Urea","\u00c1c.\u00farico",   "Urea"],
            ["Cerebro",       "Arquicorteza","Similar peces","Arquicorteza","Muy desarrollado","Neocorteza (primates)"],
        ],
        "#37474F"
    ))

    return parts


def main():
    all_content = []
    all_content.extend(build_content())
    all_content.extend(build_content_2())
    all_content.extend(build_content_3())
    all_content.extend(build_content_4())
    all_content.extend(build_content_5())
    all_content.extend(build_content_6())
    all_content.extend(build_content_7())
    all_content.extend(build_content_8())
    all_content.extend(build_content_9())

    html = HTML_HEAD + CSS + "</style>\n</head>\n<body>\n"
    html += "\n".join(all_content)
    html += "\n</body>\n</html>"

    path = "/projects/sandbox/Reino-animal-final-/Reino_Animal_Apuntes.html"
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"HTML generado: {path}")
    print(f"Abrir en navegador y usar Ctrl+P para guardar como PDF")


if __name__ == "__main__":
    main()
