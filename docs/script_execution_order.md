Script Execution Order:

Overview:
This document describes the step-by-step workflow used to clean data, generate SQL files, create the database schema, and load data into the database.

1)Download data
- Download the Triple Negative Breast Cancer (DLDCCC, Cancer Discov 2022) dataset from https://www.cbioportal.org/study/summary?id=brca_dldccc_2022


2)Data cleaning
Run 01_clean_data.py in the same directory as the raw downloaded data to clean raw data files:
- removes unnecessary lines
- standardizes missing values
- removes duplicates
- removes biologically impossible values
- ensures identifiers match across datasets
- saves the cleaned files


3)Table creation
- Create a new database on phpMyAdmin and name it TripleNegativeBreastCancer
- Run 01_clean_schema.sql on phpMyAdmin or terminal to generate the tables for the database


4)Create .sql file for populating the entire database
- Run 02_generate_sql_load.py to generate 02_load_full_database.sql, the file used to populate the entire database at once


Limitation of populating at once: time consuming and hard to troubleshoot
- Solution: split the populating so it is done by table (as detailed in the steps below)


5)Split populating so it is done one table at a time
- Run 03_split_sql_by_table.py to generate seperate .sql files per table to run one at a time
Should get these files:
- gene.sql
- patient.sql (manually renamed to 04_load_patient_table.sql)
- sample.sql (manually renamed to 05_load_sample_table.sql)
- mutation.sql
- protein_quant.sql
- mrna_expression.sql


6)Remove duplicated genes
- Run 04_remove_duplicate_genes.py to remove duplicated genes still in gene.sql, generating 03_load_gene_table.sql


7)Load Gene table
- Run 03_load_gene_table.sql to populate the gene table


8)Load Patient table
- Run 04_load_patient_table.sql to populate the Patient table


9)Load Sample table
- Run 05_load_sample_table.sql to populate the Sample table


10)Remove extra entrez gene ids from Mutation table
- Run 05_fix_missing_mutation_rows.py to remove the entrez_gene_ids in mutation.sql that are not present in the Gene table, generatating 06_load_mutation_table.sql


11)Load Mutation table
- Run 06_load_mutation_table.sql to populate the Mutation table


12)Split populating mRNA_expression table into batches
- Run 06_fix_mrna_expression.py to break populating the table into batches so it is not using too much time and memory to insert everything at once. It also removes 
any null entrez_gene_ids and any syntax issues

13)Load mRNA_expression table
- Run 07_load_mrna_expression_table.sql to populate the mRNA_expression table


14)Split Protein_quant table into batches
- Run 07_fix_protein_table.py to split the populating into batches (same reason as Step #11) and removes the entrez_gene_ids in protein_quant.sql not present in the
 Gene table, generating 08_load_protein_quant_table.sql


15)Load Protein_quant table:
- Run 08_load_protein_quant_table.sql to populate the Protein_quant table


16)Testing
- Run the DQL examples in sql/queries/queries.sql to test the data in the now fully populated TripleNegativeBreastCancer database!!
