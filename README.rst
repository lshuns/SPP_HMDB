===================================================================
 SPP_HMDB: Search PiPeline for the Human Metabolome Database (HMDB)
===================================================================

Simple pipeline for quest of information from the Human Metabolome Database (HMDB, https://hmdb.ca/). 

Build the local database
-----------------------

1. download the latest database from https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip

2. unzip downloaded file

3. mv downloaded file to ./data/ and name it as hmdb_metabolites.xml

Query
-----------------------

1. go to running/ and build two configuration files to specify the queried elements (`input_info.param') and the desired columns (`desired_info.param') as the form shown in corresponding example files.

2. change corresponding param file names in running.sh and run with `bash running.sh` 

3. find desired table file in results/


All supported tags:
-----------------------

version


creation_date


update_date


accession


status


secondary_accessions/accession


name


description


synonyms/synonym


chemical_formula


average_molecular_weight


monisotopic_molecular_weight


iupac_name


traditional_iupac


cas_registry_number


smiles


inchi


inchikey


taxonomy/description


taxonomy/direct_parent


taxonomy/kingdom


taxonomy/super_class


taxonomy/class


taxonomy/sub_class


taxonomy/molecular_framework


taxonomy/alternative_parents


taxonomy/substituents


taxonomy/external_descriptors


ontology/root


state


experimental_properties/property


predicted_properties/property


spectra/spectrum


biological_properties/cellular_locations


biological_properties/biospecimen_locations


biological_properties/tissue_locations


biological_properties/pathways


normal_concentrations/concentration


abnormal_concentrations/concentration


diseases/disease


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


general_references/reference


protein_associations/protein