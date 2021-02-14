===================================================================
 SPP_HMDB: Search PiPeline for the Human Metabolome Database (HMDB)
===================================================================

Simple pipeline for quest of information from the Human Metabolome Database (HMDB, https://hmdb.ca/). 

Build the local database
-----------------------

1. download the latest database from https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip

2. unzip downloaded file

3. run xml2feather.py from scripts/ to build the local database (Warning: demanding mechine memory required, better to run on a cluster.)


Query
-----------------------

1. go to running/ and build two configuration files to specify the queried elements (`input_info.param') and the desired columns (`desired_info.param') as the form shown in corresponding example files.

2. change corresponding param file names in running.sh and run with `bash running.sh`

3. find desired table file in results/


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

taxonomy_description
taxonomy_direct_parent
taxonomy_kingdom
taxonomy_super_class
taxonomy_class
taxonomy_sub_class
taxonomy_molecular_framework
taxonomy_alternative_parents
taxonomy_substituents
taxonomy_external_descriptors

TBD tags:
-----------------------

secondary_accessions
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