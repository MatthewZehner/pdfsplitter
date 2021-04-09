"""
@created: 2018-08-19 18:00:00

@author: (c) 2018 Jorj X. McKie

@contributor(s): 2021 Matthew Zehner

Display a PyMuPDF Document using Tkinter
-------------------------------------------------------------------------------

Dependencies:
-------------
PyMuPDF, PySimpleGUI > v2.9.0, Tkinter with Tk v8.6+, Python 3


License:
--------
GNU GPL V3+

Description
------------
Read filename from command line and start display with page 1.
Pages can be directly jumped to, or buttons for paging can be used.
For experimental / demonstration purposes, we have included options to zoom
into the four page quadrants (top-left, bottom-right, etc.).

We also interpret keyboard events to support paging by PageDown / PageUp
keys as if the resp. buttons were clicked. Similarly, we do not include
a 'Quit' button. Instead, the ESCAPE key can be used, or cancelling the window.

To improve paging performance, we are not directly creating pixmaps from
pages, but instead from the fitz.DisplayList of the page. A display list
will be stored in a list and looked up by page number. This way, zooming
pixmaps and page re-visits will re-use a once-created display list.

Added 4/8/2021: Split functionality and ability to name each pdf split page.  Split page will
save into the dist\pdfsplitter folder.  Using pyinstaller to create distributable version
of PDFSplitter.  The .exe should not be moved, only short-cutted.
Further functionality yet to be installed:
(1) Merge
(2) Multi-page or page range splits
(3) Text Extract (pdfminer.six probably required)
(4) Image Extract (pdfminder.six probably required)
(5) Open new files without having to reload program.
(6) Format for new functionality and cleaner interface. :)

"""
import sys
import fitz
import PySimpleGUI as sg
from sys import exit
from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path, PureWindowsPath

sg.theme('Material1')

if len(sys.argv) == 1:
    fname = sg.popup_get_file(
        'PDF Browser', 'PDF file to open', file_types=(("PDF Files", "*.pdf"),))
    if fname is None:
        sg.popup_cancel('Cancelling')
        exit(0)
else:
    fname = sys.argv[1]

##def new_file():
##    if len(sys.argv) == 1:
##        fname = sg.popup_get_file(
##        'PDF Browser', 'PDF file to open', file_types=(("PDF Files", "*.pdf"),))
##        if fname is None:
##            sg.popup_cancel('Cancelling')
##            exit(0)
##    else:
##        fname = sys.argv[1]
##    return fname

doc = fitz.open(fname)
print(doc)
directory = PureWindowsPath(fname)
page_count = len(doc)

# storage for page display lists
dlist_tab = [None] * page_count

title = "PyMuPDF display of '%s', pages: %i" % (fname, page_count)




def get_page(pno, zoom=0):
    """Return a PNG image for a document page number. If zoom is other than 0, one of the 4 page quadrants are zoomed-in instead and the corresponding clip returned.

    """
    dlist = dlist_tab[pno]  # get display list
    if not dlist:  # create if not yet there
        dlist_tab[pno] = doc[pno].getDisplayList()
        dlist = dlist_tab[pno]
    r = dlist.rect  # page rectangle
    mp = r.tl + (r.br - r.tl) * 0.5  # rect middle point
    mt = r.tl + (r.tr - r.tl) * 0.5  # middle of top edge
    ml = r.tl + (r.bl - r.tl) * 0.5  # middle of left edge
    mr = r.tr + (r.br - r.tr) * 0.5  # middle of right egde
    mb = r.bl + (r.br - r.bl) * 0.5  # middle of bottom edge
    mat = fitz.Matrix(2, 2)  # zoom matrix
    if zoom == 1:  # top-left quadrant
        clip = fitz.Rect(r.tl, mp)
    elif zoom == 4:  # bot-right quadrant
        clip = fitz.Rect(mp, r.br)
    elif zoom == 2:  # top-right
        clip = fitz.Rect(mt, mr)
    elif zoom == 3:  # bot-left
        clip = fitz.Rect(ml, mb)
    if zoom == 0:  # total page
        pix = dlist.getPixmap(alpha=False)
    else:
        pix = dlist.getPixmap(alpha=False, matrix=mat, clip=clip)
    return pix.getPNGData()  # return the PNG image

def page_split(currentf, name, pno):
    pdf_file = open(str(directory),'rb')
    pdf_reader = PdfFileReader(pdf_file) #open file to be split

    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pdf_reader.getPage(pno)) #retrieves current page
    split_motive = open(str(name) + '.pdf','wb') #writes new file from name provided
    pdf_writer.write(split_motive)
    split_motive.close()

    pdf_file.close() #save and close

# -------base64 Encoded Images----------
blue_x_button = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACJklEQVRYhe2XzWoTYRSGnzP5pWnJlIhpsVA3tunClngNrqxuJOAiqwS8gW6kV9BrKILpxoJduDK41GVBSwkuErdCiS2ERrAlkzY9LsZom84kM0maIPjuBmbO+3C+873DkcXND2GUDSAviIlw41LVOvAKWA+ibIjI2s3b/pWImMCaqmIA+VGadyhvCGKOEcA0RnHmbhIEY3z2tv4D/DsAsVCA/PIcZiTo+o4ZCZJfniMWCngGcK/WYf7y0X3SyThP7iXJvStRt86vmkeDFFZXSCUmeXj3Fs/ff+HkrNWztqcOPFuaJZ2MA5BKTFJ4vHKlE5fNAdIzcTLzU+jFkADefv1Opfbzz/NliE5zgHK1xs5uiebRQU8ISW1+VC8QTkZtqE7zbKHI8allG4SjhG/fQQyHuVAfQ1hvnJMrlq51ops5gDYbXTvh6xo6QXQz9wIxshxwg/AF4DQHbS3NJnidW2V6IuILwjOA27SXq7WBIDwBmBFn82yhSLZQ7B9CW94Ani7OuE778anlCJFJL3St2YbwBPCmXGX/8Mc187Y6Ifa+HbL9udKzrloN70EUCwXIzE+xs1tyvGoA0xMRMg8W2P5U4cQ6611UfSQhgF607LNrNrx+0hPA1zUUI2DHajg6HAD6CKJhQ/SVhMOE6DuKhwUx0L9gUAhFMX4viuOBEKkb2FvqQBoAYisIsq6qYC+ppvS5q4nYEM2jA9RyzwlFQaQObAEvfgGJORd+MTy29QAAAABJRU5ErkJggg=='


# -------Images----------

cur_page = 0
data = get_page(cur_page)  # show page 1 for start
image_elem = sg.Image(data=data)
goto = sg.InputText(str(cur_page + 1), size=(4, 1))

'''build frames'''
control_buttons = [[
        sg.Button('Prev'),
        sg.Button('Next'),
        sg.Text('Page:'),
        goto,sg.Text("of"), sg.Text(page_count),],
       [sg.Text("Zoom:"),
        sg.Button('Top-L'),
        sg.Button('Top-R'),
        sg.Button('Bot-L'),
        sg.Button('Bot-R'),],
    ]

split_frame = [
    [sg.Text("Input new file name, then hit split to creat new PDF of current page")],
    [sg.InputText(),sg.Button('Split', tooltip="WARNING: IF YOU DO NOT CHANGE THE NAME BEFORE CREATING A NEW PDF IT WILL OVERWRITE PREVIOUS SPLIT")],
    [sg.Text("NOTICE: File will be created in \dist\pdfsplitter folder where the .exe is located.")],
]

view_frame = [[image_elem],]

title_quit_frame = [[sg.Text(str(title)), sg.Button(image_data=blue_x_button, key="Quit")],]

'''build columns'''

col_1 = [[sg.Frame('PDF Viewer', view_frame, title_color='blue', font='Any 12', element_justification="left")],]

col_2 = [
        [sg.Image(r'C:\Users\mtzehner\Desktop\Python\New Project.png', size=(300, 300))],
        [sg.Button('New File', key="new"), sg.Text("NOT FUNCTIONING")],
        [sg.Frame('Viewer Controls', control_buttons, title_color='blue', font='Any 12')],
                
        [sg.Frame('PDF Split Creator', split_frame, title_color='blue', font='Any 12')],
        [sg.Multiline("If large document, use this to note page and potential naming, or general notes", size = (65, 18), autoscroll=True, write_only=True)],
]

col_3 = [
        [sg.Button(image_data=blue_x_button, key="Quit")],
        ]

'''layout'''

layout = [
        [sg.Column(col_1, grab=True),
         sg.VSeperator(pad=(5, 5)),
         sg.Column(col_2, vertical_alignment="top", grab=False),
         sg.Column(col_3, vertical_alignment="top", grab=True),]
]
    

my_keys = ("Next", "Next:34", "Prev", "Prior:33", "Top-L", "Top-R",
           "Bot-L", "Bot-R", "MouseWheel:Down", "MouseWheel:Up")
zoom_buttons = ("Top-L", "Top-R", "Bot-L", "Bot-R")



window = sg.Window(title, layout,
                   return_keyboard_events=True, use_default_focus=False,
                   )

old_page = 0
old_zoom = 0  # used for zoom on/off
# the zoom buttons work in on/off mode.

while True:
    event, values = window.read()#timeout=100put inside parantheses when done
    print(event, values) #remove when done
    zoom = 0
    force_page = False
    if event == sg.WIN_CLOSED or event == 'Quit':
        break
        

    if event in ("Escape:27",):  # this spares me a 'Quit' button!
        break
    if event[0] == chr(13):  # surprise: this is 'Enter'!
        try:
            cur_page = int(values[0]) - 1  # check if valid
            while cur_page < 0:
                cur_page += page_count
        except:
            cur_page = 0  # this guy's trying to fool me
        goto.update(str(cur_page + 1))
        # goto.TKStringVar.set(str(cur_page + 1))

    elif event in ("Next", "Next:34", "MouseWheel:Down"):
        cur_page += 1
    elif event in ("Prev", "Prior:33", "MouseWheel:Up"):
        cur_page -= 1
    elif event == "Top-L":
        zoom = 1
    elif event == "Top-R":
        zoom = 2
    elif event == "Bot-L":
        zoom = 3
    elif event == "Bot-R":
        zoom = 4

    if event == 'Split':
        filename = values[4]
        page_num = int(values[3])-1
        page_split(directory, filename, page_num)

##    if event == 'new':
##        doc = new_file()
        

    # sanitize page number
    if cur_page >= page_count:  # wrap around
        cur_page = 0
    while cur_page < 0:  # we show conventional page numbers
        cur_page += page_count

    # prevent creating same data again
    if cur_page != old_page:
        zoom = old_zoom = 0
        force_page = True

    if event in zoom_buttons:
        if 0 < zoom == old_zoom:
            zoom = 0
            force_page = True

        if zoom != old_zoom:
            force_page = True

    if force_page:
        data = get_page(cur_page, zoom)
        image_elem.update(data=data)
        old_page = cur_page
    old_zoom = zoom

    # update page number field
    if event in my_keys or not values[3]:
        goto.update(str(cur_page + 1))
        # goto.TKStringVar.set(str(cur_page + 1))

window.close()
