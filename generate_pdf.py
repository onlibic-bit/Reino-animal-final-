from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus.flowables import Flowable

# ── Color palette ──────────────────────────────────────────────────────────────
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
    "disease_bg":    "#FFE5E5",
    "disease_text":  "#CC0000",
    "extra_bg":      "#FFFDE7",
    "extra_text":    "#E65100",
    "card_bg":       "#F5F5F5",
    "card_border":   "#DDDDDD",
}

def hex2color(h):
    h = h.lstrip("#")
    return colors.Color(*[int(h[i:i+2],16)/255 for i in (0,2,4)])

W, H = A4


# ── Custom Flowables ───────────────────────────────────────────────────────────
class SectionBanner(Flowable):
    def __init__(self, title, subtitle="", color="#2E86AB", width=None):
        super().__init__()
        self.title    = title
        self.subtitle = subtitle
        self.color    = hex2color(color)
        self.width    = width or (W - 3*cm)
        self.height   = 1.15*cm if not subtitle else 1.5*cm

    def draw(self):
        c = self.canv
        r = 6
        c.setFillColor(self.color)
        c.roundRect(0, 0, self.width, self.height, r, fill=1, stroke=0)
        c.setFillColor(colors.white)
        if self.subtitle:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(14, self.height - 18, self.title)
            c.setFont("Helvetica", 8)
            c.drawString(16, 5, self.subtitle)
        else:
            c.setFont("Helvetica-Bold", 11)
            c.drawCentredString(self.width/2, (self.height-11)/2 + 2, self.title)

    def wrap(self, *args):
        return self.width, self.height


class InfoCard(Flowable):
    """Key-value card with colored left border."""
    def __init__(self, rows, border_color="#2E86AB", width=None):
        super().__init__()
        self.rows   = rows   # list of (label, value)
        self.border = hex2color(border_color)
        self.width  = width or (W - 3*cm)
        self.row_h  = 0.55*cm
        self.height = self.row_h * len(rows) + 8

    def draw(self):
        c = self.canv
        bg = hex2color(C["card_bg"])
        bd = hex2color(C["card_border"])
        c.setFillColor(bg)
        c.setStrokeColor(bd)
        c.roundRect(0, 0, self.width, self.height, 4, fill=1, stroke=1)
        # left accent
        c.setFillColor(self.border)
        c.roundRect(0, 0, 5, self.height, 4, fill=1, stroke=0)
        # rows
        for i, (label, val) in enumerate(reversed(self.rows)):
            y = i * self.row_h + 5
            c.setFillColor(colors.HexColor("#555555"))
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(12, y + 5, label.upper() + ":")
            c.setFillColor(colors.HexColor("#222222"))
            c.setFont("Helvetica", 8)
            c.drawString(12 + c.stringWidth(label.upper()+":", "Helvetica-Bold", 7.5) + 4, y + 5, val)

    def wrap(self, *args):
        return self.width, self.height



# ── Styles ─────────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    def S(name, parent="Normal", **kw):
        return ParagraphStyle(name, parent=base[parent], **kw)

    return {
        "title":    S("MyTitle",   "Title",   fontSize=28, textColor=colors.HexColor("#1A1A2E"),
                       spaceAfter=6, alignment=TA_CENTER, fontName="Helvetica-Bold"),
        "subtitle": S("MySub",     "Normal",  fontSize=13, textColor=colors.HexColor("#444444"),
                       spaceAfter=4, alignment=TA_CENTER),
        "body":     S("MyBody",    "Normal",  fontSize=8.5, leading=13, spaceAfter=3,
                       textColor=colors.HexColor("#222222")),
        "bullet":   S("MyBullet",  "Normal",  fontSize=8.5, leading=13, spaceAfter=2,
                       leftIndent=12, firstLineIndent=-8,
                       textColor=colors.HexColor("#222222")),
        "disease":  S("MyDis",     "Normal",  fontSize=8.5, leading=13, spaceAfter=2,
                       leftIndent=12, firstLineIndent=-8,
                       textColor=hex2color(C["disease_text"]),
                       backColor=hex2color(C["disease_bg"])),
        "extra":    S("MyExtra",   "Normal",  fontSize=8, leading=12, spaceAfter=3,
                       leftIndent=8, textColor=hex2color(C["extra_text"]),
                       backColor=hex2color(C["extra_bg"])),
        "h2":       S("MyH2",      "Heading2", fontSize=10, fontName="Helvetica-Bold",
                       textColor=colors.HexColor("#333333"), spaceBefore=8, spaceAfter=3),
        "caption":  S("MyCap",     "Normal",  fontSize=7.5, textColor=colors.HexColor("#666666"),
                       alignment=TA_CENTER),
    }


def bul(text, st):   return Paragraph(f"\u2022 {text}", st["bullet"])
def body(text, st):  return Paragraph(text, st["body"])
def dis(text, st):   return Paragraph(f"\U0001f534 {text}", st["disease"])
def h2(text, st):    return Paragraph(text, st["h2"])
def extra(text, st): return Paragraph(f"[EXTRA] {text}", st["extra"])
def sp(n=4):         return Spacer(1, n)
def banner(title, subtitle="", color="#2E86AB"):
    return SectionBanner(title, subtitle, color)

def comp_table(headers, rows, col_color="#2E86AB"):
    col_w = (W - 3*cm) / len(headers)
    data = [headers] + rows
    t = Table(data, colWidths=[col_w]*len(headers))
    hc = hex2color(col_color)
    t.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0),  hc),
        ("TEXTCOLOR",    (0,0), (-1,0),  colors.white),
        ("FONTNAME",     (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0,0), (-1,-1), 7.5),
        ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.white, colors.HexColor("#F9F9F9")]),
        ("GRID",         (0,0), (-1,-1), 0.4, colors.HexColor("#CCCCCC")),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING",   (0,0), (-1,-1), 4),
        ("BOTTOMPADDING",(0,0), (-1,-1), 4),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]))
    return t



# ══════════════════════════════════════════════════════════════════════════════
def build_story(st):
    S = []
    add = S.append

    # ── COVER ─────────────────────────────────────────────────────────────────
    add(Spacer(1, 3.5*cm))
    add(Paragraph("REINO ANIMAL", st["title"]))
    add(Spacer(1, 0.4*cm))
    add(Paragraph("Biologia \u00b7 Apuntes de clase", st["subtitle"]))
    add(Spacer(1, 0.6*cm))
    add(HRFlowable(width="80%", thickness=2, color=hex2color(C["chordata"]), spaceAfter=10))
    add(Paragraph("Phylum Cnidaria \u2192 Mammalia", st["subtitle"]))
    add(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # 1. PHYLUM CNIDARIA
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("PHYLUM CNIDARIA (Celentereos)", color=C["cnidaria"]))
    add(sp(6))
    add(InfoCard([
        ("Tambien llamados", "Celenterados (por tener cavidad)"),
        ("Ambiente",         "Exclusivamente acuaticos"),
        ("Organizacion",     "Diblasticos: Ectodermo + Mesoglea + Endodermo"),
        ("Formas",           "Polipo (sesil) o Medusa (nadadora)"),
        ("Digestivo",        "Cavidad gastrovascular - osculo de entrada y salida"),
        ("Epitelio interno", "Gastrodermis"),
        ("Circulatorio",     "NO TIENEN - usan sus celulas"),
        ("Respiratorio",     "NO TIENEN - difusion celular"),
        ("Reproductor",      "Sexual y asexual (gemacion) - hermafroditas"),
    ], border_color=C["cnidaria"]))
    add(sp(6))
    add(h2("Caracteristicas clave", st))
    add(bul("Distinguidos por sus <b>cnidocitos</b> (celulas urticantes)", st))
    add(bul("Cnidocitos poseen <b>nematocisto</b> (arpon) para atrapar presas o defenderse", st))
    add(bul("<b>Primeros animales en tener tejidos</b>", st))
    add(bul("<b>Primeros en tener sistema nervioso y muscular</b>", st))
    add(bul("Sistema nervioso: plexo nervioso bajo la dermis (neuronas simples)", st))
    add(bul("Sistema muscular: <b>mionemas</b> (celulas ricas en actina y miosina)", st))
    add(sp(6))
    add(h2("Clases del Phylum Cnidaria", st))
    add(comp_table(
        ["Clase", "Ejemplos", "Forma dominante", "Reproduccion asexual"],
        [
            ["Hydrozoa",  "Hidras, Obelia, Physalia", "Polipo (hidras) / ambas (Obelia)", "Gemacion"],
            ["Scyphozoa", "Aguamalas / aguavivas",    "Medusa",                            "Gemacion -> Efira"],
            ["Anthozoa",  "Corales, anemonas",         "Solo polipo",                       "Gemacion, division, fragmentacion"],
        ],
        col_color=C["cnidaria"]
    ))
    add(sp(4))
    add(body("<b>Efira:</b> etapa creciente de la medusa. <b>Planula:</b> larva que viaja y se incrusta para originar adulto.", st))
    add(sp(8))

    # ══════════════════════════════════════════════════════════════════════════
    # 2. PHYLUM CTENOPHORA
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("PHYLUM CTENOPHORA (Nueces de mar)", color=C["ctenophora"]))
    add(sp(6))
    add(InfoCard([
        ("Habitat",       "Planctonicos, marinos"),
        ("Caracteristica","Bioluminiscentes - hileras de cilios"),
        ("Digestivo",     "Cavidad gastrovascular (similar a medusas)"),
        ("Alimentacion",  "Tentaculos pegajosos"),
        ("Reproductor",   "Sexual hermafrodita - cigoto -> larva -> adulto"),
    ], border_color=C["ctenophora"]))
    add(sp(8))


    # ══════════════════════════════════════════════════════════════════════════
    # COMPARACION DE SIMETRIAS Y CLASIFICACION DE TRIBLASTICOS
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("COMPARACION DE SIMETRIAS Y TRIBLASTICOS", color="#607D8B"))
    add(sp(6))
    add(bul("Cnidarios y Ctenoforos: <b>simetria radial</b>", st))
    add(bul("De aqui en adelante: <b>simetria bilateral</b> (mayor movilidad y complejidad)", st))
    add(bul("Excepcion: <b>Equinodermos</b> - larvaria bilateral -> adulto radial", st))
    add(bul("Todos los bilaterales son <b>triblasticos</b> (ectodermo, mesodermo, endodermo)", st))
    add(sp(6))
    add(comp_table(
        ["Tipo", "Cavidad", "Ejemplos"],
        [
            ["Acelomados",      "Sin celoma (mesodermo solido)",       "Platelmintos, Nemertinos"],
            ["Pseudocelomados", "Pseudoceloma (no revestido del todo)", "Nematodos"],
            ["Celomados",       "Celoma verdadero (en mesodermo)",      "Anelidos, Moluscos, Artropodos, Cordados"],
        ],
        col_color="#607D8B"
    ))
    add(sp(8))

    # ══════════════════════════════════════════════════════════════════════════
    # 3. PHYLUM PLATYHELMINTHES
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("PHYLUM PLATYHELMINTHES (Gusanos planos)", color=C["platy"]))
    add(sp(6))
    add(InfoCard([
        ("Organizacion",  "Acelomados triblasticos - invertebrados"),
        ("Habitat",       "Acuaticos o parasitos de vertebrados"),
        ("Digestivo",     "Algunos por piel / otros con faringe (sin ano)"),
        ("Respiratorio",  "NO TIENEN - difusion celular"),
        ("Circulatorio",  "NO TIENEN - difusion celular"),
        ("Nervioso",      "Ganglios, axones e interneuronas - centralizacion"),
        ("Muscular",      "Mionemas o movimientos peristalticos"),
        ("Excretor",      "Protonefridios (celula flama) - secretan amoniaco"),
        ("Reproductor",   "Hermafroditas - fecundacion interna - fragmentacion en algunas sp."),
    ], border_color=C["platy"]))
    add(sp(6))

    add(h2("Clase Turbellaria (Planarias)", st))
    add(bul("<b>Primera vez sistema renal</b> (protonefridios / celula flama)", st))
    add(bul("Carnivoras - desplazamiento por cilios - hermafroditas", st))
    add(sp(5))

    add(h2("Clase Trematoda (Duelas)", st))
    add(bul("Parasitos de vertebrados", st))
    add(bul("Capa externa resistente a jugos gastricos del huesped", st))
    add(dis("Fasciola hepatica - parasito del humano por consumo de berros o caracoles", st))
    add(sp(5))

    add(h2("Clase Cestoda (Tenias / Solitarias)", st))
    add(bul("Sin tubo digestivo - hermafroditas - capa externa resistente a jugos gastricos", st))
    add(bul("Transmision: quiste o huevo. Fijacion: ganchos y ventosas en mucosa intestinal", st))
    add(bul("Formas: gusano (adulto), cisticerco y huevo", st))
    add(bul("Proglotidos: inmaduros (cerca del escolex) -> maduros (medio) -> gravidos (final). Todo el cuerpo = <b>estrobilo</b>", st))
    add(bul("<b>T. saginata</b> (res) - <b>T. solium</b> (puerco, tiene ganchos)", st))
    add(dis("Cisticercosis - solo por ingerir HUEVO de T. solium -> va a tejidos, musculo, cerebro", st))
    add(dis("Teniasis - por ingerir cisticercos (carne mal cocida)", st))
    add(dis("Sindrome de mala absorcion", st))
    add(sp(5))


    add(h2("Phylum Rhynchocoela (Nemertinos / Gusano cinta)", st))
    add(bul("Acelomados marinos", st))
    add(bul("<b>Primeros en tener sistema circulatorio cerrado</b> - 2 vasos laterales + 1 dorsal (sangre incolora)", st))
    add(bul("Tubo digestivo con boca y ano - poseen proboscide", st))
    add(sp(5))

    add(h2("Phylum Gnathostomulida (Gusanos mandibulados)", st))
    add(bul("Acelomado marino y diminuto - vive en arena y lodo de costas litorales", st))
    add(bul("Poseen mandibulas duras (gnathos = mandibula, stomos = boca)", st))
    add(sp(8))

    # ══════════════════════════════════════════════════════════════════════════
    # 4. PHYLUM NEMATODA
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("PHYLUM NEMATODA (Nemathelmintos - Pseudocelomados)", color=C["nematoda"]))
    add(sp(6))
    add(InfoCard([
        ("Organizacion",  "Pseudocelomados - gusanos cilindricos (hilo/filamento)"),
        ("Pseudoceloma",  "Tubo sellado que incrementa efectividad de contracciones musculares"),
        ("Digestivo",     "Unidireccional - faringe + boca con estiletes + ano"),
        ("Respiratorio",  "NO TIENEN - todo por piel"),
        ("Circulatorio",  "NO TIENEN - tamano pequeno"),
        ("Nervioso",      "Ganglios y somas"),
        ("Excretor",      "Secretan NH4 (amoniaco)"),
        ("Reproductor",   "Solo fecundacion sexual"),
        ("Transmision",   "Ciclo ano-boca (ingesta de huevos)"),
    ], border_color=C["nematoda"]))
    add(sp(6))
    add(h2("Parasitos importantes", st))
    add(dis("Enterobius vermicularis - forma infectante: huevo (ciclo ano-boca)", st))
    add(dis("Ascaris lumbricoides - principal parasitosis de Mexico - solo etapa larvaria, huevos con mameloides", st))
    add(dis("Filarias / Ancylostoma / Necator / Strongyloides - penetran por piel en lugares humedos -> via linfatica -> corazon. Produce sabanon en punto de entrada", st))
    add(dis("Trichinella trichiura - sin huevo, se reproducen en larvas - atraviesan mucosas -> musculo (carne porcina)", st))
    add(sp(8))

    # ══════════════════════════════════════════════════════════════════════════
    # 5. PHYLUM ANNELIDA
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("PHYLUM ANNELIDA (Gusanos anillados)", color=C["annelida"]))
    add(sp(6))
    add(InfoCard([
        ("Organizacion",  "Celomados protostomos - segmentados (metameros)"),
        ("Habitat",       "Tierra y agua dulce/salada"),
        ("Digestivo",     "Tubular con boca y ano"),
        ("Circulatorio",  "CERRADO - lombriz: 5 corazones en anillo, sin eritrocitos, solo plasma"),
        ("Respiratorio",  "Por epidermis"),
        ("Nervioso",      "Centralizado - receptores tactiles, gustativos, fotorreceptores"),
        ("Excretor",      "Metanefridios en hileras a lo largo del cuerpo"),
        ("Reproductor",   "Hermafroditas - sin fragmentacion"),
        ("Muscular",      "Circular + longitudinal (circular hace avanzar)"),
    ], border_color=C["annelida"]))
    add(sp(5))
    add(body("<b>Primera vez que hay corazon en animales!</b>", st))
    add(sp(6))
    add(comp_table(
        ["Clase", "Habitat", "Caracteristicas clave"],
        [
            ["Oligoqueta", "Terrestre",        "Amoniotelicos - hacen tuneles - clitelo en apareamiento - partenogenesis posible"],
            ["Poliqueta",  "Marina",           "Tentaculos y antenas - parapodios (locomocion + respiracion) - tagmosis - larva trocofora"],
            ["Hirudinea",  "Dulce/pantanosa",  "Sanguijuelas - 2 ventosas - enzima hirudinea (anticoagulante) - tratamiento de aterosclerosis"],
        ],
        col_color=C["annelida"]
    ))
    add(sp(8))


    # ══════════════════════════════════════════════════════════════════════════
    # 6. PHYLUM MOLLUSCA
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("PHYLUM MOLLUSCA", color=C["mollusca"]))
    add(sp(6))
    add(InfoCard([
        ("Etimologia",    "Mollus = blando - ~100,000 especies - fosiles desde el Cambrico"),
        ("Organizacion",  "Celomados protostomos triblasticos"),
        ("Cuerpo",        "Cefalopie + masa visceral + manto"),
        ("Cavidad paleal","Entre manto y masa visceral - desechos digestivos, urinarios, reproductores y respiracion"),
        ("Digestivo",     "Radula (dientes) excepto bivalvos. Cefalopodos tambien tienen pico de perico"),
        ("Circulatorio",  "Abierto (hemoceloma) EXCEPTO cefalopodos (cerrado) - corazon 3 camaras"),
        ("Sangre",        "Hemolinfa - bivalvos incolora - gasteropodos/cefalopodos AZUL-VERDOSA (hemocianina con cobre)"),
        ("Excretor",      "Metanefridios -> cavidad paleal"),
        ("Reproductor",   "Sexual - bivalvos fecundacion externa / cefalopodos: sexos sep. / gasteropodos: hermafroditas"),
    ], border_color=C["mollusca"]))
    add(sp(6))
    add(comp_table(
        ["Clase", "Ejemplos", "Caracteristicas especiales"],
        [
            ["Bivalva (Lamelibranquios)", "Mejillones, ostiones, almejas, vieiras", "Sin radula - musculos aductores - alimentacion por filtracion - vieiras: >100 ojos - estatocistos"],
            ["Gastropoda",               "Caracoles, babosas",                       "Unico animal asimetrico del reino - quimiorreceptores - ojos detectan luz - SN: 6 ganglios"],
            ["Cephalopoda",              "Pulpos (8), calamares (10), jibias (10), nautilos (90)", "3 corazones - SN cerrado - cerebro con ganglios - ojos especializados - defensa: tinta, camuflaje, mimetismo - PRIMER CEREBRO PROPIAMENTE DICHO"],
        ],
        col_color=C["mollusca"]
    ))
    add(sp(8))

    # ══════════════════════════════════════════════════════════════════════════
    # 7. PHYLUM ARTHROPODA
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("PHYLUM ARTHROPODA", color=C["arthropoda"]))
    add(sp(6))
    add(InfoCard([
        ("Organizacion",   "Celomados protostomos esquizocelomicos"),
        ("Clasificacion",  "Por apendices, segmentacion, exoesqueleto y organos sensoriales"),
        ("Exoesqueleto",   "Quitina (todos) - crustaceos: quitina + calcio"),
        ("Muda",           "Apolisis (apoptosis para soltar exoesqueleto) -> Ecdisis (salida) -> Esclerotizacion"),
        ("Circulatorio",   "Abierto - hemolinfa (azul, verde o incolora) - corazon tubular dorsal de 1 camara - hemocitos"),
        ("Digestivo",      "Unidireccional - estomodeo + mesenteron + proctodeo - cuticula quitinizada"),
        ("Excretor",       "Tubulos de Malpighi (rinones) - cristales de acido urico o guanina con heces"),
        ("Respiratorio",   "Traqueas ramificadas con espiraculos - aracnidos: filobranquias/filotraqueas"),
        ("Nervioso",       "3 pares de ganglios dorsales fusionados en cabeza - tagmosis: puede moverse sin cabeza"),
        ("Reproductor",    "Sexos separados - metamorfosis: ametabolismo / hemimetabolismo / holometabolismo"),
    ], border_color=C["arthropoda"]))
    add(sp(6))


    add(h2("Comparacion de clases principales", st))
    add(comp_table(
        ["Caracteristica",  "Insecta",          "Crustacea",             "Arachnida"],
        [
            ["Vuelan?",         "Mayoria si",        "NO",                    "NO"],
            ["Antenas",         "1 par (2)",         "2 pares (4)",           "Ninguna"],
            ["Patas",           "3 pares (6)",       "5 pares (10)",          "4 pares (8)"],
            ["Segmentacion",    "Cabeza+Torax+Abd.", "Cabeza+Torax+Abd.",     "Cefalotorax+Abd."],
            ["Exoesqueleto",    "Solo quitina",      "Quitina + calcio",      "Solo quitina"],
            ["Habitat",         "Terrestre/aereo",   "Acuatico",              "Terrestre"],
            ["Apendice bucal",  "Mandibulas",        "Mandibulas",            "Queliceros (colmillos)"],
        ],
        col_color=C["arthropoda"]
    ))
    add(sp(6))

    add(h2("Quelicerados", st))
    add(bul("Incluye: Merostomata (cangrejo cacerola/limulos), Pycnogonida (aranas de mar), Arachnida", st))
    add(bul("Sin antenas ni mandibulas - 1er apendice: queliceros (pinzas/colmillos) - 2do: pedipalpos", st))
    add(bul("Solo escorpiones tienen abdomen segmentado - excepto acaros: todos carnivoros", st))
    add(bul("Merostomata: su sangre se usa para detectar contaminacion bacteriana en medicamentos", st))
    add(sp(4))
    add(dis("Latrodectus mactans - Arana viuda negra (SLP)", st))
    add(dis("Loxosceles laeta - Arana violinista venenosa", st))
    add(dis("Enfermedad de Lyme - Borrelia burgdorferi (garrapata)", st))
    add(dis("Fiebre de las Montanas Rocosas - Rickettsia (garrapata)", st))
    add(dis("Babesiosis - Babesia bigemina (garrapata)", st))
    add(sp(6))

    add(h2("Metamorfosis en insectos", st))
    add(comp_table(
        ["Tipo", "Nombre", "Etapas"],
        [
            ["Sin metamorfosis",      "Ametabolismo",    "Huevo -> Ninfa -> Adulto (cambios minimos)"],
            ["Metamorfosis incompleta","Hemimetabolismo", "Huevo -> Ninfas sucesivas -> Adulto"],
            ["Metamorfosis completa",  "Holometabolismo", "Huevo -> Larva -> Pupa/Crisalida (capullo) -> Adulto"],
        ],
        col_color=C["arthropoda"]
    ))
    add(sp(4))
    add(body("<b>Ordenes de insectos:</b> Aptera (piojos, pulgas) - Odonata (libelulas) - Blattodea (cucarachas) - Isoptera (termitas) - Orthoptera (saltamontes, grillos) - Diptera (moscas, mosquitos) - Lepidoptera (mariposas, polillas) - Hymenoptera (abejas, avispas, hormigas) - Coleoptera (escarabajos, luciernagas)", st))
    add(sp(4))
    add(h2("Subclase Myriapoda", st))
    add(bul("Quilopodos (100 pies) y Diplopodos (1000 pies, herbivoros) - 1 par de antenas - excrecion por tubulos de Malpighi", st))
    add(sp(8))


    # ══════════════════════════════════════════════════════════════════════════
    # 8. DEUTEROSTOMOS
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("DEUTEROSTOMOS - Generalidades", color=C["deutero"]))
    add(sp(6))
    add(InfoCard([
        ("Incluye",       "Equinodermos, Hemicordados, Precordados, Cordados"),
        ("Desarrollo",    "Primero se forma el ANO, despues la boca"),
        ("Celoma",        "Enterocelomico (invaginaciones del endodermo)"),
        ("Simetria",      "Bilateral - excepcion: equinodermos adultos (radial)"),
        ("Reproduccion",  "Predomina la asexual"),
    ], border_color=C["deutero"]))
    add(sp(6))

    add(h2("Equinodermos - Grupo Ambulacraria", st))
    add(bul("Se mueven mediante <b>pies ambulacrales hidraulicos</b> - sin sangre - agua de mar por placa cribosa (madreporica)", st))
    add(bul("Digestivo: <b>unicos que sacan su estomago fuera del cuerpo</b> para digerir la presa", st))
    add(bul("Reproductor: sexos separados, fecundacion externa - asexual por fragmentacion", st))
    add(bul("Nervioso: anillo nervioso central del que parten ramas a cada brazo", st))
    add(sp(4))
    add(comp_table(
        ["Clase", "Ejemplos"],
        [
            ["Asteroidea",   "Estrellas de mar"],
            ["Echinoidea",   "Erizos de mar"],
            ["Crinoidea",    "Lirios de mar"],
            ["Holothuroidea","Pepinos de mar"],
        ],
        col_color=C["deutero"]
    ))
    add(sp(6))

    add(h2("Phylum Hemicordata (Gusanos bellota)", st))
    add(bul("Aspecto de gusano - sistema nervioso central - <b>sin notocorda ni esqueleto</b>", st))
    add(bul("Clases: Pterobranchia y Enteropneusta", st))
    add(sp(6))

    add(banner("PRECORDADOS", color=C["hemicorda"]))
    add(sp(6))
    add(bul("<b>Notocorda:</b> cordon cartilaginoso delante de la medula - soporte y proteccion del SN - en vertebrados se convierte en columna vertebral", st))
    add(sp(4))
    add(comp_table(
        ["Subphylum", "Nombre comun", "Datos clave"],
        [
            ["Quetognata",    "Gusanos flecha",       "Planctonicos marinos"],
            ["Cephalocordata","Lancetas / Anfioxos",   "Parecidos a peces sin aletas - PRIMEROS en tener notocorda - viven enterrados en arena - respiran/comen por filtracion de agua - el agua sale por el atrioporo"],
            ["Urochordata",   "Tunicados / Papas de mar","Larva: SN + notocorda - adulto: involuciona a 1 ganglio cerebral - fisiologia similar a cefalocordados"],
        ],
        col_color=C["hemicorda"]
    ))
    add(sp(8))


    # ══════════════════════════════════════════════════════════════════════════
    # 9. SUBPHYLUM CHORDATA - PECES
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("SUBPHYLUM CHORDATA - PECES (Superclase Gnatostomata)", color=C["chordata"]))
    add(sp(6))
    add(InfoCard([
        ("Agnathos",      "Peces sin mandibula - boca en ventosa - notocorda NO reemplazada (Mixines, Lampreas)"),
        ("Circulatorio",  "Cerrado - 1 auricula + 1 ventriculo - eritrocitos elipticos con nucleo"),
        ("Tegumentario",  "Escamas (reducen friccion del agua)"),
        ("Respiratorio",  "Branquias (hendiduras faringeas) - oxigeno captado por mucosa branquial"),
        ("Digestivo",     "Unidireccional - cloaca posterior (mezcla orina + heces)"),
        ("Nervioso",      "PRIMER CEREBRO - arquicorteza + medula espinal protegidas por sistema oseo"),
        ("Reproductor",   "Sexos separados - fecundacion externa mayoritaria - tiburones/rayas: interna - pterigopodos (organos copuladores en tiburones)"),
    ], border_color=C["chordata"]))
    add(sp(6))
    add(comp_table(
        ["Clase", "Esqueleto", "Ejemplos"],
        [
            ["Placodermi",  "Placas oseas (EXTINTOS)",       "-"],
            ["Condrictia",  "Cartilaginoso",                  "Tiburones, rayas, pez torpedo (20V, usado en Grecia para dolor)"],
            ["Osteictia",   "Oseo calcificado",               "Acrinopterigios (aletas con rayos, agua dulce/salada) - Sarcopterigios (peces pulmonares, aletas carnosas - Celacanto fosil viviente)"],
        ],
        col_color=C["chordata"]
    ))
    add(sp(8))

    # ══════════════════════════════════════════════════════════════════════════
    # 10. SUPERCLASE TETRAPODA - ANFIBIOS
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("SUPERCLASE TETRAPODA - CLASE ANFIBIA", color=C["anfibia"]))
    add(sp(6))
    add(InfoCard([
        ("Origen",        "Derivados de los Sarcopterigios"),
        ("Tegumentario",  "Piel sin escamas - tambien respiran por piel - queratina delgada - susceptibles a desecacion - algunas sp. liberan sustancias toxicas"),
        ("Respiratorio",  "Cutaneo (piel vascularizada) y pulmonar"),
        ("Circulatorio",  "Sangre fria - 2 auriculas + 1 ventriculo - eritrocitos elipticos con nucleo - cerrado"),
        ("Digestivo",     "Unidireccional - cloaca (huevos tambien salen por aqui)"),
        ("Excretor",      "Rinones - amoniaco o urea segun especie"),
        ("Nervioso",      "Similar al de los peces"),
        ("Reproductor",   "Anuros: fecundacion externa - renacuajos (larvas con branquias) -> metamorfosis / Apodos: fecundacion interna (cloaca) / Caudata: evitan etapa larvaria"),
    ], border_color=C["anfibia"]))
    add(sp(6))
    add(comp_table(
        ["Orden", "Nombre comun", "Caracteristicas"],
        [
            ["Gymnophiona (Apoda)", "Cecilias",                 "Sin patas - fecundacion interna"],
            ["Caudata",             "Salamandras - AJOLOTE MX", "Siempre con cola - evitan etapa larvaria"],
            ["Anura",               "Ranas y sapos",            "Sin cola de adultos - renacuajos - fecundacion externa"],
        ],
        col_color=C["anfibia"]
    ))
    add(sp(8))


    # ══════════════════════════════════════════════════════════════════════════
    # 11. CLASE REPTILIA
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("CLASE REPTILIA", color=C["reptilia"]))
    add(sp(6))
    add(InfoCard([
        ("Origen",        "Derivados de anfibios - adaptados a la vida completamente terrestre"),
        ("Tegumentario",  "Escamas - evitan perdida de liquidos"),
        ("Respiratorio",  "Pulmonados"),
        ("Circulatorio",  "Cerrado - 3 camaras - sangre fria - eritrocitos elipticos con nucleo"),
        ("Digestivo",     "Unidireccional - cloaca (orina como acido urico + heces + semen)"),
        ("Nervioso",      "Cerebro con arquicorteza - organo de Jacobson/vomeronasal (par craneal 0, detecta olores) - roseta loreal en serpientes (vision termica)"),
        ("Excretor",      "Rinones - amoniaco, acido urico o urea"),
        ("Reproductor",   "Sexos separados - huevo amniota con cascaron calcico - membranas: albumina (agua+proteinas), saco amniotico (embrion), saco vitelino (carbohidratos+lipidos), alantoides (intercambio gaseoso)"),
    ], border_color=C["reptilia"]))
    add(sp(6))
    add(comp_table(
        ["Subclase/Infraclase", "Ejemplos"],
        [
            ["Anapsida",            "Tortugas (quelonidos) - unicas que quedan de este grupo"],
            ["Dyapsida",            "Todos los reptiles actuales excepto tortugas"],
            ["Archosauromorpha",    "Dinosaurios (extintos)"],
            ["Lepidosauria",        "Serpientes y lagartos"],
            ["Terapsida",           "Reptiles mamiferos - ancestros de los mamiferos"],
        ],
        col_color=C["reptilia"]
    ))
    add(sp(8))

    # ══════════════════════════════════════════════════════════════════════════
    # 12. CLASE AVES
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("CLASE AVES", color=C["aves"]))
    add(sp(6))
    add(InfoCard([
        ("Origen",         "Derivadas de reptiles especializados en vuelo - Archaeopteryx: primer volador"),
        ("Tegumentario",   "Plumas (termorregulacion + vuelo) - cera en algunas sp. - glandula uropigea"),
        ("Respiratorio",   "Sacos aereos (menor peso + O2 extra en espiracion) - huesos huecos conectados al SR - siringe (produccion de sonidos)"),
        ("Digestivo",      "Buche (almacenar) -> Molleja (moler) -> Estomago (digerir) -> Intestinos -> Cloaca - Bolsa de Fabricio (hematopoyesis)"),
        ("Circulatorio",   "4 camaras - eritrocitos nucleares y elipticos - homeotermas (40-43C) - algunas poiquilotermas"),
        ("Excretor",       "Uricotelicas - acido urico -> cloaca (junto con heces)"),
        ("Reproductor",    "Sexos separados - huevo amniota - 1 trompa uterina + 1 ovario - LA HEMBRA determina el sexo"),
        ("Nervioso",       "Grande en relacion al cuerpo - hemisferios: comportamiento, orientacion, apareamiento, construccion del nido"),
    ], border_color=C["aves"]))
    add(sp(4))
    add(extra("El halcon peregrino alcanza 290 km/h en picada con 90 aleteos/segundo. El ave mas grande: avestruz. La mas pequena: Mellisuga helenae (zunzuncito).", st))
    add(sp(8))


    # ══════════════════════════════════════════════════════════════════════════
    # 13. CLASE MAMMALIA
    # ══════════════════════════════════════════════════════════════════════════
    add(banner("CLASE MAMMALIA", color=C["mammalia"]))
    add(sp(6))
    add(InfoCard([
        ("Origen",         "Derivados de reptiles Terapsidos - principios del Triasico (~200 Ma)"),
        ("Especies",       "~5,486 - 5 monotremas, 272 marsupiales, 5,209 placentarios"),
        ("Sinapomorfias",  "PELO y GLANDULAS MAMARIAS"),
        ("Tegumentario",   "Piel y pelaje - camuflaje, comunicacion, proteccion, termorregulacion, excrecion"),
        ("Respiratorio",   "Pulmonar"),
        ("Circulatorio",   "Endotermicos - cerrado - 4 camaras - eritrocitos biconcavos SIN nucleo - FC: musarana 1200 lpm / ballena azul 6 lpm"),
        ("Digestivo",      "Especializado + glandulas complementarias - clasificados por dieta: carnivoros, herbivoros, insectivoros, omnivoros"),
        ("Excretor",       "Renal con nefronas + vejiga urinaria - forma UREA (excepto dalmata: acido urico)"),
        ("Nervioso",       "Arquicorteza (hipocampo+limbico) + Paleocorteza (olfatoria) = Alocorteza - Neocorteza: solo bien desarrollada en primates y H. sapiens (lenguaje, comprension, emocion, memoria)"),
        ("Reproductor",    "Viviparos placentarios o marsupiales - excepto monotremas (huevo amniota) - gestacion: elefante 24 meses / zarigueva 12 dias"),
    ], border_color=C["mammalia"]))
    add(sp(6))
    add(comp_table(
        ["Subclase", "Caracteristicas", "Ejemplos"],
        [
            ["Prototheria (Monotremas)", "Nacen de huevo amniota - glandulas mamarias que sudan la leche - espolones venenosos", "Ornitorrinco, Equidna"],
            ["Theria: Marsupialia",      "Viviparos - cria nace prematura y completa desarrollo en marsupio (bolsa)",           "Canguro, koala, zarigueva"],
            ["Theria: Placentalia",      "Viviparos - desarrollo completo en utero con placenta",                                "La gran mayoria de los mamiferos"],
        ],
        col_color=C["mammalia"]
    ))
    add(sp(6))
    add(comp_table(
        ["Orden (Placentalia)", "Caracteristica", "Ejemplos"],
        [
            ["Perissodactyla",  "Dedos impares",                 "Caballos, rinocerontes, tapires"],
            ["Artiodactyla",    "Dedos pares",                   "Vacas, cerdos, jirafas, camellos"],
            ["Sirenia",         "Mamiferos acuaticos herbivoros", "Manaties, dugongos"],
            ["Chiroptera",      "Vuelan con las manos",          "Murcielagos"],
            ["Primates",        "Manos prensiles, neocorteza desarrollada", "Monos, simios, humanos"],
            ["Lagomorpha",      "Incisivos grandes, herbivoros", "Conejos, liebres"],
            ["Proboscidea",     "Con trompa",                    "Elefantes"],
            ["Carnivora",       "Dientes carnasiales",           "Perros, gatos, osos, leones"],
            ["Rodentia",        "Roedores - capibara: el mas grande", "Ratas, ardillas, capibara"],
            ["Cetacea",         "Mamiferos acuaticos",           "Ballenas, delfines"],
        ],
        col_color=C["mammalia"]
    ))
    add(sp(6))


    # ── Tabla comparativa final de VERTEBRADOS ────────────────────────────────
    add(PageBreak())
    add(banner("TABLA COMPARATIVA - VERTEBRADOS", color="#37474F"))
    add(sp(6))
    add(comp_table(
        ["Caracteristica", "Peces", "Anfibios", "Reptiles", "Aves", "Mamiferos"],
        [
            ["Temperatura",   "Fria",        "Fria",        "Fria",        "Caliente",     "Caliente"],
            ["Eritrocitos",   "Elipticos+nucleo","Elipticos+nucleo","Elipticos+nucleo","Elipticos+nucleo","Biconcavos sin nucleo"],
            ["Corazon",       "1A + 1V",     "2A + 1V",     "3 camaras",   "4 camaras",    "4 camaras"],
            ["Respiracion",   "Branquias",   "Piel+pulmon", "Pulmones",    "Pulmones+sacos","Pulmones"],
            ["Tegumento",     "Escamas",     "Piel desnuda","Escamas",     "Plumas",       "Pelo"],
            ["Reproduccion",  "Ext./Int.",   "Ext./Int.",   "Interna",     "Interna",      "Interna"],
            ["Huevo",         "Sin cascaron","Sin cascaron","Amniota calcico","Amniota calcico","Viviparos (mayoria)"],
            ["Excrecion",     "Amoniaco",    "Amoniaco/Urea","Ac.urico/Urea","Ac.urico",   "Urea"],
            ["Cerebro",       "Arquicorteza","Similar peces","Arquicorteza","Muy desarrollado","Neocorteza (primates)"],
        ],
        col_color="#37474F"
    ))

    return S


# ══════════════════════════════════════════════════════════════════════════════
def main():
    path = "/projects/sandbox/Reino-animal-final-/Reino_Animal_Apuntes.pdf"
    doc = SimpleDocTemplate(
        path, pagesize=A4,
        leftMargin=1.5*cm, rightMargin=1.5*cm,
        topMargin=1.5*cm,  bottomMargin=1.5*cm,
    )
    st = build_styles()
    story = build_story(st)
    doc.build(story)
    print(f"PDF generado: {path}")

if __name__ == "__main__":
    main()
