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

from PIL import Image
from webm.handlers import BitmapHandler, WebPHandler
from webm.tests.common import WebPEncodeMixin, IMAGE_WIDTH, IMAGE_HEIGHT, \
    PNG_BITMAP_DATA, ENCODE_FILENAME
from webm.decode import WebPDecoder

try:
    import unittest2 as unittest
except ImportError:
    import unittest
except:
    raise


class WebPEncodeTests( WebPEncodeMixin, unittest.TestCase ):
    """
    WebPEncode test cases
    """

    def setUp(self):
        # Call superclass
        super( WebPEncodeTests, self ).setUp()

        # Create test image
        self.image = BitmapHandler( PNG_BITMAP_DATA, BitmapHandler.RGB,
                                    IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_WIDTH * 3 )

    def test_encode_RGB(self):
        """
        Test the encodeRGB() method
        """
        image = self.webp_encoder.encodeRGB( self.image )

        self.assertIsInstance( image, WebPHandler )
        self.assertEqual( image.width, IMAGE_WIDTH )
        self.assertEqual( image.height, IMAGE_HEIGHT )

    def test_output_RGB(self):
        """
        Export encodeRGB() method result to file
        """
        result = self.webp_encoder.encodeRGB( self.image )
        stream = file( ENCODE_FILENAME.format( "RGB" ), "wb" )

        result.to_stream( stream )
