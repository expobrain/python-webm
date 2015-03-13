# Python-WebM #

The python-webm package is an interface to the Google WebM new video/image codec
which promise a better compression of image and video data.
The interface uses ctypes to call the libvpx/libwebm Google libraries installed
in the system.
At the moment only the libwebm library is wrapped and with some limitations.


## Platforms ##

Here a list of platforms with the current support status of the python-webm
package:

  * Windows: SUPPORTED
  * Ubuntu: SUPPORTED
  * Mac OS X: SUPPORTED


## Prerequisites ##

Below a list of prerequisites to use the python-webm package:

  * Python 2.6+ (http://www.python.org)
  * Python nose (http://code.google.com/p/python-nose)
  * libwebp from sources (http://www.webmproject.org/code/#webp-repositories) or binary distribution for the target OS
  * Python PIL (http://www.pythonware.com/products/pil)

Open the README file for more informations