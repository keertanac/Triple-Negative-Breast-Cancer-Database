import re

input_file = "/Users/keertanachagari/DB_project/2_split_sql/protein_quant.sql"
output_file = "/Users/keertanachagari/DB_project/2_split_sql/protein_quant.sql"
BATCH_SIZE = 500

with open(input_file, "r") as f:
    content = f.read()

header = re.search(r"(INSERT INTO .*? VALUES)", content, re.DOTALL).group(1)

# ✅ Split ONLY on top-level "),"
rows = re.split(r"\),\s*\(", content)

# clean first and last row
rows[0] = rows[0].split("VALUES",1)[1].strip().lstrip("(")
rows[-1] = rows[-1].rstrip(");")

clean_rows = [r.strip() for r in rows if r.strip()]

print(f"Rows found: {len(clean_rows)}")

# write batches
with open(output_file, "w") as f:
    for i in range(0, len(clean_rows), BATCH_SIZE):
        batch = clean_rows[i:i+BATCH_SIZE]

        f.write(header + "\n")

        for j, row in enumerate(batch):
            if j < len(batch) - 1:
                f.write(f"({row}),\n")
            else:
                f.write(f"({row});\n\n")

print("✅ Fixed split file created")
