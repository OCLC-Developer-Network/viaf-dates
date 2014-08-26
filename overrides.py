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
def overrides(pattern, norminput):
   """Split a date subfield into beginning date and ending date. Needed for fields with 
      multiple hyphens.

      Args:
      pattern: date pattern
      norminput: normalized date string

      Returns:
      start date portion of pattern
      start date portion of norminput
      end date portion of pattern
      end date portion of norminput
   """
   if pattern == 'NNNN-NNNN-':
      return pattern[:4], pattern[5:9], norminput[:4], norminput[5:9]
   if pattern == 'NNNN?-NNNN? av. j.-c.':
      return pattern[:5], pattern[6:], norminput[:5], norminput[6:]
   if pattern == 'NN---NNNN':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'NNNN-NNNN av. j.-c.':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'NNNN--':
      return pattern[:4], None, norminput[:4], None
   if pattern == 'NNNN-NN--':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'f. NNNN-NN-NN':
      return pattern, None, norminput, None
   if pattern == 'NNNN?-NNNN av. j.-c.':
      return pattern[:5], pattern[6:], norminput[:5], norminput[6:]
   if pattern == 'NN-NN-NNNN':
      return pattern, None, norminput, None
   if pattern == '-NNNN-':
      return None, pattern[:-1], None, norminput[:-1]
   if pattern == 'NNNN--NNNN':
      return pattern[:4], pattern[6:], norminput[:4], norminput[6:]
   if pattern == 'NNNN-NN--?':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'NNNNNNNN':
      return pattern, None, norminput, None
   if pattern == 'NN..-NNNN av. j.-c.':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'NNNN-NNN-':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'fl. NNNN-NNN-':
      return pattern[:8], pattern[9:], norminput[:8], norminput[9:]
   if pattern == 'NNNN av. j.-c.-NNNN':
      return pattern[:-5], pattern[-4:], norminput[:-5], norminput[-4:]
   if pattern == 'NNNN-NN-NN-':
      return pattern[:-1], None, norminput[:-1], None
   if pattern == 'NN-- -NNNN':
      return pattern[:4], pattern[-4:], norminput[:4], norminput[-4:]
   if pattern == 'NNNN-NN-NN':
      return pattern, None, norminput, None
   if pattern == 'NN..-NNNN? av. j.-c.':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'NNNN--...':
      return pattern[:4], pattern[6:], norminput[:4], norminput[6:]
   if pattern == 'fl. NNN--NNNN':
      return pattern[:8], pattern[-4:], norminput[:8], norminput[-4:]
   if pattern == 'fl. NN---NNNN':
      return pattern[:8], pattern[-4:], norminput[:8], norminput[-4:]
   if pattern == 'NN---NNNN?':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'fl. NNN--NNN-':
      return pattern[:8], pattern[-4:], norminput[:8], norminput[-4:]
   if pattern == 'NN..-NN.. av. j.-c.':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'NN--':
      return pattern, None, norminput, None
   if pattern == 'fl. NN--':
      return pattern, None, norminput, None
   if pattern == 'NN..?-NN..? av. j.-c.':
      return pattern[:5], pattern[6:], norminput[:5], norminput[6:]
   if pattern == 'NNN-NNN av. j.-c.':
      return pattern[:3], pattern[4:], norminput[:3], norminput[4:]
   if pattern == 'NN---NN--':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'NNN--NNN-':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'NN-..-NN..':
      return pattern[:2]+pattern[3:5], pattern[6:], norminput[:2]+norminput[3:5], norminput[6:]
   if pattern == 'NN---':
      return pattern[:-1], None, norminput[:-1], None
   if pattern == 'NNNN?-NNNN?':
      return pattern[:5], pattern[6:], norminput[:5], norminput[6:]
   if pattern == 'NNNN-NN-NN-NNNN-NN-NN':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'NNNN-N-NN':
      return pattern, None, norminput, None
   if pattern == 'NNNN-N-N':
      return pattern, None, norminput, None
   if pattern == 'NNNN-NNNN-NN-NN':
      return pattern[:4], pattern[6:], norminput[:4], norminput[6:]
   if pattern == 'NNNN-N-NN-NNNN-N-NN':
      return pattern[:9], pattern[10:], norminput[:9], norminput[10:]
   if pattern == 'NNNN-NN-NN-NNNN':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'NNNN-N-NN-NNNN-N-N':
      return pattern[:9], pattern[10:], norminput[:9], norminput[10:]
   if pattern == 'NNNN-N-N-NNNN-N-NN':
      return pattern[:8], pattern[9:], norminput[:8], norminput[9:]
   if pattern == 'NNNN-N-NN-NNNN-NN-NN':
      return pattern[:9], pattern[10:], norminput[:9], norminput[10:]
   if pattern == 'NNNN-NN-NN-NNNN-N-NN':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'month NN NNNN-NNNN-NN-NN':
      p = pattern.split('-', 1)
      n = norminput.split('-', 1)
      return p[0], p[1], n[0], n[1]
   if pattern == 'NN month NNNN-NNNN-NN-NN':
      p = pattern.split('-', 1)
      n = norminput.split('-', 1)
      return p[0], p[1], n[0], n[1]
   if pattern == 'NNNN-N-N-NNNN-N-N':
      return pattern[:8], pattern[9:], norminput[:8], norminput[9:]
   if pattern == '-NNNN-NN-NN':
      return None, pattern[1:], None, norminput[1:]
   if pattern == 'NNNN-NN-NN-month NN NNNN':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'NNNN-N-N-NNNN-NN-NN':
      return pattern[:8], pattern[9:], norminput[:8], norminput[9:]
   if pattern == 'NNNN-NN-NN-NNNN-N-N':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'NNNN-NN-NN-NN month NNNN':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'NNNN-NN-N-NNNN-N-NN':
      return pattern[:9], pattern[10:], norminput[:9], norminput[10:]
   if pattern == 'NNNN-N-NN-NNNN-NN-N':
      return pattern[:9], pattern[10:], norminput[:9], norminput[10:]
   if pattern == 'month N NNNN-NNNN-NN-NN':
      p = pattern.split('-', 1)
      n = norminput.split('-', 1)
      return p[0], p[1], n[0], n[1]
   if pattern == 'NNNN-N-N-month NN NNNN':
      return pattern[:8], pattern[9:], norminput[:8], norminput[9:]
   if pattern == 'NNNN-NN-NN-month N NNNN':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'NNNN-NN-NN-N month NNNN':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'NNNN-NN-N-NNNN-NN-NN':
      return pattern[:9], pattern[10:], norminput[:9], norminput[10:]
   if pattern == 'N month NNNN-NNNN-NN-NN':
      p = pattern.split('-', 1)
      n = norminput.split('-', 1)
      return p[0], p[1], n[0], n[1]
   if pattern == 'NNNN-NN-NN-NNNN-NN-N':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'NNNN-NN-NN-NNNN/NN/NN':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'NNNN-N-N-NNNN-NN-N':
      return pattern[:8], pattern[9:], norminput[:8], norminput[9:]
   if pattern == 'NNNN-N-NN-NNNN':
      return pattern[:9], pattern[10:], norminput[:9], norminput[10:]
   if pattern == 'NNNN-NN-NN-month NNNN':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:] 
   if pattern == 'NNNN-NN-N-NNNN-N-N':
      return pattern[:9], pattern[10:], norminput[:9], norminput[10:]
   if pattern == 'NNNN-NN-NN}}':
      return pattern, None, norminput, None
   if pattern == 'NN-NN-NNNN-NN-NN-NNNN':
      return pattern[:10], pattern[11:], norminput[:10], norminput[11:]
   if pattern == 'NNNN-N-N-month N NNNN':
      return pattern[:8], pattern[9:], norminput[:8], norminput[9:]
   if pattern == 'NNNN-NNNN-N-NN':
      return pattern[:4], pattern[5:], norminput[:4], norminput[5:]
   if pattern == 'NNNN-N-NN-month NNNN':
      return pattern[:9], pattern[10:], norminput[:9], norminput[10:]
   if pattern == 'c. NNNN-NNNN-NN-NN':
      return pattern[:7], pattern[8:], norminput[:7], norminput[8:]
   if pattern == 'NNNN-N-N-NNNN':
      pattern[:4], pattern[5:], norminput[:4], norminput[5:]

   return None

