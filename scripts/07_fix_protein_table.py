import re

# --- File paths (update these if needed) ---
GENE_SQL = "03_load_gene_table.sql"
PROTEIN_SQL = "protein_quant.sql"
OUTPUT_SQL = "09_load_protein_table.sql"

# Step 1: Parse all valid hugo_symbols from gene_deduped.sql
valid_genes = set()
gene_pattern = re.compile(r"^\(([^,]+),\s*'([^']+)'")

with open(GENE_SQL, 'r') as f:
    for line in f:
        line = line.strip().rstrip(',').rstrip(';')
        match = gene_pattern.match(line)
        if match:
            entrez_id = match.group(1).strip()
            hugo_symbol = match.group(2).strip()
            if entrez_id.upper() != 'NULL':
                valid_genes.add(hugo_symbol)

print(f"Valid genes found in Gene table: {len(valid_genes)}")

# Step 2: Parse protein_quant SQL into batches, filter rows, rewrite cleanly
hugo_pattern = re.compile(r"hugo_symbol='([^']+)'")

kept = 0
removed = 0

with open(PROTEIN_SQL, 'r') as f_in, open(OUTPUT_SQL, 'w') as f_out:
    current_batch = []   # holds valid data lines for the current INSERT batch
    in_batch = False

    def flush_batch(f_out, batch):
        """Write a complete INSERT block from a list of value lines."""
        if not batch:
            return
        f_out.write("INSERT INTO Protein_quant (sample_id, entrez_gene_id, abundance, zscore) VALUES\n")
        for i, row in enumerate(batch):
            # Strip any existing trailing comma/semicolon, then add correct punctuation
            clean = row.rstrip().rstrip(',').rstrip(';')
            if i < len(batch) - 1:
                f_out.write(clean + ',\n')
            else:
                f_out.write(clean + ';\n')
        f_out.write('\n')

    for line in f_in:
        stripped = line.strip()

        # Comment lines — pass through
        if stripped.startswith('--'):
            f_out.write(line)
            continue

        # Blank lines — pass through
        if not stripped:
            f_out.write(line)
            continue

        # New INSERT statement — flush previous batch and start a new one
        if stripped.upper().startswith('INSERT'):
            flush_batch(f_out, current_batch)
            current_batch = []
            in_batch = True
            continue  # We'll rewrite the INSERT header ourselves in flush_batch

        # Data row — filter by hugo_symbol
        if in_batch:
            match = hugo_pattern.search(stripped)
            if match:
                symbol = match.group(1)
                if symbol in valid_genes:
                    current_batch.append(stripped)
                    kept += 1
                else:
                    removed += 1
            else:
                current_batch.append(stripped)  # keep non-gene rows just in case

    # Flush the final batch
    flush_batch(f_out, current_batch)

print(f"Rows kept:    {kept}")
print(f"Rows removed: {removed}")
print(f"Output written to: {OUTPUT_SQL}")
