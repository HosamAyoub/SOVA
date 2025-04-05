# SOVA (Sight Over Voice Ally)

SOVA is a smart, assistive wearable designed to empower blind and visually impaired individuals by transforming visual information into audible cues. By leveraging computer vision, OCR, text-to-speech technologies, and an integrated hardware system on a Raspberry Pi 4 platform, SOVA provides real-time situational awareness and independent navigation.



## Table of Contents

- [Overview](#overview)
- [Abstract](#abstract)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Software Components](#software-components)
  - [Machine Learning and Computer Vision](#machine-learning-and-computer-vision)
  - [OCR and Text-to-Speech](#ocr-and-text-to-speech)
- [Integration and Operation Modes](#integration-and-operation-modes)
- [Yocto-based Linux Image](#yocto-based-linux-image)
- [Usage](#usage)
- [Results and Performance Evaluation](#results-and-performance-evaluation)
- [Future Work](#future-work)
- [Acknowledgements](#acknowledgements)
- [Authors and Supervisors](#authors-and-supervisors)
- [License](#license)



## Overview

SOVA (Sight Over Voice Ally) bridges the accessibility gap for blind and visually impaired (BVI) individuals. The system integrates a webcam-equipped smart glasses setup with a Raspberry Pi 4 to capture, process, and interpret visual data in real time. It then converts recognized text and objects into spoken audio, allowing users to navigate public spaces safely and independently.



## Abstract

Visual impairment affects millions globally, with over 285 million people facing challenges in daily life due to reduced or lost sight. SOVA addresses these challenges by combining:
- **Real-Time Image Processing:** Capturing live images through smart glasses.
- **Object & Text Recognition:** Using computer vision and OCR (Tesseract) to interpret surroundings.
- **Audio Feedback:** Converting recognized information into speech using a text-to-speech API.

This innovative approach enables BVI individuals to access crucial environmental information on the go.



## Features

- **Real-Time Object and Text Recognition:**  
  Processes live video streams to detect and identify objects and printed text.
- **Audio Feedback:**  
  Converts visual cues into speech, allowing users to understand their surroundings without needing to see.
- **Wearable and Portable:**  
  Compact design integrated into smart glasses for comfortable, continuous use.
- **Cost-Effective and Open-Source:**  
  Built on affordable hardware and open-source software (OpenCV, Tesseract, mimic API).
- **Raspberry Pi 4 Integration:**  
  Provides robust processing power for real-time data analysis.

<figure>
<img src="https://github.com/HosamAyoub/SOVA/blob/main/images/Glasses.png" alt="Smart Glasses">
<figcaption><b>Figure:<b/> Smart Glasses built with 3D printer to help the blind in their daily life.</figcaption>
</figure>


## System Architecture

SOVA comprises two primary subsystems:

1. **Hardware Components:**
   - **Smart Glasses:**  
     Equipped with an integrated webcam to capture the user's environment.
   - **Raspberry Pi 4:**  
     Acts as the central processing unit for image capture and processing.
   - **Power, Mic, Headphone, and Connectivity Modules:**  
     - **Mic:** Captures user voice commands.
     - **Headphone:** Delivers audio feedback.
     - **Camera & Flash:** Capture real-time photos and video under various lighting conditions.
     - **Push Buttons & Ultrasonic Sensor:** Facilitate mode switching and measure distances.

2. **Software Pipeline:**
   - **Image Acquisition & Preprocessing:**  
     Captures images via the webcam and enhances them for analysis.
   - **Computer Vision & OCR:**  
     Uses OpenCV and Tesseract to detect objects and extract text.
   - **Audio Synthesis:**  
     Converts recognized text into speech via a text-to-speech engine.



## Software Components

### Machine Learning and Computer Vision

SOVA implements machine learning and computer vision techniques to boost recognition accuracy. Key aspects include:
- **Object Detection:**  
  Identifies obstacles and objects in real time.
- **Image Preprocessing and Annotation:**  
  Enhances images for optimal processing.
- **Evaluation Metrics:**  
  Uses tools like confusion matrices and mean average precision (mAP) for performance evaluation.

    <figure>
    <img src="https://github.com/HosamAyoub/SOVA/blob/main/images/AI%20vs%20ML%20vs%20DL.png" alt="AI vs ML vs DL">
    <figcaption><p><b>Figure:</b> Comparison of AI, Machine Learning, and Deep Learning methods.</p></figcaption>
    </figure>

    <figure>
    <img src="https://github.com/HosamAyoub/SOVA/blob/main/images/Computer%20Vision%20Tasks.png" alt="Computer Vision Tasks">
    <figcaption><p><b>Figure:</b> Overview of computer vision tasks for environmental analysis.</p></figcaption>
    </figure>

### OCR and Text-to-Speech

- **Optical Character Recognition (OCR):**  
  Tesseract extracts text from captured images.
- **Text-to-Speech (TTS):**  
  A TTS engine (e.g., mimic API) converts text into audible speech.

   ![Image Annotation Process](https://github.com/HosamAyoub/SOVA/blob/main/images/Image%20Annotation%20Process.png)
   *Figure: Process of annotating images for OCR training.*



## Integration and Operation Modes

The integration script coordinates various hardware components and models to operate in two primary modes: **Power-Saving Mode** and **SOVA Mode**. This ensures efficient performance while providing comprehensive assistance.

### Hardware Components Utilized
- **Raspberry Pi 4:** Real-time processing and model execution.
- **Microphone:** Continuously captures voice commands.
- **Headphone:** Provides clear audio feedback.
- **Camera and Flash:** Capture high-quality images and videos in all lighting conditions.
- **Push Buttons:** Allow mode switching from power-saving to full SOVA operation.
- **Ultrasonic Sensor:** Measures distances in power-saving mode to inform the user.

### Operation Modes

#### Power-Saving Mode
- **Purpose:**  
  Conserve power and reduce CPU load.
- **Functionality:**  
  - The ultrasonic sensor measures distances at regular intervals.
  - Provides periodic audio feedback about nearby objects.
  - Monitors a push button; when pressed, switches to SOVA mode.

#### SOVA Mode
- **Purpose:**  
  Run comprehensive assistance models based on voice commands.
- **Functionality:**  
  - **Voice Command Detection:**  
    Uses an offline voice recognition model (Vosk) running in the background.
  - **Model Activation:**  
    Depending on voice commands:
    - **Face Recognition:**  
      - Announces known faces (e.g., friend Mohamed) or prompts to add unknown faces.
    - **Color Detection:**  
      - Identifies and announces colors when requested.
    - **Wallet & Keys Detection:**  
      - Guides the user to locate keys or wallet.
    - **OCR:**  
      - Reads out text when commanded.
      
The script (see `main.py`) listens for voice commands, processes audio in real time, and launches the corresponding models via subprocesses. It also manages mode switching through push button events, ensuring a balance between energy efficiency and full functionality.



## Yocto-based Linux Image

To optimize performance and reduce resource usage, we built a custom Linux image using the Yocto Project. Unlike the standard GUI-based Raspberry Pi image, our Yocto image is lightweight and tailored specifically for SOVA, providing several benefits:
- **Optimized Performance:**  
  A minimal Linux distribution that loads faster and uses fewer system resources.
- **Reduced Footprint:**  
  By including only the essential components, the image occupies less storage space and reduces memory usage.
- **Customization:**  
  The Yocto Project's layered architecture (using OpenEmbedded and BitBake) allowed us to create a custom distribution that meets the specific needs of SOVA, including better power management and streamlined application integration.

This custom Linux image enhances the overall responsiveness of the system and extends battery life, ensuring that SOVA operates efficiently in real-time.




## Usage

- **Navigation Assistance:**  
  In power-saving mode, the ultrasonic sensor measures distances and provides periodic audio feedback about nearby objects.
  
- **Advanced Assistance:**  
  In SOVA mode, the voice recognition system continuously listens for commands. For example:
  - "Who is here?" triggers the face recognition model.
  - "What is this color?" triggers the color detection model.
  - "Where are my keys?" or "Where is my wallet?" triggers the corresponding detection model.
  - "Can you read this?" activates the OCR model to read text aloud.
  > Unless it's all real-time analysis (offline) the user can ask any question he want and the required model will run, not 1 specific question for every model.
  
- **Interactive Model Training:**  
  If an unknown face is detected, the system can prompt the user to add the new face by capturing headshots and training the recognition model.

- **Check The project video:**
  From [here](https://drive.google.com/file/d/1yzV2mCZMOBQOcQ9X4bPADtr_EdqX7H1A/view?usp=drive_link)


## Results and Performance Evaluation

Performance evaluation includes:
- **Confusion Matrix:**  
  Displays the accuracy of object and text recognition modules.

- **Mean Average Precision (mAP):**  
  Assesses the accuracy of object detection within the user’s field of view.

These metrics ensure that SOVA delivers reliable assistance under various conditions.



## Future Work

Planned enhancements include:
- **Advanced Object Recognition:**  
  Integration of more sophisticated deep learning models for improved accuracy.
- **Enhanced Audio Feedback:**  
  Customization of voice modulation and support for multiple languages.
- **Battery Optimization:**  
  Extending operational time through further power management improvements.
- **User-Centered Design:**  
  Refining ergonomics and interface based on feedback from BVI users.



## Acknowledgements

This project is dedicated to the blind community, whose resilience inspires us daily. Special thanks to:
- **Dr. Fatma Mazen** and **Dr. Sara Ashry** for their invaluable supervision.
- Friends and colleagues (Merihan Shaban, Maysson Khalaf) for their contributions.
- Eng. Ramy Adel and Eng. Mazen Osama for technical guidance and support.



## Authors and Supervisors

**Authors:**  
- Hosam Ayoub Bayoumi  
- Hesham Yasser Ahmed  
- Shehab Emad Abd-ElTawwab  
- Amr Hosam Yassin  

**Supervisor:**  
- Dr. Fatma Mazen
