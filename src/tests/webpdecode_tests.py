#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctypes import create_string_buffer
from webpdecode import WEBPDECODE, WebPDecoder, WebPImage
import os
import sys
import unittest


IMAGE_FILE      = os.path.join( os.path.dirname( __file__ ),
                                "vancouver2.webp" )
IMAGE_DATA      = file( IMAGE_FILE, "rb" ).read()
IMAGE_WIDTH     = 644
IMAGE_HEIGHT    = 484


class WebPDecodeTests( unittest.TestCase ):

    def setUp(self):
        if sys.platform != "win32":
            from ctypes import CDLL

            self.assertIsInstance( WEBPDECODE, CDLL )

        else:
            raise NotImplementedError(
                "Test non implemented under {}".format( sys.platform )
            )

        self.decoder = WebPDecoder()

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
