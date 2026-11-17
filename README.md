# Tesis EIT pulmonar: estimación del volumen tidal a partir de tomografía de impedancia eléctrica

Primer borrador de tesis sobre la monitorización de la ventilación con **Tomografía de Impedancia Eléctrica (EIT)**.
Se trabaja con un dataset público de PhysioNet y se incluye:

1. Un **pipeline** de procesamiento de la señal EIT global (filtrado, detección y validación de ciclos respiratorios).
2. Un **modelo** que estima el volumen inspirado por ciclo a partir de características EIT y reporta métricas.
3. Una **skill de investigación** para Claude Code (búsqueda y verificación de bibliografía, estructura del borrador).
4. La **bibliografía** verificada (BibTeX y tabla resumen).
5. El **primer borrador en PDF**, generado automáticamente a partir de los resultados.

> Estado: primer borrador (no versión final). Los puntos pendientes están marcados `[COMPLETAR]` o `[VERIFICAR]` en el PDF.
> Avance por fases en [PROGRESO.md](PROGRESO.md).

---

## Estructura del repositorio

```
EIT_TESISUI/
├── README.md                     ← este archivo
├── CLAUDE.md                     ← contexto e instrucciones para Claude Code
├── PROGRESO.md                   ← bitácora de avance por fases
├── requirements.txt              ← dependencias de Python
├── .claude/
│   └── skills/
│       ├── README.md             ← qué son las skills y cómo se usan
│       └── investigacion-eit/
│           └── SKILL.md          ← skill de investigación (bibliografía + estructura IMRyD)
├── .vscode/                      ← configuración de VS Code (tareas para ejecutar todo)
├── data/
│   ├── README.md                 ← fuente, licencia y descripción de columnas
│   └── ProcessedData_Subject03.csv
├── src/
│   ├── pipeline_eit.py           ← paso 1: procesamiento de la señal y ciclos
│   ├── modelo_eit.py             ← paso 2: modelos de volumen y métricas
│   └── generar_borrador.py       ← paso 3: genera el PDF del borrador
├── resultados/
│   ├── matriz_ciclos_todos.csv   ← una fila por ciclo (32 variables)
│   ├── caracteristicas_todos.csv ← resumen por sujeto
│   ├── parametros_usados.json    ← parámetros del pipeline en la última ejecución
│   ├── sujeto03/                 ← figuras y tablas del pipeline
│   └── modelo/                   ← métricas, predicciones y figuras del modelo
├── bibliografia/
│   ├── referencias.bib           ← 11 referencias (10 con DOI verificado)
│   ├── tabla_bibliografia.md     ← tabla resumen de cada paper
│   └── papers/                   ← PDFs de papers (solo local, no se suben)
├── borrador/
│   └── borrador_EIT.pdf          ← primer borrador IMRyD
├── docs/
│   └── prompt_trabajo.md         ← prompt usado para trabajar con Claude Code
└── archivo/
    └── versiones_previas/        ← scripts antiguos (solo historial, no se usan)
```

## Cómo ejecutar

Requisitos: Python 3.10 o superior.

```bash
pip install -r requirements.txt

python src/pipeline_eit.py      # 1. procesa data/ y escribe resultados/
python src/modelo_eit.py        # 2. entrena y evalúa modelos -> resultados/modelo/
python src/generar_borrador.py  # 3. genera borrador/borrador_EIT.pdf
```

En **VS Code**: `Terminal > Run Task…` y elegir **"4. Ejecutar todo"**, o cada paso por separado.

> `src/pipeline_eit.py` muestra las figuras en ventanas (`MOSTRAR_FIGURAS = True`). Para ejecutarlo sin ventanas,
> cambia esa constante a `False`; las tareas de VS Code ya lo ejecutan sin ventanas.

## Datos

*Respiratory dataset from PEEP study with expiratory occlusion* v1.0.0 (Guy et al., 2023, PhysioNet,
[doi:10.13026/d767-e709](https://doi.org/10.13026/d767-e709)). Ver [data/README.md](data/README.md).

## Método y resultados principales (sujeto 03)

- **Pipeline:** 301 ciclos detectados, 297 válidos; frecuencia respiratoria ≈ 18,3 rpm.
- **Modelo:** objetivo = volumen inspirado por integración del flujo (`vol_insp_flujo`). Validación cruzada
  **temporal** por 5 bloques contiguos (un solo sujeto, sin barajar).

| Modelo | R² | RMSE [L] | Límites de acuerdo (Bland–Altman) [L] |
|---|---|---|---|
| Lineal (solo ΔZ) | −0,21 | 0,351 | −0,68 / +0,70 |
| Ridge (solo variables EIT) | 0,31 | 0,265 | −0,53 / +0,51 |
| Ridge (EIT + presión) | 0,84 | 0,127 | −0,26 / +0,24 |
| Random Forest (EIT + presión) | 0,63 | 0,195 | −0,40 / +0,36 |

**Lectura:** ΔZ global por sí sola no estima bien el volumen bajo cambios de PEEP. La mayor parte del desempeño
del mejor modelo proviene de la presión, que no es una señal EIT. Detalle en `resultados/modelo/metricas_modelo.json`
y en el borrador.

## Trabajo con Claude Code (skills)

La carpeta [.claude/skills/](.claude/skills/) contiene la skill **`investigacion-eit`**, que Claude Code carga
automáticamente al abrir este proyecto. Define cómo buscar y verificar papers, cómo registrarlos en
`bibliografia/` y la estructura del borrador. Ver [.claude/skills/README.md](.claude/skills/README.md).

## Limitaciones

Un único sujeto, sin validación externa; el volumen de referencia proviene de la integración del flujo.
El detalle está en la sección 7 del borrador.
