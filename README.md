# Lab 4 - Database-Driven Feature Table
## Repo Overview

| File | Description |
|---|---|
| `cohort.db` | Database (provided) |
| `LAB4.ipynb` | Jupyter Notebook with the sql (Task 1)|
| `build_features.py` | Python script that creates feature table (Task 2)|
| `feature_table.tsv` | Final feature table (Task 2)|
| `data_dictionary.csv` | Description of the final table columns (Task 4) |
| `SOURCE.md` | Information about the original dataset (provided) |
| `generate_data.py` | Provided script for rebuilding the database (provided)|
| `AI_USAGE.md` | Documentation of AI assistance |

Requirements:
Python3
Pandas
SQLite (sqlite3)

Instructions:
1. Clone repository (git clone)
2. Ensure all files are in the same folder
3. Run script:
  ```bash
   python3 build_features.py
   ```
  It will read in the database, run SQL queries, combine dfs, and create a final table.The    excepted output is 566 rows and 11 columns [See data dictionary for column names].

Note: Install pandas if needed
```bash
   python3 -m pip install pandas
```
## Task Write-Up Requirements
1. Explore the schema. Write out (in your submission) the tables, columns, and foreign key relationships as you understand them from inspecting the database. State the grain (what one row represents) of each table.

   - Patients: patient_id, sex, age_at_diagnosis, stage, vital_status, followup_months
         - Grain: Row per patient
         - Primary key: patient_id
   - Samples: sample_id, patient_id, tissue_source_site, tmb_nonsynonymous, aneuploidy_score, msi_mantis_score
         - Grain: Row per tumor sample
         - Primary key: sample_id
         - Foreign key: patient_id - Relationship should connect tumor samples to                      respective patients (from patients table)
   - Mutation: mutation_id, sample_id, gene_symbol, variant_classification, variant_type, protein_change, chromosome, start_pos, end_pos, t_ref_count, t_alt_count
         - Grain: Row per mutation in tumor samples
         - Primary key: mutation_id
         - Forgein key: sample_id, gene_symbol
           Relationship should connect mutations to respecitve samples and genes (from samples & mutations tables)
   - Gene: gene_symbol, entrez_gene_id, chromosome
         - Grain: Row per gene
         - Primary key: gene_symbol
         

2. Write SQL queries to:

    - For each patient and each of these five genes (TP53, KRAS, EGFR, STK11, KEAP1), count the protein-altering mutations (exclude Silent).:
        *Expected: 566 patieents x 5 genes = 2,830
         Acutal: 2,830*
    - Count patients per tissue source site per tumor stage.
        *Expected: One row per tissue + tumor - I did not have a number guess.
         Acutal: 142*
    - For each query, record the row count you expected and the row count you got (Week 8, habit 1). If they differ, explain why.

3. Build a feature table: one row per patient (566 rows), with columns for sex, age at diagnosis, stage, tissue source site, tumor mutation burden, and one column per gene from Task 2 (its protein-altering mutation count). Do this by combining SQL (for the querying/joining) with Python or R scripting (for reshaping into wide format), not pure SQL pivoting.
   - See build_feature.py
   - Script combined patient info, tumor info, and gene info.
   - 566 patients, 11 columns, one row per patient
   - Results is saved in feature_table.tsv

4. Handle missing data explicitly: some patients lack sex, age, or stage, and most patients have no mutation in any given gene. Document how you handled each kind of gap (e.g., left join and keep the NA, not silently dropping patients). Show the patient count before and after your joins so a reader can see no one was lost by accident. A gene count of zero and a missing value mean different things; say which one you used and why.
  
  - Missing data was checked for using feature_table.isna().sum().
  
  <img width="279" height="262" alt="Screenshot 2026-10-30 at 8 03 03 PM" src="https://github.com/user-attachments/assets/95f7faee-0a17-43fe-9e6b-69a081d0baaa" />

  - Patients before joins: 566
  - Patients after joins: 566
  - Unique patients: 566
  - For gene counts I used zero to represent no mutations that qualified, rather than NA which means missing data entirely. 

6. Metadata: produce a small data dictionary (column name, meaning, units, source table) for your final feature table.

   - Data dictionary saved as .csv [data_dictionary.csv]
   
