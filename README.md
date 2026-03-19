# esp32-robot-ai

ESP32-based robot with camera streaming, web control, and ball detection logic.

## Files
- `5.2_ESP32Cam_WIFI_Web.ino` - ESP32-CAM streaming code
- `5.1_Arduino_All_Web.ino` - robot web control code
- `ball_detect_stop.py` - Python ball detection and stop request logic

## Project goal
Detect a ball from the camera stream and stop the robot automatically.

## Planned workflow
1. Connect to ESP32-CAM stream
2. Detect red ball with Python/OpenCV
3. Send stop request to robot
4. Tune detection and stability

## Current status
- [x] GitHub repository created
- [x] Camera/control source files uploaded
- [x] Initial ball detection script added
- [ ] Confirm camera stream URL
- [ ] Confirm robot stop URL
- [ ] Test detection live
- [ ] Integrate and tune
