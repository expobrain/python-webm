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

from ctypes import create_string_buffer
from tests.common import AbstractWebPDecodeTests, IMAGE_DATA, IMAGE_WIDTH, \
    IMAGE_HEIGHT
from webpdecode import WebPImage
import unittest


class WebPDecodeTests( AbstractWebPDecodeTests, unittest.TestCase ):

    def test_get_info(self):
        """
        Test the getInfo() method
        """
        result = self.decoder.getInfo( IMAGE_DATA )

        self.assertIsInstance( result, tuple )
        self.assertEqual( len( result ), 2 )
        self.assertIsInstance( result[0], int )
        self.assertIsInstance( result[1], int )

    def test_get_info_error(self):
        """
        Test the getInfo() method
        """
        with self.assertRaises( Exception ):
            self.decoder.getInfo( create_string_buffer(0) )

    def test_decode_RGB(self):
        """
        Test the decodeRGB() method
        """
        result  = self.decoder.decodeRGB( IMAGE_DATA )
        size    = IMAGE_WIDTH * IMAGE_HEIGHT * 3

        self.assertIsInstance( result, WebPImage )
        self.assertTrue( len(result.bitmap), size )
        self.assertEqual( result.format, WebPImage.RGB )
        self.assertEqual( result.width, IMAGE_WIDTH )
        self.assertEqual( result.height, IMAGE_HEIGHT )

    def test_decode_RGBA(self):
        """
        Test the decodeRGBA() method
        """
        result  = self.decoder.decodeRGBA( IMAGE_DATA )
        size    = IMAGE_WIDTH * IMAGE_HEIGHT * 4

        self.assertIsInstance( result, WebPImage )
        self.assertTrue( len(result.bitmap), size )
        self.assertEqual( result.format, WebPImage.RGBA )
        self.assertEqual( result.width, IMAGE_WIDTH )
        self.assertEqual( result.height, IMAGE_HEIGHT )

    def test_decode_BGR(self):
        """
        Test the decodeBGR() method
        """
        self.skipTest( "Segmentation fault" )

        result  = self.decoder.decodeBGR( IMAGE_DATA )
        size    = IMAGE_WIDTH * IMAGE_HEIGHT * 3

        self.assertIsInstance( result, WebPImage )
        self.assertTrue( len(result.bitmap), size )
        self.assertEqual( result.format, WebPImage.BGR )
        self.assertEqual( result.width, IMAGE_WIDTH )
        self.assertEqual( result.height, IMAGE_HEIGHT )

    def test_decode_BGRA(self):
        """
        Test the decodeBGRA() method
        """
        self.skipTest( "Segmentation fault" )

        result  = self.decoder.decodeBGR( IMAGE_DATA )
        size    = IMAGE_WIDTH * IMAGE_HEIGHT * 4

        self.assertIsInstance( result, WebPImage )
        self.assertTrue( len(result.bitmap), size )
        self.assertEqual( result.format, WebPImage.BGRA )
        self.assertEqual( result.width, IMAGE_WIDTH )
        self.assertEqual( result.height, IMAGE_HEIGHT )

    def test_decode_YUV(self):
        """
        Test the decodeYUV() method
        """
        self.skipTest( "Segmentation fault" )

        result  = self.decoder.decodeYUV( IMAGE_DATA )
        size    = IMAGE_WIDTH * IMAGE_HEIGHT * 3

        self.assertIsInstance( result, WebPImage )
        self.assertTrue( len(result.bitmap), size )
        self.assertEqual( result.format, WebPImage.YUV )
        self.assertEqual( result.width, IMAGE_WIDTH )
        self.assertEqual( result.height, IMAGE_HEIGHT )


class WebPImageTests( unittest.TestCase ):
    """
    WebPImage tests cases
    """

    def test_image_types_enum(self):
        """
        Test image types enumerator
        """
        self.assertEqual( WebPImage.RGB, 0 )
        self.assertEqual( WebPImage.RGBA, 1 )
        self.assertEqual( WebPImage.BGR, 2 )
        self.assertEqual( WebPImage.BGRA, 3 )
        self.assertEqual( WebPImage.YUV, 4 )

    def test_is_valid(self):
        """
        Test isValid() property
        """
        # Invalid
        self.assertFalse( WebPImage().isValid )
        self.assertFalse( WebPImage( IMAGE_DATA ).isValid )
        self.assertFalse( WebPImage( None, None ).isValid )
        self.assertFalse( WebPImage( None, None, IMAGE_WIDTH ).isValid )
        self.assertFalse(
            WebPImage( None, None, IMAGE_WIDTH, IMAGE_HEIGHT ).isValid )

        # Valid
        image = WebPImage(IMAGE_DATA, WebPImage.RGB, IMAGE_WIDTH, IMAGE_HEIGHT)

        self.assertTrue( image.isValid )
        self.assertEqual( image.bitmap, IMAGE_DATA )
        self.assertEqual( image.format, WebPImage.RGB )
        self.assertEqual( image.width, IMAGE_WIDTH )
        self.assertEqual( image.height, IMAGE_HEIGHT )
