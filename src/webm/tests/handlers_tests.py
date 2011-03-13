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

from webm.handlers import WebPImage
from webm.tests.common import IMAGE_DATA, IMAGE_WIDTH, IMAGE_HEIGHT


try:
    import unittest2 as unittest
except ImportError:
    import unittest
except:
    raise


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
        self.assertFalse( WebPImage( None, WebPImage.YUV, 0, 0, None ).isValid )

        # Valid
        image = WebPImage( IMAGE_DATA,
                           WebPImage.RGB,
                           IMAGE_WIDTH,
                           IMAGE_HEIGHT )

        self.assertTrue( image.isValid )
        self.assertEqual( image.bitmap, IMAGE_DATA )
        self.assertEqual( image.format, WebPImage.RGB )
        self.assertEqual( image.width, IMAGE_WIDTH )
        self.assertEqual( image.height, IMAGE_HEIGHT )

    def test_is_valid_yuv(self):
        """
        Test isValid() property for YUV format
        """
        # Create fake Y and UV bitmaps
        bitmap      = bytearray( IMAGE_WIDTH * IMAGE_HEIGHT )
        uv_bitmap   = bytearray( int( IMAGE_WIDTH * IMAGE_HEIGHT / 2 ))

        # Create image instance
        image = WebPImage( bitmap,
                           WebPImage.YUV,
                           IMAGE_WIDTH, IMAGE_HEIGHT,
                           u_bitmap=uv_bitmap, v_bitmap=uv_bitmap,
                           stride=IMAGE_WIDTH, uv_stride=int(IMAGE_WIDTH/2) )

        self.assertTrue( image.isValid )
        self.assertEqual( image.bitmap, bitmap )
        self.assertEqual( image.format, WebPImage.YUV )
        self.assertEqual( image.width, IMAGE_WIDTH )
        self.assertEqual( image.height, IMAGE_HEIGHT )
        self.assertEqual( image.u_bitmap, uv_bitmap )
        self.assertEqual( image.v_bitmap, uv_bitmap )
        self.assertEqual( image.stride, IMAGE_WIDTH )
        self.assertEqual( image.uv_stride, int(IMAGE_WIDTH / 2) )
