# Material-Analysis-uSing-Python-SQL-Power-BI
 ## This document provides Documentation for the Python-based **(ETL)** pipeline designed to ingest raw material transaction logs and product master data, cleanse and enrich the datasets, and load them into a centralized **MySQL relational database**.   The resulting structured database schema serves as the SSO truth for  (BI) reporting.
 ##ETL FLOW : Sharepoint Folder > Python> SQL>Power BI
 
 ### Primary Data Sources
1. **Material Transaction Logs (`MATERIALTRANSACTION.xlsx`)**
   - **Format**: Excel Spreadsheet (`Sheet1`)
   - **Ingestion Rule**: Skip first 16 header/metadata rows (`skiprows=16`).
   - **Type**: Operational Fact Data containing transaction quantities, inventory movements, order numbers, and costs.

2. **Product Master Data (`Mgrpdb(Sheet1) (1).csv`)**
   - **Format**: Comma-Separated Values (`latin1` character encoding)
   - **Type**: Dimension Data providing material group mappings and item metadata.

---

## 4. Detailed Data Transformation & Cleansing Rules

### A. Fact Table Transformations (`fact_material_transactions`)
* **Column Pruning**: Dropped 20 metadata, accounting, and legacy audit columns to streamline schema size and optimize performance:
* **Data Sanitization**:
  - Empty or whitespace-only values in the `Item` column are replaced with `np.nan` using regular expressions (`^\\s*$`).
  - Rows with missing `Item` values are dropped (`dropna`) to maintain relational integrity.
* **Type Standardizations**:
  - `Order Number` and `Transaction Id` columns are cast to nullable integers (`Int64`) and converted to string representations to prevent scientific notation formatting during SQL ingestion.

### B. Dimension Table Transformations (`dim_product`)
* **Deduplication**: Retained the latest product record per item code using `drop_duplicates(subset=["Item"], keep="last")`.
* **Category Parsing**: Extracted condition indicators embedded within the item SKU structure using Regex pattern matching:
  - **Pattern**: `^[^-]*-[^-]*(\\d)-` (Extracts the single digit occurring between the 2nd and 3rd hyphen).
* **Business Logic Mapping**:
  | Extracted Code | Mapped Category | Description |
  | :---: | :---: | :--- |
  | **1** | `New` | Brand new manufacturing stock |
  | **2** | `New` | Secondary new stock allotment |
  | **3** | `rs1` | Refurbished / Reconditioned Status 1 |
  | **4** | `rs2` | Refurbished / Reconditioned Status 2 |
  | **5** | `repair` | Under maintenance or repair |
  | **6** | `pulled` | Pulled from field service / Decommissioned |
  | *Other / Null* | `Other` | Unclassified items |

---

## 5. Database Target Schema Configuration

The processed datasets are loaded into a **MySQL** database instance.


* **Tables Created**:
  1. `fact_material_transactions`: Stores sanitized transaction logs.
  2. `dim_product`: Stores normalized item master attributes and parsed condition categories.
* **Optimization Parameters**:
  - `if_exists="replace"`: Ensures idempotent pipeline execution.
  - `chunksize=1000`: Batch size optimized for memory-efficient I/O.
  - `method="multi"`: Enables multi-row SQL INSERT statements for optimized throughput.

---

## 6. Reporting Setup (PowerBI)
The database is then connected to Power BI for reporting

* **Connection Method**:
  Hybrid of Direct Query and Import
* ** Refresh**:
  Scheduled refreshing
* **Implemented**:
  1, Data Modeling
  2, Creation of dim_date table
  3, Defined KPIs and visualised and analysed data
  4, Implemented RLS and subsription based report sharing
