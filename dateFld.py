# -*- coding: utf-8 -*-
""" Parse date subfields from MARC data into beginning and ending year, month and day.
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

import sys, re, unicodedata, locale
try:
   from hijri import hijri_to_gregorian
except:
   from hijristub import hijri_to_gregorian
from handates import handates
from overrides import overrides

##http://www.karlin.mff.cuni.cz/network/prirucky/javatut/java/intl/locales.html
##http://docs.oracle.com/javase/1.4.2/docs/guide/intl/locale.doc.html
interesting = ['da_DK',
'de_AT',
'de_CH',
'de_DE',
'el_GR',
'en_CA',
'en_GB',
'en_IE',
'en_US',
'es_ES',
'fi_FI',
'fr_BE',
'fr_CA',
'fr_CH',
'fr_FR',
'it_CH',
'it_IT',
#'ja_JP',
#'ko_KR',
'nl_BE',
'nl_NL',
'no_NO',
#'no_NO_B',
'pt_PT',
'sv_SE',
'tr_TR',
'cs_CZ',]
##'zh_CN',
##'zh_TW',]

monthLookup = {'jan':1, 'en':1, 'ene':1,'led':1, 'janv':1,'january':1, 'janvier':1, 'januar':1,
   'feb':2, 'febr':2, 'un':2, 'fevr':2,'february':2,'fevrier':2,'februar':2,
   'ún'.decode('utf-8'):2, 'févr'.decode('utf-8'):2,
   'mar':3, 'marzo':3, 'mars':3, 'march':3, 'brez':3, 'břez'.decode('utf-8'):3,
   'apr':4, 'dub':4, 'april':4, 'abr':4, 'avr':4, 'avril':4,
   'may':5, 'kvet':5, 'mayo':5, 'maj':5, 'mai':5, 'kveten':5, 'květ'.decode('utf-8'):5,
   'maijs':5,
   'june':6, 'cerv':6, 'jun':6, 'juni':6, 'juin':6, 'jūn'.decode('utf-8'):7,
   'july':7, 'cerven':7, 'jul':7, 'juli':7, 'juil':7, 'juillet':7,
   'červ'.decode('utf-8'):7, 'červen'.decode('utf-8'):7, 'jūl'.decode('utf-8'):7,
   'aug':8, 'srp':8, 'ag':8, 'aout':8,'august':8,
   'sept':9, 'sep':9, 'zari':9, 'zar':9,'september':9,'septembre':9,
   'září'.decode('utf-8'):9,
   'oct':10, 'rij':10, 'october':10, 'okt':10, 'octobre':10, 'oktober':10,
   'říj'.decode('utf-8'):10,
   'nov':11, 'list':11,'november':11,'novembre':11,
   'dec':12, 'pros':12, 'dic':12, 'december':12, 'decembre':12, 'desember':12}

def lookharder(month1):
   """Look for a prefix match between the given month1 and known month names."""
   options = filter(lambda x: x.startswith(month1), mons)
   if not options: return 0
   return monthLookup[options[0]]

def fixupMMDD(month, day):
   """Swap MM/DD if MM > 12. Zero both if MM > 12 and DD not valid for MM. Convert month name
      to MM.
   """
   if month.isdigit():
      # swap MM/DD inversion
      if int(month) > 12: month, day = day, month
      if month.isdigit() and (int(month) < 1 or int(month) > 12): month, day = '0', '0'
   else:
      month = str(monthLookup.get(month, lookharder(month)))
   if not month: month = '0'
   if not day: day = '0'
   elif int(day) > monthDays[int(month)-1]: day = '0'
   return ['%02d' % int(month), '%02d' % int(day)]

loc = locale.getlocale()
for i in interesting:
   locale.setlocale(locale.LC_TIME, i)
   for x in xrange(1, 13):
      mon = eval('locale.MON_%s' % x)
      monthLookup[unicodedata.normalize('NFKD', locale.nl_langinfo(mon).decode('cp1252').lower())] = x
      mon = eval('locale.ABMON_%s' % x)
      monthLookup[unicodedata.normalize('NFKD', locale.nl_langinfo(mon).decode('cp1252').lower())] = x
locale.setlocale(locale.LC_TIME, loc)

fallback = re.compile('(\d\d\d\d)')

mons = monthLookup.keys()
mons.sort(key=lambda x:len(x),reverse=True)
monthMasker7 = re.compile(r'(\s|^|[.\-?])(%s)(\.?)(\s|$|[.\-?])' % '|'.join(mons), re.U)
# ignore the fact that feb only has 29 days every 4 years
monthDays = [31,29,31,30,31,30,31,31,30,31,30,31]

isCenturyPattern = re.compile('''(^|\ |\.|-)(s\.\ ?|tallet|-?talet|stol|sec\.?|jh\.?|sz|cent|
              в|siècle|eeuw|séc|jahrh(\.|undert|undeert)|årh\.?|\ e\.?$|
              מאה\ ה
              |gs\.|
              מאה\ ה
              |
              القرن\ ال
              |
              ق\.\ (?=N|\d)
              |[N0-9]{2}\ e\.?$)'''.decode('utf-8'), re.VERBOSE)
isCentury2Pattern = re.compile('((th|rd|nd|st)?\.? cent(ury)?\.?)|(cent th)')
isCenturyFollowsNumbers = re.compile('(N|\d)( ?th c(\.|en|nt)| ?d?e ?e\.?|e s\.?|jh\.| w\.)')
isRomanCentury = re.compile('(^| )([ivx]{1,10})([^a-z0-9.])(w(iek)?\.?)?')
def isCentury(pattern):
   ic = isCenturyPattern.search(pattern)
   if ic and ic.group(2):
      if 'cent' in ic.group(2):
         for ic2 in isCentury2Pattern.findall(pattern):
            yield ic2[0]
      else:
         yield ic.group(2)
      return

   ic = isCenturyFollowsNumbers.search(pattern)
   if ic:
      yield ic.group(2)
      return

   #look for uppercase roman numerals
   r = isRomanCentury.search(pattern)
   if r:
      if (len(r.group(2)) == 1 and not r.group(4)) or r.group(2) in ('xx', 'xxx'):
         pass  ## not good century
      else:
         yield r.group(4)

romanCenturies =  {'i': '1',   'ii':'2',    'iii':'3',    'iv':'4', 'v':'5',
       'vi':'6',   'vii':'7',   'viii':'8',   'ix':'9', 'x':'10',
       'xi':'11',  'xii': '12', 'xiii':'13', 'xiv':'14',
       'xv':'15',  'xvi':'16',  'xvii':'17',  'xviii':'18',
       'xix':'19', 'xx':'20',   'xxi':'21',   'xxii':'22'}
centurySpan = re.compile('(\d{1,2})\D*/\D*\d{1,2}')
centuryYears = re.compile('(\d{3,4})')
century = re.compile('(\d\d? ?\D+ ?)?(\d{1,2})')
centuryRoman = re.compile(r'(?:\s|^|-|\.|/)([xiv]{1,5})(?:\s|$|-|\.|\?|\\|/)')

F_IS_FLOURISHED = 'fIsFlourished'

canIgnore = re.compile(u'''(\u0645|    # indicates gregorian (which I assume)
                            \u202c|    # directional printing chars
                            \u200e|
                            \u200f|
                            levde|     # ?survived in swedish
                            "|         # quotes are uninteresting
                            g|         # indicates gregorian
                            )
                          ''', re.VERBOSE)

isDeath = re.compile('''^d\.\ ?|      # died
                        ^m\.\ ?|     # mort
                         ^zemř\.|
                         gest\.?|     # gestorben
                         توف(ي|ى)
                         |ум\.|
                         ت(\.|\ )
                         |died|
                         ^st\.\       # german - starb
                         '''.decode('utf-8'), re.VERBOSE)

isFlourished = re.compile('(^ca\. fl\.|(^|\s)fl(\.| |$)|^činný|^jin shi|chin shih|^époque|\
^ju ren|^verksam|^actif|^active|^حكم|činná|uzpl\.|\
ازدهر|كان حيا)'.decode('utf-8'))
altisFlourished = re.compile('(^ca\. fl\.|(^|\s)fl(\.| |$)|^činný|^f\.|^jin shi|chin shih|^époque|\
^ju ren|^verksam|^actif|^active|^حكم|činná|uzpl\.|\
ازدهر|كان حيا)'.decode('utf-8'))

isHijri = re.compile('هـ\.?|(?<=\d)h'.decode('utf-8'))

isCirca = re.compile('(^|\s| |\.)(circa|c(\.|a\.?)|um|erwähnt|oder später|\
ок\.|حو(\.?|في)|نحو|vor|nach|approximately|na[\d N]|\
depois de|antes de|vers|après|ante|non ante|post|ap )'.decode('utf-8'))
isCircaDontPull = re.compile('\?')

isBirth = re.compile('^b\. ?|^nar|^n\. ?|^né|geb\. ?|р\.|^و\.|ولد|^f\. ?|dz\.'.decode('utf-8'))
altisBirth = re.compile('^b\. ?|^nar|^n\. ?|^né|geb\. ?|р\.|^و\.|ولد|dz\.'.decode('utf-8'))

wildpattern1 = re.compile('(\d\d\d\d?)( أ?و \d\d?|/\d\d?| or \d\d?\d?| ou \d\d?\??| ?или \d\d?| vai \d\d?\d?\d?)'.decode('utf-8'))
wildpattern3 = re.compile('(?:[^0-9]|^)(\d\d\d)(x|\.|\?)(\??)')
wildpattern4 = re.compile('(\d\d\d\d?) (eller|ou) (\d\d\d\d?)')
wildpattern2 = re.compile('(\d\d)(\.\.|xx|\?\?|__|--)\??')

ad1 = re.compile('(a\. ?d\. ?)')
ad2 = re.compile('(d[ .]{0,2}c[ .]{1,2})')
ad3 = re.compile('(ap.*?j[-. ]*ch?\.?)')
ad4 = re.compile('((na|n)[. ]*chr\.?)')
ad5 = re.compile('(e[ .]*kr)')
ad6 = re.compile('(po[. ]*kr\.?)')
def isAD(pattern):
   for p in [ad1, ad2, ad3, ad4, ad5, ad6]:
      f = p.search(pattern)
      if f: 
         newway = f.group(1)
         return newway
   return None
   
bc1 = re.compile('(b[ .]{0,2}c(\.| |$))')
bc2 = re.compile(r'(\ba[ .]{0,2}c[ .]{0,2}\b)')
bc3 = re.compile('((av|avt|avant)[ .]+j[-. ]*ch?\.?)')
bc4 = re.compile('((voor|v)[. ]*ch?r?\.?)')
bc5 = re.compile('(f[ .]*kr)')
bc6 = re.compile('(př[. ]*kr\.?)'.decode('utf-8'))
bc7 = re.compile('''(לפנה"ס
                    |до н\.э
                    |ق\.
                    |bce)'''.decode('utf-8'), re.VERBOSE)
bc8 = re.compile('(p(\.|irms) ?m\. ?ē?\.?)'.decode('utf-8'))
bc9 = re.compile('((^| )v(\. )?(?=[0-9N]))')

def isBC(pattern):
   for p in [bc1, bc2, bc3, bc4, bc5, bc6, bc7, bc8, bc9]:
      f = p.search(pattern)
      if f: 
         newway = f.group(1)
         return newway
   return None

allwild = re.compile('^([.?*\- ])*$')  # pattern for all wild characters

NNNNmonthNN = re.compile('(\d\d\d\d) +([^0-9. ]*)\.? ?(\d\d?)')
def parseNNNNmonthNN(d):
   found = NNNNmonthNN.search(d)
   return found.group(1), found.group(2), found.group(3)

NNNNmonth = re.compile('(\d\d\d\d) +([^0-9. ]*)\.?')
def parseNNNNmonth(d):
   found = NNNNmonth.search(d)
   return found.group(1), found.group(2), '00'

NNmonthNNNN = re.compile('(\d\d?)\.? +([^0-9. ]*)\.? +(\d\d\d\d?)')
def parseNNmonthNNNN(d):
   found = NNmonthNNNN.search(d)
   return found.group(3), found.group(2), found.group(1)

monthNN_NNNN = re.compile('([^0-9. ]*)\.? +(\d\d?) +(\d\d\d\d)')
def parsemonthNN_NNNN(d):
   found = monthNN_NNNN.search(d)
   return found.group(3), found.group(1), found.group(2)

NNNN_NNmonth = re.compile('(\d\d\d\d) +(\d\d?) +([^0-9. ]*)\.?')
def parseNNNN_NNmonth(d):
   found = NNNN_NNmonth.search(d)
   return found.group(1), found.group(3), found.group(2)

NNNN_NN_NN = re.compile('(\d\d\d\d)(?: |-|/)(\d\d?)(?: |-|/)(\d\d?)')
def parseNNNN_NN_NN(d):
   found = NNNN_NN_NN.search(d)
   return found.group(1), found.group(2), found.group(3)

NNNNNNNN = re.compile('(\d\d\d\d)(\d\d)(\d\d)')
def parseNNNNNNNN(d):
   found = NNNNNNNN.search(d)
   return found.group(1), found.group(2), found.group(3)

NN_NNNN = re.compile('(\d\d)\.(\d\d\d\d)')
def parseNN_NNNN(d):
   found = NN_NNNN.search(d)
   return found.group(2), found.group(1), ''

NN_NN_NNNN = re.compile('(\d\d?)(?:-|/|\.)(\d\d?)(?:-|/|\.)(\d\d\d\d)')
def parseNN_NN_NNNN(d):
   found = NN_NN_NNNN.search(d)
   return found.group(3), found.group(2), found.group(1)

NNNN = re.compile('(\d\d?\d?\d?)')
def parseNNNN(d):
   found = NNNN.search(d)
   return found.group(1), '', ''

knownDatePatterns = {
   'NNNN month NN' : parseNNNNmonthNN,
   'NNNN monthNN' : parseNNNNmonthNN,
   'NNNN month N' : parseNNNNmonthNN,
   'NNNN monthN' : parseNNNNmonthNN,
   'NNNN month' : parseNNNNmonth,
   'NN month NNNN' : parseNNmonthNNNN,
   'NN month NNN' : parseNNmonthNNNN,
   'N month NNNN' : parseNNmonthNNNN,
   'month NN NNNN' : parsemonthNN_NNNN,
   'month N NNNN' : parsemonthNN_NNNN,
   'NNNN NN month' : parseNNNN_NNmonth,
   'NNNN N month' : parseNNNN_NNmonth,
   'NNNN NN NN' : parseNNNN_NN_NN,
   'NNNN-NN-NN' : parseNNNN_NN_NN,
   'NNNN/NN/NN' : parseNNNN_NN_NN,
   'NNNN-NN-NN-' : parseNNNN_NN_NN,
   'NNNN N N' : parseNNNN_NN_NN,
   'NNNN/N/N' : parseNNNN_NN_NN,
   'NNNN/N/NN' : parseNNNN_NN_NN,
   'NNNN/NN/N' : parseNNNN_NN_NN,
   'NN.NN.NNNN' : parseNN_NN_NNNN,
   'NN-NN-NNNN' : parseNN_NN_NNNN,
   'NN/NN/NNNN' : parseNN_NN_NNNN,
   'NN.N.NNNN' : parseNN_NN_NNNN,
   'N.NN.NNNN' : parseNN_NN_NNNN,
   'N.N.NNNN' : parseNN_NN_NNNN,
   'NN.NNNN' : parseNN_NNNN,
   'NNNNNNNN' : parseNNNNNNNN,
   'NNNN' : parseNNNN,
   'NNN' : parseNNNN,
   'NN' : parseNNNN,
   'N' : parseNNNN,
}

def sanity(date1parsed, date2parsed, datetype):
   """Check that the date range makes sense. The dates aren't in the future. They span
      a reasonable range (ie 115 years for a 'lived' date).

      Either date might be set to [0, '', ''] if it seems wrong. The month and day can get
      swapped if it looks like they need it. The month name gets replaced with MM.

      Wrong: 
      -datetype is 'lived' and range is > 115 years
      -datetype is 'circa' and range is > 130 years
      -datetype is 'flourished' and range is > 200 years
      -datetype is 'lived' and range is < 5 years
      -range is < 20 and both could be century references
      -end > beginning of range
      -either year is > 2100
      -month is not in the range 01-12
      -day is not in the allowable range for that month

      Args:
      date1parsed: [year, month, day]
      date2parsed: [year, month, day]
      datetype: 'lived', 'circa', or 'flourished'

      Returns:
      date1parsed 
      date2parsed
   """
   if date1parsed and int(date1parsed[0]) > 2100:
      date1parsed = [0, '', '']
   if date2parsed and int(date2parsed[0]) > 2100:
      date2parsed = [0, '', '']
   start, end = 0, 0
   if date1parsed and date2parsed:
      start = int(date1parsed[0])
      end = int(date2parsed[0])
   if start and end:
      if end < start: end = 0
      elif end - start > 115 and datetype == 'lived': start, end = 0, 0
      elif end - start > 130 and datetype == 'circa': start, end = 0, 0
      elif end - start > 200 and datetype == 'flourished': start, end = 0, 0
      elif end - start < 5 and datetype == 'lived': start, end = 0, 0
      elif end - start < 20:
         if (end in [12, 13, 14, 15, 16, 17, 18, 19, 20] or
             start in [12, 13, 14, 15, 16, 17, 18, 19, 20]): start, end = 0, 0
      if not start:
         date1parsed = [0, '', '']
         date2parsed = [0, '', '']
      if not end:
         date2parsed = [0, '', '']
   if date1parsed and date1parsed[1]:
      month, day = fixupMMDD(date1parsed[1], date1parsed[2])
      date1parsed = [date1parsed[0], month, day]
   if date2parsed and date2parsed[1]:
      month, day = fixupMMDD(date2parsed[1], date2parsed[2])
      date2parsed = [date2parsed[0], month, day]
   return date1parsed, date2parsed

class dateFld(object):
   def __init__(self, datesub, flags=F_IS_FLOURISHED):
      """Initializes a dateFld object from a date subfield.

      Args:
         datesub: A date subfield including the subfield code.
         flags: Defaults to F_IS_FLOURISHED to indicate that 'f' means flourished instead of born. 
                Use the empty string to indicate that 'f' is born.
      """

      self.date1parsed = [0, '', '']
      self.date2parsed = [0, '', '']
      self.datetype = 'lived'

      self.date1 = None
      self.date1pattern = None
      self.date2 = None
      self.date2pattern = None

      self.flags = flags
      self.hijri =    None
      # necessary normalizing to allow successful split
      norminput, pattern = self.startPattern(datesub)  # sets hijri

      if norminput in handates:
         self.date1parsed, self.date2parsed, self.datetype = handates[norminput]
         return 
      if norminput.find('dynasty') != -1: return

      # sets date1, date1pattern, date2, date2pattern
      self.split(norminput, pattern)          

      ## if a mix of century and "real" date, only parse the "real" date
      date1IsCentury, date2IsCentury = None, None
      if self.date1pattern:
         date1IsCentury = [j for j in isCentury(self.date1pattern)]
      if self.date2pattern:
         date2IsCentury = [j for j in isCentury(self.date2pattern)]
      if self.date1 and self.date2 and (date1IsCentury or date2IsCentury) and not (date1IsCentury and date2IsCentury):
         # usable year in non-century date so use it
         if date1IsCentury and 'NNN' in self.date2pattern: 
            self.date1, self.date1pattern = None, None
            date1IsCentury, date2IsCentury = None, None
         elif 'NNN' in self.date1pattern:
            self.date2, self.date2pattern = None, None
            date1IsCentury, date2IsCentury = None, None

      if date1IsCentury or date2IsCentury: self.doCentury()
      else:
         date1isBC = False
         if self.date1pattern and self.date1:
            rc = self.parseDate(self.date1, self.date1pattern) 
            if not rc[0]:
               rc = self.solveWildCards(self.date1, self.date1pattern, True, rc[2])
            if not rc[0]:
               found = fallback.search(self.date1)
               if found: self.date1parsed = [int(found.group(1)), '', '']
            else:
               self.date1pattern, self.date1parsed, date1isBC = rc
               if date1isBC: self.date1parsed[0] = self.dobc(self.date1parsed[0])
         if self.date2pattern and self.date2:
            rc = self.parseDate(self.date2, self.date2pattern) 
            if not rc[0]:
               rc = self.solveWildCards(self.date2, self.date2pattern, False, rc[2])
            if not rc[0]:
               found = fallback.search(self.date2)
               if found: self.date2parsed = [int(found.group(1)), '', '']
            else:
               self.date2pattern, self.date2parsed, date2isBC = rc
               if date2isBC and self.date2pattern:
                  self.date2parsed[0] = self.dobc(self.date2parsed[0])
                  if not date1isBC: self.date1parsed[0] = self.dobc(self.date1parsed[0])
                  self.date2parsed[0] = int(self.date2parsed[0])

            if self.hijri:
               if self.date1parsed[0]:
                  self.date1parsed[0] = hijri_to_gregorian(self.date1parsed[0], 1, 1)[0]
               if self.date2parsed[0]:
                  self.date2parsed[0] = hijri_to_gregorian(self.date2parsed[0], 1, 1)[0]

      self.date1parsed, self.date2parsed = sanity(self.date1parsed, self.date2parsed, self.datetype)

   def startPattern(self, input):
      """Do the normalization that is possible before splitting the string and that is needed 
         to split the string.

         Args:
            input: date subfield

         Returns:
            (norminput, pattern)
            norminput is the normalized date subfield. pattern is the preliminary date pattern. 
            The pattern will continue to be refined after the date is split.

         Sets:
            self.hijri: if the date subfield is hijri
            self.datetype: if the date was flourished
      """
      pattern = unicodedata.normalize('NFKD', unicode(input[1:]).lower())
      pattern = ''.join([unicode(unicodedata.digit(d, d)) for d in pattern])
      pattern = re.sub(',', ' ', pattern)
      # convert various dashes to dash
      pattern = re.sub(u'\u2212|\u2013|\u2014|\u05be|\u2010|\u2015|\u30fb', '-', pattern)
      pattern = pattern.replace('bzw.', '-') ## from DNB records
      pattern = re.sub(u'\u061f', '?', pattern)  # arabic question mark
      pattern = re.sub('----|-t\.|\[.*h\]| reg\..*$| age .*$', '', pattern)
      pattern = re.sub('\(|\)|;|<|>|\]|\[', '', pattern)
      ## moved these to overrides
      ##pattern = re.sub('av\. ?j\.?-\.?c', 'av jc', pattern)
      ##pattern = re.sub('-talet', ' talet', pattern)
      pattern = re.sub('\[|\]', '', pattern)
      pattern = pattern.replace('xxxx', '').replace('gegenwart', '')
      pattern = re.sub('\.{4,10}', '', pattern)
      pattern = pattern.strip(' ')
      pattern = re.sub(' +', ' ', pattern)
      flourishedpattern = isFlourished if self.flags.find('fIsFlourished') == -1 else altisFlourished
      if flourishedpattern.search(pattern):
         pattern = flourishedpattern.sub('', pattern)
         self.datetype = 'flourished'
      norminput = pattern
      pattern = monthMasker7.sub(r'\1month\4', pattern)
      self.hijri = isHijri.search(pattern)
      if self.hijri:
         pattern = isHijri.sub('', pattern).strip()
         norminput = isHijri.sub('', norminput).strip()
      pattern = re.sub('\d', 'N', pattern)
      return norminput, pattern

   def split(self, norminput, pattern):
      """Split a date substring into begining (birth) and ending (death) dates or 
         determine that the field is an ending (death) date.

         Args:
            norminput: created by startPattern()
            pattern: created by startPattern()

         Returns:
            None

         Sets:
            self.date1: portion of norminput describing the beginning date
            self.date1pattern: portion of pattern describing the beginning date
            self.date2: portion of norminput describing the ending date
            self.date2pattern: portion of pattern describing the ending date
      """
      death = isDeath.search(pattern)
      if death:
         self.date2, self.date2pattern = isDeath.sub('', norminput), isDeath.sub('', pattern)
         return
      hyphencount = pattern.count('-')
      if hyphencount == 0:
         if 'NNNNNNNN' in pattern:
            f = re.search('(\d{8})', norminput)
            y2, y1 = f.group(1)[4:], f.group(1)[:4]
            m2, d2 = y2[:2], y2[2:]
            if abs(int(y2) - int(y1)) < 100 or int(m2) > 12 or int(d2) > 31:
               norminput = norminput.replace(y1, y1+'-', 1)
               pattern = pattern.replace('NNNN', 'NNNN-', 1)
               hyphencount = 1
         else:
            self.date1, self.date1pattern = norminput.replace('-', ''), pattern
            return
      if hyphencount == 1:
         self.date1pattern, self.date2pattern = pattern.split('-')
         self.date1, self.date2 = norminput.split('-')
         self.date1 = self.date1.strip()
         self.date2 = self.date2.strip()
         self.date1pattern = self.date1pattern.strip()
         self.date2pattern = self.date2pattern.strip()
         return

      o = overrides(pattern, norminput)
      if o:
         self.date1pattern, self.date2pattern, self.date1, self.date2 = o
         return
      self.date1pattern = pattern
      self.date1 = norminput

   def dobc(self, year):
      """Convert year to its BC equivalent (ie, multiply by -1!)"""
      return year if not year else year * -1

   def __repr__(self):
       """Formatted for display."""
       towrite = ''
       mylist = [self.date1, self.date1pattern, self.date1parsed, 
          self.date2, self.date2pattern, self.date2parsed, self.datetype]
       towrite = '\t'.join([unicode(x) for x in mylist])
       return towrite.encode('utf-8')

   def solveWildCards(self, dateString, datePattern, isDate1, bc):
      """Recognize and resolve wild cards in date patterns.
       
         Args:
            dateString: normalized date string
            datePattern: pattern so far 
            isDate1: start/end (birth/death) indication
            bc: flag if we already know the date is BC

         Returns:
            (datePattern, [year, mm, dd], isbc)
            datePattern: modified datePattern
            [year, mm, dd]: parsed year, month and day
            isbc: boolean indicating pattern was for a BC date
            
         Sets:
            self.datetype
      """
      ## basically 'circa'
      # or NN
      found = wildpattern1.search(dateString)
      if found:
         dateString = wildpattern1.sub(r'\1', dateString)
         datePattern = 'NNNN'
         rc = self.parseDate(dateString, datePattern)
         if self.datetype == 'lived': self.datetype = 'circa'
         return rc
      ## basically circa
      ## ? can be circa or wild
      ## . can be wild or punc
      ## x is wild
      # .[?]
      # x
      # ?
      found = wildpattern3.search(dateString)
      if found:
         if (found.group(3) or ## definitely wild if has circa flag at end.
             ## more likely to be wild if starts with '0' or '1' or '20' ie. 197.
             found.group(1)[0] in '01' or found.group(1).startswith('20') or
             found.group(2) == 'x'):
            if isDate1: newdigit = '9' if bc else '0'
            else: newdigit = '0' if bc else '9'
         else: ## more likely to be circa or punc
            newdigit = ''
         dateString = wildpattern3.sub(r'\g<1>%s' % newdigit, dateString)
         datePattern = 'NNNN'
         rc = self.parseDate(dateString, datePattern)
         if self.datetype == 'lived': self.datetype = 'circa'
         return rc
      ## another form of circa
      found = wildpattern4.search(dateString)
      if found:
         dateString = wildpattern4.sub(r'\g<1>', dateString)
         datePattern = 'NNNN'
         rc = self.parseDate(dateString, datePattern)
         if self.datetype == 'lived': self.datetype = 'circa'
         return rc
      ## basically a century
      ## NN..
      ## NNxx
      ## NN__
      ## NN--
      ## NN??
      found = wildpattern2.search(dateString)
      if found:
         newdigits = '50'
         dateString = wildpattern2.sub(r'\g<1>%s' % newdigits, dateString)
         datePattern = 'NNNN'
         rc = self.parseDate(dateString, datePattern)
         self.datetype = 'flourished'
         return rc
      return None, None, bc

   def parseDate(self, dateString, datePattern):
      """Recognize and resolve wild cards in date patterns.
       
         Args:
            dateString: normalized date string
            datePattern: pattern so far 

         Returns:
            (datePattern, [year, mm, dd], isbc)
            datePattern: modified datePattern
            [year, mm, dd]: parsed year, month and day
            isbc: boolean indicating pattern was for a BC date
            
         Sets:
            self.datetype
      """
      if allwild.search(datePattern): 
         return '', [0, '', ''], False

      bc, circa, flourished = None, None, None
      if datePattern not in knownDatePatterns:
         birthpattern = isBirth if self.flags.find('fIsFlourished') == -1 else altisBirth
         datePattern = birthpattern.sub('', datePattern).strip()
         dateString = birthpattern.sub('', dateString).strip()
      if datePattern not in knownDatePatterns:
         bc = isBC(datePattern)
         if bc: 
            datePattern = datePattern.replace(bc, '').strip()
            dateString = dateString.replace(bc, '').strip()
      if datePattern not in knownDatePatterns:
         ad = isAD(datePattern)
         if ad:
            datePattern = datePattern.replace(ad, '').strip()
            dateString = dateString.replace(ad, '').strip()
      if datePattern not in knownDatePatterns:
         circa = isCirca.search(datePattern)
         if circa:  
            ## do this one twice. some dates have 2 and they overlap
            datePattern = isCirca.sub('', datePattern).strip()
            datePattern = isCirca.sub('', datePattern).strip()
            dateString = isCirca.sub('', dateString).strip()
            dateString = isCirca.sub('', dateString).strip()
      if datePattern not in knownDatePatterns:
         flourishedpattern = isFlourished if self.flags.find('fIsFlourished') == -1 else altisFlourished
         flourished = flourishedpattern.search(datePattern)
         if flourished:
            datePattern = flourishedpattern.sub('', datePattern).strip()
            dateString = flourishedpattern.sub('', dateString).strip()
      if datePattern not in knownDatePatterns:
         noisestuff = canIgnore.search(datePattern)
         if noisestuff:
            datePattern = canIgnore.sub('', datePattern).strip()
            dateString = canIgnore.sub('', dateString).strip()
      if datePattern and (datePattern[-1] == '.' or datePattern[0] == '.'):
         if ' ' in datePattern or '?' in datePattern:
            datePattern = datePattern.strip('.').strip()
            dateString = dateString.strip('.').strip()
      if 'NNNN' in datePattern and datePattern[-1] == '.':
         datePattern = datePattern.strip('.').strip()
         dateString = dateString.strip('.').strip()
      if flourished: self.datetype = 'flourished'
      elif (circa or isCircaDontPull.search(datePattern)) and self.datetype == 'lived': self.datetype = 'circa'
      if datePattern in knownDatePatterns:
         year, month, day = knownDatePatterns[datePattern](dateString)
         return datePattern, [int(year), month, day], bc
      return None, None, bc

   def doCentury(self):
      """Parse a date subfield containing century reference(s).
       
         Sets:
            self.date1parsed: [year, mm, dd] for beginning (birth) year
            self.date2parsed: [year, mm, dd] for ending (death) year
      """
      year1 = self.parseCentury(self.date1) if self.date1 else 0
      year2 = self.parseCentury(self.date2) if self.date2 else 0
      if self.hijri:
         ## formula of hijri century + 6 -> gregorian century -1 * 100
         ## using this per Gina from EGAXA.
         if year1: year1 += 6
         if year2: year2 += 6
      if year1 > 0: year1 -= 1
      if year2 > 0: year2 -= 1
      year1 *= 100
      year2 *= 100
      if year1 and year2:
         ## if date2 is BC then so is date1
         if year2 < 0 and year1 > 0: year1 *= -1
         if year2 - year1 > 200: year1, year2 = 0, 0
         elif year2 > year1: 
             year1 += 50
             year2 -= 49
      self.date1parsed = [int(year1), '' ,'']
      self.date2parsed = [int(year2), '' ,'']

   def parseCentury(self, dateString):
      """Parse a date portion containing century reference.

         Args: 
            dateString: string to parse

         Returns:
            year that represents the century 
       
         Sets:
            self.datetype: flourished
      """
      bc = isBC(dateString)
      if bc: dateString = dateString.replace(bc, '')
      self.datetype = 'flourished'
      found = centuryYears.search(dateString)
      if found: return (int(found.group(1)) // 100) + 1
      found = centuryRoman.search(dateString)
      while found:
         rdate = found.group(1)
         dateString = dateString.replace(rdate, romanCenturies[rdate], 1)
         found = centuryRoman.search(dateString)
      clean = dateString.replace('.','')
      found = centurySpan.search(clean)
      if found: cent = found.group(1)
      if not found:
         found = century.search(clean)
         if found: cent = found.group(2)
      if found:
         cent = int(cent)
         if bc: cent *= -1
         return cent
      return 0

