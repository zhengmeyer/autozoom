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

# Case 1: zoom band <-> recorded band
# ALL stations have the same frequency coverage 2048 MHz.
# Bandwidth is 2^N, with a minimum bandwidth of 32 MHz.
def allvlbi(freqs):
  z = {}
  refbw = 2048
  reffreqs = []
  refnchans = 0

  # get the smallest bandwidth of all frequency setup
  # use it as reference for zoom frequency
  for f in freqs.keys():
    if refbw >= int(freqs[f]['bandwidth']):
      refbw = int(freqs[f]['bandwidth'])
      reffreqs = freqs[f]['band_freqs']
      refnchans = freqs[f]['num_channels']
  
  if not reffreqs or refnchans == 0:
    raise Exception("No reference frequency setup found!")

  for f in freqs.keys():
    z[f]=[]
    num_zf = int(freqs[f]['bandwidth']) / refbw
    if num_zf == 1:
      z[f] = []
    else:
      for ch in range(refnchans):
        z[f].append("addZoomFreq = freq@%f/bw@%f" % (reffreqs[ch], refbw))
  return z

# Case 2: ALMA <-> 2048 MHz VLBI
def almavlbi(freqs):
  return

def zoom_options():

  zoom_options = {1 : allvlbi,
                  2 : almavlbi}
  return zoom_options
