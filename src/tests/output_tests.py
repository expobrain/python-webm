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

from tests.common import AbstractWebPDecodeTests, IMAGE_DATA
import os
import platform
import sys
from yuv import YUVDecoder

try:
    import unittest2 as unittest
except ImportError:
    import unittest
except:
    raise


class WebPDecodeOutputTests( AbstractWebPDecodeTests, unittest.TestCase ):
    """
    Same as WebPDecodeOutput test cases but saving the decoded output to disk
    """

    BASE_FILENAME = os.path.join( os.path.dirname( __file__ ),
                                  "output_{0}.png" )

    def setUp(self):
        # Try to load PIL package
        try:
            from PIL import Image
        except ImportError:
            self.skipTest( "PIL package not available" )
        except:
            raise

        # Make it global
        global Image

        # Call superclass
        super( WebPDecodeOutputTests, self ).setUp()

    def test_decode_RGB(self):
        """
        Export decodeRGB() method result to file
        """
        result = self.decoder.decodeRGB( IMAGE_DATA )
        image  = Image.frombuffer( "RGB",
                                    (result.width, result.height),
                                    str(result.bitmap),
                                    "raw", "RGB", 0, 1 )
        image.save( self.BASE_FILENAME.format( "RGB" ) )

    def test_decode_RGBA(self):
        """
        Export decodeRGBA() method result to file
        """
        result = self.decoder.decodeRGBA( IMAGE_DATA )
        image  = Image.frombuffer( "RGBA",
                                    (result.width, result.height),
                                    result.bitmap,
                                    "raw", "RGBA", 0, 1 )
        image.save( self.BASE_FILENAME.format( "RGBA" ) )

    def test_decode_BGR(self):
        """
        Export decodeBGR() method result to file
        """
        result = self.decoder.decodeBGR( IMAGE_DATA )
        image  = Image.frombuffer( "RGB",
                                    (result.width, result.height),
                                    str(result.bitmap),
                                    "raw", "BGR", 0, 1 )
        image.save( self.BASE_FILENAME.format( "BGR" ) )

    def test_decode_BGRA(self):
        """
        Export decodeBGRA() method result to file
        """
        result  = self.decoder.decodeBGRA( IMAGE_DATA )
        image  = Image.frombuffer( "RGBA",
                                    (result.width, result.height),
                                    str(result.bitmap),
                                    "raw", "BGRA", 0, 1 )
        image.save( self.BASE_FILENAME.format( "BGRA" ) )

    def _convert_yuv_to_rgb(self, image):
        buffer = bytearray()
        y_buffer = bytearray( image.bitmap )
        u_buffer = bytearray( image.u_bitmap )
#        v_buffer = bytearray( image.v_bitmap )

        for h in xrange( image.height ):
            for w in xrange( image.width ):
                y_index     = h * image.stride + w
                uv_index    = h * image.uv_stride + int(w/2)

                y = y_buffer[ y_index ]
                u = u_buffer[ uv_index ] >> 4
                v = u_buffer[ uv_index ]  & 0b1111

                for byte in YUVDecoder.YUVtoRGB(y, u, v):
                    buffer.append( byte )

        return str( buffer )

    @unittest.skip( "NOT FIXED YET")
    def test_decode_YUV(self):
        """
        Export decodeYUV() method result to file
        """
        # Get YUV data and convert to RGB
        result  = self.decoder.decodeYUV( IMAGE_DATA )
        rgb     = self._convert_yuv_to_rgb( result )

        # Save image
        image = Image.frombuffer( "RGB",
                                  (result.width, result.height),
                                  rgb,
                                  "raw", "RGB", 0, 1 )
        image.save( self.BASE_FILENAME.format( "YUV" ) )
