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
import sys


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
WEBPDECODE.WebPGetInfo.restype      = c_uint


class HeaderError( Exception ):
    """
    Exception for image header operations and manipulations
    """
    pass


class WebPImage( object ):
    """
    Holds WebP image data and informations
    """
    RGB     = 0
    RGBA    = 1
    BGR     = 2
    BGRA    = 3
    YUV     = 4

    FORMATS = ( RGB, RGBA, BGR, BGRA, YUV )

    def __init__(self, bitmap=None, format=None, width=-1, height=-1):
        """
        Constructor accepts the decode image data as a bitmap and its
        width/height. Passing a null image data, and invalid format or a non
        positive integer for width/height creates an instance to an invalid WebP
        image.
        """
        self._bitmap    = bitmap
        self._format    = format
        self._width     = width
        self._height    = height
        self._is_valid  = ( bitmap != None
                            and format in self.FORMATS
                            and width > -1
                            and height > -1 )

    @property
    def format(self):
        """
        Return if the image bitmap format

        :rtype: M{WebPImage.FORMATS}
        """
        return self._format

    @property
    def isValid(self):
        """
        Return if the current image bitmap is valid

        :rtype: bool
        """
        return self._is_valid

    @property
    def bitmap(self):
        """
        Return if the image bitmap data

        :rtype: bool
        """
        return self._bitmap

    @property
    def width(self):
        """
        Return if the image width

        :rtype: int
        """
        return self._width

    @property
    def height(self):
        """
        Return if the image height

        :rtype: int
        """
        return self._height


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
        bitmap_p = decode_func( data, size, byref(width), byref(height) )

        # Copy decoded data into a buffer
        width   = width.value
        height  = height.value
        size    = width * height * pixel_sz
        bitmap  = create_string_buffer( size )

        memmove( bitmap, bitmap_p, size )

        # End
        return ( bitmap, width, height )

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

        ret = WEBPDECODE.WebPGetInfo( data, size, byref(width), byref(height) )

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
                                              self.PIXEL_SZ )

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
        bitmap_p = WEBPDECODE.WebPDecodeYUV( data,
                                             size,
                                             byref(width), byref(height),
                                             byref(u), byref(v),
                                             byref(stride), byref(uv_stride) )

        # Copy decoded data into a buffer
        width   = width.value
        height  = height.value
        size    = width * height * self.PIXEL_SZ
        bitmap  = create_string_buffer( size )

        memmove( bitmap, bitmap_p, size )

        # End
        return WebPImage( bitmap, WebPImage.YUV, width, height )
