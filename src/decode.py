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

from ctypes import byref, c_int, c_uint, create_string_buffer, memmove, c_void_p
from handlers import WebPImage
import sys

# Generic constants
__VERSION__ = "0.1.3beta"


# Per-OS setup
if sys.platform == "win32":
    from ctypes import windll as loader

    LIBRARY = "libwebpdecode.dll"

elif sys.platform == "linux2":
    from ctypes import cdll as loader

    LIBRARY = "libwebpdecode.so"

elif sys.platform == "darwin":
    from ctypes import cdll as loader

    LIBRARY = "libwebpdecode.dylib"

else:
    raise NotImplementedError(
        "Test non implemented under {0}".format( sys.platform )
    )

# Load library
WEBPDECODE = loader.LoadLibrary( LIBRARY )

# Set return types
WEBPDECODE.WebPDecodeRGB.restype    = c_void_p
WEBPDECODE.WebPDecodeRGBA.restype   = c_void_p
WEBPDECODE.WebPDecodeBGR.restype    = c_void_p
WEBPDECODE.WebPDecodeBGRA.restype   = c_void_p
WEBPDECODE.WebPDecodeYUV.restype    = c_void_p
WEBPDECODE.WebPGetInfo.restype      = c_uint


class HeaderError( Exception ):
    """
    Exception for image header operations and manipulations
    """
    pass


class WebPDecoder( object ):
    """
    Pure Python interface for the Google WebP decode library
    """

    PIXEL_SZ        = 3
    PIXEL_ALPHA_SZ  = 4

    def _decode(self, data, decode_func, pixel_sz):
        """
        Decode the given WebP image data using given decode and with the given
        pixel size in bytes

        :param data: The original WebP image data
        :param decode_func: The decode function to be used
        :param pixel_sz: The pixel data size in bytes to calculate the decoded
                         image size buffer

        :type data: bytearray
        :type decode_func: function
        :type pixel_sz: int

        :rtype: tuple(bytearray, int, int)
        """
        # Prepare parameters
        width   = c_int(-1)
        height  = c_int(-1)
        size    = c_uint( len(data) )

        # Decode image an return pointer to decoded data
        bitmap_p = decode_func( str(data), size, byref(width), byref(height) )

        # Copy decoded data into a buffer
        width   = width.value
        height  = height.value
        size    = width * height * pixel_sz
        bitmap  = create_string_buffer( size )

        memmove( bitmap, bitmap_p, size )

        # End
        return ( bytearray(bitmap), width, height )

    def getInfo(self, data):
        """
        Return the width and the height from the given WebP image data

        :param data: The original WebP image data
        :type data: bytearray
        :rtype: tuple(int, int)
        """
        width   = c_int(-1)
        height  = c_int(-1)
        size    = c_uint( len(data) )

        ret = WEBPDECODE.WebPGetInfo( str(data),
                                      size,
                                      byref(width), byref(height) )

        if ret == 0:
            raise HeaderError
        else:
            return ( width.value, height.value )

    def decodeRGB(self, data):
        """
        Decode the given WebP image data to a RGB bitmap

        :param data: The original WebP image data
        :type data: bytearray
        :rtype: WebPImage
        """
        bitmap, width, height = self._decode( data,
                                              WEBPDECODE.WebPDecodeRGB,
                                              self.PIXEL_SZ )

        return WebPImage( bitmap, WebPImage.RGB, width, height )

    def decodeBGR(self, data):
        """
        Decode the given WebP image data to a BGR bitmap

        :param data: The original WebP image data
        :type data: bytearray
        :rtype: WebPImage
        """
        bitmap, width, height = self._decode( data,
                                              WEBPDECODE.WebPDecodeBGR,
                                              self.PIXEL_SZ )

        return WebPImage( bitmap, WebPImage.BGR, width, height )

    def decodeBGRA(self, data):
        """
        Decode the given WebP image data to a BGRA bitmap

        :param data: The original WebP image data
        :type data: bytearray
        :rtype: WebPImage
        """
        bitmap, width, height = self._decode( data,
                                              WEBPDECODE.WebPDecodeBGRA,
                                              self.PIXEL_ALPHA_SZ )

        return WebPImage( bitmap, WebPImage.BGRA, width, height )

    def decodeRGBA(self, data):
        """
        Decode the given WebP image data to a RGBA bitmap

        :param data: The original WebP image data
        :type data: bytearray
        :rtype: WebPImage
        """
        bitmap, width, height = self._decode( data,
                                              WEBPDECODE.WebPDecodeRGBA,
                                              self.PIXEL_ALPHA_SZ )

        return WebPImage( bitmap, WebPImage.RGBA, width, height )

    def decodeYUV(self, data):
        """
        Decode the given WebP image data to a YUV bitmap

        :param data: The original WebP image data
        :type data: bytearray
        :rtype: WebPImage
        """
        # Prepare parameters
        width       = c_int(-1)
        height      = c_int(-1)
        size        = c_uint( len(data) )
        u           = create_string_buffer(0)
        v           = create_string_buffer(0)
        stride      = c_int(-1)
        uv_stride   = c_int(-1)

        # Decode image an return pointer to decoded data
        bitmap_p = WEBPDECODE.WebPDecodeYUV( str(data),
                                             size,
                                             byref(width), byref(height),
                                             u, v,
#                                             byref(u), byref(v),
                                             byref(stride), byref(uv_stride) )

        # Convert data to Python types
        width       = width.value
        height      = height.value
        stride      = stride.value
        uv_stride   = uv_stride.value

        # Copy decoded data into a buffer
        size    = stride * height
        bitmap  = create_string_buffer( size )

        memmove( bitmap, bitmap_p, size )

        # Copy UV chrominace bitmap
        uv_size     = uv_stride * height
        u_bitmap    = create_string_buffer( uv_size )
        v_bitmap    = create_string_buffer( uv_size )

        memmove( u_bitmap, u, uv_size )
        memmove( v_bitmap, v, uv_size )

        # End
        return WebPImage( bytearray(bitmap),
                          WebPImage.YUV, width, height,
                          u_bitmap=bytearray(u_bitmap),
                          v_bitmap=bytearray(v_bitmap),
                          stride=stride, uv_stride=uv_stride )
