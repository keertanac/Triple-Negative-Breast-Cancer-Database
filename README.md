# Triple-Negative-Breast-Cancer-Database

## Overview
This project designs and builds a relational database to store and analyze multi-omics data from a triple-negative breast cancer (TNBC) dataset (DLDCCC, *Cancer Discovery* 2022).

## Dataset
Data was obtained from cBioPortal:  
https://www.cbioportal.org/study/summary?id=brca_dldccc_2022 

Includes:
- Clinical data (patient and sample metadata)
- RNA-seq gene expression data
- Protein quantification data
- Somatic mutation data

Final dataset:
- **59 patients**
- **79 samples**

---

## Database Schema

### Core Tables
Full ER diagram: `diagrams/final_er_diagram.png`
- **Patient** → patient-level information  
- **Sample** → information for each individual sample  
- **Gene** → reference table for gene identifiers  
- **Mutation** → mutation events per sample  
- **mRNA_expression** → gene expression values per sample  
- **Protein_quant** → protein abundance per sample

### Relationships
- One patient → many samples  
- One sample → many mutations  
- One gene → many mutations  
- Many-to-many:
  - Sample ↔ Gene (mRNA_expression)
  - Sample ↔ Gene (Protein_quant)

---

## Workflow

The full pipeline is documented in:  `docs/script_execution_order.md`

### Summary:
1. Download data from cBioPortal
2. Clean raw data using Python
3. Create database schema (MySQL)
4. Generate SQL insert statements
5. Load data (split by table for debugging)
6. Validate data using DQL queries

---

## How to Run

1. Clean data by running 01_clean_data.py
2. Create and name a new database ('TripleNegativeBreastCancer') in phpMyAdmin
3. Create the schema by uploading 01_create_schema.sql directly into phpMyAdmin or by running:

```bash
#install mysql
sudo dnf install mysql

#use the following to create the schema, assuming your shared folder is named sf_database:
mysql -h 127.0.0.1 -P 3306 -u root -pinstructor < /media/sf_database/01_create_schema.sql
```

4. Follow instructions outlined in `docs/script_execution_order.md` to generate SQL load files
5. Populate tables (example for Gene table):

```bash
mysql -h 127.0.0.1 -P 3306 -u root -pinstructor < /media/sf_database/03_load_gene_table.sql
```
6. Test the data by running queries in `sql/queries/queries.sql`

---

## Project Documentation
- Data Dictionary --> `docs/data_dictionary.md`
- Decisions and Limitations --> `docs/decisions_and_limitations.md`
- Execution Workflow --> `docs/script_execution_order.md`
- Full Write-Up --> `docs/project_writeup.pdf`

---

## Future Work
- Integrate Neo4j to explore relationships within the data
