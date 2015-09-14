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
from cases import zoom_options

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
  
  f['band_freqs'] = band_freqs
  f['num_channels'] = numchans
  f['band_overlap'] = 0.0

  if f['side_band'] == 'L':
    if len(band_freqs) > 1:
      # sometimes the first band only consists of half bandwidth
      # need to consider it later
      f['band_overlap'] =  f['bandwidth'] - (band_freqs[0] - band_freqs[1])
    f['min_freq'] = band_freqs[numchans-1] - f['bandwidth'] + f['band_overlap']
    f['max_freq'] = band_freqs[0]

  if f['side_band'] == 'U':
    if len(band_freqs) > 1:
      # sometimes the first band only consists of half bandwidth
      # need to consider it later
      f['band_overlap'] = f['bandwidth'] - (band_freqs[1] - band_freqs[0])
    f['min_freq'] = band_freqs[0]
    f['max_freq'] = band_freqs[numchans-1] + f['bandwidth']

  f['f_coverage'] = f['max_freq'] - f['min_freq']
  
  return f

# calculate the zoom frequencies of the given mode
def cal_zoomfreqs(v, md):
  freqs = {}
  zfreqs = {}
  
  for f in v['MODE'][md].getall('FREQ'):
    # get frequency information from each frequency setup
    freqs[f[0]] = get_freqsetup(v['FREQ'][f[0]])

  # !!!!!!!!!!!!!!!!!
  # check whether all frequency setup has the same min_freq and max_freq
  # check whether all bandwidth are 2^N

  # calculate zoom frequencies
  # !!!!!!!!!!!!!!!!!!!!!!!!!!!
  # always select one at the moment
  options = zoom_options()
  zfreqs = options[2](freqs)
  return zfreqs

def Autozoom(vexfile, scan, v2dfile):
  zoomfreqs = {}
  fp = open(vexfile, 'r')
  v = vex.parse(fp.read())
  fp.close()
  # calculate zoom frequencies for each station within each mode
  md = v['SCHED'][scan]['mode']
  zoomfreqs[md] = {}
  zoom = cal_zoomfreqs(v, md)
  for freq in v['MODE'][md].getall('FREQ'):
    for st in v['STATION']:
      if st in freq:
        zoomfreqs[md][st] = zoom[freq[0]]

  #print(zoomfreqs[md])

  # read .v2d file
  v2d = open(v2dfile, 'r')
  
  # construct name for the new v2d file (with scan number in it)
  name = v2dfile.split('.')[:-1]
  name.extend([scan, 'v2d'])
  name = '.'.join(name)

  scanv2d = open(name, 'w')
  token = False;
  for line in v2d:
    if line.strip()[:7] == 'ANTENNA':
      token = True;
      st = line.strip()[-2:]
    if line.strip() == '}' and token == True:
      token = False
      for zf in zoomfreqs[md][st]:
        scanv2d.write('\t%s\n' % zf)
    scanv2d.write(line)

  # write station zoomfreqs into a new .v2d file (with scan number in the filename)
  v2d.close()
  scanv2d.close()
  return

# input parameters: vex.file.name scan
if __name__=="__main__":
  import sys
  Autozoom(sys.argv[1], sys.argv[2], sys.argv[3])
