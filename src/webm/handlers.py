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


class BitmapHandler( object ):
    """
    Holds decode WebP image data and extra informations
    """
    RGB     = 0
    RGBA    = 1
    BGR     = 2
    BGRA    = 3
    YUV     = 4

    FORMATS = ( RGB, RGBA, BGR, BGRA, YUV )

    def __init__(self, bitmap, format, width, height, stride,
                 u_bitmap=None, v_bitmap=None, uv_stride=-1 ):
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
        self.bitmap    = bitmap
        self.u_bitmap  = u_bitmap
        self.v_bitmap  = v_bitmap
        self.stride    = stride
        self.uv_stride = uv_stride
        self.format    = format
        self.width     = width
        self.height    = height

        # Check if bitma handler is valid
        is_valid  = ( isinstance( bitmap, bytearray)
                      and format in self.FORMATS
                      and width > -1
                      and height > -1 )

        # Additional setups for YUV image
        if is_valid and format == self.YUV:
            # Check if YUV image is valid
            is_valid = ( isinstance( u_bitmap, bytearray )
                         and isinstance( v_bitmap, bytearray )
                         and stride > -1
                         and uv_stride > -1 )

        # Set valid flag
        self.is_valid = is_valid


class WebPHandlerError( IOError ):
    pass


class RiffWrite( object ):

    @staticmethod
    def read_length(source):
        """
        Read the data length from the given source

        :param source: The opened file
        :type source: file-like object
        :rtype: int
        """
        return struct.unpack( "<L", source.read(4) )[0]

    @staticmethod
    def read_tag(source):
        """
        Read the chunk tag from the given source

        :param source: The opened file
        :type source: file-like object
        :rtype: string
        """
        return struct.unpack( b"<4s", source.read(4) )[0]

    @staticmethod
    def write_tag(dest, tag):
        """
        Write the chunk tag to the given destination

        :param dest: The opened file
        :param tag: The chunk tag to be written

        :type dest: file-like object
        :type tag: string
        """
        dest.write( struct.pack( "<4s", tag ) )

    @staticmethod
    def write_length(dest, data):
        """
        Write the data length to the given destination

        :param dest: The opened file
        :param data: The data which the length will be written

        :type dest: file-like object
        :type data: buffer
        """
        dest.write( struct.pack( "<L", len(data ) ) )

    @staticmethod
    def write_data(dest, data):
        """
        Write the data to the given destination adding a pad byte if the data's
        length is odd

        :param dest: The opened file
        :param data: The data which will be written

        :type dest: file-like object
        :type data: buffer
        """
        dest.write( str(data) )

        if len(data) % 2:
            dest.write( 0x00 )


class WebPHandler( object ):
    """
    Contains data relative to an WebP encoded image and allow loading and saving
    .webp files.

    The code is base on the documentation at
    http://code.google.com/speed/webp/docs/riff_container.html

    Public properties:

    * data        The WebP encoded image data
    * width       The image's width, -1 if the image s not valid
    * height      The image's height, -1 if the image s not valid
    * is_valid    True if the image's data is valid else False
    """

    @staticmethod
    def from_file( filename ):
        """
        Load a .webp file and return the WebP handler

        :param filename: The file's name to be loaded
        :type filename: string
        :rtype: WebPHandler
        """
        return WebPHandler.from_stream( file( filename, "rb" ) )

    @staticmethod
    def from_stream( stream ):
        """
        Create a WebP handler from a file-like object

        :param stream: The file-like stream
        :type stream: file-like object
        :rtype: WebPHandler
        """
        from webm.decode import WebPDecoder

        # Check RIFF tag
        if RiffWrite.read_tag( stream ) != "RIFF":
            raise WebPHandlerError( "Not a RIFF file" )

        # Get VP8 chunk
        length  = RiffWrite.read_length( stream )
        source  = StringIO( stream.read( length ) )

        # Check WEBP and VP8 tag
        if RiffWrite.read_tag( source ) != "WEBP":
            raise WebPHandlerError( "WEBP chunk is missing" )

        if RiffWrite.read_tag( source ) != "VP8 ":
            raise WebPHandlerError( "VP8 chunk is missing")

        # Get data chunk
        length  = RiffWrite.read_length( source )
        data    = bytearray( source.read( length ) )

        # Create WebP handler
        return WebPHandler( data, *WebPDecoder.getInfo( data ) )

    def __init__(self, data=None, width=1, height=1):
        """
        Constructor accepts the data, width and height of the WebP encoded image

        :param source: The image encoded data
        :param width: The image's width
        :param height: The image's height

        :type data: bytearray
        :type width: int
        :type height: int
        """
        # Public attributes
        self.data   = data
        self.width  = width
        self.height = height

    def to_stream(self, stream):
        """
        Save the current image into the given sream as a .webp image format

        :param stream: The destination stream
        :type stream: file-like object
        """
        # Create VP8 chunk
        vp8_chunk = StringIO()

        RiffWrite.write_tag( vp8_chunk, "VP8 " )
        RiffWrite.write_length( vp8_chunk, self.data )
        RiffWrite.write_data( vp8_chunk, self.data )

        # Create WEBP chunk
        webp_chunk = StringIO()

        RiffWrite.write_tag( webp_chunk, "WEBP" )
        RiffWrite.write_data( webp_chunk, vp8_chunk.getvalue() )

        # Write file
        webp_chunk = webp_chunk.getvalue()

        RiffWrite.write_tag( stream, "RIFF" )
        RiffWrite.write_length( stream, webp_chunk )
        RiffWrite.write_data( stream, webp_chunk )

    @property
    def is_valid(self):
        """
        Returns True if the current image is valid

        :rtype: bool
        """
        return self.data != None and ( self.width > -1 and self.height > -1 )
