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
from ctypes import create_string_buffer
from webm.handlers import WebPImage
from webm.tests.common import WebPDecodeMixin, IMAGE_DATA, IMAGE_WIDTH, \
    IMAGE_HEIGHT, OUTPUT_FILENAME

try:
    import unittest2 as unittest
except ImportError:
    import unittest
except:
    raise


class WebPDecodeTests( WebPDecodeMixin, unittest.TestCase ):
    """
    WebPDecode test cases
    """

    def test_get_info(self):
        """
        Test the getInfo() method
        """
        result = self.webp_decoder.getInfo( IMAGE_DATA )

        self.assertIsInstance( result, tuple )
        self.assertEqual( len( result ), 2 )
        self.assertIsInstance( result[0], int )
        self.assertIsInstance( result[1], int )

    def test_get_info_error(self):
        """
        Test the getInfo() method
        """
        with self.assertRaises( Exception ):
            self.webp_decoder.getInfo( create_string_buffer(0) )

    def test_decode_RGB(self):
        """
        Test the decodeRGB() method
        """
        result  = self.webp_decoder.decodeRGB( IMAGE_DATA )
        size    = IMAGE_WIDTH * IMAGE_HEIGHT * 3

        self.assertIsInstance( result, WebPImage )
        self.assertEqual( len(result.bitmap), size )
        self.assertEqual( result.format, WebPImage.RGB )
        self.assertEqual( result.width, IMAGE_WIDTH )
        self.assertEqual( result.height, IMAGE_HEIGHT )

    def test_decode_RGBA(self):
        """
        Test the decodeRGBA() method
        """
        result  = self.webp_decoder.decodeRGBA( IMAGE_DATA )
        size    = IMAGE_WIDTH * IMAGE_HEIGHT * 4

        self.assertIsInstance( result, WebPImage )
        self.assertEqual( len(result.bitmap), size )
        self.assertEqual( result.format, WebPImage.RGBA )
        self.assertEqual( result.width, IMAGE_WIDTH )
        self.assertEqual( result.height, IMAGE_HEIGHT )

    def test_decode_BGR(self):
        """
        Test the decodeBGR() method
        """
        result  = self.webp_decoder.decodeBGR( IMAGE_DATA )
        size    = IMAGE_WIDTH * IMAGE_HEIGHT * 3

        self.assertIsInstance( result, WebPImage )
        self.assertEqual( len(result.bitmap), size )
        self.assertEqual( result.format, WebPImage.BGR )
        self.assertEqual( result.width, IMAGE_WIDTH )
        self.assertEqual( result.height, IMAGE_HEIGHT )

    def test_decode_BGRA(self):
        """
        Test the decodeBGRA() method
        """
        result  = self.webp_decoder.decodeBGRA( IMAGE_DATA )
        size    = IMAGE_WIDTH * IMAGE_HEIGHT * 4

        self.assertIsInstance( result, WebPImage )
        self.assertEqual( len(result.bitmap), size )
        self.assertEqual( result.format, WebPImage.BGRA )
        self.assertEqual( result.width, IMAGE_WIDTH )
        self.assertEqual( result.height, IMAGE_HEIGHT )

    def test_decode_YUV(self):
        """
        Test the decodeYUV() method
        """
        result  = self.webp_decoder.decodeYUV( IMAGE_DATA )
        size    = IMAGE_WIDTH * IMAGE_HEIGHT

        self.assertIsInstance( result, WebPImage )
        self.assertEqual( len(result.bitmap), size )
        self.assertEqual( result.format, WebPImage.YUV )
        self.assertEqual( result.width, IMAGE_WIDTH )
        self.assertEqual( result.height, IMAGE_HEIGHT )
        self.assertEqual( len(result.u_bitmap),
                          int( (IMAGE_WIDTH + 1) / 2) * IMAGE_HEIGHT )
        self.assertEqual( len(result.v_bitmap),
                          int( (IMAGE_WIDTH + 1) / 2) * IMAGE_HEIGHT )
        self.assertEqual( result.uv_stride * IMAGE_HEIGHT,
                          int( (IMAGE_WIDTH + 1) / 2) * IMAGE_HEIGHT )

    def test_output_RGB(self):
        """
        Export decodeRGB() method result to file
        """
        result = self.webp_decoder.decodeRGB( IMAGE_DATA )
        image  = Image.frombuffer( "RGB",
                                    (result.width, result.height),
                                    str(result.bitmap),
                                    "raw", "RGB", 0, 1 )
        image.save( OUTPUT_FILENAME.format( "RGB" ) )

    def test_output_RGBA(self):
        """
        Export decodeRGBA() method result to file
        """
        result = self.webp_decoder.decodeRGBA( IMAGE_DATA )
        image  = Image.frombuffer( "RGBA",
                                    (result.width, result.height),
                                    result.bitmap,
                                    "raw", "RGBA", 0, 1 )
        image.save( OUTPUT_FILENAME.format( "RGBA" ) )

    def test_output_BGR(self):
        """
        Export decodeBGR() method result to file
        """
        result = self.webp_decoder.decodeBGR( IMAGE_DATA )
        image  = Image.frombuffer( "RGB",
                                    (result.width, result.height),
                                    str(result.bitmap),
                                    "raw", "BGR", 0, 1 )
        image.save( OUTPUT_FILENAME.format( "BGR" ) )

    def test_output_BGRA(self):
        """
        Export decodeBGRA() method result to file
        """
        result  = self.webp_decoder.decodeBGRA( IMAGE_DATA )
        image  = Image.frombuffer( "RGBA",
                                    (result.width, result.height),
                                    str(result.bitmap),
                                    "raw", "BGRA", 0, 1 )
        image.save( OUTPUT_FILENAME.format( "BGRA" ) )
