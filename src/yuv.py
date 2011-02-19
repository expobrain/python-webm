#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2011, Daniele Esposti <expo@expobrain.net>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * The name of the contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from webpdecode import WebPImage

"""
Porting of the YUVtoRGB converter code from the Chromium project. See
third_party/libwebp/yuv.c and /third_party/libwebp/yuv.h files for the original
source code.
"""

YUV_FIX         = 16            # fixed-point precision
YUV_RANGE_MIN   = -227          # min value of r/g/b output
YUV_RANGE_MAX   = 256 + 226     # max value of r/g/b output
YUV_HALF        = 1 << (YUV_FIX - 1)
VP8kVToR        = [0] * 256
VP8kUToB        = [0] * 256
VP8kVToG        = [0] * 256
VP8kUToG        = [0] * 256
VP8kClip        = [0] * (YUV_RANGE_MAX - YUV_RANGE_MIN);


def _init_yuv_module():
    """
    Initialise the YUVtoRGB lookup tables
    """
    for i in xrange(256):
        VP8kVToR[i] = (89858 * (i - 128) + YUV_HALF) >> YUV_FIX
        VP8kUToG[i] = -22014 * (i - 128) + YUV_HALF
        VP8kVToG[i] = -45773 * (i - 128)
        VP8kUToB[i] = (113618 * (i - 128) + YUV_HALF) >> YUV_FIX

    for i in xrange( YUV_RANGE_MIN, YUV_RANGE_MAX ):
        k = ((i - 16) * 76283 + YUV_HALF) >> YUV_FIX
        k = 0 if k < 0 else 255 if k > 255 else k

        VP8kClip[i - YUV_RANGE_MIN] = k

# Initialise YUVtoRGB lookup table only once
_init_yuv_module()


class YUVDecoder( object ):
    """
    Collection of static functions to covert YUV data to different formats
    """

    @staticmethod
    def YUVtoRGB(image):
        """
        Convert the given WebP image instance from a YUV format to an RGB format

        :param image: The WebP image in YUV format
        :type image: WebPImage
        :rtype: WebPImage
        """
        # Convert YUV to RGB
        rgb_bitmap = bytearray()

        for i in xrange( len( image.bitmap ) ):
            # Get YUV data
            y = image.bitmap[i]
            u = image.u_bitmap[i]
            v = image.v_bitmap[i]

            # Calculate RGB values
            r_off = VP8kVToR[v]
            g_off = (VP8kVToG[v] + VP8kUToG[u]) >> YUV_FIX
            b_off = VP8kUToB[u]

            r = VP8kClip[y + r_off - YUV_RANGE_MIN]
            g = VP8kClip[y + g_off - YUV_RANGE_MIN]
            b = VP8kClip[y + b_off - YUV_RANGE_MIN]

            # Push values into buffer
            rgb_bitmap.append( r )
            rgb_bitmap.append( g )
            rgb_bitmap.append( b )

        # Return the WebPImage in RGB format
        return WebPImage( rgb_bitmap,
                          WebPImage.RGB,
                          image.width, image.height )


"""
inline static void VP8YuvToRgb(uint8_t y, uint8_t u, uint8_t v,
                               uint8_t* const rgb) {
  const int r_off = VP8kVToR[v];
  const int g_off = (VP8kVToG[v] + VP8kUToG[u]) >> YUV_FIX;
  const int b_off = VP8kUToB[u];
  rgb[0] = VP8kClip[y + r_off - YUV_RANGE_MIN];
  rgb[1] = VP8kClip[y + g_off - YUV_RANGE_MIN];
  rgb[2] = VP8kClip[y + b_off - YUV_RANGE_MIN];
}

inline static void VP8YuvToRgba(int y, int u, int v, uint8_t* const rgba) {
  VP8YuvToRgb(y, u, v, rgba);
  rgba[3] = 0xff;
}

inline static void VP8YuvToBgr(uint8_t y, uint8_t u, uint8_t v,
                               uint8_t* const bgr) {
  const int r_off = VP8kVToR[v];
  const int g_off = (VP8kVToG[v] + VP8kUToG[u]) >> YUV_FIX;
  const int b_off = VP8kUToB[u];
  bgr[0] = VP8kClip[y + b_off - YUV_RANGE_MIN];
  bgr[1] = VP8kClip[y + g_off - YUV_RANGE_MIN];
  bgr[2] = VP8kClip[y + r_off - YUV_RANGE_MIN];
}

inline static void VP8YuvToBgra(int y, int u, int v, uint8_t* const bgra) {
  VP8YuvToBgr(y, u, v, bgra);
  bgra[3] = 0xff;
}
"""
