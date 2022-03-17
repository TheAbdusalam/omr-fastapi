# Optical Mark Recognition
This repository is a basic optical mark recognition to score exam-papers using python and FastApi.


Repository:  https://github.com/abdusalam-mah/omr-fastapi

> NB : currently only works with "choose the correct answer" type of questions

# 

### Usage
#
1. install these packages first

    `pip install fastapi uvicorn numpy opencv-python`

2. after that to start the server run 

    `python server.py`

3. use PostMan or Axios to send a POST request with an image file, get an example image from `app/temp/images/` it looks something like:
![example image](https://github.com/abdusalam-mah/omr-fastapi/app/temp/images/test-image.png?raw=true)

### To do next
* add request validation
* process testing
* support different scoring types
* add support for additional paper types
