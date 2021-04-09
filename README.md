# pdfsplitter
View and split pdf with naming functionality


Foundational code taken from PySimpleGui.org Cookbook and Demo programs.
Added functionality, layout, and basic logo.

I have plans for future updates beyond just splitting, but no basic timelines...its whenever I can get a chance.


Issues:  
-You have to restart the program everytime you want to open a new file.
-Interface doesn't seem entirely intuitive - I'm no GUI expert


How to use:

place files in location of choice.
Open dist folder
Open pdfsplitter folder
Locate pdfsplitter.exe (put together using pyinstaller)
DO NOT MOVE THIS FILE, ONLY CREATE SHORTCUTS (con of using pyinstaller)

It will prompt you to locate PDF.  Navigate and open PDF of choice.

On left is a viewer of the file.  You can use your mousewheel, keyboard, or Viewer Controls to zoom in (click same button to zoom back out), and view each page of the document easily.

Once you have the page you want split (only 1 page at a time, no ranges yet, looking for future functionality of this), in the box next to Split button, write the name of the file you want it to be.  Example:  TestPage1

Hit split.  

In the dist\pdfsplitter folder it will generate a single page pdf of the currently viewed page as name provided (Example would be TestPage1.pdf).  

You can use the multiline box below this to take notes on pages and names if working with a larger document.  

Once done, exit.  Sweet and simple.

MUCH Thanks to PySimpleGui and the main author of the Demo Program: Jorj X. McKie
