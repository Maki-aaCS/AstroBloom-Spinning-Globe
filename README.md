# AstroBloom-Spinning-Globe

This is my *(Makimaa Omkararuban)* workflow for the AstroBloom Nasa Space Apps Competition.

**How do I access this on my web browser if it doesn't open when I click it through my File Explorer (for Windows)?**
Either:
- Open this link (can be opened through deployment - is part of this github repository): http://earthinnovation.design/

Or
- Go to your command prompt (cmd)
- Insert your file path (example: if your file is in you desktop in a folder name called 'AstroBloom', type
  cd desktop/AstroBloom
- On the next line type: python -m local.server 8000 (This helps you access local servers since your laptop restricts some sites)
- Next, go to your web-broswer and type http://localhost:8000/YourFileNameHere.html
- Now you should see your Globe (like the one below) :)
<img width="2879" height="1428" alt="image" src="https://github.com/user-attachments/assets/3f0740d5-d830-441c-b6c5-c7e0bc9e66c4" />

**What does each file do?**

- **AstroBloom_Pulse:** An update to Vika's spinning globe code. Note: **AstroBloom_Pulse_Final is the final version** with the functioning month slider and pulses showing for several locations in each country.
- AstroBloom_Gamified_Raw in 'Raw' branch: A first trial sample as to how the gamified version of the spinning globe will look.
- AstroBloom_Gamified1: Working functions including timer, points system and popups.
- AstroBloom_Gamified2: The final Spinning globe with youtube popups for each location along with score system.
- **AstroBloom_Agri&Bloom_Gamified** no called **index.html**: 'Gamified' spinning globe, but with Agriculture added! (Note: the use of generative AI is acknowledged in the comments of this code).
  
- **NDVIPredictions: This file doesn't have any direct link to the spinning globe, but is part of my workflow.** Gives NDVI predictions for the five countries used for sampling (Japan, Alaska, Madagascar, New Zealand and Fiji). Used NDVI data from 2018-2023 to predict 2023-2024 NDVI patterns. (Note: Use of generative AI mentioned in code comments.


**How to use the final file?**

For the **NDVIPredictions** python file (opened in code editor and press run to execute):
- You will first be able to see the NDVI pattern for 2018-2023 either using the hdf you attach, or if nothing is attached, it will use sample data (part of the code). The examples attached here are for Japan.
<img width="1763" height="871" alt="image" src="https://github.com/user-attachments/assets/e374e25a-2557-4d95-ab4f-33ed3043e979" />
- This will then be followed by the NDVI Prediction for 2023-2024.
<img width="1760" height="860" alt="image" src="https://github.com/user-attachments/assets/a5fbddcc-21eb-4c41-8a7e-3b720621a6e2" />



For the **Astrobloom_Agri&Bloom_Gamified** html file which is now called **index.html** (opened in webrowser mostly):

- Hover around (or on) pulsating circles to see location.

- Click on location to see a video of blooming flowers in that location.
- Once the location is clicked, you will obtain 100 points (can be seen top-left corner of the screen for score).
<img width="2879" height="1453" alt="image" src="https://github.com/user-attachments/assets/f265b25b-7298-4fa5-a34b-f3e1ceff77e7" />
- Once you have viewed all areas, a tick mark will appear beside you final total score.


  
- To switch between blooming and agriculture, there is a drop down menu on the top-right corner of the page.
<img width="2879" height="1439" alt="image" src="https://github.com/user-attachments/assets/6edb912e-5c49-4477-bc3c-8cd46078e229" />






  


