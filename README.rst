===================================================================
 SPP_HMDB: Search PiPeline for the Human Metabolome Database (HMDB)
===================================================================

Simple pipeline for quest of information in the Human Metabolome Database (HMDB, https://hmdb.ca/). 

Build the local database
-----------------------

1. Download the latest database from https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip

2. run xml2feather.py from scripts/ (Warning: demanding mechine memory required, better to run on a cluster.)


Query
-----------------------

1. Go to running/ and build `desired_info.param' and  `input_info.param' as the form shown in corresponding example files.

2. Run run.py

3. Find desired table file in results/


Current supported tags:
-----------------------

version
creation_date
update_date
HMDB_ID
status
name
description
chemical_formula
average_molecular_weight
monisotopic_molecular_weight
iupac_name
traditional_iupac
cas_registry_number
smiles
inchi
inchikey
state
kegg_id
foodb_id
chemspider_id
drugbank_id
pdb_id
chebi_id
pubchem_compound_id
biocyc_id
wikipedia_id
knapsack_id
phenol_explorer_compound_id
bigg_id
metlin_id
vmh_id
fbonto_id
synthesis_reference
synonyms

TBD tags:
-----------------------

secondary_accessions
taxonomy
ontology
experimental_properties
predicted_properties
spectra
biological_properties
normal_concentrations
abnormal_concentrations
diseases
general_references
protein_associations