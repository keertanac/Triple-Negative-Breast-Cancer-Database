import re

# =========================================================
# FILE PATHS
# =========================================================
GENE_SQL = "/Users/keertanachagari/DB_project/sql/03_load_gene_table.sql"

# giant protein file
PROTEIN_SQL = "/Users/keertanachagari/DB_project/sql/protein_quant.sql"

# cleaned + split output
OUTPUT_SQL = "/Users/keertanachagari/DB_project/sql/09_load_protein_quant_table.sql"

# rows per INSERT batch
BATCH_SIZE = 500

# =========================================================
# STEP 1 — LOAD VALID GENE SYMBOLS
# =========================================================
valid_genes = set()

gene_pattern = re.compile(r"^\(([^,]+),\s*'([^']+)'")

with open(GENE_SQL, "r") as f:
    for line in f:
        line = line.strip().rstrip(",").rstrip(";")

        match = gene_pattern.match(line)

        if match:
            entrez_id = match.group(1).strip()
            hugo_symbol = match.group(2).strip()

            if entrez_id.upper() != "NULL":
                valid_genes.add(hugo_symbol)

print(f"✅ Valid genes loaded: {len(valid_genes)}")

# =========================================================
# STEP 2 — READ ENTIRE PROTEIN SQL FILE
# =========================================================
with open(PROTEIN_SQL, "r") as f:
    content = f.read()

# =========================================================
# STEP 3 — EXTRACT INSERT HEADER
# =========================================================
header_match = re.search(
    r"(INSERT INTO\s+Protein_quant\s*\(.*?\)\s*VALUES)",
    content,
    re.DOTALL | re.IGNORECASE
)

if not header_match:
    raise ValueError("❌ Could not find INSERT header")

header = header_match.group(1)

# =========================================================
# STEP 4 — EXTRACT ONLY VALUES SECTION
# =========================================================
values_section = content.split("VALUES", 1)[1]

# remove trailing semicolon
values_section = values_section.strip().rstrip(";")

# =========================================================
# STEP 5 — SPLIT ROWS
# =========================================================
rows = re.split(r"\),\s*\(", values_section)

# clean first and last rows
rows[0] = rows[0].lstrip("(")
rows[-1] = rows[-1].rstrip(")")

clean_rows = [r.strip() for r in rows if r.strip()]

print(f"✅ Total rows found: {len(clean_rows)}")

# =========================================================
# STEP 6 — FILTER ROWS BY VALID hugo_symbol
# =========================================================
hugo_pattern = re.compile(r"hugo_symbol='([^']+)'")

filtered_rows = []

kept = 0
removed = 0

for row in clean_rows:

    match = hugo_pattern.search(row)

    # if no hugo_symbol exists, keep row just in case
    if not match:
        filtered_rows.append(row)
        kept += 1
        continue

    symbol = match.group(1)

    if symbol in valid_genes:
        filtered_rows.append(row)
        kept += 1
    else:
        removed += 1

print(f"✅ Rows kept:    {kept}")
print(f"❌ Rows removed: {removed}")

# =========================================================
# STEP 7 — WRITE CLEANED + BATCHED OUTPUT
# =========================================================
with open(OUTPUT_SQL, "w") as f:

    for i in range(0, len(filtered_rows), BATCH_SIZE):

        batch = filtered_rows[i:i+BATCH_SIZE]

        f.write(header + "\n")

        for j, row in enumerate(batch):

            clean = row.strip().rstrip(",").rstrip(";")

            if j < len(batch) - 1:
                f.write(f"({clean}),\n")
            else:
                f.write(f"({clean});\n\n")

print("✅ Finished writing cleaned batched SQL file")
print(f"📄 Output file: {OUTPUT_SQL}")
