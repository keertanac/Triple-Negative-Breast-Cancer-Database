import re

input_file = "gene.sql"
output_file = "03_load_gene_table.sql"

seen = set()
kept_rows = []

with open(input_file, "r") as f:
    lines = f.readlines()

insert_prefix = None

for line in lines:
    stripped = line.strip()

    if stripped.startswith("INSERT INTO Gene"):
        insert_prefix = stripped
        continue

    if not stripped or stripped.startswith("--"):
        continue

    m = re.match(r"^\(([^,]+),\s*'([^']+)',\s*'([^']+)'\)\s*[;,]?$", stripped)
    if not m:
        continue

    entrez_id = m.group(1).strip()
    hugo_symbol = m.group(2).strip()
    chromosome = m.group(3).strip()

    if hugo_symbol not in seen:
        seen.add(hugo_symbol)
        kept_rows.append((entrez_id, hugo_symbol, chromosome))

with open(output_file, "w") as f:
    f.write("INSERT INTO Gene (entrez_gene_id, hugo_symbol, chromosome) VALUES\n")
    for i, (entrez_id, hugo_symbol, chromosome) in enumerate(kept_rows):
        ending = "," if i < len(kept_rows) - 1 else ";"
        f.write(f"({entrez_id}, '{hugo_symbol}', '{chromosome}'){ending}\n")

print(f"Kept {len(kept_rows)} unique hugo_symbol rows.")
print(f"Wrote deduplicated file to {output_file}")
