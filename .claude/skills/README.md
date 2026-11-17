# Skills de Claude Code

Una *skill* es un conjunto de instrucciones reutilizables que Claude Code carga cuando la tarea lo requiere.
Las skills de esta carpeta (`.claude/skills/<nombre>/SKILL.md`) se detectan automáticamente al abrir el proyecto
en VS Code con Claude Code, y también se pueden invocar escribiendo `/<nombre>` en el chat.

| Skill | Para qué sirve | Se usa en |
|---|---|---|
| [`investigacion-eit`](investigacion-eit/SKILL.md) | (A) buscar y verificar papers de EIT pulmonar (palabras clave, fuentes, criterios de inclusión y exclusión, verificación de DOI); (B) registrar referencias en `bibliografia/referencias.bib` y `tabla_bibliografia.md`; (C) estructura IMRyD del borrador | Fase 2 (bibliografía) y Fase 4 (borrador) |

## Formato de una skill

```markdown
---
name: nombre-de-la-skill
description: Cuándo debe usarse (Claude Code lo lee para decidir si cargarla).
---
# Instrucciones
...
```

Para agregar una nueva skill, crea `.claude/skills/<nombre>/SKILL.md` con ese formato.
