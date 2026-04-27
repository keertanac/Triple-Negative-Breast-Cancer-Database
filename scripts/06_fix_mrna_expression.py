import re

# --- File paths (update if needed) ---
GENE_SQL    = "/Users/keertanachagari/DB_project/2_split_sql/03_load_gene_table.sql.sql"
INPUT_SQL   = "/Users/keertanachagari/DB_projecft/2_split_sql/mrna_expression.sql"
OUTPUT_SQL  = "/Users/keertanachagari/DB_project/2_split_sql/07_load_mrna_expression.sql"
BATCH_SIZE  = 1000

# Step 1: Parse valid hugo_symbols from gene_deduped.sql
valid_genes = set()
gene_pattern = re.compile(r"^\(([^,]+),\s*'([^']+)'")

with open(GENE_SQL, 'r') as f:
    for line in f:
        line = line.strip().rstrip(',').rstrip(';')
        match = gene_pattern.match(line)
        if match:
            entrez_id  = match.group(1).strip()
            hugo_symbol = match.group(2).strip()
            if entrez_id.upper() != 'NULL':
                valid_genes.add(hugo_symbol)

print(f"Valid genes in Gene table: {len(valid_genes)}")

# Step 2: Read and filter all data rows
hugo_pattern  = re.compile(r"hugo_symbol='([^']+)'")
null_values   = re.compile(r",\s*NULL,\s*NULL\s*\)?[,;]?\s*$", re.IGNORECASE)

kept    = 0
removed = 0
valid_rows = []

with open(INPUT_SQL, 'r') as f:
    for line in f:
        stripped = line.strip()

        # Skip comments, blank lines, INSERT headers
        if not stripped or stripped.startswith('--') or stripped.upper().startswith('INSERT'):
            continue

        # Skip rows where rsem_value and zscore are both NULL
        if null_values.search(stripped):
            removed += 1
            continue

        # Skip rows whose gene is not in the Gene table
        match = hugo_pattern.search(stripped)
        if match:
            symbol = match.group(1)
            if symbol not in valid_genes:
                removed += 1
                continue

        # Clean the row: strip leading/trailing whitespace and any trailing comma/semicolon
        clean = stripped.rstrip().rstrip(',').rstrip(';').rstrip(')')
        # Re-add the closing paren (it was part of the value tuple)
        clean = clean + ')'
        valid_rows.append(clean)
        kept += 1

print(f"Rows kept:    {kept}")
print(f"Rows removed: {removed}")

# Step 3: Write out in batches with correct comma/semicolon punctuation
with open(OUTPUT_SQL, 'w') as f:
    f.write("-- Data for table: mrna_expression\n\n")

    for i in range(0, len(valid_rows), BATCH_SIZE):
        batch = valid_rows[i:i + BATCH_SIZE]
        f.write("INSERT INTO mRNA_expression (sample_id, entrez_gene_id, rsem_value, zscore) VALUES\n")
        for j, row in enumerate(batch):
            if j < len(batch) - 1:
                f.write(row + ',\n')
            else:
                f.write(row + ';\n')
        f.write('\n')

print(f"Output written to: {OUTPUT_SQL}")
