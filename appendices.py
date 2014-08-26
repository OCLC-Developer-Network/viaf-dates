from __future__ import print_function
""" Driver that reads datefields.txt and passes them to dateFld. Create report
    showing top 99% of patterns to be checked for correctness. Also shows unparsed
    values with multiple hyphens in case we can add them to overrides.py
"""
"""
Copyright 2014 OCLC Online Computer Library Center

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys, types
from dateFld import dateFld, F_IS_FLOURISHED

def myprint(*args, **kwargs):
   towrite = kwargs.get('sep', '\t').join([a.encode('utf-8') if isinstance(a, types.UnicodeType) else str(a) for a in args])
   print(towrite, **kwargs)

if __name__=='__main__':
    from collections import Counter
    ctr = Counter()
    results = {}
    totalocc = 0
    unhandled = Counter()
    for line in open('datefields.txt', 'rb'):
       dsub, srcid, occ = line.decode('utf-8').strip().split('\t')
       occ = int(occ)
       df = dateFld(dsub, '')
       # split found a beginning date
       if df.date1:  
          totalocc += occ
          df.date1pattern = df.date1pattern.strip() if df.date1pattern else None
          # count occurences of date pattern
          ctr[df.date1pattern] += occ
          # save highest occuring example that parsed into this date pattern
          if df.date1pattern not in results or results[df.date1pattern][2] < occ:
             results[df.date1pattern] = (dsub, srcid, occ, df)
          # if date has multiple hyphens and year is still 0 then
          # overrides.py could not split the date.
          if df.date1pattern.count('-') > 1 and df.date1parsed[0] == 0:
             unhandled[df.date1pattern] += occ
       # split found an ending date
       if df.date2:
          totalocc += occ
          df.date2pattern = df.date2pattern.strip() if df.date2pattern else None
          ctr[df.date2pattern] += occ
          if df.date2pattern not in results or results[df.date2pattern][2] < occ:
             results[df.date2pattern] = (dsub, srcid, occ, df)
 
    myprint('datepatterns', len(results), 'total occurences', totalocc)
    subtotal = 0
    for pattern in ctr.most_common(40):
       pattern, total = pattern
       dsub, srcid, occ, df = results[pattern]
       subtotal += total
       myprint(pattern, total, dsub, srcid, occ, df, '%.4lf' % (float(subtotal) / totalocc))

    for pattern in unhandled.most_common(10):
       pattern, total = pattern
       myprint('UNHANDLED', pattern, total)
