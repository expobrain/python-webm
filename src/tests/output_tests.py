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

from tests.common import AbstractWebPDecodeTests, IMAGE_DATA, IMAGE_WIDTH,\
    IMAGE_HEIGHT
import os
import platform

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
                                    result.bitmap,
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

    @unittest.skipIf( platform.architecture()[0] == "64bit",
                      "Segmentation fault under 64bit" )
    def test_decode_BGR(self):
        """
        Export decodeBGR() method result to file
        """
        result = self.decoder.decodeBGR( IMAGE_DATA )
        image  = Image.frombuffer( "RGB",
                                    (result.width, result.height),
                                    result.bitmap,
                                    "raw", "BGR", 0, 1 )
        image.save( self.BASE_FILENAME.format( "BGR" ) )

    @unittest.skipIf( platform.architecture()[0] == "64bit",
                      "Segmentation fault under 64bit" )
    def test_decode_BGRA(self):
        """
        Export decodeBGRA() method result to file
        """
        result  = self.decoder.decodeBGRA( IMAGE_DATA )
        image  = Image.frombuffer( "RGBA",
                                    (result.width, result.height),
                                    result.bitmap,
                                    "raw", "BGRA", 0, 1 )
        image.save( self.BASE_FILENAME.format( "BGRA" ) )
