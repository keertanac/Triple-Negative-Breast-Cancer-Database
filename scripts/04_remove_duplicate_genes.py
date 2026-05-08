import re

# =========================================================
# INPUT / OUTPUT FILES
# =========================================================
input_file = "gene.sql"
output_file = "03_load_gene_table.sql"

# =========================================================
# READ ENTIRE FILE
# =========================================================
with open(input_file, "r") as f:
    content = f.read()

# =========================================================
# STRICT ROW EXTRACTION
# =========================================================
rows = re.findall(
    r"\(\s*([0-9]+(?:\.[0-9]+)?)\s*,\s*'([^']+)'\s*,\s*'([^']+)'\s*\)",
    content
)

print(f"🔎 Rows found: {len(rows)}")

# =========================================================
# REMOVE TRUE DUPLICATE ENTREZ IDS
# =========================================================
seen_ids = set()
kept_rows = []

for raw_entrez, hugo_symbol, chromosome in rows:

    # normalize numeric ID
    entrez_id = str(int(float(raw_entrez)))

    if entrez_id not in seen_ids:

        seen_ids.add(entrez_id)

        kept_rows.append(
            (
                entrez_id,
                hugo_symbol.strip(),
                chromosome.strip()
            )
        )

# =========================================================
# WRITE CLEANED SQL
# =========================================================
with open(output_file, "w") as f:

    f.write(
        "INSERT INTO Gene "
        "(entrez_gene_id, hugo_symbol, chromosome) VALUES\n"
    )

    for i, (entrez_id, hugo_symbol, chromosome) in enumerate(kept_rows):

        ending = "," if i < len(kept_rows) - 1 else ";"

        f.write(
            f"({entrez_id}, "
            f"'{hugo_symbol}', "
            f"'{chromosome}'){ending}\n"
        )

print(f"✅ Final unique gene IDs: {len(kept_rows)}")
print("🎉 Finished successfully")
