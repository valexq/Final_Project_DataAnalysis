# Proyecto de analítica de datos y modelo predictivo sobre cambio climático

Proyecto integrador orientado al desarrollo de una solución completa de análisis de datos, inteligencia de negocios y aprendizaje computacional, utilizando indicadores climáticos globales como caso de estudio.

El proyecto implementa un flujo de trabajo end-to-end que incluye procesos ETL, análisis exploratorio de datos (EDA), visualización de información, generación de dashboards y construcción de modelos predictivos supervisados.
## Integrantes

Grupo 5

| Nombre | Fase principal | GitHub |
| --- | --- | --- |
| Vanessa Alfaro |  | `@valexq` |
| Juan Manuel Valencia |  | `@Juanchos2905` |
| Ziuvar Ruiz | Fases 1 y 2 - ETL y EDA | `@ziuvar` |
| Juan Cardona | | `@jcardser` |
---

# 1. Descripción del proyecto

Este proyecto tiene como objetivo analizar indicadores relacionados con el cambio climático en múltiples países entre los años 2000 y 2023, utilizando técnicas de analítica de datos y aprendizaje automático para extraer patrones, generar conocimiento útil y construir modelos predictivos.

El dataset incluye variables como:

- Temperatura promedio
- Emisiones de CO₂
- Nivel del mar
- Precipitaciones
- Participación de energías renovables
- Área forestal
- Eventos climáticos extremos

A partir de estos datos se desarrolló una solución analítica completa que permite:

- Procesar y transformar datos mediante pipelines ETL.
- Analizar tendencias y correlaciones climáticas.
- Generar visualizaciones y dashboards interactivos.
- Construir modelos predictivos supervisados.
- Formular conclusiones y recomendaciones basadas en evidencia.

---

# 2. Objetivos

## Objetivo general

Desarrollar un proyecto integral de análisis de datos y aprendizaje computacional aplicado al estudio del cambio climático, incorporando procesos ETL, inteligencia de negocios y modelado predictivo.

## Objetivos específicos

- Identificar y transformar fuentes de datos relevantes.
- Realizar limpieza y análisis exploratorio de datos.
- Diseñar visualizaciones y dashboards para apoyar la toma de decisiones.
- Implementar modelos de aprendizaje supervisado.
- Evaluar el rendimiento de los modelos mediante métricas apropiadas.
- Generar conclusiones y recomendaciones estratégicas.

---

# 3. Relación con los resultados de aprendizaje

## Inteligencia de Negocios (BI)

- Definición de reglas de negocio para el tratamiento de datos.
- Diseño de un modelo de datos para explotación analítica.
- Creación de dashboards interactivos para visualización de insights.

## Analítica de datos (AD)

- Implementación del proceso ETL.
- Limpieza y transformación de datos.
- Análisis exploratorio y visualización de patrones.

## Aprendizaje computacional (AC)

- Implementación de modelos supervisados.
- Evaluación mediante métricas de desempeño.
- Aplicación de técnicas de Machine Learning.

---

# 4. Tecnologías utilizadas

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11 |
| Manipulación de datos | pandas, numpy |
| Visualización | matplotlib, seaborn, plotly |
| Machine Learning | scikit-learn |
| Notebooks | Jupyter Notebook |
| Persistencia | CSV, Parquet |
| Testing | pytest |

---

# 5. Arquitectura del proyecto

```text
climate_analytics_project/
│
├── data/
│   ├── raw/              # Datos originales
│   ├── cleaned/          # Datos limpios
│   ├── processed/        # Datos transformados
│   └── external/         # Datos externos de apoyo
│
├── notebooks/            # Notebooks del análisis
│
├── reports/
│   ├── figures/          # Gráficas exportadas
│   ├── tables/           # Tablas y métricas
│   └── final_report/     # Informe final
│
├── src/                  # Código fuente reutilizable
│
├── tests/                # Pruebas unitarias
│
├── requirements.txt
├── environment.yml
└── README.md
```

---

# 6. Fase 1 - Recopilación y Transformación de Datos

Esta fase implementa el proceso ETL solicitado en el documento del proyecto. La fuente principal es `data/raw/climate_change_dataset.csv`, un dataset climático con 1,000 registros, 15 países y periodo 2000-2023.

## Objetivo de la fase

Dejar una base limpia, validada y documentada para que las siguientes fases puedan desarrollar EDA, inteligencia de negocios y modelado predictivo sin repetir tareas de preparación.

## Proceso implementado

- Extracción del CSV original desde `data/raw/`.
- Normalización de nombres de columnas a formato `snake_case`.
- Conversión de tipos de dato.
- Limpieza de espacios en variables de texto.
- Eliminación de duplicados exactos si existen.
- Ordenamiento por país y año.
- Validación de reglas de calidad: años 2000-2023, población positiva, porcentajes entre 0 y 100 y métricas climáticas no negativas.
- Generación de datasets limpios, dataset procesado, reporte de calidad y diccionario de datos.

## Cómo ejecutar la fase

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar el ETL:

```bash
python -m src.etl
```

Ejecutar pruebas:

```bash
python -m pytest
```

## Entregables generados

| Archivo | Uso |
| --- | --- |
| `notebooks/00_data_collection_transformation.ipynb` | Notebook explicativo de la fase 1 |
| `data/cleaned/climate_change_cleaned.csv` | Dataset limpio para EDA |
| `data/processed/climate_change_model_ready.csv` | Dataset procesado para BI y modelado |
| `reports/tables/data_quality_report.csv` | Reporte de calidad por columna |
| `reports/tables/data_quality_rules.csv` | Resultado de reglas de validación |
| `reports/tables/data_dictionary.csv` | Diccionario de datos |

## Uso por las siguientes fases

- Fase 2 - EDA: usar `data/cleaned/climate_change_cleaned.csv`.
- Fase 3 - BI: usar `data/processed/climate_change_model_ready.csv` y `reports/tables/data_dictionary.csv`.
- Fase 4 - Modelado predictivo: usar el dataset procesado y realizar allí el split, escalado, codificación y entrenamiento.

---

# 7. Fase 2 - Análisis Exploratorio de Datos (EDA)

Esta fase utiliza el dataset limpio generado en la fase 1 para revisar la calidad final de los datos, analizar su comportamiento inicial y construir visualizaciones de apoyo para BI y modelado.

## Proceso implementado

- Confirmación de valores faltantes, duplicados y estructura del dataset limpio.
- Estadísticas descriptivas de las variables numéricas.
- Resúmenes agregados por país y por año.
- Visualización de distribuciones, tendencias temporales y relaciones entre variables.
- Cálculo de matriz de correlación y ranking de correlaciones más relevantes.

## Cómo ejecutar la fase

```bash
python -m src.eda
```

## Entregables generados

| Archivo | Uso |
| --- | --- |
| `notebooks/01_data_understanding.ipynb` | Notebook ejecutado de EDA |
| `reports/tables/eda_preliminary_summary.csv` | Resumen preliminar del dataset limpio |
| `reports/tables/eda_numeric_summary.csv` | Estadísticas descriptivas |
| `reports/tables/eda_country_summary.csv` | Indicadores agregados por país |
| `reports/tables/eda_yearly_summary.csv` | Indicadores agregados por año |
| `reports/tables/eda_correlation_matrix.csv` | Matriz de correlación |
| `reports/tables/eda_top_correlations.csv` | Ranking de correlaciones |
| `reports/figures/eda_distributions.png` | Distribuciones de variables |
| `reports/figures/eda_yearly_trends.png` | Tendencias anuales |
| `reports/figures/eda_correlation_heatmap.png` | Mapa de calor de correlaciones |
| `reports/figures/eda_country_temperature_co2.png` | Relación por país entre temperatura, CO2 y energía renovable |
