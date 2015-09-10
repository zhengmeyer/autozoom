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
  f['bandwidth'] = float(freq['chan_def'][3].split(' ')[0])
  f['band_freqs'] = []
  for ch in freq.getall('chan_def'):
    numchans += 1
    f['band_freqs'].append(float(ch[1].split(' ')[0]))
  f['num_channels'] = numchans
  if f['side_band'] == 'L':
    f['min_freq'] = f['band_freqs'][numchans-1] - f['bandwidth']
    f['max_freq'] = f['band_freqs'][0]
  if f['side_band'] == 'R':
    f['min_freq'] = f['band_freqs'][0]
    f['max_freq'] = f['band_freqs'][numchans-1] + f['bandwidth']
  return f

# calculate the zoom frequencies of the given mode
def cal_zoomfreqs(v, md):
  f = {}
  zf = {}
  # get frequency information from each frequency setup
  for freq in md.getall('FREQ'):
    f[freq[0]] = get_freqsetup(v['FREQ'][freq[0]])
  # calculate zoom frequencies
  zf = f
  return zf

def st_zoomfreqs(v, md, st):
  z = {}
  mode = v['MODE'][md]
  zoom = cal_zoomfreqs(v, mode)
  for freq in mode.getall('FREQ'):
    if st in freq:
      z = zoom[freq[0]]
  return z

def Autozoom(file):
  zoomfreqs = {}
  fp = open(file, 'r')
  v = vex.parse(fp.read())
  fp.close()
  # calculate zoom frequencies for each station within each mode
  for md in v['MODE']:
    zoomfreqs[md] = {}
    for st in v['STATION']:
      zoomfreqs[md][st] = st_zoomfreqs(v, md, st)
    print(zoomfreqs)
    # insert station zoomfreqs into .v2d file
  return

if __name__=="__main__":
  import sys
  Autozoom(sys.argv[1])
