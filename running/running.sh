# @Author: lshuns
# @Date:   2021-02-13 12:17:28
# @Last Modified by:   lshuns
# @Last Modified time: 2022-02-24 18:46:16

# usage: run.py [-h] [--getAllTags] [--input_info param_file] [--desired_info param_file]
#               [--data_base param_file] [--version]

# SPP_HMDB v0.3: extract chemical info from HMDB database.

# optional arguments:
#   -h, --help            show this help message and exit
#   --getAllTags          Get all supported tag names.
#   --input_info param_file
#                         A configuration file including input info.
#   --desired_info param_file
#                         A configuration file including desired info.
#   --data_base param_file
#                         The HMDB database.
#   --version             The pipeline version.

# file name of input info
# input_file=input_info_example.param
input_file=input_info_global_targets.param
# file name of desired info
desired_info=desired_info_example.param

# running script
python ../scripts/run.py --input_info ${input_file} --desired_info ${desired_info} --data_base /disks/shear15/ssli/SPP_HMDB/data/hmdb_metabolites.xml