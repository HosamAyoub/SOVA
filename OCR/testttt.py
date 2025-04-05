from picamera2 import Picamera2

picam2 = Picamera2()
#still_config = picam2.create_still_configuration({'size':(1280, 720), 'format':'RGB888'})
#picam2.configure(still_config)
#picam2.still_configuration.main.format = "RGB888"
picam2.still_configuration.align()
picam2.configure("still")
picam2.set_controls({"ExposureTime": 150000, "AnalogueGain": 15.0, "Saturation": 1.3, "Contrast": 1.0, "Sharpness": 1.0})
picam2.start()
picam2.capture_file("Newwww1.jpg")
picam2.stop()