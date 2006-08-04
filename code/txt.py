"""text and font classes, helps everyone to text"""

import pygame, pygame.font, gfx
from mysysfont import SysFont

FontPool = {}



def initialize():
    pygame.font.init()
    return 1


class Font:
    def __init__(self, name, size, bold=0, italic=0):
        val = name, size
        if FontPool.has_key(val):
            font = FontPool[val]
        else:
            font = SysFont(name, size, bold, italic)
            FontPool[val] = font
        self.font = font

    def render(self, *args):
        return self.font.render(*args)

    def set_underline(self, *args):
        return self.font.set_underline(*args)

    def set_italic(self, *args):
        return self.font.set_italic(*args)

    def set_bold(self, *args):
        return self.font.set_bold(*args)

    def text(self, color, text, center=None, pos='center'):
        bgd = 0, 0, 0
        if text is None: text = ' '
        try:
            if gfx.surface.get_bytesize()>1:
                img = self.font.render(text, 1, color, bgd)
                img.set_colorkey(bgd, pygame.RLEACCEL)
            else:
                img = self.font.render(text, 0, color)
            img = img.convert()
        except (pygame.error, TypeError):
            #print 'TEXTFAILED', text
            img = pygame.Surface((10, 10))
            #raise
        r = img.get_rect()
        if center: setattr(r, pos, center)
        return [img, r]


    def textbox(self, color, text, width, bgcolor, topmargin=6):
        sidemargin = 6
        lines = []
        for line in text.splitlines():
            cursize = 0
            build = ''
            for word in line.split():
                wordspace = word + ' '
                size = self.font.size(wordspace)[0]
                if size + cursize >= width:
                    lines.append(build)
                    cursize = size
                    build = wordspace
                else:
                    build += wordspace
                    cursize += size
            lines.append(build)

        lineheight = self.font.get_linesize()
        height = len(lines) * lineheight + topmargin + sidemargin
        width += sidemargin * 2
        surf = pygame.Surface((width, height))
        surf.fill(bgcolor)
        pos = topmargin
        for line in lines:
            if line:
                img = self.font.render(line, 1, color, bgcolor)
                img.set_colorkey(bgcolor)
                surf.blit(img, (sidemargin, pos))
            pos += lineheight

        return surf
