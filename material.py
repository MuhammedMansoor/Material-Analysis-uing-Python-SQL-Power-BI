## 6. Python Pipeline Source Code

```python
import numpy as np
import openpyxl
import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import URL, create_engine

# ---------------------------------------------------------
# 1. Extract & Transform: Fact Material Transactions
# ---------------------------------------------------------
fact_mat = pd.read_excel(
    xxxxxx",
    sheet_name="xxxx",
    skiprows=16,
    index_col=0,
)

# Columns excluded for reporting optimization
cols_to_drop = [
    xxxx
]
fact_mat = fact_mat.drop(columns=cols_to_drop, errors="ignore")

# Clean blank items and handle data types
fact_mat["xxxx"] = fact_mat["xxxx"].replace(r"^\\s*$", np.nan, regex=True)
fact_mat = fact_mat.dropna(subset=["xxxx"])

cols_to_convert = ["xxxx"]
fact_mat[cols_to_convert] = fact_mat[cols_to_convert].astype("Int64").astype(str)


# ---------------------------------------------------------
# 2. Extract & Transform: Dimension Product Master
# ---------------------------------------------------------
dim_product = pd.read_csv(
    xxxx,
    encoding="latin1",
)

# Deduplicate product records
dim_product = dim_product.drop_duplicates(subset=["xxxx"], keep="last")

# Extract category digit from SKU string structure
extracted_digit = dim_product["xxxx"].astype(str).str.extract(r"^[^-]*-[^-]*(\\d)-")[0]

# Business mapping logic
category_map = {
    "1": "New",
    "2": "New",
    "3": "rs1",
    "4": "rs2",
    "5": "repair",
    "6": "pulled",
}

dim_product["item category"] = extracted_digit.map(category_map).fillna("Other")
dim_product.set_index("Item")


# ---------------------------------------------------------
# 3. Load: Database Engine Setup & Export
# ---------------------------------------------------------
connection_url = URL.create(
    drivername="mysql+pymysql",
    username="xxxx",
    password="xxxxxx",
    host="xxxx",
    port=xxxx,
    database="xxxx",
)
engine = create_engine(connection_url)

# Load Fact Table
fact_mat.to_sql(
    name="fact_material_transactions",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000,
    method="multi",
)

# Load Dimension Table
dim_product.to_sql(
    name="dim_product",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=1000,
    method="multi",
)

print(
    f"Successfully exported {len(fact_mat)} rows from material transaction "
    f"& {len(dim_product)} rows to 'mat_transactio_analysis' schema!"
)
