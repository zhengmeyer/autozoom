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

ALMABW = 58.59375
EPSILON = 0.00001
MAXBW = 2048.0

class Zoom:
  def __init__(self):
    self.z = {}
    self.reffreqs = []
    self.refnchans = 0
    self.refbw = 0.0

  def addzoomfreqs(self, freqs):
    if not self.reffreqs or self.refnchans == 0:
      raise Exception("No reference frequency setup found!!!")
    for f in freqs.keys():
      self.z[f] = []
      # if bandwidth of the frequency setup is not the same as reference bandwidth
      if freqs[f]['bandwidth'] - self.refbw >= EPSILON:
        for ch in range(self.refnchans):
          self.z[f].append("addZoomFreq = freq@%f/bw@%f" % (self.reffreqs[ch], self.refbw))
    return self.z

# check if a number is 2^N
def is_pow2(num):
  return num > 0 and ((num & (num - 1) == 0))
  

# Case 1: zoom band <-> recorded band
# ALL stations have the same frequency coverage (max. 2048 MHz).
# Start and end frequencies of all stations are the same. Bandwidth is 2^N.
def allvlbi(freqs):
  zoom = Zoom()

  # add case-specific code here
  zoom.refbw = MAXBW
  pow2 = True
  minfreqs = set()
  maxfreqs = set()
  # get the smallest bandwidth of all frequency setup
  # use it as reference for zoom frequency
  for f in freqs.keys():
    pow2 &= is_pow2(int(freqs[f]['bandwidth']))
    minfreqs.add(freqs[f]['min_freq'])
    maxfreqs.add(freqs[f]['max_freq'])
    if int(zoom.refbw) >= int(freqs[f]['bandwidth']):
      zoom.refbw = int(freqs[f]['bandwidth'])
      zoom.reffreqs = freqs[f]['band_freqs']
      zoom.refnchans = freqs[f]['num_channels']
  
  if not pow2:
    raise Exception("Not all bandwidth is 2^N!!!")
  if len(minfreqs) != 1 or len(maxfreqs) != 1:
    raise Exception("Start frequency or end frequency of antennas are not the same!!!")

  return zoom.addzoomfreqs(freqs)

# Case 2: ALMA <-> 2048 MHz VLBI
# ALMA uses the normal configuration, i.e. ALMA's channels are overlapped,
# the band centers are 62.5 * 15/16 = 58.59375 MHz apart.
# Use ALMA as reference station, center-align ALMA bands.
# User can define zoom bandwidth, default zoom bandwidth is ALMABW=58.59375 MHz.
def almavlbi(freqs, zoombw):
  zoom = Zoom()

  # add case-specific code here
  if zoombw == None:
    zoombw = ALMABW
  zoom.refbw = zoombw
  
  return zoom.addzoomfreqs(freqs)

# To add new cases, comment out the following template,
# and add case-specific code

#def newcase(freqs):
#  zoom = Zoom()
#
#  # add case-specific code here
#
#  return zoom.addzoomfreqs(freqs)

# Add newcase into zoom_options as hown below
def zoom_options():

  zoom_options = {1 : allvlbi,
                  2 : almavlbi
                 #3 : newcase
                  }
  return zoom_options
