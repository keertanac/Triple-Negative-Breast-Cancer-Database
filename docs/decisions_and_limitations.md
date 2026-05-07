Decisions and Limitations:

Certain columns in the raw data files were not included in the final database structure. 
Below outlines which columns were removed from which files and why:

data_clinical_sample.txt:
- stimulatory immune modulator proteins
- inhibitory immune modulator proteins
- HLA immune modulator proteins
- absolute immune score

Reasoning: These variables are derived features calculated from RNA expression data, 
protein data, and immune deconvolution algorithms. Storing them in the database would 
introduce redundancy and could lead to inconsistencies if the values are recomputed in 
the future.

- xCell immune score
- xCell stroma score
- xCell microenvironment score

Reasoning: xCell scores are cell-type inference metrics derived from expression data. 
They are computationally generated rather than directly measured, which can introduce 
redundancy and inconsistency if recalculated.

dna_mutations.txt:
- NCBI build → dataset-wide metadata, not mutation-specific, and all rows use the same 
genome build (GRCh37). Storing it wastes space and violates normalization.
- strand → implicit from gene annotation given the gene symbol and genomic coordinates.
- dbsnp_rs → lookup identifier, not part of the mutation itself; it can change across 
database versions and a single variant can have multiple identifiers.
- mutation status → all rows are labeled "SOMATIC," so it provides no distinguishing information.
- HGVSp_short → shorthand for HGVSp, so keeping it would violate normalization.
- refseq → transcript annotation, not a mutation event.
- protein_position → derived from transcript sequence and codon location; not intrinsic to 
the mutation itself and may change if transcript definitions are updated.
- codons → annotation-level information, not a core mutation property.
- exon_number → transcript-based interpretation; a mutation affects the genome, not exon numbering.
- annotation_status → pipeline metadata that does not describe the mutation itself.

*Also excluded many columns that were completely empty.*

No information from data_cna.txt or dna_log2_cna.txt was used: copy number information 
was not central to the primary analyses of gene expression, protein abundance, and mutation 
patterns. Including it would increase database complexity without adding meaningful insight.

No information from data_gene_panel_matrix.txt was used: this file contained the 
mutations_profile and gistic_profile columns, which are metadata describing how the data 
was generated rather than characteristics of the tumor itself. All values were "WXS" 
(Whole Exome Sequencing), meaning there was no variation across samples.

---

I acknowledge that there are a few limitations to this database and its creation:

1. The data loading process ended up being more complicated than expected and required several 
steps and extra scripts along the way. After running into issues such as duplicate entries, 
missing foreign keys, and formatting errors, additional scripts had to be created to fix and 
regenerate SQL files for each table. While this troubleshooting ensured that the final database 
was accurate, it made the workflow more complex and less straightforward than a simpler, 
single-script approach.

2. The project did not include implementation of the Neo4j component due to time constraints. 
The plan was to use SQL to identify differentially expressed genes and then load those genes 
into Neo4j to explore their relationships. Using Neo4j would have made it easier to examine 
connections between genes, samples, and mutations, such as shared patterns or interactions. 
In the future, incorporating this step would make the project stronger by helping to explore 
relationships more deeply.
