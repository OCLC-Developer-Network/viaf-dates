OCLC Python 2.7 VIAF Date Parsing
==================================

This code parses MARC dates, written for Python 2.7.

Installation
------------

Clone the repository:

`git clone https://github.com/OCLC-Developer-Network/oclc-auth-python.git`

Running the Example
====================

1. python appendices.py 

This will read the datefields.txt file, parse all of the dates in the file and output information for the 40 most common date patterns encountered. It will also tell which patterns with multiple hyphens were not parsed.

Using the Library
=================

d = dateFld('d1962 January 31') will return an object with 3 important fields. d.date1parsed is a list of 3 values: [year, month, day]. d.date2parsed also contains a list of [year, month, day]. d.datetype is 'lived', 'circa' or 'flourished'. Use datetype tells you the precision of the values in date1parsed and date2parsed. 'lived' says the dates are birth (date1parsed) and death (date2parsed) dates and should be accurate += 3 years. 'circa' says the dates are a guess and should be given a 10 year error of margin. 'flourished' are more likely to be dates the person worked or a century date and are given 100 years leeway.
