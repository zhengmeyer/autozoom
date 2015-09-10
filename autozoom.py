#########################################################################
# <AutoZoom: calculate ZoomFreqs automatically>                         #             
# Copyright (C) <2015> <Zheng Meyer-Zhao>                               #
#                                                                       #
# AutoZoom is free software: you can redistribute it and/or modify      #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# AutoZoom is distributed in the hope that it will be useful,           #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <http://www.gnu.org/licenses/>. #
#########################################################################

import vex

# Retrieve information from frequency setup
# Keys: side_band, num_channels, bandwidth, band_freqs, sample_rate
def get_freqsetup(freq):
  f = {}
  numchans = 0
  f['sample_rate'] = freq['sample_rate']
  f['side_band'] = freq['chan_def'][2]
  f['bandwidth'] = freq['chan_def'][3]
  f['band_freqs'] = []
  for ch in freq.getall('chan_def'):
    numchans += 1
    f['band_freqs'].append(ch[1])
  f['num_channels'] = numchans
  return f

# Dictionary antenna channels structure
# {STATION: {MODE: frequency_setup } }
# see get_freqsetup for Keys in frequency_setup
def get_antchannels(v):
  d = {}
  # loop through MODE, retrieve antenna FREQ setup
  for st in v['STATION']:
    d[st] = {}
    for md in v['MODE']:
      d[st][md] = {}
      for freq in v['MODE'][md].getall('FREQ'):
        if st in freq:
          d[st][md] = get_freqsetup(v['FREQ'][freq[0]])
  return d;


def calc_zoomfreqs(v):
  antchannels = get_antchannels(v);
  print(antchannels)
  return

def Autozoom(file):
  fp = open(file, 'r')
  v = vex.parse(fp.read())
  fp.close()
  calc_zoomfreqs(v)
  return

if __name__=="__main__":
  import sys
  Autozoom(sys.argv[1])
