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
# Keys: min_freq, band_overlap, max_freq, side_band, f_coverage,
# bandwidth, num_channels, sample_rate
def get_freqsetup(freq):
  f = {}
  numchans = 0
  f['sample_rate'] = float(freq['sample_rate'].split(' ')[0])
  f['side_band'] = freq['chan_def'][2]
  f['bandwidth'] = float(freq['chan_def'][3].split(' ')[0])
  band_freqs = []
  for ch in freq.getall('chan_def'):
    numchans += 1
    band_freqs.append(float(ch[1].split(' ')[0]))
  
  f['num_channels'] = numchans

  if f['side_band'] == 'L':
    f['min_freq'] = band_freqs[numchans-1] - f['bandwidth']
    f['max_freq'] = band_freqs[0]
  if f['side_band'] == 'U':
    f['min_freq'] = band_freqs[0]
    f['max_freq'] = band_freqs[numchans-1] + f['bandwidth']

  f['f_coverage'] = f['max_freq'] - f['min_freq']
  f['band_overlap'] = f['f_coverage'] - f['bandwidth'] * numchans
  
  return f

# calculate the zoom frequencies of the given mode
def cal_zoomfreqs(v, md):
  freqs = {}
  zfreqs = {}
  
  for f in v['MODE'][md].getall('FREQ'):
    # get frequency information from each frequency setup
    freqs[f[0]] = get_freqsetup(v['FREQ'][f[0]])
  print(freqs)
  # calculate zoom frequencies
  zfreqs = freqs
  return zfreqs

def Autozoom(file, md):
  zoomfreqs = {}
  fp = open(file, 'r')
  v = vex.parse(fp.read())
  fp.close()
  # calculate zoom frequencies for each station within each mode
  zoomfreqs[md] = {}
  zoom = cal_zoomfreqs(v, md)
  for freq in v['MODE'][md].getall('FREQ'):
    for st in v['STATION']:
      if st in freq:
        zoomfreqs[md][st] = zoom[freq[0]]

  # insert station zoomfreqs into .v2d file
  return

if __name__=="__main__":
  import sys
  Autozoom(sys.argv[1], sys.argv[2])
