## Valorant Ai AimBot + TriggerBot

Description: this is an aimbot alon with triggerbot that utilizes the yolov11 model to predict the position of enemies and target head and torso using computer vision
and sends mouse inputs using arduino microcontroller

How to use:
1. create a custom environment , preferably python 3.8.10 others work too I think
2. https://developer.nvidia.com/cuda-11-8-0-download-archive?target_os=Windows <-- download cuda
3. `pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118`
4. install the varies dependencies given in main.py [note: `pip install pywin32` for `win32gui` ]
5. `python main.py` to run
6. make sure to change put keybindings for fire to 'p'.
7. change the enemy color to purple for better accuracy
8. keep the mouse sensitivity at 0.8
9. needs an arduino leonardo
10. add ino script to it

