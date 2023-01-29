# RPi-TrailCam
Scripts to turn an RPi with a Camera and GPIO PIR Sensor into a motion detection Trail Cam

This is the 2nd time I've written Python, and while I'm happy with how this is all working I'm sure someone more experienced could get this done far more simply.

These scripts are written for a Raspberry Pi. I am using a Pi Zero with Raspberry Pi OS in it's minimal version. CPU load is very low and the _scripts_ use only a couple of MB of RAM at most.

My goal for this is to have it running on battery power for a couple of days. I will continue to develop the Capture side so that, when motion is detected, it will use a Cellular connection to send me a low res JPG file, and then capture a video or a series of high quality images that it will store locally. Right now, for testing, it's just on my home WiFi.

To help minimize SD card writes, I create a small RAM disk on boot where I do any non-permanent writes. I create this with the below line in the /etc/fstab file. You can set the size to anything you want, but it is using system RAM. The data will be lost when the systems reboots. But, the RAM disk only uses RAM when data is actually stored. It doesn't pre-allocate the space, so you system will have access to any RAM not being actively used by files. Be careful not to exhuast the available RAM!

<br><code>image_storage           /images        tmpfs   size=256M          0       0</code>

You'll see I keep the 'movement' trigger file in this location, and the JPG for uploading. Images I want to store permentaly will be loaded to the SD card.

For this process to work, both scripts should just be kept running. I'll work to get a systemd service written up at some point, but for now I'll probably just use crontab to launch them on boot.

With both scripts running, they just wait for each other. Each one works, while the other waits.

The 'MotionCheck.py' script (Python3) is always checking for motion. When it finds it, it creates a small file and waits until that file is gone.

The 'Capture' script (Bash) is always checking for the small file the MotionCheck.py script creates. When it sees it, it triggers the capture process to take an image (And, in future other images/videos). When the capture routine is complete, it then removes the small file. The MotionCheck script then begins looking for motion again.

I found doing this in a more integrated way would give me 'multiple triggers' for motion. If motion was triggered, it would start the capture. During the capture though, if more motion was seen, it would 'queue' up another capture, over and over. So, even when motion stopped, it might still be processing the 'queue' of motion for several more minutes.

Like I said, someone more experienced could, I'm sure, do this more efficiently.
