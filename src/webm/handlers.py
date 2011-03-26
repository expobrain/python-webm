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

from cStringIO import StringIO
import struct


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

    def __init__(self, bitmap=None, format=None, width=-1, height=-1,
                 u_bitmap=None, v_bitmap=None, stride=-1, uv_stride=-1 ):
        """
        Constructor accepts the decode image data as a bitmap and its
        width/height.

        Passing a null image data, and invalid format or a non
        positive integer for width/height creates an instance to an invalid WebP
        image.

        If the image is in YUV format the bitmap parameter will be the Y(luma)
        component and the U/V chrominance component bitmap must be passed else
        the image will be invalid. The Y bitmap stride and the UV bitmap stride
        must be passed as well.

        :param bitmap: The image bitmap
        :param format: The image format
        :param width: The image width
        :param height: The mage height
        :param u_bitmap: The U chrominance component bitmap
        :param v_bitmap: The V chrominance component bitmap
        :param stride: The Y bitmap stride
        :param uv_stride: The UV stride

        :type bitmap: bytearray
        :type format: M{WebPImage.FORMATS}
        :type width: int
        :type height: int
        :type u_bitmap: bytearray
        :type v_bitmap: bytearray
        :type stride: int
        :type uv_stride: int
        """
        self._bitmap    = bitmap
        self._u_bitmap  = u_bitmap
        self._v_bitmap  = v_bitmap
        self._stride    = stride
        self._uv_stride = uv_stride
        self._format    = format
        self._width     = width
        self._height    = height
        self._is_valid  = ( isinstance( bitmap, bytearray)
                            and format in self.FORMATS
                            and width > -1
                            and height > -1 )

        # Additional setups for YUV image
        if self._is_valid and format == self.YUV:
            # Check if YUV image is valid
            self._is_valid = ( isinstance( u_bitmap, bytearray )
                               and isinstance( v_bitmap, bytearray )
                               and stride > -1
                               and uv_stride > -1 )

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
        Return the image bitmap data

        :rtype: bool
        """
        return self._bitmap

    @property
    def width(self):
        """
        Return the image width

        :rtype: int
        """
        return self._width

    @property
    def height(self):
        """
        Return the image height

        :rtype: int
        """
        return self._height

    @property
    def u_bitmap(self):
        """
        Return the U chrominance bitmap

        :rtype: bytearray
        """
        return self._u_bitmap

    @property
    def v_bitmap(self):
        """
        Return the V chrominance bitmap

        :rtype: bytearray
        """
        return self._v_bitmap

    @property
    def stride(self):
        """
        Return the bitmap stride

        :rtype: int
        """
        return self._stride

    @property
    def uv_stride(self):
        """
        Return the UV chrominance bitmap stride

        :rtype: int
        """
        return self._uv_stride


class WebPHandlerError( IOError ):
    pass


class WebPHandler( object ):
    """
    Contains data relative to an WebP encoded image and allow loading and saving
    .webp files
    """

    @staticmethod
    def load( filename ):
        return WebPHandler( file( filename, "rb" ) )

    def __init__(self, source):
        from webm.decode import WebPDecoder

        # Convert data to a file-like object
        if not hasattr( source, "read" ):
            source = StringIO( source )

        # Public attributes
        self.data = self._get_data( source )
        self.width, self.height = WebPDecoder.getInfo( self.data )
        self.is_valid = True


    def _get_data(self, source):
        # Check RIFF tag
        if self._read_tag( source ) != "RIFF":
            raise WebPHandlerError( "Not a RIFF file" )

        # Get VP8 chunk
        length  = self._read_size( source )
        source  = StringIO( source.read( length ) )

        # Check WEBP and VP8 tag
        if self._read_tag( source ) != "WEBP":
            raise WebPHandlerError( "WEBP chunk is missing" )

        if self._read_tag( source ) != "VP8 ":
            raise WebPHandlerError( "VP8 chunk is missing")

        # Get data chunk
        length = self._read_size( source )
        source = source.read( length )

        # End
        return source

    def _read_size(self, source):
        return struct.unpack( "<L", source.read(4) )[0]

    def _read_tag(self, source):
        return struct.unpack( b"<4s", source.read(4) )[0]

    def _write_tag(self, dest, tag):
        dest.write( struct.pack( "<4s", tag ) )

    def _write_size(self, dest, data):
        dest.write( struct.pack( "<L", len(data ) ) )

    def _write_data(self, dest, data):
        dest.write( data )

        if len(data) % 2:
            dest.write( 0x00 )

    def save(self, filename):
        # Create VP8 chunk
        vp8_chunk = StringIO()

        self._write_tag( vp8_chunk, "VP8 " )
        self._write_size( vp8_chunk, self.data )
        self._write_data( vp8_chunk, self.data )

        # Create WEBP chunk
        webp_chunk = StringIO()

        self._write_tag( webp_chunk, "WEBP" )
        self._write_data( webp_chunk, vp8_chunk.getvalue() )

        # Write file
        webp_chunk = webp_chunk.getvalue()
        dest = file( filename, "wb" )

        self._write_tag( dest, "RIFF" )
        self._write_size( dest, webp_chunk )
        self._write_data( dest, webp_chunk )

        dest.close()
