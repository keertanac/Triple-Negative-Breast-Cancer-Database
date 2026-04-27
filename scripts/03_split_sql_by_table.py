import re
import os

input_file = "/Users/keertanachagari/Downloads/load_data.sql"
output_dir = "/Users/keertanachagari/Downloads/split_sql"

# Create output folder
os.makedirs(output_dir, exist_ok=True)

# Read file
with open(input_file, "r") as f:
    content = f.read()

# Regex to capture INSERT statements
pattern = r"(INSERT INTO\s+(\w+)\s*\(.*?\)\s*VALUES\s*.*?;)"
matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)

# Dictionary to store table-wise inserts
tables = {}

for full_stmt, table_name in matches:
    table_name = table_name.lower()

    if table_name not in tables:
        tables[table_name] = []

    tables[table_name].append(full_stmt.strip())

# Write separate files per table
for table, statements in tables.items():
    file_path = os.path.join(output_dir, f"{table}.sql")

    with open(file_path, "w") as f:
        f.write(f"-- Data for table: {table}\n\n")
        for stmt in statements:
            f.write(stmt + "\n\n")

print("✅ SQL files created per table in:", output_dir)
