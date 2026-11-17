# Datos

## Fuente

**Respiratory dataset from PEEP study with expiratory occlusion**, versión 1.0.0
Guy, E. F. S., Clifton, J. A., Caljé-van der Klei, T., Chen, R., Knopp, J., Moeller, K., & Chase, J. G. (2023). PhysioNet.
https://doi.org/10.13026/d767-e709 · https://physionet.org/content/respiratory-dataset/1.0.0/

Artículo descriptor: Guy et al. (2024), *Data in Brief* 52, 109874. https://doi.org/10.1016/j.dib.2023.109874

PhysioNet también pide citar: Goldberger et al. (2000), *Circulation* 101(23), e215–e220.

- **Licencia:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/),
  acceso abierto. Se redistribuye aquí sin modificaciones, con la atribución indicada arriba.
- **Protocolo:** 80 adultos, CPAP con PEEP creciente en pasos de 0,5 cmH2O cada 30 s, oclusiones espiratorias
  rápidas y EIT con Dräger PulmoVista 500.

## Archivo incluido

`ProcessedData_Subject03.csv` (sujeto 03, carpeta `Processed_Dataset` del repositorio original).
Para analizar otros sujetos, descarga sus `ProcessedData_SubjectXX.csv` en esta carpeta: el pipeline procesa todos
los archivos que coincidan con `ProcessedData_Subject*.csv`.

| Columna | Unidad | Frecuencia | Descripción |
|---|---|---|---|
| `Time [s]` | s | 100 Hz | tiempo de la señal de flujo y presión |
| `Pressure [cmH2O]` | cmH2O | 100 Hz | presión en la vía aérea |
| `Flow [L/s]` | L/s | 100 Hz | flujo |
| `V_tidal [L]` | L | 100 Hz | volumen tidal |
| `Chest [mm]`, `Abd [mm]` | mm | 100 Hz | circunferencia torácica y abdominal |
| `Inspiratory Indicies` | índice de fila | – | inicios inspiratorios (serie de flujo) |
| `Time (Aeration Data)_[s]` | s | 50 Hz | tiempo de la serie EIT (0 = fila sin dato EIT) |
| `Global Aeration` | u.a. | 50 Hz | aireación global EIT |
| `Inspiratory Indicies (Aeration Data)` | índice de fila | – | inicios inspiratorios (serie EIT) |
