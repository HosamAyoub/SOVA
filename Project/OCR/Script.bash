libcamera-still -n -q 100 --saturation 0 --sharpness 3 -o Image.jpg
python TessFinal2.py Image.jpg
#rm Image.jpg