# install cv  - to python2

    brew tap homebrew/science
    brew install opencv
    /usr/local/Cellar/opencv/(you_version)

    cd (you_virtualenv/lib/python(version))
        __example= /.virtualenvs/pyth2.7venv/lib/python2.7

    ln -s /usr/local/Cellar/opencv/2.4.13.2/lib/python2.7/site-packages/cv.py cv.py
    ln -s /usr/local/Cellar/opencv/2.4.13.2/lib/python2.7/site-packages/cv2.so cv2.so

