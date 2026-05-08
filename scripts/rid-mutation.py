import re

# Input/output files
mutation_file = "/Users/keertanachagari/DB_project/split_sql/mutation.sql"
gene_file = "/Users/keertanachagari/DB_project/split_sql/03_load_gene_table.sql"
output_file = "/Users/keertanachagari/DB_project/split_sql/06_load_mutation_table.sql"

# -------------------------------
# Step 1: Extract valid gene IDs
# -------------------------------
with open(gene_file, "r") as f:
    gene_content = f.read()

# Extract first value in each row (entrez_gene_id)
gene_matches = re.findall(r"\((\d+)\.0,", gene_content)
valid_gene_ids = set(int(x) for x in gene_matches)

print(f"✅ Loaded {len(valid_gene_ids)} valid gene IDs")

# -------------------------------
# Step 2: Read mutation file
# -------------------------------
with open(mutation_file, "r") as f:
    content = f.read()

# Extract header + values
header = re.search(r"(INSERT INTO .*? VALUES)", content, re.DOTALL).group(1)
values_block = re.search(r"VALUES\s*(.*);", content, re.DOTALL).group(1)

# Extract rows
rows = re.findall(r"\((.*?)\)", values_block, re.DOTALL)

print(f"🔎 Total mutation rows: {len(rows)}")

# -------------------------------
# Step 3: Filter bad rows
# -------------------------------
clean_rows = []
seen = set()

for row in rows:
    row_clean = row.strip()

    parts = [p.strip() for p in row_clean.split(",")]

    # entrez_gene_id is second column
    gene_val = parts[1]

    # ❌ skip NULL
    if gene_val == "NULL":
        continue

    # convert float → int (because of .0)
    try:
        gene_id = int(float(gene_val))
    except:
        continue

    # ❌ skip genes not in Gene table
    if gene_id not in valid_gene_ids:
        continue

    # remove duplicates
    if row_clean not in seen:
        seen.add(row_clean)
        clean_rows.append(row_clean)

print(f"✅ Rows after cleaning: {len(clean_rows)}")

# -------------------------------
# Step 4: Write cleaned SQL
# -------------------------------
with open(output_file, "w") as f:
    f.write("-- Cleaned mutation data (FK-safe)\n\n")
    f.write(header + "\n")

    for i, row in enumerate(clean_rows):
        if i < len(clean_rows) - 1:
            f.write(f"({row}),\n")
        else:
            f.write(f"({row});\n")

print(f"🎉 06_load_mutation_table.sql created successfully!")
