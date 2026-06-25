#!/usr/bin/env python3
"""Generates Reino_Animal_Apuntes.pdf using only Python standard library."""
import struct, zlib, os

class PDF:
    def __init__(self):
        self.objects = []
        self.pages = []
        self.current_stream = ""
        self.font_name = "Helvetica"
        self.font_size = 11
        self.y = 800
        self.page_w, self.page_h = 595.28, 841.89
        self.margin = 50
        self.max_y = self.page_h - 50
        self.min_y = 50

    def _add_obj(self, content):
        self.objects.append(content)
        return len(self.objects)

    def _enc(self, s):
        out = []
        for ch in s:
            code = ord(ch)
            if code < 256:
                out.append(ch if code >= 32 and ch not in '()\\' else f'\\{oct(code)[2:].zfill(3)}')
            else:
                out.append('?')
        return ''.join(out)

    def new_page(self):
        if self.current_stream:
            self._finish_page()
        self.current_stream = ""
        self.y = self.max_y

    def _finish_page(self):
        stream = self.current_stream.encode('latin-1', errors='replace')
        length = len(stream)
        obj_id = self._add_obj(f"<< /Length {length} >>\nstream\n".encode('latin-1') + stream + b"\nendstream")
        self.pages.append(obj_id)

    def set_font(self, bold=False, size=11):
        self.font_name = "Helvetica-Bold" if bold else "Helvetica"
        self.font_size = size
        fn = "/F2" if bold else "/F1"
        self.current_stream += f"BT {fn} {size} Tf ET\n"

    def set_color(self, r, g, b):
        self.current_stream += f"{r:.2f} {g:.2f} {b:.2f} rg {r:.2f} {g:.2f} {b:.2f} RG\n"

    def rect(self, x, y, w, h):
        self.current_stream += f"{x:.1f} {y:.1f} {w:.1f} {h:.1f} re f\n"

    def text(self, x, y, s):
        safe = self._enc(s)
        self.current_stream += f"BT /F1 {self.font_size} Tf {x:.1f} {y:.1f} Td ({safe}) Tj ET\n"

    def text_bold(self, x, y, s):
        safe = self._enc(s)
        self.current_stream += f"BT /F2 {self.font_size} Tf {x:.1f} {y:.1f} Td ({safe}) Tj ET\n"

    def _check_page(self, needed=20):
        if self.y - needed < self.min_y:
            self.new_page()

    def banner(self, title, color=(0.2, 0.4, 0.7)):
        self._check_page(30)
        self.y -= 25
        self.set_color(*color)
        self.rect(self.margin, self.y - 5, self.page_w - 2*self.margin, 20)
        self.set_color(1, 1, 1)
        self.text_bold(self.margin + 8, self.y, title)
        self.set_color(0, 0, 0)
        self.y -= 20

    def line(self, s, indent=0):
        self._check_page(15)
        self.y -= 14
        self.text(self.margin + indent, self.y, s)

    def bullet(self, s):
        self.line(f"- {s}", indent=10)

    def alert(self, s):
        self.line(f"[!] {s}", indent=10)

    def spacer(self, h=10):
        self.y -= h

    def build(self):
        if self.current_stream:
            self._finish_page()
        # Build PDF structure
        out = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"
        offsets = []
        obj_num = 1
        # Catalog=1, Pages=2, Font1=3, Font2=4, then page objects, then stream objects
        n_pages = len(self.pages)
        # Pre-calculate object IDs
        # 1=catalog, 2=pages, 3=font1, 4=font2, page_objs=5..5+n-1, stream already stored
        # Rebuild: objects list has stream contents, we need page+stream pairs
        # Simpler: write everything sequentially
        all_objs = []
        # obj1: catalog
        all_objs.append("<< /Type /Catalog /Pages 2 0 R >>")
        # obj2: pages - page obj IDs start at 5
        page_obj_ids = list(range(5, 5 + n_pages))
        kids = " ".join(f"{p} 0 R" for p in page_obj_ids)
        all_objs.append(f"<< /Type /Pages /Kids [{kids}] /Count {n_pages} >>")
        # obj3: Font Helvetica
        all_objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
        # obj4: Font Helvetica-Bold
        all_objs.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
        # page objects (each references its stream)
        stream_start = 5 + n_pages
        for i in range(n_pages):
            sid = stream_start + i
            pg = (f"<< /Type /Page /Parent 2 0 R "
                  f"/MediaBox [0 0 {self.page_w} {self.page_h}] "
                  f"/Contents {sid} 0 R "
                  f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> >>")
            all_objs.append(pg)
        # stream objects
        for i, stream_obj_id in enumerate(self.pages):
            all_objs.append(self.objects[stream_obj_id - 1])  # raw bytes handled below

        # Now write
        out = b"%PDF-1.4\n"
        offsets = []
        for idx, obj in enumerate(all_objs):
            offsets.append(len(out))
            num = idx + 1
            if isinstance(obj, bytes):
                out += f"{num} 0 obj\n".encode() + obj + b"\nendobj\n"
            else:
                out += f"{num} 0 obj\n{obj}\nendobj\n".encode('latin-1', errors='replace')
        # xref
        xref_pos = len(out)
        total = len(all_objs) + 1
        out += b"xref\n"
        out += f"0 {total}\n".encode()
        out += b"0000000000 65535 f \n"
        for off in offsets:
            out += f"{off:010d} 00000 n \n".encode()
        out += b"trailer\n"
        out += f"<< /Size {total} /Root 1 0 R >>\n".encode()
        out += b"startxref\n"
        out += f"{xref_pos}\n".encode()
        out += b"%%EOF\n"
        return out


def main():
    pdf = PDF()

    # Cover page
    pdf.new_page()
    pdf.set_font(bold=True, size=24)
    pdf.y = 500
    pdf.set_color(0.1, 0.3, 0.6)
    pdf.text_bold(120, 500, "REINO ANIMAL")
    pdf.set_font(bold=False, size=16)
    pdf.set_color(0, 0, 0)
    pdf.text(180, 460, "Biologia - Apuntes de clase")
    pdf.text(220, 420, "Zoologia General")

    # CNIDARIA
    pdf.new_page()
    pdf.set_font(size=11)
    pdf.banner("PHYLUM CNIDARIA", (0.1, 0.4, 0.6))
    pdf.bullet("Diblasticos (2 capas: ectodermo y endodermo), acuaticos")
    pdf.bullet("Cnidocitos: celulas urticantes con nematocisto (toxina)")
    pdf.bullet("Simetria radial, cavidad gastrovascular")
    pdf.bullet("Clase Hydrozoa: Hydra, coloniales/solitarios, agua dulce")
    pdf.bullet("Clase Scyphozoa: Medusas verdaderas, fase medusoide dominante")
    pdf.bullet("Clase Anthozoa: Corales y anemonas, solo forma polipo")
    pdf.spacer()

    pdf.banner("PHYLUM CTENOPHORA", (0.2, 0.5, 0.5))
    pdf.bullet("Bioluminiscentes, exclusivamente marinos")
    pdf.bullet("Tentaculos pegajosos (coloblastos) - NO cnidocitos")
    pdf.bullet("Ctenes: peines de cilios para locomocion")
    pdf.spacer()

    pdf.banner("SIMETRIAS Y CAVIDADES CORPORALES", (0.4, 0.3, 0.5))
    pdf.bullet("Radial: multiples planos (Cnidaria, Ctenophora)")
    pdf.bullet("Bilateral: un plano (mayoria de animales)")
    pdf.bullet("Acelomados: sin cavidad (Platyhelminthes)")
    pdf.bullet("Pseudocelomados: cavidad sin mesodermo completo (Nematoda)")
    pdf.bullet("Celomados: celoma verdadero rodeado de mesodermo")
    pdf.spacer()

    # PLATYHELMINTHES
    pdf.banner("PHYLUM PLATYHELMINTHES", (0.6, 0.2, 0.3))
    pdf.bullet("Acelomados, simetria bilateral, aplanados dorsoventralmente")
    pdf.bullet("Clase Turbellaria: vida libre, planarias, regeneracion")
    pdf.bullet("Clase Trematoda: parasitos con ventosas")
    pdf.alert("Fasciola hepatica: ciclo con caracol, infecta higado bovino/humano")
    pdf.bullet("Clase Cestoda: tenias, cuerpo segmentado (proglotides)")
    pdf.alert("Taenia solium: cisticercosis (larva en tejidos), teniasis (adulto intestinal)")
    pdf.alert("Taenia saginata: por carne de res mal cocida")
    pdf.spacer()

    # NEMATODA
    pdf.banner("PHYLUM NEMATODA", (0.5, 0.4, 0.1))
    pdf.bullet("Pseudocelomados, cilindricos, cuticula protectora")
    pdf.bullet("Enterobius vermicularis: oxiuros, prurito anal nocturno")
    pdf.bullet("Ascaris lumbricoides: nematodo intestinal grande, ciclo pulmonar")
    pdf.bullet("Filarias: transmitidas por mosquitos, elefantiasis")
    pdf.bullet("Trichinella spiralis: enquistada en musculo, por cerdo crudo")
    pdf.spacer()

    # ANNELIDA
    pdf.banner("PHYLUM ANNELIDA", (0.3, 0.5, 0.2))
    pdf.bullet("Celomados, cuerpo segmentado (metamerizacion)")
    pdf.bullet("Sistema circulatorio cerrado, 5 corazones (arcos aorticos)")
    pdf.bullet("Clase Oligoqueta: lombriz de tierra, clitelo, hermafroditas")
    pdf.bullet("Clase Poliqueta: marinos, parapodios, branquias")
    pdf.bullet("Clase Hirudinea: sanguijuelas, hirudina anticoagulante")

    # MOLLUSCA
    pdf.new_page()
    pdf.banner("PHYLUM MOLLUSCA", (0.2, 0.3, 0.6))
    pdf.bullet("Radula (lengua raspadora), manto secreta concha")
    pdf.bullet("Hemolinfa (sangre con hemocianina - azul)")
    pdf.bullet("Clase Bivalva: 2 valvas, filtradores, pie excavador")
    pdf.bullet("Clase Gastropoda: caracoles/babosas, torsion visceral")
    pdf.bullet("Clase Cephalopoda: pulpos/calamares, 3 corazones")
    pdf.alert("Cephalopoda: primer cerebro complejo, ojos tipo camara")
    pdf.spacer()

    # ARTHROPODA
    pdf.banner("ARTHROPODA", (0.6, 0.3, 0.1))
    pdf.bullet("Exoesqueleto de quitina, apendices articulados")
    pdf.bullet("Muda (ecdisis): crecimiento por cambio de exoesqueleto")
    pdf.bullet("Insecta: 3 pares patas, 1-2 pares alas, traqueas")
    pdf.bullet("Crustacea: cefalotorax, branquias, 5+ pares apendices")
    pdf.bullet("Arachnida: queliceros, 4 pares patas, sin antenas")
    pdf.bullet("Quelicerados: aranhas, escorpiones, pedipalpos")
    pdf.bullet("Metamorfosis: completa (holometabola) vs incompleta (hemimetabola)")
    pdf.spacer()

    # DEUTEROSTOMOS
    pdf.banner("DEUTEROSTOMOS", (0.4, 0.2, 0.5))
    pdf.bullet("Boca se forma despues del ano en desarrollo embrionario")
    pdf.bullet("Equinodermos: piel con espinas, simetria pentarradial adulta")
    pdf.bullet("Pies ambulacrales: locomocion por sistema acuifero (vascular)")
    pdf.bullet("Clases: Asteroidea, Echinoidea, Holothuroidea, Ophiuroidea")
    pdf.bullet("Hemicordata: gusanos bellota, hendiduras faringeas")
    pdf.spacer()

    # PRECORDADOS
    pdf.banner("PRECORDADOS", (0.3, 0.4, 0.5))
    pdf.bullet("Notocorda: estructura de sosten, precursora de columna")
    pdf.bullet("Cephalocordata: anfioxo, notocorda toda la vida")
    pdf.bullet("Urochordata: tunicados, larva con notocorda, adulto sesil")
    pdf.spacer()

    # PECES
    pdf.banner("CHORDATA - PECES", (0.1, 0.4, 0.5))
    pdf.bullet("Primer vertebrado con cerebro desarrollado")
    pdf.bullet("Condrictios: esqueleto cartilaginoso, tiburones/rayas")
    pdf.bullet("Osteictios: esqueleto oseo, vejiga natatoria")
    pdf.bullet("Respiracion branquial, ectotermicos, 2 camaras (1A+1V)")

    # ANFIBIOS
    pdf.new_page()
    pdf.banner("ANFIBIOS", (0.2, 0.5, 0.3))
    pdf.bullet("Derivan de peces sarcopterigios (aletas lobuladas)")
    pdf.bullet("Piel vascularizada: respiracion cutanea + pulmonar")
    pdf.bullet("Corazon: 2 auriculas + 1 ventriculo (3 camaras)")
    pdf.bullet("Orden Anura: ranas/sapos, sin cola adulto, salto")
    pdf.bullet("Orden Caudata: salamandras, con cola, regeneracion")
    pdf.bullet("Orden Gymnophiona: cecilias, apodos, excavadores")
    pdf.spacer()

    # REPTILIA
    pdf.banner("REPTILIA", (0.5, 0.4, 0.2))
    pdf.bullet("Huevo amniota: conquista definitiva del medio terrestre")
    pdf.bullet("Corazon 3 camaras (cocodrilos 4), ectotermicos")
    pdf.bullet("Organo de Jacobson: quimiorrecepcion (lengua bifida)")
    pdf.bullet("Piel con escamas corneas, sin glandulas")
    pdf.bullet("Ordenes: Squamata, Testudines, Crocodilia")
    pdf.spacer()

    # AVES
    pdf.banner("AVES", (0.1, 0.3, 0.5))
    pdf.bullet("Corazon 4 camaras, endotermicos, alta tasa metabolica")
    pdf.bullet("Sacos aereos: ventilacion unidireccional eficiente")
    pdf.bullet("Plumas: vuelo, aislamiento, cortejo")
    pdf.bullet("Huesos neumaticos (huecos): reducen peso para vuelo")
    pdf.bullet("Hembra determina sexo: ZW hembra, ZZ macho")
    pdf.spacer()

    # MAMMALIA
    pdf.banner("MAMMALIA", (0.5, 0.2, 0.4))
    pdf.bullet("Pelo, glandulas mamarias, diafragma muscular")
    pdf.bullet("Corazon 4 camaras, endotermicos, eritrocitos sin nucleo")
    pdf.bullet("Monotremas: ponen huevos (ornitorrinco, equidna)")
    pdf.bullet("Marsupiales: cria en marsupio (canguro, koala)")
    pdf.bullet("Placentarios: placenta completa, mayor desarrollo fetal")
    pdf.bullet("Ordenes: Carnivora, Rodentia, Chiroptera, Cetacea, Primates")
    pdf.spacer()

    # TABLA COMPARATIVA
    pdf.new_page()
    pdf.banner("TABLA COMPARATIVA - VERTEBRADOS", (0.3, 0.2, 0.4))
    pdf.spacer(5)
    pdf.set_font(bold=True, size=9)
    pdf.line("Grupo       | Temp  | Eritroc. | Corazon | Respir.  | Tegumento   | Reprod.   | Excr.", indent=5)
    pdf.set_font(size=9)
    pdf.line("Peces       | Ecto  | Nucleados| 2cam    | Branquial| Escamas     | Oviparo   | Amonio", indent=5)
    pdf.line("Anfibios    | Ecto  | Nucleados| 3cam    | Cut+Pulm | Piel humeda | Ovip(agua)| Urea", indent=5)
    pdf.line("Reptiles    | Ecto  | Nucleados| 3-4cam  | Pulmonar | Esc.corneas | Huevo amn.| Ac.urico", indent=5)
    pdf.line("Aves        | Endo  | Nucleados| 4cam    | Pulm+Sac | Plumas      | Huevo amn.| Ac.urico", indent=5)
    pdf.line("Mamiferos   | Endo  | S/nucleo | 4cam    | Pulmonar | Pelo        | Viviparo* | Urea", indent=5)
    pdf.spacer()
    pdf.set_font(size=8)
    pdf.line("* Excepto monotremas (oviparo) y marsupiales (desarrollo en marsupio)", indent=5)

    # Write PDF
    data = pdf.build()
    outpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Reino_Animal_Apuntes.pdf")
    with open(outpath, 'wb') as f:
        f.write(data)
    print(f"PDF generado: {outpath} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
