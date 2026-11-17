# CLAUDE.md – Tesis EIT pulmonar

Contexto para Claude Code. Leer primero `PROGRESO.md` para saber en qué fase está el trabajo.

## Proyecto
Estimación del volumen tidal a partir de la señal EIT global, usando el dataset público de PhysioNet
"Respiratory dataset from PEEP study with expiratory occlusion" (sujeto 03 en `data/`).

## Stack
Python 3.10+ con numpy, pandas, scipy, matplotlib, scikit-learn y reportlab (ver `requirements.txt`).

## Estructura y flujo
- `src/pipeline_eit.py`: lee `data/` y escribe `resultados/` (ciclos y características).
- `src/modelo_eit.py`: lee `resultados/matriz_ciclos_todos.csv` y escribe `resultados/modelo/`.
- `src/generar_borrador.py`: lee `resultados/` y `bibliografia/referencias.bib` y escribe `borrador/borrador_EIT.pdf`.
- Skill del proyecto: `.claude/skills/investigacion-eit/` (bibliografía y estructura IMRyD).

## Reglas
1. Ahorro de tokens: no leer el CSV completo (usar encabezado o resúmenes con pandas), no releer archivos y no imprimir tablas largas.
2. No inventar referencias ni cifras: toda cifra del borrador debe salir de `resultados/`; lo no verificado se marca `[VERIFICAR]`.
3. No modificar `data/` ni editar a mano los archivos de `resultados/`; se regeneran con los scripts.
4. Trabajar por fases, actualizar `PROGRESO.md` al terminar cada una y esperar confirmación.
5. Validar ejecutando los scripts antes de dar algo por terminado.
6. Respuestas en español, breves.
