"""Genera borrador/borrador_EIT.pdf (primer borrador IMRyD).

Toda cifra se lee de resultados/ (pipeline y modelo) y las referencias de bibliografia/referencias.bib.
Uso:  python src/generar_borrador.py   (ejecutar antes src/pipeline_eit.py y src/modelo_eit.py)
"""
import json
import re
from datetime import date
from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

BASE = Path(__file__).resolve().parents[1]
RES = BASE / "resultados"
SALIDA = BASE / "borrador" / "borrador_EIT.pdf"
ANCHO_UTIL = 16.5 * cm

# ---------------------------------------------------------------- fuentes y estilos
FUENTE, FUENTE_B = "Helvetica", "Helvetica-Bold"
_fonts = Path(r"C:\Windows\Fonts")
if (_fonts / "arial.ttf").exists():  # Arial cubre Δ, −, ≤ (Helvetica base no)
    pdfmetrics.registerFont(TTFont("Arial", str(_fonts / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(_fonts / "arialbd.ttf")))
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial", boldItalic="Arial-Bold")
    FUENTE, FUENTE_B = "Arial", "Arial-Bold"

_ss = getSampleStyleSheet()
EST = {
    "titulo": ParagraphStyle("t", parent=_ss["Title"], fontName=FUENTE_B, fontSize=16, leading=20),
    "sub": ParagraphStyle("s", parent=_ss["Normal"], fontName=FUENTE, fontSize=9, textColor=colors.HexColor("#52514e"), alignment=1),
    "h1": ParagraphStyle("h1", parent=_ss["Heading1"], fontName=FUENTE_B, fontSize=13, spaceBefore=12, spaceAfter=6),
    "h2": ParagraphStyle("h2", parent=_ss["Heading2"], fontName=FUENTE_B, fontSize=11, spaceBefore=8, spaceAfter=4),
    "p": ParagraphStyle("p", parent=_ss["Normal"], fontName=FUENTE, fontSize=10, leading=14, alignment=TA_JUSTIFY, spaceAfter=6),
    "cap": ParagraphStyle("c", parent=_ss["Normal"], fontName=FUENTE, fontSize=8.5, leading=11, textColor=colors.HexColor("#52514e"), spaceAfter=10),
    "ref": ParagraphStyle("r", parent=_ss["Normal"], fontName=FUENTE, fontSize=8.5, leading=11, leftIndent=12, firstLineIndent=-12, spaceAfter=3),
    "celda": ParagraphStyle("cel", parent=_ss["Normal"], fontName=FUENTE, fontSize=8, leading=10),
}
COMPLETAR = '<font color="#c0392b"><b>[COMPLETAR]</b></font>'


def P(texto, estilo="p"):
    return Paragraph(texto.replace("[COMPLETAR]", COMPLETAR).replace("[VERIFICAR]", '<font color="#c0392b"><b>[VERIFICAR]</b></font>'), EST[estilo])


def num(x, d=2):
    return f"{x:.{d}f}".replace(".", ",").replace("-", "−")


# ---------------------------------------------------------------- bibliografía
def leer_bib(ruta):
    texto = ruta.read_text(encoding="utf-8")
    refs = {}
    for tipo, clave, cuerpo in re.findall(r"@(\w+)\{([^,]+),(.*?)\n\}", texto, flags=re.S):
        campos = {k.lower(): v for k, v in re.findall(r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", cuerpo)}
        for k, v in campos.items():
            v = v.replace("{\\'e}", "é").replace('{\\"o}', "ö").replace("\\_", "_")
            campos[k] = re.sub(r"[{}]", "", v)
        refs[clave.strip()] = {"tipo": tipo, **campos}
    return dict(sorted(refs.items()))


def autores(ref):
    lista = [a.strip() for a in ref["author"].split(" and ")]
    return [a for a in lista if a != "others"], "others" in lista


def cita(refs, clave):
    lista, otros = autores(refs[clave])
    ap = [a.split(",")[0] for a in lista]
    nombre = ap[0] if len(ap) == 1 and not otros else (f"{ap[0]} y {ap[1]}" if len(ap) == 2 and not otros else f"{ap[0]} et al.")
    return f"{nombre}, {refs[clave]['year']}"


def citas(refs, *claves):
    return "(" + "; ".join(cita(refs, c) for c in claves) + ")"


def referencia_completa(r):
    lista, otros = autores(r)
    txt = "; ".join(lista) + ("; et al." if otros else "")
    txt += f" ({r['year']}). {r['title']}. "
    if r["tipo"] == "misc":
        txt += f"{r.get('howpublished', '')}. "
    else:
        txt += f"<i>{r['journal']}</i>"
        txt += f", {r['volume']}" if "volume" in r else ""
        txt += f"({r['number']})" if "number" in r else ""
        txt += f", {r['pages']}" if "pages" in r else ""
        txt += ". "
    if "doi" in r:
        txt += f"https://doi.org/{r['doi']}"
    if "VERIFICAR" in r.get("note", ""):
        txt += " [VERIFICAR]"
    return txt


# ---------------------------------------------------------------- tablas y figuras
def tabla(datos, anchos):
    filas = [[Paragraph(str(c), EST["celda"]) for c in fila] for fila in datos]
    t = Table(filas, colWidths=anchos, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef0f3")),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.HexColor("#52514e")),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, colors.HexColor("#52514e")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def figura(ruta, pie, alto_max=19 * cm):
    w, h = ImageReader(str(ruta)).getSize()
    ancho = min(ANCHO_UTIL, alto_max * w / h)
    return KeepTogether([Image(str(ruta), width=ancho, height=ancho * h / w), P(pie, "cap")])


# ---------------------------------------------------------------- documento
def construir():
    refs = leer_bib(BASE / "bibliografia" / "referencias.bib")
    m = json.loads((RES / "modelo" / "metricas_modelo.json").read_text(encoding="utf-8"))
    met = m["metricas_oof"]
    pip = pd.read_csv(RES / "caracteristicas_todos.csv", dtype={"Sujeto": str}).iloc[0]
    par = json.loads((RES / "parametros_usados.json").read_text(encoding="utf-8"))
    vol = m["volumen_referencia_L"]
    lin, rid, rf, eit = (met[k] for k in ["Lineal (ΔZ)", "Ridge (multivariable)", "Random Forest (multivariable)", "Ridge (solo EIT)"])
    c = lambda *k: citas(refs, *k)

    h = []
    h += [P("Estimación del volumen tidal a partir de tomografía de impedancia eléctrica en un dataset público: "
            "pipeline de procesamiento y modelos de regresión", "titulo"),
          P(f"Primer borrador · [COMPLETAR: autor, programa, profesor guía] · {date.today():%d-%m-%Y}", "sub"),
          Spacer(1, 10)]

    h += [P("Resumen", "h1"), P(
        "La tomografía de impedancia eléctrica (EIT) permite monitorizar la ventilación pulmonar de forma no invasiva, "
        "pero la conversión de la variación de impedancia (ΔZ) a volumen depende de la calibración y de las condiciones "
        f"de ventilación. Se analizó el sujeto 03 de un dataset público de PhysioNet {c('Guy2023_dataset')}, con EIT, "
        f"flujo y presión registrados durante CPAP con PEEP creciente. Un pipeline de filtrado y segmentación detectó "
        f"{int(pip['n_ciclos'])} ciclos, de los cuales {int(pip['n_validos'])} fueron válidos "
        f"(frecuencia respiratoria {num(pip['FR_resp_min'], 1)} rpm). Se estimó el volumen inspirado por ciclo "
        f"(media {num(vol['media'])} L) con cuatro modelos y validación cruzada temporal por bloques. ΔZ por sí sola "
        f"se correlacionó débilmente con el volumen (r = {num(m['r_pearson_dZ_vs_volumen_sin_modelo'])}; "
        f"R² = {num(lin['R2'])}). Un modelo Ridge con variables exclusivamente EIT alcanzó R² = {num(eit['R2'])} "
        f"(RMSE {num(eit['RMSE_L'], 3)} L), y al añadir la presión media del circuito R² = {num(rid['R2'])} "
        f"(RMSE {num(rid['RMSE_L'], 3)} L; límites de acuerdo {num(rid['BA_LoA_inf_L'])} a {num(rid['BA_LoA_sup_L'])} L). "
        "Los residuos del modelo lineal siguen el nivel de presión, lo que indica que la relación ΔZ–volumen cambia con la PEEP. "
        "Se concluye que la estimación de volumen basada solo en ΔZ global no es robusta bajo cambios de PEEP y que se "
        "requiere calibración dependiente de la condición ventilatoria. [COMPLETAR: revisar conclusión tras analizar más sujetos.]")]

    h += [P("1. Introducción", "h1"), P(
        "La monitorización de la ventilación es central en el manejo de pacientes con soporte respiratorio. La EIT torácica "
        "reconstruye, a partir de corrientes de baja intensidad aplicadas mediante un cinturón de electrodos, imágenes de la "
        f"distribución de impedancia del tórax con alta resolución temporal {c('Leonhardt2012_holygrail', 'Frerichs2017_consensus')}. "
        f"Algoritmos de reconstrucción de consenso como GREIT {c('Adler2009_GREIT')} permiten obtener series temporales de "
        "impedancia global cuyas variaciones se asocian al volumen corriente."), P(
        "Sin embargo, la relación entre ΔZ y volumen no es universal: depende del sujeto, de la posición del cinturón y del "
        f"volumen pulmonar de fin de espiración, que cambia con la PEEP {c('Bikker2009_lungvolume')}. Disponer de datasets "
        f"públicos con EIT y una referencia de flujo simultánea {c('Guy2024_databrief')} permite estudiar esta relación de forma reproducible."), P(
        "<b>Objetivo:</b> implementar un pipeline reproducible de procesamiento de la señal EIT global y evaluar modelos que "
        "estimen el volumen inspirado por ciclo a partir de características EIT, cuantificando el efecto de la presión de la vía aérea. "
        "[COMPLETAR: pregunta de investigación e hipótesis formales.]")]

    h += [P("2. Estado del arte", "h1"),
          P("2.1 Fundamentos y consenso", "h2"), P(
        f"El grupo TREND estableció la terminología y recomendaciones de análisis de la EIT torácica {c('Frerichs2017_consensus')}, "
        f"y revisiones previas resumieron sus índices de ventilación y perfusión {c('Leonhardt2012_holygrail')}. GREIT unificó la "
        f"reconstrucción lineal 2D de imágenes pulmonares {c('Adler2009_GREIT')}."),
          P("2.2 Relación impedancia–volumen", "h2"), P(
        f"En pacientes de UCI, la relación lineal ΔZ–volumen no permitió estimar el volumen pulmonar a distintos niveles de PEEP "
        f"{c('Bikker2009_lungvolume')}. En voluntarios, la variación tidal global fue reproducible y se correlacionó con el volumen "
        f"tidal del neumotacógrafo {c('Caruana2017_reproducibility')}."),
          P("2.3 Procesamiento de señal y detección de respiraciones", "h2"), P(
        f"La detección de ciclos es un paso crítico; se han propuesto algoritmos basados en cruces por cero con umbrales de amplitud "
        f"y frecuencia {c('Khodadad2018_breathdetection')}, y la frecuencia respiratoria derivada de EIT se ha validado frente a "
        f"capnografía mediante Bland–Altman {c('Wisse2024_respiratoryrate')}."),
          P("2.4 Ventilación regional y datos abiertos", "h2"), P(
        f"Índices regionales como el índice de inhomogeneidad global {c('Zhao2009_GI')} requieren las imágenes completas. "
        f"PhysioNet {c('Goldberger2000_physionet')} aloja el dataset utilizado {c('Guy2023_dataset')}. "
        "[COMPLETAR: ampliar con trabajos que hayan usado este mismo dataset y con métodos de aprendizaje automático en EIT.]")]

    h += [P("3. Datos", "h1"), P(
        f"Se utilizó el <i>Respiratory dataset from PEEP study with expiratory occlusion</i> v1.0.0 {c('Guy2023_dataset', 'Guy2024_databrief')}, "
        "que reúne 80 sujetos adultos registrados con un equipo Dräger PulmoVista 500 durante CPAP con PEEP creciente en pasos de "
        "0,5 cmH<sub>2</sub>O cada 30 s y oclusiones espiratorias rápidas. [VERIFICAR: rango de PEEP (4–12 vs 4–20 cmH<sub>2</sub>O, las fuentes difieren).] "
        "Se analizó el archivo procesado del sujeto 03 (<i>ProcessedData_Subject03.csv</i>), que contiene presión, flujo, volumen tidal, "
        "circunferencias torácica y abdominal (100 Hz) y aireación global EIT (50 Hz), con índices inspiratorios para ambas series. "
        "El dataset es de acceso abierto bajo licencia Creative Commons Attribution 4.0 International (CC BY 4.0). "
        "[COMPLETAR: características del sujeto (grupo, sexo) y aprobación ética del estudio original.]")]

    h += [P("4. Métodos", "h1"), P("4.1 Pipeline de procesamiento", "h2"), P(
        f"La aireación global se filtró con un Butterworth pasa-bajos de orden {par['ORDEN_FILTRO']} de fase cero, comparando "
        f"frecuencias de corte de {', '.join(str(f) for f in par['FC_COMPARAR'])} Hz y usando {num(par['FC_ANALISIS'], 0)} Hz para el análisis "
        f"({num(par['FC_FLUJO'], 0)} Hz para el flujo). Se detectaron mínimos y máximos con separación mínima de {num(par['DIST_MIN_S'], 1)} s "
        f"y prominencia relativa {num(par['PROM_REL'])}. Cada ciclo (mínimo–máximo–mínimo) se validó por duración "
        f"({num(par['DUR_MIN_S'], 1)}–{num(par['DUR_MAX_S'], 0)} s), por razones de duración y amplitud respecto de una ventana local de "
        f"{par['VENTANA_LOCAL']} ciclos ({num(par['RATIO_DUR'][0], 1)}–{num(par['RATIO_DUR'][1], 1)}), por presencia de un único pico y por "
        f"concordancia con el inicio inspiratorio del flujo (tolerancia {num(par['TOL_ONSET_S'], 1)} s). Por ciclo se calcularon amplitud (ΔZ), "
        "duración, tiempos inspiratorio y espiratorio, áreas bajo la curva y el volumen inspirado por integración del flujo "
        "(<i>vol_insp_flujo</i>), usado como referencia. [COMPLETAR: revisar que la descripción coincida con el código.]"),
          P("4.2 Modelos de estimación de volumen", "h2"), P(
        "Se compararon cuatro modelos: (i) regresión lineal con ΔZ; (ii) Ridge con variables solo EIT (ΔZ, duración, tiempo inspiratorio, "
        "área inspiratoria); (iii) Ridge y (iv) Random Forest con las variables EIT más la presión media del ciclo, como indicador del nivel de PEEP. "
        f"Por tratarse de un único sujeto, se usó validación cruzada temporal de {len(next(iter(m['R2_por_bloque'].values())))} bloques contiguos sin barajar; "
        "todas las métricas se calculan sobre predicciones fuera de muestra."),
          P("4.3 Métricas", "h2"), P(
        "R², coeficiente de Pearson, RMSE, MAE, error relativo (MAE / volumen medio) y análisis de Bland–Altman (sesgo y límites de acuerdo "
        "al 95 %). Implementación en Python (pandas, SciPy, scikit-learn); código en <i>src/pipeline_eit.py</i> y <i>src/modelo_eit.py</i>.")]

    h += [P("5. Resultados", "h1"), P("5.1 Procesamiento de la señal", "h2"), tabla([
        ["Métrica", "Valor"],
        ["Ciclos detectados / válidos", f"{int(pip['n_ciclos'])} / {int(pip['n_validos'])}"],
        ["Frecuencia respiratoria [rpm]", num(pip["FR_resp_min"], 1)],
        ["Duración de ciclo, mediana ± DE [s]", f"{num(pip['duracion_mediana'])} ± {num(pip['duracion_std'])}"],
        ["Ti EIT / Ti flujo, mediana [s]", f"{num(pip['Ti_eit_mediano'])} / {num(pip['Ti_flujo_mediano'])}"],
        ["Amplitud ΔZ, mediana (IQR) [u.a.]", f"{num(pip['amplitud_mediana'], 0)} ({num(pip['amplitud_IQR'], 0)})"],
        ["Volumen inspirado de referencia, media ± DE [L]", f"{num(vol['media'])} ± {num(vol['DE'])}"],
    ], [10 * cm, 5 * cm]), P("Tabla 1. Métricas descriptivas del pipeline (resultados/caracteristicas_todos.csv, resultados/modelo/metricas_modelo.json).", "cap")]
    sujeto = RES / "sujeto03"
    for archivo, pie in [("01_filtros_sujeto03.png", "Figura 1. Comparación de frecuencias de corte del filtro sobre la aireación global."),
                         ("04_ciclos_validos_sujeto03.png", "Figura 2. Ciclos válidos detectados por el pipeline.")]:
        if (sujeto / archivo).exists():
            h.append(figura(sujeto / archivo, pie, alto_max=9 * cm))

    h += [P("5.2 Estimación del volumen", "h2"), tabla(
        [["Modelo", "R²", "r", "RMSE [L]", "MAE [L]", "Error rel. [%]", "Sesgo [L]", "LoA [L]"]] +
        [[n, num(v["R2"]), num(v["r_pearson"]), num(v["RMSE_L"], 3), num(v["MAE_L"], 3), num(v["error_rel_pct"], 1),
          num(v["BA_sesgo_L"], 3), f"{num(v['BA_LoA_inf_L'])} / {num(v['BA_LoA_sup_L'])}"] for n, v in met.items()],
        [4.6 * cm, 1.2 * cm, 1.2 * cm, 1.6 * cm, 1.6 * cm, 1.8 * cm, 1.6 * cm, 2.6 * cm]),
          P(f"Tabla 2. Métricas fuera de muestra (validación temporal por bloques, n = {m['n_ciclos_validos']} ciclos). LoA: límites de acuerdo de Bland–Altman.", "cap"),
          tabla([["Modelo"] + [f"Bloque {i + 1}" for i in range(len(next(iter(m["R2_por_bloque"].values()))))]] +
                [[n] + [num(x) for x in v] for n, v in m["R2_por_bloque"].items()], [5.5 * cm] + [2 * cm] * 5),
          P("Tabla 3. R² dentro de cada bloque temporal.", "cap"), P(
        f"ΔZ aislada explicó poca variabilidad del volumen (r = {num(m['r_pearson_dZ_vs_volumen_sin_modelo'])}). Combinar variables EIT elevó "
        f"R² a {num(eit['R2'])}, y añadir la presión media a {num(rid['R2'])} (Ridge) y {num(rf['R2'])} (Random Forest). "
        "Los residuos del modelo lineal muestran una tendencia que sigue el aumento progresivo de la presión (Figura 5).")]
    for archivo, pie in [("fig_pred_vs_real.png", "Figura 3. Volumen predicho vs. real (predicciones fuera de muestra); línea discontinua: identidad."),
                         ("fig_bland_altman.png", "Figura 4. Análisis de Bland–Altman por modelo."),
                         ("fig_residuos_tiempo.png", "Figura 5. Residuos en el tiempo por modelo y presión media del ciclo; líneas punteadas: límites de bloques de validación.")]:
        h.append(figura(RES / "modelo" / archivo, pie))

    h += [P("6. Discusión", "h1"), P(
        f"La débil relación entre ΔZ global y volumen inspirado en este sujeto contrasta con correlaciones altas reportadas en voluntarios "
        f"en condiciones estables {c('Caruana2017_reproducibility')}, pero es coherente con que la relación ΔZ–volumen se altera al cambiar la PEEP "
        f"{c('Bikker2009_lungvolume')}: el protocolo modifica el volumen de fin de espiración y la zona pulmonar que capta el plano del cinturón. "
        "La mejora al incluir la presión indica que un modelo útil requiere información de la condición ventilatoria o una recalibración por nivel de PEEP. "
        "Dado que la presión no proviene de la EIT, el desempeño del modelo combinado no debe atribuirse a la EIT por sí sola. "
        f"La frecuencia respiratoria obtenida es comparable con el tipo de validación de {cita(refs, 'Wisse2024_respiratoryrate')}. "
        "[COMPLETAR: comparar cifras concretas con la literatura y discutir el posible efecto de la CPAP sobre el volumen integrado del flujo.]")]
    h += [P("7. Limitaciones", "h1"), P(
        "(i) Un único sujeto: los resultados no son generalizables y la validación es intra-sujeto. (ii) La validación temporal mezcla niveles de PEEP "
        "entre entrenamiento y prueba; el primer bloque (sin CPAP) queda fuera del rango de entrenamiento, con R² negativo. (iii) Solo se usó la señal EIT "
        "global, sin información regional. (iv) El volumen de referencia proviene de la integración del flujo, sensible a deriva y a fugas. "
        "(v) Los parámetros del pipeline se ajustaron sobre el mismo registro. [COMPLETAR]")]
    h += [P("8. Trabajo futuro", "h1"), P(
        "Extender el análisis a los 80 sujetos con validación <i>leave-one-subject-out</i>; modelar explícitamente el nivel de PEEP (calibración por escalón); "
        f"incorporar índices regionales a partir de las imágenes EIT crudas {c('Zhao2009_GI')}; comparar el detector de ciclos con algoritmos publicados "
        f"{c('Khodadad2018_breathdetection')}. [COMPLETAR]")]

    h += [PageBreak(), P("Referencias", "h1")] + [P(referencia_completa(r), "ref") for r in refs.values()]
    return h


def pie_pagina(canvas, doc):
    canvas.saveState()
    canvas.setFont(FUENTE, 8)
    canvas.setFillColor(colors.HexColor("#52514e"))
    canvas.drawString(2.2 * cm, 1.2 * cm, "Borrador – Tesis EIT pulmonar")
    canvas.drawRightString(A4[0] - 2.2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


if __name__ == "__main__":
    SALIDA.parent.mkdir(exist_ok=True)
    doc = SimpleDocTemplate(str(SALIDA), pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                            title="Borrador EIT", author="[COMPLETAR]")
    doc.build(construir(), onFirstPage=pie_pagina, onLaterPages=pie_pagina)
    print(f"PDF generado: {SALIDA}")
