# C4driverbuilder
This python program will allow you to use a custom icon in the Control4 Scenario Experience Button.
It does this by taking the original driver with plain buttons and replaces the image files used
for the icons.

Pre-requisites:  Python3, an image file and the Control4 experience-button-scenario.c4z driver.
You must also have the package pillow installed.  If you get an error saying ModuleNotFoundError: No module named 'PIL'
then from the command line type python3 -m pip install pillow

I have tried this on Windows 10, Linux and Ubuntu on Win10 using SFU. I think it should work on a Mac as well.
The driver can be downloaded from http://drivers.control4.com/experience-button-scenario.c4z

You need at least one png image file that will be used for the new icon. If desired, you can also provide a second
image file that is the selected version of this button. Let's assume the default icon image file is called stones.png. 
Then you could also have an image file for the selected button which must be named stones_selected.png and it must be 
in the same folder.

The main image file must be a png file and ideally it should be square and 1024x1024 or larger.

Place the image file(s) in a folder along with this file and the original, unaltered C4 driver file, which is
experience-button-scenario.c4z.

Run the program with: "python3 c4driver.py stones" assuming that the image file is stones.png.
The program should just take a few seconds to run.  You should end up with an additonal file in that folder
called stones.c4z.  This is a control4 driver  file.  Have your dealer install this in the room and give it the name
you want to be displayed in the Navigator. This script will create a log file with info  - in this example stones.log

For more info on how to alter a driver to  use your own custom icons see the following Youtube
video: https://www.youtube.com/watch?v=wW-eOh3sWFM&t=95s

Recommendations: - Your icon will look best if you do some preparation. Try to find a file with a transparent 
background. Use image editing software (I use paint.net https://www.getpaint.net/download.html which is free) to make this file 
square. If your image file is smaller than 1024x1024 then it will have to be stretched and may not look very good. You can also make
a selected icon.  This is the icon that will appear after you push the custom experience button.
