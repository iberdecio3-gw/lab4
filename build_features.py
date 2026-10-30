
import sqlite3, pandas as pd

# Connect to database (same as Week 8 demo)
con = sqlite3.connect("cohort.db")

def q(sql):
    return pd.read_sql(sql, con)

# Count mutations for five genes
gene_counts = q('''
WITH target_genes(gene_symbol) AS (
    VALUES ('TP53'), ('KRAS'), ('EGFR'),
           ('STK11'), ('KEAP1')
)
SELECT p.patient_id, g.gene_symbol,
       COUNT(m.mutation_id) AS mutation_count
FROM patients p
CROSS JOIN target_genes g
LEFT JOIN samples s ON s.patient_id = p.patient_id
LEFT JOIN mutations m ON m.sample_id = s.sample_id
    AND UPPER(TRIM(m.gene_symbol)) = g.gene_symbol
    AND m.variant_classification != 'Silent'
GROUP BY p.patient_id, g.gene_symbol
ORDER BY p.patient_id, g.gene_symbol
''')

print(len(gene_counts), "gene count rows")

# Count patients by tissue source site and stage
site_stage = q('''
SELECT s.tissue_source_site, p.stage,
       COUNT(DISTINCT p.patient_id) AS patient_count
FROM patients p
LEFT JOIN samples s ON s.patient_id = p.patient_id
GROUP BY s.tissue_source_site, p.stage
ORDER BY s.tissue_source_site, p.stage
''')

print(len(site_stage), "site-stage rows")

# Get clinical information
clinical = q('''
SELECT p.patient_id, p.sex, p.age_at_diagnosis,
       p.stage, s.tissue_source_site, s.tmb_nonsynonymous
FROM patients p
LEFT JOIN samples s ON s.patient_id = p.patient_id
ORDER BY p.patient_id
''')

print(len(clinical), "clinical rows")

# Turn gene counts into columns
gene_wide = gene_counts.pivot(
    index='patient_id',
    columns='gene_symbol',
    values='mutation_count'
).reset_index()

gene_wide.columns.name = None

# Join clinical information and gene counts
feature_table = clinical.merge(
    gene_wide,
    on='patient_id',
    how='left',
    validate='one_to_one'
)

# Fill missing mutation counts with zero
genes = ['TP53', 'KRAS', 'EGFR', 'STK11', 'KEAP1']
feature_table[genes] = feature_table[genes].fillna(0).astype(int)

# Arrange columns
feature_table = feature_table[
    ['patient_id', 'sex', 'age_at_diagnosis', 'stage',
     'tissue_source_site', 'tmb_nonsynonymous'] + genes
]

# Check final row count
print(len(feature_table), "final rows")
print(feature_table['patient_id'].nunique(), "unique patients")
print(feature_table.shape)

# Save feature table
feature_table.to_csv("feature_table.tsv", sep="\t",
                     index=False, na_rep="NA")

con.close()

