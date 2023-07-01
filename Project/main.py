import RPi.GPIO as GPIO
import argparse
import queue
import sys
import sounddevice as sd
import subprocess
from vosk import Model, KaldiRecognizer
import time
from pygame import mixer, quit


options = {'face': ['face', 'person', 'friend', 'here\'s', 'frank', 'who', 'whoa', 'who\'s', 'hope', 'name', 'versa', 'burst', 'detect', 'addict'],
           'keys': ['keys', 'key', 'geese', 'keith', 'geeze', 'these', 'mikey'],
           'wallet': ['wallet', 'all', 'while', 'on', 'old'],
           'color': ['color', 'colour'],
           'read': ['read', 'text', 'hurry', 'harry', 'resist', 'her eat', 'hickest', 'ickets', 'paper', 'book', 'menu', 'story'],
           'stop': ['stop', 'terminate', 'rminate', 'urn', 'turn', 'fair enough', 'scott'],
           'bye': ['bye', 'by', 'boy', 'goodbye'],
           'add': ['add', 'at', 'hat', 'had', 'at']}

processes = []
q = queue.Queue()


GPIO.setmode(GPIO.BOARD)
trigPIN = 16
echoPIN = 18
btnPIN = 36
flashPIN = 31

GPIO.setup(trigPIN, GPIO.OUT)
GPIO.setup(echoPIN, GPIO.IN)
GPIO.setup(flashPIN, GPIO.OUT)
GPIO.setup(btnPIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.add_event_detect(btnPIN, GPIO.FALLING, bouncetime=500)

def play_audio(audio_file):
    mixer.init()
    mixer.music.load(audio_file)
    mixer.music.play()
    while mixer.music.get_busy():
        continue
    quit()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def stop():
    for p in processes:
        if p.poll() is None:
            p.terminate()
    GPIO.output(flashPIN, GPIO.LOW)

def func():
    #subprocess.Popen(["./mimic1/mimic", "-t", "Hello, I am SOVA. How can I help you?"])
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-l", "--list-devices", action="store_true",
        help="show list of audio devices and exit")
    args, remaining = parser.parse_known_args()
    if args.list_devices:
        ##print(sd.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])
    parser.add_argument(
        "-f", "--filename", type=str, metavar="FILENAME",
        help="audio file to store recording to")
    parser.add_argument(
        "-d", "--device", type=int_or_str,
        help="input device (numeric ID or substring)")
    parser.add_argument(
        "-r", "--samplerate", type=int, help="sampling rate")
    parser.add_argument(
        "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
    args = parser.parse_args(remaining)

    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, "input")
            args.samplerate = int(device_info["default_samplerate"])
            
        if args.model is None:
            model = Model(lang="en-us")
        else:
            model = Model(lang=args.model)

        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None
        
        play_audio("MainVoiceCommands/Hello.wav")
        with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device,
                dtype="int16", channels=1, callback=callback):
            print("#" * 80)
            print("Press Ctrl+C to stop the recording")
            print("#" * 80)

            rec = KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result().strip("{}\n\"").lstrip("  \"text\" : ")
                    print(result)
                    words = result.split(' ')
                    if (words[0] in options['face']) or (words[-1] in options['face']):
                        stop()
                        p1 = subprocess.Popen(["python3", "FaceRecognition/facial_req.py"])
                        #subprocess.Popen(["./mimic1/mimic", "-t", "Running the face recognition Program."])
                        play_audio("MainVoiceCommands/Face.wav")
                        processes.append(p1)
                    elif (words[-1] in options['color']) or ((len(words) > 4) and (words[3] in options['color'])):
                        stop()
                        p2 = subprocess.Popen(["python3", "ColorDetection/Color_detection.py"])
                        play_audio("MainVoiceCommands/Color.wav")
                        processes.append(p2)
                    elif words[-1] in options['keys']:
                        stop()
                        p3 = subprocess.Popen(["python3", "KeysDetection/KeysModel.py"])
                        #subprocess.Popen(["./mimic1/mimic", "-t", "Running the keys detection Program."])
                        play_audio("MainVoiceCommands/Keys.wav")
                        processes.append(p3)
                    elif (len(words) > 2) and (words[-2] in options['wallet'] or words[-1] in options['wallet']):
                        stop()
                        p4 = subprocess.Popen(["python3", "WalletDetect/DetectWallet.py"])
                        #subprocess.Popen(["./mimic1/mimic", "-t", "Running the wallet detection Program."])
                        play_audio("MainVoiceCommands/Wallet.wav")
                        processes.append(p4)
                    elif (len(words) > 2) and ((words[2] in options['read']) or (words[-1] in options['read']) or (words[0] in options['read'])):
                        stop()
                        p5 = subprocess.Popen(["python3", "OCR/NewOCR/OCR.py"])
                        #subprocess.Popen(["./mimic1/mimic", "-t", "Running the Reading Program."])
                        play_audio("MainVoiceCommands/Reading.wav")
                        processes.append(p5)
                    elif (len(words) > 2) and (words[-2] in options['add']):
                        stop()
                        result = rec.Result().strip("{}\n\"").lstrip("  \"text\" : ")
                        print(result)
                        subprocess.Popen(["mkdir", f"FaceRecognition/dataset/{words[-1]}"])
                        print("\nMake directory\n")
                        p6 = subprocess.Popen(["python3", "FaceRecognition/headshots_picam.py", words[-1]])
                        subprocess.Popen(["./mimic1/mimic", "-t", f"Taking pictures to {words[-1]}. You can just say stop at any time to stop taking pictures and start trainning"])
                        processes.append(p6)
                        ################################################
                        while result not in options['stop']:
                            data = q.get()
                            if rec.AcceptWaveform(data):
                                result = rec.Result().strip("{}\n\"").lstrip("  \"text\" : ")
                                print(result)
                                if result in options['stop']:
                                    stop()
                                    p7 = subprocess.Popen(["python3", "FaceRecognition/train_model.py"])
                                    #subprocess.Popen(["./mimic1/mimic", "-t", "Running the face detection train Program."])
                                    play_audio("MainVoiceCommands/Train.wav")
                                    processes.append(p7)
                                    break
                                
                    elif words[0] in options['stop']:
                        stop()
                        play_audio("MainVoiceCommands/Stop.wav")
                    elif words[0] in options['bye']:
                        stop()
                        print("\nDone...")
                        return
                        
                if dump_fn is not None:
                    dump_fn.write(data)
                


    except KeyboardInterrupt:
        print("\nDone")
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ": " + str(e))
        

def ultrasonic():
    subprocess.call(["./mimic1/mimic", "-t", "Running power saving mode."])
    meters = 10
    old_meters = 10
    while True:
        GPIO.output(trigPIN, GPIO.LOW)
        time.sleep(2E-6)
        GPIO.output(trigPIN, GPIO.HIGH)
        time.sleep(10E-6)
        GPIO.output(trigPIN, GPIO.LOW)
        while not GPIO.input(echoPIN):
            pass
        echoStartTime = time.time()
        while GPIO.input(echoPIN):
            pass
        echoEndTime = time.time()
        pingTravelTime = echoEndTime - echoStartTime
        meters = round((pingTravelTime * 1E3)/ 5.3, 2)
        measure = (abs(meters - old_meters) / old_meters ) * 100
        if measure >= 15:
            old_meters = meters
            print(f"An object is {meters} meters away from you.")
            subprocess.call(["./mimic1/mimic", "-t", f"An object is {meters} meters away from you."])
        time.sleep(2)
        if GPIO.event_detected(btnPIN):
            print('Done')
            break



if __name__ == '__main__':
    try:
        while True:
            ultrasonic()
            func()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('\nDone.')
