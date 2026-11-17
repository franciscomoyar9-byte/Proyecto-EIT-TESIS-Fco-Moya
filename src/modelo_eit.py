"""Modelo EIT -> volumen tidal por ciclo.

Usa la salida del pipeline (`resultados/matriz_ciclos_todos.csv`); no recalcula ciclos.
Objetivo: predecir `vol_insp_flujo` [L] (volumen inspirado integrado del flujo) a partir
de la variación de impedancia global por ciclo (ΔZ = `amplitud`) y otras características.
Validación: K-fold temporal por bloques contiguos (sin barajar), porque hay un solo sujeto
y los ciclos vecinos están correlacionados.

Uso:  python src/modelo_eit.py   (ejecutar antes src/pipeline_eit.py)
Salidas: resultados/modelo/{metricas_modelo.csv, metricas_modelo.json, predicciones_oof.csv, fig_*.png}
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, RidgeCV
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parents[1]  # raíz del repositorio
ENTRADA = BASE / "resultados" / "matriz_ciclos_todos.csv"
RESUMEN_PIPELINE = BASE / "resultados" / "caracteristicas_todos.csv"
SALIDA = BASE / "resultados" / "modelo"

OBJETIVO = "vol_insp_flujo"
VARS_EIT = ["amplitud", "duracion", "Ti_eit", "auc_insp_rel"]  # solo derivadas de la señal EIT
VARS_MULTI = VARS_EIT + ["presion_media"]  # + presión del circuito (no EIT)
N_BLOQUES = 5
SEMILLA = 0

MODELOS = {
    "Lineal (ΔZ)": (["amplitud"], lambda: LinearRegression()),
    "Ridge (multivariable)": (VARS_MULTI, lambda: make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 13)))),
    "Random Forest (multivariable)": (VARS_MULTI, lambda: RandomForestRegressor(n_estimators=300, min_samples_leaf=5, random_state=SEMILLA)),
    "Ridge (solo EIT)": (VARS_EIT, lambda: make_pipeline(StandardScaler(), RidgeCV(alphas=np.logspace(-3, 3, 13)))),
}

# Paleta categórica validada (skill dataviz, modo claro), en orden fijo por modelo.
COLORES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
TINTA, TINTA_2, GRILLA = "#0b0b0b", "#52514e", "#e4e3df"


def cargar_ciclos() -> pd.DataFrame:
    d = pd.read_csv(ENTRADA)
    valido = d["valido"].astype(str).str.lower().isin(["true", "1"])
    d = d.loc[valido].dropna(subset=VARS_MULTI + [OBJETIVO])
    return d.sort_values("t_inicio").reset_index(drop=True)


def metricas(y, yhat) -> dict:
    dif = yhat - y
    sesgo, de = dif.mean(), dif.std(ddof=1)
    mae = mean_absolute_error(y, yhat)
    return {
        "R2": r2_score(y, yhat),
        "r_pearson": pearsonr(y, yhat)[0],
        "RMSE_L": float(np.sqrt(mean_squared_error(y, yhat))),
        "MAE_L": mae,
        "error_rel_pct": 100 * mae / y.mean(),  # MAE / media del volumen de referencia
        "BA_sesgo_L": sesgo,
        "BA_LoA_inf_L": sesgo - 1.96 * de,
        "BA_LoA_sup_L": sesgo + 1.96 * de,
    }


def validar_por_bloques(d: pd.DataFrame, columnas, fabrica):
    X, y = d[columnas].to_numpy(), d[OBJETIVO].to_numpy()
    pred = np.empty_like(y)
    bloque = np.empty(len(y), dtype=int)
    r2_bloques = []
    for k, (ent, prueba) in enumerate(KFold(N_BLOQUES, shuffle=False).split(X)):
        modelo = fabrica().fit(X[ent], y[ent])
        pred[prueba] = modelo.predict(X[prueba])
        bloque[prueba] = k + 1
        r2_bloques.append(r2_score(y[prueba], pred[prueba]))
    return pred, bloque, r2_bloques


def estilo(ax, titulo, xlabel, ylabel):
    ax.set_title(titulo, fontsize=10, color=TINTA, loc="left")
    ax.set_xlabel(xlabel, fontsize=9, color=TINTA_2)
    ax.set_ylabel(ylabel, fontsize=9, color=TINTA_2)
    ax.tick_params(colors=TINTA_2, labelsize=8)
    ax.grid(color=GRILLA, linewidth=0.6)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(GRILLA)


def graficar(d, preds, tabla):
    y = d[OBJETIVO].to_numpy()
    nombres = list(preds)

    fig, axes = plt.subplots(2, 2, figsize=(9, 8), sharex=True, sharey=True)
    lim = [0, max(y.max(), max(p.max() for p in preds.values())) * 1.05]
    for ax, n, c in zip(axes.flat, nombres, COLORES):
        ax.plot(lim, lim, color=TINTA_2, linewidth=1, linestyle="--")
        ax.scatter(y, preds[n], s=14, color=c, alpha=0.7, edgecolors="white", linewidths=0.5)
        estilo(ax, f"{n}\nR² = {tabla.loc[n, 'R2']:.2f}", "Volumen real [L]", "Volumen predicho [L]")
    fig.tight_layout()
    fig.savefig(SALIDA / "fig_pred_vs_real.png", dpi=200)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharey=True)
    for ax, n, c in zip(axes.flat, nombres, COLORES):
        media, dif = (y + preds[n]) / 2, preds[n] - y
        ax.scatter(media, dif, s=14, color=c, alpha=0.7, edgecolors="white", linewidths=0.5)
        fila = tabla.loc[n]
        for v, etiqueta in [(fila["BA_sesgo_L"], "sesgo"), (fila["BA_LoA_inf_L"], "−1,96 DE"), (fila["BA_LoA_sup_L"], "+1,96 DE")]:
            ax.axhline(v, color=TINTA_2, linewidth=1, linestyle="-" if etiqueta == "sesgo" else "--")
            ax.annotate(f"{etiqueta} {v:+.2f}", (1, v), xycoords=("axes fraction", "data"),
                        ha="right", va="bottom", fontsize=7, color=TINTA_2)
        estilo(ax, n, "Media (real, predicho) [L]", "Predicho − real [L]")
    fig.tight_layout()
    fig.savefig(SALIDA / "fig_bland_altman.png", dpi=200)
    plt.close(fig)

    fig, axes = plt.subplots(len(nombres) + 1, 1, figsize=(11, 10), sharex=True)
    t = d["t_inicio"].to_numpy()
    for ax, n, c in zip(axes, nombres, COLORES):
        ax.axhline(0, color=TINTA_2, linewidth=0.8)
        ax.plot(t, preds[n] - y, color=c, linewidth=1.2)
        estilo(ax, n, "", "Residuo [L]")
    axes[-1].plot(t, d["presion_media"], color=TINTA_2, linewidth=1.2)
    estilo(axes[-1], "Presión media por ciclo (referencia del nivel de PEEP)", "Tiempo [s]", "cmH₂O")
    limites = d.groupby("bloque")["t_inicio"].min().to_numpy()[1:]
    for ax in axes:
        for x in limites:
            ax.axvline(x, color=GRILLA, linewidth=1.2, linestyle=":")
    fig.tight_layout()
    fig.savefig(SALIDA / "fig_residuos_tiempo.png", dpi=200)
    plt.close(fig)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    d = cargar_ciclos()
    y = d[OBJETIVO].to_numpy()

    preds, filas, r2_por_bloque = {}, [], {}
    for nombre, (columnas, fabrica) in MODELOS.items():
        pred, bloque, r2_b = validar_por_bloques(d, columnas, fabrica)
        preds[nombre], r2_por_bloque[nombre] = pred, r2_b
        d["bloque"] = bloque
        filas.append({"modelo": nombre, "variables": "+".join(columnas), **metricas(y, pred)})
    tabla = pd.DataFrame(filas).set_index("modelo")

    r_dz, _ = pearsonr(d["amplitud"], y)
    resumen = {
        "n_ciclos_validos": int(len(d)),
        "objetivo": OBJETIVO,
        "validacion": f"KFold temporal por bloques contiguos, k={N_BLOQUES}, sin barajar",
        "r_pearson_dZ_vs_volumen_sin_modelo": r_dz,
        "volumen_referencia_L": {"media": y.mean(), "DE": y.std(ddof=1), "min": y.min(), "max": y.max()},
        "metricas_oof": tabla.drop(columns="variables").round(4).to_dict(orient="index"),
        "R2_por_bloque": {k: [round(v, 4) for v in vs] for k, vs in r2_por_bloque.items()},
        "metricas_descriptivas_pipeline": pd.read_csv(RESUMEN_PIPELINE, dtype={"Sujeto": str}).iloc[0].to_dict(),
    }

    tabla.round(4).to_csv(SALIDA / "metricas_modelo.csv")
    (SALIDA / "metricas_modelo.json").write_text(json.dumps(resumen, indent=2, ensure_ascii=False, default=float), encoding="utf-8")
    pd.DataFrame({"t_inicio": d["t_inicio"], "bloque": d["bloque"], "real": y, **preds}).to_csv(SALIDA / "predicciones_oof.csv", index=False)
    graficar(d, preds, tabla)

    print(f"Ciclos válidos: {len(d)} | r(ΔZ, volumen) = {r_dz:.3f}")
    print(tabla.drop(columns="variables").round(3).to_string())
    print("R² por bloque:", {k: [round(v, 2) for v in vs] for k, vs in r2_por_bloque.items()})


if __name__ == "__main__":
    main()
