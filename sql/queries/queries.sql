--count rows in each table
SELECT 'Gene' AS table_name, COUNT(*) FROM Gene
UNION
SELECT 'mRNA_expression', COUNT(*) FROM mRNA_expression
UNION
SELECT 'Mutation', COUNT(*) FROM Mutation
UNION
SELECT 'Patient', COUNT(*) FROM Patient
UNION
SELECT 'Protein_quant', COUNT(*) FROM Protein_quant
UNION
SELECT 'Sample', COUNT(*) FROM Sample;

--list all patients
SELECT *
FROM Patient;

--count samples per patient
SELECT patient_id, COUNT(*) AS num_samples
FROM Sample
GROUP BY patient_id;

--view gene expression for a few genes
SELECT 
g.hugo_symbol AS gene,
e.sample_id,
e.rsem_value,
e.zscore
FROM Gene g
JOIN mRNA_expression e 
ON g.entrez_gene_id = e.entrez_gene_id
LIMIT 20;

--average expression per gene
SELECT 
g.hugo_symbol,
AVG(e.rsem_value) AS avg_expression
FROM Gene g
JOIN mRNA_expression e 
ON g.entrez_gene_id = e.entrez_gene_id
GROUP BY g.hugo_symbol
ORDER BY avg_expression DESC
LIMIT 10;

--expression per sample
SELECT 
e.sample_id,
g.hugo_symbol,
e.rsem_value,
e.zscore
FROM mRNA_expression e
JOIN Gene g 
ON e.entrez_gene_id = g.entrez_gene_id
LIMIT 20;

--protein vs mrna comparison
SELECT 
g.hugo_symbol,
AVG(e.rsem_value) AS avg_mrna,
AVG(p.abundance) AS avg_protein
FROM Gene g
JOIN mRNA_expression e 
ON g.entrez_gene_id = e.entrez_gene_id
JOIN Protein_quant p 
ON g.entrez_gene_id = p.entrez_gene_id
GROUP BY g.hugo_symbol
LIMIT 20;

--mutations per gene
SELECT 
g.hugo_symbol,
COUNT(m.mutation_id) AS mutation_count
FROM Gene g
JOIN Mutation m 
ON g.entrez_gene_id = m.entrez_gene_id
GROUP BY g.hugo_symbol
ORDER BY mutation_count DESC
LIMIT 10;

--mutations per patient
SELECT 
p.patient_id,
COUNT(m.mutation_id) AS total_mutations
FROM Patient p
JOIN Sample s 
ON p.patient_id = s.patient_id
JOIN Mutation m 
ON s.sample_id = m.sample_id
GROUP BY p.patient_id;

--join sample and patient data
SELECT 
s.sample_id,
p.patient_id
FROM Sample s
JOIN Patient p 
ON s.patient_id = p.patient_id;

--full integration query
SELECT 
p.patient_id,
s.sample_id,
g.hugo_symbol,
e.rsem_value,
e.zscore,
pqt.abundance,
m.mutation_id
FROM Patient p
JOIN Sample s 
ON p.patient_id = s.patient_id
LEFT JOIN mRNA_expression e 
ON s.sample_id = e.sample_id
LEFT JOIN Protein_quant pqt 
ON s.sample_id = pqt.sample_id
LEFT JOIN Mutation m 
ON s.sample_id = m.sample_id
LEFT JOIN Gene g 
ON e.entrez_gene_id = g.entrez_gene_id
LIMIT 50;
