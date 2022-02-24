# -*- coding: utf-8 -*-
# @Author: ssli
# @Date:   2022-02-24 18:28:55
# @Last Modified by:   lshuns
# @Last Modified time: 2022-02-24 18:43:37

### extract desired columns from a given xlsx file

import pandas as pd 

# >>> input info
inpath = '../data/Global_targets.xlsx'
col_HMDB = 'HMDB_ID'

# >>> output info
outpath = '../running/input_info_global_targets.param'

# >>> workhorse
## load catalogue
cata = pd.read_excel(inpath, engine='openpyxl')
### get HMDB_ID
HMDB_ID = cata[col_HMDB].dropna().values

## write out
with open(outpath, 'w') as f:

    print('# used tag name', file=f)

    print('HMDB_ID:\n\n', file=f)

    for val in HMDB_ID:
        print(val, file=f)
print('extracted results saved to', outpath)


