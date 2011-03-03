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

from decode import WEBPDECODE, WebPDecoder
import os
import sys


IMAGE_FILE      = os.path.join( os.path.dirname( __file__ ),
                                "vancouver2.webp" )
OUTPUT_FILENAME = os.path.join( os.path.dirname( __file__ ),
                                "output_{0}.png" )
IMAGE_DATA      = bytearray( file( IMAGE_FILE, "rb" ).read() )
IMAGE_WIDTH     = 644
IMAGE_HEIGHT    = 484


class WebPDecodeMixin( object ):
    """
    Mixin class to help WebPDecode unit tests
    """

    def setUp(self):
        if sys.platform != "win32":
            from ctypes import CDLL

            self.assertIsInstance( WEBPDECODE, CDLL )

        else:
            raise NotImplementedError(
                "Test non implemented under {0}".format( sys.platform )
            )

        # Create decoder instance
        self.webp_decoder = WebPDecoder()
