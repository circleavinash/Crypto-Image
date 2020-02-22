# Crypto-Image
A simple project to hide information in images.
Includes two functions:
  1. Encode: Takes an image and text to be hidden in the image; writes an encoded image file.
  2. Decode: Takes an image with encoded text; writes a binary image with text "written" on it.
  
CLI:

    $python3 --action encode --image <path to image> --text <text to hide>
    (or)
    $python -a encode -i <path to image> -t <text to hide>
  
  
    $python3 --action decode -- image <path to encoded image>
    (or)
    #python -a decode -i <path to encoded image>
