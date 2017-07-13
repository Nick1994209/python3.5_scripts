##  mac install tesseract

##### Install leptonica with TIFF support (and every other format, just in case)
    brew install --with-libtiff --with-openjpeg --with-giflib leptonica

##### Install Ghostscript
    brew install gs

##### Install ImageMagick with TIFF and Ghostscript support
    brew install --with-libtiff --with-ghostscript imagemagick

##### Install Tesseract devel with all languages
    brew install --all-languages tesseract

##### python
    pip install tesseract