# -*- coding: utf-8 -*-
import sys

def hijri_to_gregorian(year, month, day):
   print "Go find and download the hijri code."
   sys.exit()

"""
Details here about the hijri code and where to find it.

Might be found here: https://github.com/ojuba-org/hijra/blob/master/hijra.py

Or this is what was in the file that I downloaded:

Hijri Islamic Calendar converting functions,
Copyright (c) 2006-2008 Muayyad Saleh Alsadi<alsadi@gmail.com>
Based on an enhanced algorithm designed by me
the algorithm is discussed in a book titled "ﺢﺗﻯ ﻻ ﻥﺪﺨﻟ ﺞﺣﻭﺭ ﺎﻠﻀﺑﺎﺑ"
(not yet published)

This file can be used to implement apps, gdesklets or karamba ..etc

This algorithm is based on integer operations
which that there is no round errors (given accurate coefficients)
the accuracy of this algorithm is based on 3 constants (p,q and a)
where p/q is the full months percentage [ gcd(p,q) must be 1 ]
currently it's set to 191/360 which mean that there is 191 months
having 30 days in a span of 360 years, other months are 29 days.
and a is just a shift.


    Released under terms on Waqf Public License.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the latest version Waqf Public License as
    published by Ojuba.org.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

    The Latest version of the license can be found on
    "http://www.ojuba.org/wiki/doku.php/waqf/license"


Portions of this algorithm is based on that found on GNU EMACS
the difference is that this algorithm does not set
all months to a fixed number of days (in the original algorithm
first month always have 30 days)


The original GNU Emacs LISP algorithm
Copyright (C) 1995, 1997, 2001 Free Software Foundation, Inc.
        Edward M. Reingold <reingold@cs.uiuc.edu>
  Technical details of all the calendrical calculations can be found in
  ``Calendrical Calculations'' by Nachum Dershowitz and Edward M. Reingold,
  Cambridge University Press (1997).
  Comments, corrections, and improvements should be sent to
   Edward M. Reingold               Department of Computer Science
   (217) 333-6733                   University of Illinois at Urbana-Champaign
   reingold@cs.uiuc.edu             1304 West Springfield Avenue
"""

