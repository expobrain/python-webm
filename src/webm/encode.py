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

from ctypes import c_int, c_float, c_void_p, byref
from webm.handlers import WebPImage
import sys


# Per-OS setup
if sys.platform == "win32":
    from ctypes import windll as loader

    LIBRARY = "libwebp.dll"

elif sys.platform == "linux2":
    from ctypes import cdll as loader

    LIBRARY = "libwebp.so"

elif sys.platform == "darwin":
    from ctypes import cdll as loader

    LIBRARY = "libwebp.dylib"

else:
    raise NotImplementedError(
        "Test non implemented under {0}".format( sys.platform )
    )

# Load library
WEBPENCODE = loader.LoadLibrary( LIBRARY )

# Set return types
WEBPENCODE.WebPEncodeRGB.restype = c_int


class WebPEncoder( object ):
    """
    Pure Python interface for the Google WebP encode library
    """

    def encodeRGB(self, image, quality=100):
        """
        Encode the given RGB image with the given quality

        :param image: The RGB image
        :param quality: The encode quality factor

        :type image: WebPImage
        :type quality: float
        """
        data        = str( image.bitmap )
        width       = c_int( image.width )
        height      = c_int( image.height )
        stride      = c_int( image.width )
        q_factor    = c_float( 1 )
        output      = c_void_p()

        size = WEBPENCODE.WebPEncodeRGB( data,
                                         width, height, stride,
                                         q_factor, byref(output) )

        if size == 0:
            raise RuntimeError( "Error during image encoding" )
        else:
            return WebPImage( output, WebPImage.RGB, image.width, image.height )
