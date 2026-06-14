# Wikipedia-Traffic-Forecasting-MLOps-Platform
Here's what **every file/folder in the repository is for** once the project is complete.

```text
wikipedia-traffic-forecasting/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
├── notebooks/
├── src/
├── models/
├── mlruns/
├── api/
├── tests/
├── docker/
└── configs/
```

---

# Root Files

## README.md

Project documentation.

Contains:

* Project overview
* Dataset description
* Architecture diagram
* Setup instructions
* API usage
* Results

---

## requirements.txt

Python dependencies.

Example:

```txt
pandas
numpy
lightgbm
xgboost
scikit-learn
mlflow
fastapi
uvicorn
requests
```

---

## .gitignore

Prevents large/generated files from entering git.

Example:

```text
data/
mlruns/
__pycache__/
*.pkl
*.parquet
```

---

# data/

Stores datasets.

```text
data/
├── raw/
├── processed/
└── monitoring/
```

---

## data/raw/

Raw data directly from Wikimedia.

### pages.csv

Top 500 selected pages.

```csv
page_name,total_views
ChatGPT,145823912
...
```

---

### pageviews.csv

Raw history.

```csv
page_name,date,views
ChatGPT,2021-07-01,12345
...
```

---

## data/processed/

Feature engineered data.

### features.csv

Contains:

```text
lag_1
lag_7
lag_30
rolling_mean_7
...
target_views
```

Used for training.

---

## data/monitoring/

Production monitoring logs.

### predictions.csv

Stores predictions.

```csv
page,prediction_date,predicted_views
```

---

### actuals.csv

Stores actual traffic.

```csv
page,date,actual_views
```

---

### metrics.csv

Stores errors.

```csv
page,date,mape
```

---

# notebooks/

Exploration and experimentation.

---

## 01_dataset_exploration.ipynb

Check:

* Missing values
* Traffic trends
* Popular pages

---

## 02_feature_engineering.ipynb

Prototype lag features.

---

## 03_model_experiments.ipynb

Try:

* Linear Regression
* RF
* XGBoost
* LightGBM

before productionizing.

---

# src/

Actual project code.

---

# src/ingestion/

Dataset generation.

---

## top_pages.py

Gets top pages from Wikimedia.

Produces:

```text
pages.csv
```

---

## page_history.py

Downloads 1800-day history.

Produces:

```text
pageviews.csv
```

---

## build_dataset.py

Runs the entire ingestion pipeline.

```bash
python build_dataset.py
```

---

# src/features/

Feature engineering.

---

## lag_features.py

Creates:

```python
lag_1
lag_7
lag_30
```

---

## build_features.py

Generates final ML dataset.

Produces:

```text
features.csv
```

---

# src/training/

Model training.

---

## train.py

Trains models.

Produces:

```text
model.pkl
```

and MLflow runs.

---

## evaluate.py

Computes:

```text
MAE
RMSE
MAPE
```

Selects best model.

---

## mlflow_utils.py

Helper functions for:

```text
log_params
log_metrics
register_model
```

---

# src/inference/

Prediction logic.

---

## feature_builder.py

Creates inference features from recent history.

---

## predict.py

Loads model and predicts tomorrow's views.

---

# src/monitoring/

Production monitoring.

---

## collect_actuals.py

Downloads actual pageviews after predictions are made.

---

## compute_metrics.py

Computes production errors.

---

## drift_detection.py

Checks:

```text
rolling_mape
```

Triggers retraining if threshold exceeded.

---

# src/retraining/

Retraining workflow.

---

## retrain.py

Retrains model using latest data.

---

## model_selection.py

Compares:

```text
candidate model
vs
production model
```

Promotes if better.

---

# models/

Stores models.

```text
models/
├── staging/
└── production/
```

---

## production/

Currently deployed model.

---

## staging/

New candidate models.

---

# mlruns/

Automatically created by MLflow.

Contains:

```text
Experiments
Metrics
Artifacts
Models
```

Usually not committed to git.

---

# api/

FastAPI application.

---

## main.py

Defines endpoints.

Example:

```http
POST /predict
```

---

## schemas.py

Pydantic request/response schemas.

Example:

```python
PredictRequest
PredictResponse
```

---

# tests/

Unit tests.

---

## test_features.py

Verify lag feature creation.

---

## test_training.py

Verify training pipeline.

---

## test_api.py

Verify FastAPI endpoint.

---

# docker/

Containerization.

---

## Dockerfile.api

Container for inference service.

---

## Dockerfile.training

Container for training jobs.

---

# configs/

Configuration files.

---

## data.yaml

Dataset settings.

```yaml
top_pages: 500
history_days: 1800
```

---

## training.yaml

Training hyperparameters.

```yaml
model: lightgbm
```

---

## monitoring.yaml

Monitoring thresholds.

```yaml
mape_threshold: 15
```

---

If I were building this today, I'd start with only:

```text
src/ingestion/
data/raw/
README.md
requirements.txt
```

and add the other folders only when you reach that stage. Prematurely creating everything often leads to a lot of empty files.
