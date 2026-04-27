#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os

############################################
# SETTINGS
############################################

INPUT_FILES = [
    "data_clinical_patient.txt",
    "data_clinical_sample.txt",
    "data_cna.txt",
    "data_log2_cna.txt",
    "data_gene_panel_matrix.txt",
    "data_mrna_seq_rsem.txt",
    "data_mrna_seq_rsem_zscores_ref_all_samples.txt",
    "data_mutations.txt",
    "data_protein_quantification.txt",
    "data_protein_quantification_zscores.txt"
]

OUTPUT_DIR = "cleaned_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)


############################################
# GENERAL CLEANING FUNCTIONS
############################################

def load_data(file):
    """
    Load data while removing metadata/comment rows.
    """
    return pd.read_csv(
        file,
        sep="\t",
        comment="#",
        low_memory=False
    )


def standardize_missing(df):
    """
    Convert common missing value representations to NaN.
    """
    df.replace(["NA", "NaN", "", "null", "None"], np.nan, inplace=True)
    return df


def remove_duplicates(df):
    """
    Remove duplicate rows.
    """
    df = df.drop_duplicates()
    return df


############################################
# BIOLOGICAL VALIDATION FUNCTIONS
############################################

def clean_percent_columns(df):
    """
    Ensure percentage columns are between 0 and 100.
    """
    for col in df.columns:
        if "percent" in col.lower() or "tumor_content" in col.lower():
            df.loc[(df[col] < 0) | (df[col] > 100), col] = np.nan
    return df


def clean_expression_values(df):
    """
    Remove extreme expression values that are likely artifacts.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].clip(-50, 50)
    return df


def clean_cna_values(df):
    """
    CNA should normally be integers between -2 and +2.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].clip(-5, 5)
    return df


def clean_mutation_data(df):
    """
    Validate mutation positions and counts.
    """
    if "Start_Position" in df.columns:
        df = df[df["Start_Position"] > 0]

    if "End_Position" in df.columns:
        df = df[df["End_Position"] > 0]

    return df


############################################
# FILE-SPECIFIC CLEANING
############################################

def clean_clinical(df):

    df = standardize_missing(df)
    df = remove_duplicates(df)

    df = clean_percent_columns(df)

    return df


def clean_expression(df):

    df = standardize_missing(df)
    df = remove_duplicates(df)

    df = clean_expression_values(df)

    return df


def clean_cna(df):

    df = standardize_missing(df)
    df = remove_duplicates(df)

    df = clean_cna_values(df)

    return df


def clean_mutations(df):

    df = standardize_missing(df)
    df = remove_duplicates(df)

    df = clean_mutation_data(df)

    return df


############################################
# MAIN PIPELINE
############################################

def clean_file(file):

    print(f"Cleaning {file}")

    df = load_data(file)

    if "clinical" in file:
        df = clean_clinical(df)

    elif "mutation" in file:
        df = clean_mutations(df)

    elif "cna" in file:
        df = clean_cna(df)

    elif "mrna" in file or "protein" in file:
        df = clean_expression(df)

    else:
        df = standardize_missing(df)
        df = remove_duplicates(df)

    out_file = os.path.join(OUTPUT_DIR, "cleaned_" + file)

    df.to_csv(out_file, sep="\t", index=False)

    print(f"Saved cleaned file -> {out_file}")


############################################
# RUN CLEANING
############################################

def main():

    for file in INPUT_FILES:

        if os.path.exists(file):
            clean_file(file)
        else:
            print(f"Warning: {file} not found")


if __name__ == "__main__":
    main()
