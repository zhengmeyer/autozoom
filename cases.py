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

# check if a number is 2^N
def is_pow2(num):
  return num > 0 and ((num & (num - 1) == 0))

# add zoom freqencies to each antenna
def addzoomfreqs(zf, refnchans, refbw):
  for ch in range(refnchans):
        zf.append("addZoomFreq = freq@%f/bw@%f" % (reffreqs[ch], refbw))

# Case 1: zoom band <-> recorded band
# ALL stations have the same frequency coverage (max. 2048 MHz).
# Start and end frequencies of all stations are the same. Bandwidth is 2^N.
def allvlbi(freqs):
  z = {}
  reffreqs = []
  refnchans = 0
  refbw = 2048.0
  pow2 = True
  minfreqs = set()
  maxfreqs = set()

  # get the smallest bandwidth of all frequency setup
  # use it as reference for zoom frequency
  for f in freqs.keys():
    pow2 &= is_pow2(int(freqs[f]['bandwidth']))
    minfreqs.add(freqs[f]['min_freq'])
    maxfreqs.add(freqs[f]['max_freq'])
    if int(refbw) >= int(freqs[f]['bandwidth']):
      refbw = int(freqs[f]['bandwidth'])
      reffreqs = freqs[f]['band_freqs']
      refnchans = freqs[f]['num_channels']
  
  if not pow2:
    raise Exception("Not all bandwidth is 2^N!!!")
  if len(minfreqs) != 1 or len(maxfreqs) != 1:
    raise Exception("Start frequency or end frequency of antennas are not the same!!!")
  if not reffreqs or refnchans == 0:
    raise Exception("No reference frequency setup found!!!")

  for f in freqs.keys():
    z[f] = []
    num_zf = int(freqs[f]['bandwidth']) / refbw
    if num_zf == 1:
      z[f] = []
    else:
      addzoomfreqs(z[f], refnchans, refbw)
  return z

# Case 2: ALMA <-> 2048 MHz VLBI
# ALMA uses the normal configuration, i.e. ALMA's channels are overlapped:
# the band centers are 62.5 * 15/16 = 58.59375 MHz apart.
def almavlbi(freqs):
  z = {}
  reffreqs = []
  refnchans = 0
  refbw = 2048.0

  for f in freqs.keys():
    z[f] = []
    addzoomfreqs(z[f], refnchans, refbw)
  return z

# Add more cases here
#def newcase(freqs):
#  z = {}
#  reffreqs = []
#  refnchans = 0
#  refbw = 2048.0
#  # add contents here
#
#  for f in freqs.keys():
#    z[f] = []
#    # add contents here
#
#    addzoomfreqs(z, f, refnchans, refbw)
#  return z

# Add newcase into zoom_options as hown below
def zoom_options():

  zoom_options = {1 : allvlbi,
                  2 : almavlbi
                 #3 : newcase
                  }
  return zoom_options
