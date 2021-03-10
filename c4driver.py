"""
Initially published on github on March 9, 2021

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
background. Use image editing software (I use paint.net which is free) to make this file square. If your image
file is smaller than 1024x1024 then it will have to be stretched and may not look very good. You can also make
a selected icon.  This is the icon that will appear after you push the custom experience button.

"""

import re
from datetime import datetime
import zipfile 
import os, sys
from PIL import Image
import shutil
import glob
from pathlib import Path
import logging

def make_image_files(infile,outfileprefix):
    im=Image.open(infile) #maybe check for valid filename
    logger.info ("Using image file: "+infile+" - image format is: "+im.format+", size is:"+str(im.size))
    sizelist=[16, 32, 70, 90, 300, 512, 1024] #sizes in pixels of image files to be created
    for sz in sizelist:
        size=(sz,sz)
        outfile=outfileprefix+"_"+str(sz)+".png"  #outfileprefix will be default or selected
        logger.info ("Creating: "+outfile)
        if infile != outfile:
                try:
                    new_image=im.resize(size)
                    new_image.save(outfile, "png")
                except OSError:
                    print("cannot create resized image for", infile)
                    logger.error("cannot create resized image for"+ infile)
  
def parse_xml_file(file_name,drivername): #probably can cut this down to one line and not bother with a function
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y %H:%M")

    xml1="<created>.*</created>"  #This is to change the created date with current date/time see https://stackoverflow.com/questions/16159969/replace-all-text-between-2-strings-python
    xml2="<modified>.*</modified>" #This is to change the modified date with current date/time
    c="<created>"+current_time+"</created>"
    m="<modified>"+current_time+"</modified>"
    stext="experience-button-scenario" #driver name used for files
    stext2="Scenario - Experience Button" # driver name that is hard coded - may need to change to make it more flexible
    rtext=drivername
    fin = open(file_name, "rt")
    data = fin.read() #read file into data variable
    data = data.replace(stext, rtext) #replaces the names of all of the icon files
    data = data.replace(stext2, rtext) #replaces the name of the driver
    data=re.sub(xml1,c,data,flags=re.DOTALL) #replaces the created date
    data=re.sub(xml2,m,data,flags=re.DOTALL) #replaces the modified date
    fin.close() #close xml file that was read
    fin = open(file_name, "wt") #open xml file to write
    fin.write(data) #write updated xml file
    fin.close()

if len(sys.argv) <2:
    print ()
    sys.exit("Terminating as no filename provided for image file please provide an image name as an argument.")

# Define constants
orig_driver_name = "experience-button-scenario.c4z" #This file must exist in the base folder
outdir="tempdir" #Temporary folder to hold unzipped original C4Z file and image files.
image_path = "temp_image" #Temporary folder to hold all of the icon files
drivername=sys.argv[1] #The driver and icon file name passed in the command line
orig_image_file=drivername+".png" #This is the original image file which must be provided and it must be "drivername".png
base_selected_file=drivername+"_selected.png" #This is the provided selected file that will be used, it is optional

logging.basicConfig(filename=drivername+'.log',filemode='w', level=logging.INFO,format='%(message)s') #set up logging
logger=logging.getLogger()
now = datetime.now()
current_time = now.strftime("%m/%d/%Y %H:%M")
logger.info("Started running script at: "+current_time+"\n")

if not(os.path.exists(orig_driver_name)) :
    sys.exit("Terminating as there is no file called experience-button-scenario.c4z in current directory.")

if not(os.path.exists(base_selected_file)): #Look to see if there is a selected file
    base_selected_file=orig_image_file #If there isn't then just use the default file
    logger.info ("No selected image file so using the same image file for both default and selected")
xml_file_name=os.path.join(outdir,"driver.xml") #This is the driver file with xml code - it will be slightly altered
Path(image_path).mkdir(parents=True, exist_ok=True) #Create the temporaty folder for the icon files
defaultimagepath=os.path.join(image_path,"default") #path name for selected icon images
selectedimagepath=os.path.join(image_path,"selected") #path name for default icon images

make_image_files(orig_image_file,defaultimagepath)  #Make all of the default files
make_image_files(base_selected_file,selectedimagepath)  #Make all of the selected files

zipfile.ZipFile(orig_driver_name).extractall(path=outdir)  #extracts driver file to the path given
parse_xml_file(xml_file_name,drivername) #parses xml to change icon names for buttons and xml parameters - name, created and modified
oldiconpath=os.path.join(outdir,"www","icons-old")
shutil.rmtree(oldiconpath) #remove icons-old folder - no one knows why this folder exists - lazy coder?
shutil.move(os.path.join(image_path,"default_16.png"),os.path.join(outdir,"www","icons","device_sm.png")) #move the device small icon to the driver file
shutil.move(os.path.join(image_path,"default_32.png"),os.path.join(outdir,"www","icons","device_lg.png")) #move the device large icon to the driver file
os.remove(os.path.join(image_path,"selected_16.png")) #These files weren't needed but it was easier to create them in a loop and then delete
os.remove(os.path.join(image_path,"selected_32.png")) #These files weren't needed but it was easier to create them in a loop and then delete
def_files=glob.glob(os.path.join(image_path,"default_*.png")) # This is a list of all of the default image files 
sel_files=glob.glob(os.path.join(image_path,"selected*.png")) # This is all of the selected image files
for file in def_files+sel_files:
    shutil.copy(file,os.path.join(outdir,"www","icons","device")) #Copy all of the icon files to the proper folder
shutil.rmtree(image_path) #remove the temporary folder for the resized image files
shutil.make_archive(drivername,"zip",os.path.join(os.getcwd(),outdir))  #Make the zip file, have to use zip as an extension
shutil.rmtree(outdir) #remove the folder for the resized image files
shutil.move(drivername+".zip",drivername+".c4z") #Change extension to c4z


