from pathlib import Path
import pandas as pd
import math

# ==============================
# 1. PATHS
# ==============================
base = Path("/Users/keertanachagari/DB_project/cleaned_data")

patient_file = base / "cleaned_data_clinical_patient.txt"
sample_file = base / "cleaned_data_clinical_sample.txt"
mutation_file = base / "cleaned_data_mutations.txt"
mrna_file = base / "cleaned_data_mrna_seq_rsem.txt"
mrna_z_file = base / "cleaned_data_mrna_seq_rsem_zscores_ref_all_samples.txt"
protein_file = base / "cleaned_data_protein_quantification.txt"
protein_z_file = base / "cleaned_data_protein_quantification_zscores.txt"
gene_panel_file = base / "cleaned_data_gene_panel_matrix.txt"

output_sql = Path.home() / "Desktop" / "tnbc_load.sql"

# ==============================
# 2. HELPERS
# ==============================
def is_blank(x):
    return pd.isna(x) or str(x).strip() in ["", "nan", "None"]

def sql_str(x):
    return "NULL" if is_blank(x) else "'" + str(x).replace("'", "''") + "'"

def sql_num(x):
    return "NULL" if is_blank(x) else str(x)

def chunks(lst, n=500):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def bulk_insert(table, cols, rows):
    if not rows:
        return ""
    out = []
    for part in chunks(rows):
        values = ",\n ".join(["(" + ", ".join(r) + ")" for r in part])
        out.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES\n{values};\n\n")
    return "".join(out)

# ==============================
# 3. LOAD DATA
# ==============================
patient_df = pd.read_csv(patient_file, sep="\t")
sample_df = pd.read_csv(sample_file, sep="\t")
mutation_df = pd.read_csv(mutation_file, sep="\t")

mrna_df = pd.read_csv(mrna_file, sep="\t")
mrna_z_df = pd.read_csv(mrna_z_file, sep="\t")

protein_df = pd.read_csv(protein_file, sep="\t")
protein_z_df = pd.read_csv(protein_z_file, sep="\t")

gene_panel_df = pd.read_csv(gene_panel_file, sep="\t")

# ==============================
# 4. PATIENT TABLE
# ==============================
patient_rows = []
patient_map = {}

for i, r in patient_df.iterrows():
    pid = r["PATIENT_ID"]
    race = r["RACE"]
    patient_rows.append((sql_str(race),))
    patient_map[pid] = f"(SELECT patient_id FROM Patient WHERE race={sql_str(race)} LIMIT 1)"

# ==============================
# 5. SAMPLE TABLE
# ==============================
sample_rows = []

gene_panel_map = dict(zip(gene_panel_df["SAMPLE_ID"], gene_panel_df["mutations"]))

for _, r in sample_df.iterrows():
    sid = r["SAMPLE_ID"]
    pid = r["PATIENT_ID"]

    patient_fk = f"(SELECT patient_id FROM Patient WHERE race={sql_str(patient_df.loc[patient_df.PATIENT_ID==pid,'RACE'].values[0])} LIMIT 1)"

    sample_rows.append((
        sql_str(sid),
        patient_fk,
        sql_str(r["PCR_RESPONSE"]),
        sql_str(r["COLLECTION_EVENT"]),
        sql_str(r["PAM50_SUBTYPE"]),
        sql_str(r["TNBC_SUBTYPE"]),
        sql_str(r["RCB"]),
        sql_num(r["TUMOR_CONTENT"]),
        sql_str(r["CD3_PERCENT"]),
        sql_str(r["PDL1_CPS"]),
        sql_num(r["CIN"]),
        sql_str(r["MUTATION_LOAD"]),
        sql_str(r["MSI_SCORE"]),
        sql_num(r["XCELL_IMMUNE"]),
        sql_num(r["XCELL_STROMA"]),
        sql_num(r["TP_ESTIMATE"]),
        sql_num(r["PBMGP_SCORE"]),
        sql_num(r["RNA_SCORE"]),
        sql_str(r["LIG1_CLASSIFICATION"]),
        sql_str(r["SOMATIC_STATUS"]),
        sql_str(r["ONCOTREE_CODE"]),
        sql_str(r["TREATMENT_STATUS"]),
        sql_str(gene_panel_map.get(sid)),
        sql_str(gene_panel_map.get(sid))
    ))

# ==============================
# 6. GENE TABLE
# ==============================
genes = set()

# from mutation file
for _, r in mutation_df.iterrows():
    genes.add((r["Entrez_Gene_Id"], r["Hugo_Symbol"], r["Chromosome"]))

gene_rows = [(sql_num(e), sql_str(h), sql_str(c)) for (e,h,c) in genes if not is_blank(e)]

# ==============================
# 7. MUTATION TABLE
# ==============================
mutation_rows = []

for _, r in mutation_df.iterrows():
    mutation_rows.append((
        sql_str(r["Tumor_Sample_Barcode"]),
        sql_num(r["Entrez_Gene_Id"]),
        sql_num(r["Start_Position"]),
        sql_num(r["End_Position"]),
        sql_str(r["Consequence"]),
        sql_str(r["Variant_Classification"]),
        sql_str(r["Variant_Type"]),
        sql_str(r["Reference_Allele"]),
        sql_str(r["Tumor_Seq_Allele2"]),
        sql_num(r["t_ref_count"]),
        sql_num(r["t_alt_count"]),
        sql_str(r["HGVSc"]),
        sql_str(r["HGVSp"]),
        sql_str(r["Transcript_ID"])
    ))

# ==============================
# 8. mRNA EXPRESSION (LONG FORMAT)
# ==============================
mrna_long = mrna_df.melt(id_vars=["Hugo_Symbol"], var_name="sample_id", value_name="rsem")
mrna_z_long = mrna_z_df.melt(id_vars=["Hugo_Symbol"], var_name="sample_id", value_name="zscore")

mrna_merged = mrna_long.merge(mrna_z_long, on=["Hugo_Symbol","sample_id"])

mrna_rows = []
for _, r in mrna_merged.iterrows():
    mrna_rows.append((
        sql_str(r["sample_id"]),
        f"(SELECT entrez_gene_id FROM Gene WHERE hugo_symbol={sql_str(r['Hugo_Symbol'])} LIMIT 1)",
        sql_num(r["rsem"]),
        sql_num(r["zscore"])
    ))

# ==============================
# 9. PROTEIN (LONG FORMAT)
# ==============================
prot_long = protein_df.melt(id_vars=["Composite.Element.REF"], var_name="sample_id", value_name="abundance")
prot_z_long = protein_z_df.melt(id_vars=["Composite.Element.REF"], var_name="sample_id", value_name="zscore")

prot = prot_long.merge(prot_z_long, on=["Composite.Element.REF","sample_id"])

protein_rows = []
for _, r in prot.iterrows():
    gene_symbol = r["Composite.Element.REF"].split("|")[0]
    protein_rows.append((
        sql_str(r["sample_id"]),
        f"(SELECT entrez_gene_id FROM Gene WHERE hugo_symbol={sql_str(gene_symbol)} LIMIT 1)",
        sql_num(r["abundance"]),
        sql_num(r["zscore"])
    ))

# ==============================
# 10. WRITE SQL
# ==============================
sql = []
sql.append("START TRANSACTION;\n\n")

sql.append(bulk_insert("Patient", ["race"], patient_rows))
sql.append(bulk_insert("Gene", ["entrez_gene_id","hugo_symbol","chromosome"], gene_rows))
sql.append(bulk_insert("Sample", [
    "sample_id","patient_id","pCR_response","collection_event","pam50_subtype",
    "TNBC_subtype","residual_cancer_burden","tumor_content","CD3_pos_IHC",
    "PDL1_combined_pos_score","chromosomal_instability","nonsyn_mutation_load",
    "somatic_MSI","immune_score","stromal_score","tumor_purity",
    "pbmgp_score","rna_score","LIG1_classification","somatic_status",
    "oncotree_code","treatment_status","mutations_profile","gistic_profile"
], sample_rows))

sql.append(bulk_insert("Mutation", [
    "sample_id","entrez_gene_id","chrom_start_pos","chrom_end_pos","consequence",
    "variant_classification","variant_type","ref_allele","alt_allele",
    "tumor_ref_count","tumor_alt_count","hgvs_c","hgvs_p","transcript_id"
], mutation_rows))

sql.append(bulk_insert("mRNA_expression",
    ["sample_id","entrez_gene_id","rsem_value","zscore"], mrna_rows))

sql.append(bulk_insert("Protein_quant",
    ["sample_id","entrez_gene_id","abundance","zscore"], protein_rows))

sql.append("COMMIT;")

output_sql.write_text("".join(sql))
print("SQL file generated:", output_sql)
