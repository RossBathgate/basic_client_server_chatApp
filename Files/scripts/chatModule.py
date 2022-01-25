import textwrap
import pygame
window = pygame.display.set_mode((800,1000))

class msg():
    #width must be less than 600...

    def __init__(self,y,fill,text,sender,msgId,alignRight):
        self.x = 0
        self.y = y
        self.fill = fill
        self.text = textwrap.wrap(text, width = 26) #returns a list of lines
        self.fontSize = 25
        self.sender = sender
        self.msgId = msgId
        self.alignRight = alignRight

        #---calculateDimensions---
        #r is the border radius
        r = self.fontSize

        #determine width and height of the message box
        lineLengths = [len(t) for t in self.text]
        lineLengths.append(len(self.sender))
        self.h = r+self.fontSize*(len(self.text)+2) #note the +2 for the sender's name and gap
        #self.w = r+self.fontSize*max(lineLengths)
        self.w = int(r+(self.fontSize//1.4*max(lineLengths))) #1.4 included to manually alter the spacing.  Before, it was too wide.

        #alignment --> left or right...
        w, h = pygame.display.get_surface().get_size()
        if self.alignRight:
            self.x = w-self.w

    def draw(self):
        #r is the border radius
        r = self.fontSize

        #corner circles
        pygame.draw.circle(window, self.fill, (self.x+r, self.y+r), r)
        pygame.draw.circle(window, self.fill,(self.x + self.w - r, self.y + r),r)
        pygame.draw.circle(window, self.fill,(self.x+r, self.y+self.h-r),r)
        pygame.draw.circle(window, self.fill,(self.x+self.w-r, self.y+self.h-r),r)

        #edge rects
        pygame.draw.rect(window, self.fill, (self.x + r, self.y, self.w - 2*r, r))
        pygame.draw.rect(window, self.fill, (self.x+r, self.y + self.h - r, self.w - 2*r, r))
        pygame.draw.rect(window, self.fill, (self.x, self.y+r, r, self.h - 2*r))
        pygame.draw.rect(window, self.fill, (self.x+self.w-r, self.y+r, r, self.h - 2*r))

        #centre rect
        pygame.draw.rect(window, self.fill, (self.x + r, self.y + r, self.w - 2*r, self.h - 2*r))

        #display sender text
        senderTextPos = (self.x+r, self.y+r)
        font = pygame.font.SysFont("Sans Serif",30)
        text = font.render(self.sender,False, (0,0,0))
        window.blit(text, senderTextPos)

        #display message contents
        for i in range(len(self.text)):
            textPos = (self.x + r, self.y + r + (self.fontSize * (i+1))) #Note hte i+1 to include the sender line
            font = pygame.font.SysFont("Arial",self.fontSize)
            text = font.render(self.text[i], False, (0,0,0))
            window.blit(text, textPos)


class button():
    def __init__(self,x,y,w,h,fill,text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.fill = fill
        self.text = text

    def clicked(self,mousePos):
        mX,mY = mousePos
        return mX in range(self.x,self.x+self.w+1) and mY in range(self.y, self.y+self.h+1)

    def draw(self):
        #r is the border radius
        r = 15

        #corner circles
        pygame.draw.circle(window, self.fill, (self.x+r, self.y+r), r)
        pygame.draw.circle(window, self.fill,(self.x + self.w - r, self.y + r),r)
        pygame.draw.circle(window, self.fill,(self.x+r, self.y+self.h-r),r)
        pygame.draw.circle(window, self.fill,(self.x+self.w-r, self.y+self.h-r),r)

        #edge rects
        pygame.draw.rect(window, self.fill, (self.x + r, self.y, self.w - 2*r, r))
        pygame.draw.rect(window, self.fill, (self.x+r, self.y + self.h - r, self.w - 2*r, r))
        pygame.draw.rect(window, self.fill, (self.x, self.y+r, r, self.h - 2*r))
        pygame.draw.rect(window, self.fill, (self.x+self.w-r, self.y+r, r, self.h - 2*r))

        #centre rect
        pygame.draw.rect(window, self.fill, (self.x + r, self.y + r, self.w - 2*r, self.h - 2*r))

        #display text
        textPos = (self.x+r, self.y+self.w//2.5)
        font = pygame.font.SysFont("Sans Serif",35)
        text = font.render(self.text,False, (0,0,0))
        window.blit(text, textPos)


class textbox():
    def __init__(self,x,y,w,h,placeholder):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.placeholder = placeholder
        self.text = self.placeholder

    def display_text(self,MAX_DISPLAY_LINES):
        if self.text == "":
            self.text = self.text = self.placeholder
        lines = textwrap.wrap(self.text, width = 33)
        line_height = self.h // MAX_DISPLAY_LINES
        #fontSize = line_height
        fontSize = 25

        #if there is less than the most number of displayable lines, display all, else display the max number of them
        if len(lines) <= MAX_DISPLAY_LINES:
            for i in range(len(lines)):
                line = lines[i]

                #display current entered text
                textPos = (self.x, self.y + (i*line_height))
                font = pygame.font.SysFont("Arial",fontSize)
                text = font.render(line, False, (0,0,0))
                window.blit(text, textPos)

        else:
            #there are more than [MAX_DISPLAY_LINES] lines
            counter = 0

            for i in range(len(lines)):
                if i > len(lines) - MAX_DISPLAY_LINES - 1:
                    line = lines[i]

                    #display current entered text
                    textPos = (self.x, self.y + (counter*line_height))
                    font = pygame.font.SysFont("Arial",fontSize)
                    text = font.render(line, False, (0,0,0))
                    window.blit(text, textPos)

                    counter += 1
