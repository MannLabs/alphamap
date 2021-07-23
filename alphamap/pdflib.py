#!/usr/bin/env python
# coding: utf-8

# This script has kindly been provided by Julia Schessner.

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph


from pdfrw import PdfReader, PdfDict
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl
from reportlab.platypus import Flowable
from reportlab.lib.enums import TA_JUSTIFY,TA_LEFT,TA_CENTER,TA_RIGHT

# The following class was copied from https://stackoverflow.com/questions/3448365/pdf-image-in-pdf-document-using-reportlab-python (answer from skidzo, 2017)
class PdfImage(Flowable):
    """
    PdfImage wraps the first page from a PDF file as a Flowable
    which can be included into a ReportLab Platypus document.
    Based on the vectorpdf extension in rst2pdf (http://code.google.com/p/rst2pdf/)

    This can be used from the place where you want to return your matplotlib image
    as a Flowable:

        img = BytesIO()

        fig, ax = plt.subplots(figsize=(canvaswidth,canvaswidth))

        ax.plot([1,2,3],[6,5,4],antialiased=True,linewidth=2,color='red',label='a curve')

        fig.savefig(img,format='PDF')

        return(PdfImage(img))

    """

    def __init__(self, filename_or_object, width=None, height=None, kind='direct'):
        # If using StringIO buffer, set pointer to begining
        if hasattr(filename_or_object, 'read'):
            filename_or_object.seek(0)
            #print("read")
        self.page = PdfReader(filename_or_object, decompress=False).pages[0]
        self.xobj = pagexobj(self.page)

        self.imageWidth = width
        self.imageHeight = height
        x1, y1, x2, y2 = self.xobj.BBox

        self._w, self._h = x2 - x1, y2 - y1
        if not self.imageWidth:
            self.imageWidth = self._w
        if not self.imageHeight:
            self.imageHeight = self._h
        self.__ratio = float(self.imageWidth)/self.imageHeight
        if kind in ['direct','absolute'] or width==None or height==None:
            self.drawWidth = width or self.imageWidth
            self.drawHeight = height or self.imageHeight
        elif kind in ['bound','proportional']:
            factor = min(float(width)/self._w,float(height)/self._h)
            self.drawWidth = self._w*factor
            self.drawHeight = self._h*factor

    def wrap(self, availableWidth, availableHeight):
        """
        returns draw- width and height

        convenience function to adapt your image
        to the available Space that is available
        """
        return self.drawWidth, self.drawHeight

    def drawOn(self, canv, x, y, _sW=0):
        """
        translates Bounding Box and scales the given canvas
        """
        if _sW > 0 and hasattr(self, 'hAlign'):
            a = self.hAlign
            if a in ('CENTER', 'CENTRE', TA_CENTER):
                x += 0.5*_sW
            elif a in ('RIGHT', TA_RIGHT):
                x += _sW
            elif a not in ('LEFT', TA_LEFT):
                raise ValueError("Bad hAlign value " + str(a))

        #xobj_name = makerl(canv._doc, self.xobj)
        xobj_name = makerl(canv, self.xobj)

        xscale = self.drawWidth/self._w
        yscale = self.drawHeight/self._h

        x -= self.xobj.BBox[0] * xscale
        y -= self.xobj.BBox[1] * yscale

        canv.saveState()
        canv.translate(x, y)
        canv.scale(xscale, yscale)
        canv.doForm(xobj_name)
        canv.restoreState()


def draw_paragraph(text, pdf, cw, ch, poi, centered_vertically=False):
    P = Paragraph(text)
    w,h = P.wrap(cw, ch)
    if not centered_vertically:
        poi[1] -= h
    else:
        poi[1] -= h+int((ch-h)/2)
    P.drawOn(pdf, poi[0], poi[1])
    poi[0] += w
    return poi

def draw_plotly(fig, pdf, cw, ch, poi, rescale=False, centerv=True, centerh=True,
                rasterize = False, png_scaling=4):
    w = fig.layout.width
    if w is None:
        w = cw
        if rescale:
            fig.update_layout(width=w)
    h = fig.layout.height
    if h is None:
        h = ch
        if rescale:
            fig.update_layout(height=h)
    if centerh:
        poi[0] += int((cw-w)/2)
    if centerv:
        poi[1] -= h+int((ch-h)/2)
    else:
        poi[1] -= h
    if rasterize:
        img = ImageReader(BytesIO(fig.to_image(format='png', scale=png_scaling)))
        pdf.drawImage(img, poi[0], poi[1], width=w, height=h)
    else:
        img = PdfImage(BytesIO(fig.to_image(format='pdf')), width=w, height=h)
        img.drawOn(pdf, poi[0], poi[1])
    poi[0] += w
    return poi


def draw_bytes(b, pdf, cw, ch, poi):
    poi[1] -= ch
    pdf.drawImage(ImageReader(BytesIO(b)), poi[0], poi[1])
    poi[0] += cw
    return poi


def draw_content(pdf, content, width=595, height=842, border=40, spacing=7, png_scaling=4, verbose=False):
    content_width = width-(2*border)
    content_height = height-(2*border)
    pointer = [border, height-border]
    fontsize = pdf._fontsize
    if type(content) == str:
        draw_paragraph(content, pdf, content_width, content_height, pointer, centered_vertically=True)
    elif str(type(content)) == "<class 'plotly.graph_objs._figure.Figure'>":
        draw_plotly(content, pdf, content_width, content_height, pointer, png_scaling=png_scaling)
    elif type(content) == bytes:
        draw_bytes(content, pdf, content_width, content_height, pointer)
    elif type(content) == list:

        # initialize left content-height
        ch = content_height

        for ri, row in enumerate(content):

            if verbose:
                print('row', ri, 'left space:', content_width, ch, 'pointer:', pointer)

            # draw row
            if type(row) == str:
                pointer = draw_paragraph(row, pdf, content_width, ch, pointer)
            elif str(type(row)) == "<class 'plotly.graph_objs._figure.Figure'>":
                pointer = draw_plotly(row, pdf, content_width, ch, pointer,
                                      centerv=False, png_scaling=png_scaling)
            elif type(row) == bytes:
                pointer = draw_bytes(row, pdf, content_width, ch, pointer)
            elif type(row) == list:

                # initialize left content-width and store pointer height, initialize max height
                cw = content_width
                poih = pointer[1]
                poihmax = 0

                for ii, i in enumerate(row):

                    if verbose:
                        print('item', ii, 'left space:', cw, ch, 'pointer:', pointer)

                    # draw item
                    if type(i) == str:
                        pointer = draw_paragraph(i, pdf, cw, ch, pointer)
                    elif str(type(i)) == "<class 'plotly.graph_objs._figure.Figure'>":
                        pointer = draw_plotly(i, pdf, cw, ch, pointer,
                                              centerv=False, centerh=False, png_scaling=png_scaling)
                    elif type(i) == bytes:
                        pointer = draw_bytes(i, pdf, cw, ch if poihmax == 0 else poihmax, pointer)
                    else:
                        pointer = draw_paragraph("Unknown content of {} passed.".format(str(type(i))), pdf,
                                       cw, ch, pointer)

                    # check max height, reset height pointer for next item, raise overflow warning,
                    # add spacing and recalculate leftover content width
                    poihmax = max(poihmax, poih-pointer[1])
                    pointer[1] = poih
                    if pointer[0] > content_width+border:
                        print("-------\nWarning\nContent is overflowing to the right of the page.\n-------")
                    pointer[0] += spacing
                    cw = content_width-(pointer[0]+border)

                # adjust pointer to maximum height for next row to be drawn
                pointer[1] = poih-poihmax

            else:
                pointer = draw_paragraph("Unknown content of {} passed.".format(str(type(row))), pdf,
                               cw, ch, pointer)
            # reset width pointer for next row, raise overflow warning,
            # add spacing and recalculate leftover content height
            pointer[0] = border
            if pointer[1] < border:
                print("-------\nWarning\nContent is overflowing at the bottom of the page.\n-------")
            pointer[1] -= spacing
            ch = pointer[1]-border

    else:
        draw_paragraph("Unknown content of {} passed.".format(str(type(content))), pdf,
                       content_width, content_height, pointer, centered_vertically=True)
