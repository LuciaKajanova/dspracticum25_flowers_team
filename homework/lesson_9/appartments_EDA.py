import pandas as pd
import numpy as np

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error


# ======================================================
# 1. Načítanie dát
# ======================================================

train = pd.read_csv("appartments_train.csv")
test  = pd.read_csv("appartments_test.csv")

# Cieľová premenná
y = train["price"]

# Stĺpce, ktoré z modelu nechceme (ID, text, dátumy, adresa)
drop_cols = ["price", "id", "address", "text", "first_seen", "last_seen"]

X = train.drop(columns=drop_cols)
X_test_final = test.drop(columns=drop_cols[1:])  # tu neexistuje "price"

# ======================================================
# 2. Custom transformer: imputácia total_floors podľa construction
# ======================================================

class TotalFloorsByConstruction(BaseEstimator, TransformerMixin):
    """
    Vyplní chýbajúce total_floors mediánom v rámci skupiny 'construction'.
    Predpokladá, že vstup je pandas DataFrame obsahujúci stĺpce:
    - 'construction'
    - 'total_floors'
    """
    def __init__(self, construction_col="construction", floors_col="total_floors"):
        self.construction_col = construction_col
        self.floors_col = floors_col
        self.medians_ = None

    def fit(self, X, y=None):
        X_df = X.copy()
        # spočítame mediány podľa typu konstrukcie
        self.medians_ = (
            X_df.groupby(self.construction_col)[self.floors_col]
                .median()
                .to_dict()
        )
        # fallback: ak by niektorá construction nebola v medians_
        self.global_median_ = X_df[self.floors_col].median()
        return self

    def transform(self, X):
        X = X.copy()
        mask_na = X[self.floors_col].isna()

        # pre NA hodnoty vyber median podľa construction
        def fill_value(row):
            cons = row[self.construction_col]
            if pd.isna(row[self.floors_col]):
                return self.medians_.get(cons, self.global_median_)
            else:
                return row[self.floors_col]

        if mask_na.any():
            X.loc[mask_na, self.floors_col] = X[mask_na].apply(fill_value, axis=1)

        return X


# ======================================================
# 3. Definícia numerických a kategóriálnych stĺpcov
# ======================================================

# po custom tranformeri zostanú názvy stĺpcov rovnaké
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

print("Numeric columns:", numeric_cols)
print("Categorical columns:", categorical_cols)

# ======================================================
# 4. Predspracovanie: ColumnTransformer
# ======================================================

# numerické: NA -> median
numeric_transformer = SimpleImputer(strategy="median")

# kategórie: NA -> "Unknown", následne OneHotEncoder
categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse=False))
])

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols)
    ]
)

# ======================================================
# 5. Celá pipeline: custom transformer + preprocess + model
# ======================================================

model = RandomForestRegressor(
    n_estimators=300,
    max_depth=None,
    random_state=42,
    n_jobs=-1
)

pipe = Pipeline(steps=[
    ("group_imputer", TotalFloorsByConstruction(
        construction_col="construction",
        floors_col="total_floors"
    )),
    ("preprocess", preprocess),
    ("model", model)
])

# ======================================================
# 6. Train/valid split + tréning + MAPE
# ======================================================

X_train, X_val, y_train, y_val = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

pipe.fit(X_train, y_train)

y_val_pred = pipe.predict(X_val)

mape_val = mean_absolute_percentage_error(y_val, y_val_pred) * 100
print(f"Validation MAPE: {mape_val:.2f} %")

# ======================================================
# 7. Tréning na všetkých train dátach a predikcia pre test
# ======================================================

pipe.fit(X, y)

test_pred = pipe.predict(X_test_final)

submission = pd.DataFrame({
    "id": test["id"],
    "price": test_pred
})

submission.to_csv("submission.csv", index=False)
print("Uložené do 'submission.csv'")
