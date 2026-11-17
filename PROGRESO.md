# PROGRESO – Tesis EIT pulmonar

## Fase 0 – Reconocimiento (completada 2026-11-10)
- Leídos: `parametros_usados.json`, `caracteristicas_todos.csv` (301 ciclos, 297 válidos, FR 18.3 rpm), cabecera de `ProcessedData_Subject03.csv` y de `matriz_ciclos_todos.csv` (301×32, incluye `amplitud` ΔZ, `duracion`, `Ti_eit`, `auc_rel`, `vol_insp_flujo`, `valido`).
- Python 3.14.8 tiene numpy, pandas, scipy, matplotlib y seaborn. **Faltan** scikit-learn y reportlab (instalarlos requiere aprobación).
- Pendiente de decidir: qué referencia de volumen tidal usar por ciclo (`vol_insp_flujo` ya calculado o pico de `V_tidal` sacado del CSV original).
- Próximo: Fase 1 (skill `investigacion-eit`).

## Fase 1 – Skill de investigación (completada 2026-11-10)
- Decisiones del usuario: se instalaron scikit-learn 1.9.1 y reportlab 5.1.0; la referencia de volumen es `vol_insp_flujo`; se trabaja en la raíz de este repositorio (`EIT_TESISUI/`).
- Se creó `.claude/skills/investigacion-eit/SKILL.md` con tres partes: (A) búsqueda y verificación, (B) registro en .bib y tabla, (C) estructura IMRyD.
- Próximo: Fase 2 (bibliografía de 10–15 papers con DOI).

## Fase 2 – Bibliografía (completada 2026-11-10)
- Dataset identificado: PhysioNet "Respiratory dataset from PEEP study with expiratory occlusion" v1.0.0 (Guy et al. 2023, doi 10.13026/d767-e709) + artículo descriptor Data in Brief 52:109874 (2024). El sujeto 03 está en CPAP con PEEP creciente, así que tener en cuenta los cambios de PEEP en el modelo.
- `bibliografia/referencias.bib` y `bibliografia/tabla_bibliografia.md`: 11 referencias, 10 con DOI verificado y 1 `[VERIFICAR]` (Caruana 2017, sin DOI).
- Próximo: Fase 3 (`modelo_eit.py`: ΔZ → `vol_insp_flujo`, validación temporal por bloques).

## Fase 3 – Modelo y métricas (completada 2026-11-10)
- `modelo_eit.py` lee `resultados/matriz_ciclos_todos.csv` (297 ciclos válidos). Hace KFold temporal con 5 bloques contiguos y escribe en `resultados/modelo/` (métricas csv/json, predicciones OOF y 3 figuras).
- Resultados OOF: Lineal ΔZ R² −0,21 (r(ΔZ,Vt) = 0,28); Ridge R² 0,84, RMSE 0,127 L, sesgo BA −0,008 L, LoA ±0,25 L; RF R² 0,63.
- Hallazgo: el residuo del modelo lineal sigue a la presión (PEEP), así que la relación ΔZ/Vt cambia con PEEP (coherente con Bikker 2009). En Ridge, `presion_media` es la variable de mayor peso y no es una señal EIT. El R² por bloque es bajo en los bloques 1–2.
- Agregado (con aprobación del usuario) el modelo "Ridge (solo EIT)", sin presión: R² 0,31, RMSE 0,265 L, LoA ±0,52 L. La presión aporta la mayor parte del desempeño del Ridge multivariable.
- Próximo: Fase 4 (borrador PDF).

## Fase 4 – Borrador PDF (completada 2026-11-10)
- `borrador/generar_pdf.py` (reportlab) genera `borrador/borrador_EIT.pdf`: 8 páginas, IMRyD completo, 3 tablas, 5 figuras y 11 referencias.
- Todas las cifras se leen de `resultados/` y las citas de `bibliografia/referencias.bib`. Para regenerar, ver el README (sección "Cómo ejecutar").
- Pendiente del autor: los `[COMPLETAR]` y `[VERIFICAR]` (en rojo en el PDF), la revisión visual del PDF y la descripción del pipeline frente al código.

## Fase 5 – Orden del repositorio para GitHub (completada 2026-11-10)
- Nueva estructura: `src/`, `data/`, `resultados/`, `bibliografia/`, `borrador/`, `docs/`, `archivo/` y `.claude/skills/`, con README, CLAUDE.md, requirements.txt, .gitignore y tareas de VS Code.
- Se reparó el pipeline, que había perdido la sangría y no ejecutaba: ahora es `src/pipeline_eit.py`, con rutas relativas. Reproduce los CSV previos de forma idéntica (diferencia máxima 0).
- Los scripts antiguos se movieron a `archivo/versiones_previas/`.
- Próximo: subir a GitHub (git no está instalado en este equipo) y completar los `[COMPLETAR]`.

## Sesión 2026-11-16 – Espacio de trabajo
- El título de la ventana de VS Code ahora es "Tarea proyecto de tesis". Se configura con `window.title` en `C:\Users\56940\Downloads\proyecto 10 nov\.vscode\settings.json`.
- Sigue sin estar instalado git, así que no hay control de versiones: el respaldo de todo el trabajo son los archivos en disco.
- Se instalaron Git 2.56 y GitHub CLI 2.104. El repositorio público quedó en https://github.com/franciscomoyar9-byte/Proyecto-EIT-TESIS-Fco-Moya (rama `main`, 44 archivos).
- Los commits se firman con el correo noreply de GitHub, configurado en el `git config` local del repositorio, para no exponer el correo personal.
- Para subir cambios: `git add -A; git commit -m "..."; git push`.
- Próximo: completar los `[COMPLETAR]` y `[VERIFICAR]` del borrador.

