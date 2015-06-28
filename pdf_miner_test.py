"""
PDF is more like an image. A mix of text and binary. Not human readable is raw form.
> less filename.pdf

Also, needs to be read backwards. Alot of info you need first, is at the end of the file. (Something to do with concat'ing pdfs?)


Parts of PDF (http://brendanzagaeski.appspot.com/0005.html):
    - header
        - e.g. "treat this file's contents as text or binary"
    - body
        - dictionaries, array, name, string, nums (as strings)
        - but the contents inside these data structures are goobleygook
        - catalog object, page objects, indirect stream.
    - xref (xref table)
        - ??
            -mentions how all the object in the body are laid out?
            -in relation to each other?
    - trailer
        - root object (PDF is like a root structure)
        - each page is like a child node
        - trailer includes startsxref and EOF


Reading disc blocks (block size 1).
> dd if=filename.pdf bs=1
skipping to certain xref'ed objects
> dd if=filename.pdf bs=1 skip=2

"""

#######################################################
# FIRST APPROACH.
#   - getting the bach cmds to work, but not the imported libraries.
#   - do quick hack first to get working.

import subprocess

filename = "Bill-1.pdf"
bash_cmd = "env/bin/pdf2txt.py -o output.html %s" % filename

process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]


#######################################################
# SECOND APPROACH.
#   - getting the libraries to work

# TODO: currently, I keep getting only None objects.

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice


# PARSING THE FILE

# Open a PDF file.
fp = open('Bill-2.pdf', 'rb')
# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)
# Create a PDF document object that stores the document structure.
# Supply the password for initialization.
password = "testing"
document = PDFDocument(parser, password)
# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed
# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()
# Create a PDF device object.
device = PDFDevice(rsrcmgr)
# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)
# Process each page contained in the document.
for page in PDFPage.create_pages(document):
    output = interpreter.process_page(page)
    print output




