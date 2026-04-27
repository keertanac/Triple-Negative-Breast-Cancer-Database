#DB PROJECT -- SQL TABLE CREATING

CREATE TABLE Patient
(
    patient_id VARCHAR(50) AUTO_INCREMENT PRIMARY KEY,
    race VARCHAR(100)
);

CREATE TABLE Sample
(
    sample_id VARCHAR(50) PRIMARY KEY,
    patient_id INT UNSIGNED NOT NULL,
    pCR_response VARCHAR(100),
    collection_event VARCHAR(50),
    pam50_subtype VARCHAR(50),
    TNBC_subtype VARCHAR(50),
    residual_cancer_burden VARCHAR(10),
    tumor_content DECIMAL(5,2),
    CD3_pos_IHC VARCHAR(20),
    PDL1_combined_pos_score VARCHAR(10),
    chromosomal_instability DECIMAL(6,3),
    nonsyn_mutation_load VARCHAR(10),
    somatic_MSI VARCHAR(10),
    immune_score DECIMAL(6,3),
    stromal_score DECIMAL(6,3),
    tumor_purity DECIMAL(6,3),
    pbmgp_score DECIMAL(6,3),
    rna_score DECIMAL(6,3),
    LIG1_classification VARCHAR(50),
    somatic_status VARCHAR(50),
    oncotree_code VARCHAR(10),
    treatment_status VARCHAR(20),
    mutations_profile VARCHAR(20),
    gistic_profile VARCHAR(10),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id)
);

CREATE TABLE Gene
(
    entrez_gene_id INT UNSIGNED PRIMARY KEY,
    hugo_symbol VARCHAR(20) UNIQUE,
    chromosome VARCHAR(5)
);

CREATE TABLE Mutation
(
    mutation_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sample_id VARCHAR(50),
    entrez_gene_id INT UNSIGNED NULL,
    chrom_start_pos INT UNSIGNED,
    chrom_end_pos INT UNSIGNED,
    consequence VARCHAR(300),
    variant_classification VARCHAR(300),
    variant_type VARCHAR(50),
    ref_allele VARCHAR(300),
    alt_allele VARCHAR(500),
    tumor_ref_count INT UNSIGNED,
    tumor_alt_count INT UNSIGNED,
    hgvs_c VARCHAR(255),
    hgvs_p VARCHAR(255),
    transcript_id VARCHAR(255),
    FOREIGN KEY (sample_id) REFERENCES Sample(sample_id),
    FOREIGN KEY (entrez_gene_id) REFERENCES Gene(entrez_gene_id)
);

CREATE TABLE mRNA_expression
(
    sample_id VARCHAR(50),
    entrez_gene_id INT UNSIGNED,
    rsem_value DECIMAL(10,4),
    zscore DECIMAL(6,3),
    PRIMARY KEY (sample_id, entrez_gene_id),
    FOREIGN KEY (sample_id) REFERENCES Sample(sample_id),
    FOREIGN KEY (entrez_gene_id) REFERENCES Gene(entrez_gene_id)
);

CREATE TABLE Protein_quant
(
    sample_id VARCHAR(50),
    entrez_gene_id INT UNSIGNED,
    abundance DECIMAL(10,4),
    zscore DECIMAL(6,3),
    PRIMARY KEY (sample_id, entrez_gene_id),
    FOREIGN KEY (sample_id) REFERENCES Sample(sample_id),
    FOREIGN KEY (entrez_gene_id) REFERENCES Gene(entrez_gene_id)
);
