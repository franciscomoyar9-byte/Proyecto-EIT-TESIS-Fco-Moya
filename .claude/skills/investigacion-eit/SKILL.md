---
name: investigacion-eit
description: Procedimiento para buscar, verificar y registrar bibliografía sobre Tomografía de Impedancia Eléctrica (EIT) pulmonar y para estructurar el borrador IMRyD de la tesis. Usar al buscar papers, actualizar bibliografia/referencias.bib o tabla_bibliografia.md, o redactar el borrador.
---

# Investigación EIT pulmonar

## A. Buscar y verificar papers
1. **Palabras clave**, combinándolas con AND/OR:
   - "electrical impedance tomography" OR "EIT" AND (lung OR pulmonary OR ventilation)
   - "tidal volume" OR "impedance-volume" OR "global impedance" AND (pneumotachograph OR spirometry OR ventilator)
   - "regional ventilation", "tidal variation", "breath detection", "signal processing", "filtering"
   - "open dataset" OR "public database" AND EIT; también el nombre del dataset (`ProcessedData_Subject`)
2. **Fuentes, en este orden:** PubMed → IEEE Xplore → Google Scholar → arXiv → PhysioNet / Zenodo / figshare (datasets).
3. **Criterios de inclusión:**
   - EIT torácica/pulmonar en humanos o animales.
   - Al menos uno de estos temas: validación EIT vs neumotacógrafo/volumen tidal, procesamiento de señal, ventilación regional o datasets abiertos.
   - Años 2010–2026; se admiten clásicos anteriores solo si son fundacionales (p. ej. consensos).
   - En inglés o español, con revisión por pares o preprint identificado como tal.
4. **Criterios de exclusión:** EIT no torácica (cerebral, mama), resúmenes de congreso sin texto completo, duplicados.
5. **Verificación obligatoria:**
   - El DOI o URL debe aparecer en el resultado de la búsqueda; si es posible, comprobarlo en `https://doi.org/<DOI>`.
   - Título, primer autor, año y revista deben coincidir con la fuente.
   - Si algo no se pudo confirmar, registrar la referencia igual pero marcarla `[VERIFICAR]` en `note` y en la tabla.
   - Nunca completar datos bibliográficos de memoria.

## B. Registrar referencias
1. **`bibliografia/referencias.bib`**, una entrada por paper:
   ```bibtex
   @article{ApellidoAAAA_palabra,
     author  = {Apellido, N. and Apellido2, N.},
     title   = {...},
     journal = {...},
     year    = {AAAA}, volume = {..}, number = {..}, pages = {..},
     doi     = {10.xxxx/xxxxx},
     url     = {https://doi.org/10.xxxx/xxxxx},
     note    = {Verificado AAAA-MM-DD | [VERIFICAR]}
   }
   ```
   - Clave: `PrimerApellidoAño_palabraclave`, sin tildes.
   - Datasets: `@misc` con `howpublished` y la URL del repositorio.
2. **`bibliografia/tabla_bibliografia.md`**, una fila por referencia y una línea por celda:
   `| Autor-año | Título | Objetivo | Método | Métricas | Relevancia para mi trabajo |`
   - En Relevancia, decir en qué sección de la tesis se usa (intro, métodos, discusión) y por qué.
3. Mantener el mismo orden en el `.bib` y en la tabla (alfabético por clave). Revisar duplicados por DOI.

## C. Estructura del borrador (IMRyD)
1. **Título** y **Resumen** (≤250 palabras): objetivo, datos, métodos, resultado principal y conclusión.
2. **Introducción**: problema clínico (monitorización de la ventilación), qué es EIT, brecha y objetivo.
3. **Estado del arte**: síntesis de `tabla_bibliografia.md`, agrupada por tema (validación de volumen, procesamiento de señal, ventilación regional, datasets).
4. **Datos**: fuente pública, sujeto, señales, frecuencias de muestreo y licencia.
5. **Métodos**:
   - Pipeline: filtrado, detección de extremos, segmentación y validación de ciclos.
   - Modelo: variables, validación temporal por bloques y métricas.
6. **Resultados**: solo cifras que estén en `resultados/` (tablas y figuras con su ruta de origen).
7. **Discusión**: comparación con la literatura (citar claves del `.bib`).
8. **Limitaciones**: 1 sujeto, ausencia de validación externa, supuestos del pipeline, etc.
9. **Trabajo futuro**.
10. **Referencias**: generadas desde `referencias.bib`.

En todo el borrador, marcar con `[COMPLETAR]` lo que el autor deba revisar o escribir. No inventar cifras ni citas.
