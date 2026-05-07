Data dictionary:

Patient table:
- patient_id: INT (PK) --> Unique identifier for each patient 
- race: VARCHAR(100) --> Self-reported or clinically recorded race category

Sample table:
- sample_id --> VARCHAR(50) (PK) --> Unique identifier for each sample
- patient_id --> INT (FK) --> References the patient from whom the sample was obtained
- pCR_response --> VARCHAR(100) --> Indicates whether the patient achieved pathological complete response
- collection_event --> VARCHAR(50) --> Describes timing of sample collection (e.g., baseline, post-treatment)
- pam50_subtype --> VARCHAR(50) --> Molecular subtype classification of the tumor based on gene expression patterns from the PAM50 assay
- TNBC_subtype --> VARCHAR(50) --> Sub-classification specific to triple-negative breast cancer
- residual_cancer_burden --> VARCHAR(10) --> Clinical classification of tumor burden remaining after treatment. Values include 0 (no residual disease), I (minimal), II (moderate), and III (extensive residual disease).
- tumor_content --> DECIMAL --> Estimated proportion of tumor cells in the sample
- CD3_pos_IHC --> VARCHAR(20) --> Immunohistochemistry measurement of T-cell infiltration
- PDL1_combined_pos_score --> VARCHAR(10) --> PD-L1 expression score used in immunotherapy evaluation
- chromosomal_instability --> DECIMAL --> Measure of genomic instability within the tumor
- nonsyn_mutation_load --> VARCHAR(10) --> Number of mutations altering protein sequence
- somatic_MSI --> VARCHAR(10) --> VARCHAR(4) --> Microsatellite instability status
- immune_score --> DECIMAL --> Composite score reflecting immune cell infiltration
- stromal_score --> DECIMAL --> Score reflecting stromal (non-tumor) cell presence
- tumor_purity --> DECIMAL --> Estimated fraction of tumor cells vs normal cells
- pbmgp_score --> DECIMAL --> Protein based multigene proliferation score - summarizes how fast tumor cells are dividing based on protein levels from multiple genes
- rna_score --> DECIMAL --> RNA based multi gene proliferation score 
- LIG1_classification --> VARCHAR(50) --> Categorical classification of the LIG1 gene status in each sample - WT (wild type, indicating normal gene function), CN Loss (copy number loss, indicating reduced gene copies and potential loss of function)
- somatic_status --> VARCHAR(50) --> Indicates whether the tumor sample has a matched normal sample from the same patient
- oncotree_code --> VARCHAR(10) --> All samples are labeled 'BRCA', indicating cancer
- treatment_status --> VARCHAR(20) --> Clinical treatment stage or status

Gene table:
- entrez_gene_id --> INT (PK) --> Unique gene identifier from NCBI
- hugo_symbol --> VARCHAR(20) --> Standard gene symbol
- chromosome --> VARCHAR(5) --> Chromosome location

mRNA Expression table:
- sample_id --> VARCHAR(50) (PK, FK) --> Sample identifier
- entrez_gene_id --> INT (PK, FK) --> Gene identifer
- rsem_value --> DECIMAL --> Gene expression level (RSEM normalized)
- zscore --> DECIMAL --> Standardized protein expression value

Protein Quant table:
- sample_id --> VARCHAR(50) (PK, FK) --> Identifier for the sample
- entrez_gene_id --> INT (PK, FK) --> Identifier for the gene
- abundance --> DECIMAL --> Measured protein abundance
- zscore --> DECIMAL --> Standardized protein expression value

Mutation table:
- mutation_id --> INT (PK) --> Unique identifier for each mutation
- sample_id --> VARCHAR(50) (FK) --> Sample in which the mutation was detected
- entrez_gene_id --> INT (FK, NULL allowed) --> Associated gene; NULL for intergenic mutations
- chrom_start_pos --> INT --> Genomic start position of the mutation
- chrom_end_pos --> INT --> Genomic end position of the mutation
- consequence --> VARCHAR(300) --> The biological effect of a mutation on a gene
- variant_classification --> VARCHAR(300) --> Functional impact (e.g., missense, nonsense)
- variant_type --> VARCHAR(50) --> Mutation type (e.g., SNP, insertion, deletion)
- ref_allele --> VARCHAR(300) --> Reference DNA sequence
- alt_allele --> VARCHAR(500) --> Altered DNA sequence
- tumor_ref_count --> INT --> Number of reads supporting reference allele
- tumor_alt_count --> INT --> Number of reads supporting alternate allele
- hgvs_c --> VARCHAR(255) --> Coding DNA-level mutation (HGVS notation)
- hgvs_p --> VARCHAR(255) --> Protein-level mutation (HGVS notation)
- transcript_id --> VARCHAR(255) --> Transcript used for annotation
