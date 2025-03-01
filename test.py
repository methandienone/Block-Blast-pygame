import math
import random
from pygame import mixer
import pygame


class COLORZ:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vec = (x, y, z)
        self.mag = math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def normalise(self):
        if self.mag == 0:
            return self.copy()
        return COLORZ(self.x / self.mag, self.y / self.mag, self.z / self.mag)

    def copy(self):
        return COLORZ(self.x, self.y, self.z)

    def dot(self, drugoy_cvet):
        return self.x * drugoy_cvet.x + self.y * drugoy_cvet.y + self.z * drugoy_cvet.z

    def multiply_vec(self, drugoy_cvet):
        return COLORZ(self.x * drugoy_cvet.x, self.y * drugoy_cvet.y,
                      self.z * drugoy_cvet.z)

    def clamp(self, niz_granica=(0, 0, 0), verh_granica=(255, 255, 255)):
        return COLORZ(min(max(self.x, niz_granica[0]), verh_granica[0]),
                      min(max(self.y, niz_granica[1]), verh_granica[1]),
                      min(max(self.z, niz_granica[2]), verh_granica[2]))

    def set(self, x=False, y=False, z=False):
        if x:
            self.x = x
        if y:
            self.y = y
        if z:
            self.z = z

    def update_val(self):
        self.vec = (self.x, self.y, self.z)
        self.mag = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def __add__(self, drugoy_color):
        return COLORZ(self.x + drugoy_color.x, self.y + drugoy_color.y,
                      self.z + drugoy_color.z)

    def __sub__(self, drugoy_color):
        return COLORZ(self.x - drugoy_color.x, self.y - drugoy_color.y,
                      self.z - drugoy_color.z)

    def __mul__(self, mag):
        return COLORZ(self.x * mag, self.y * mag, self.z * mag)

    def __truediv__(self, mag):
        return COLORZ(self.x / mag, self.y / mag, self.z / mag)

    def __neg__(self):
        return COLORZ(-self.x, -self.y, -self.z)

    def __abs__(self):
        return COLORZ(abs(self.x), abs(self.y), abs(self.z))

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vec = (x, y)
        self.mag = math.sqrt(x ** 2 + y ** 2)

    def normalise(self):
        if self.mag == 0:
            return self.copy()
        return Vec2(self.x / self.mag, self.y / self.mag)

    def copy(self):
        return Vec2(self.x, self.y)

    def dot(self, cvet):
        return self.x * cvet.x + self.y * cvet.y

    def multiply_vec(self, cvet):
        return Vec2(self.x * cvet.x, self.y * cvet.y)

    def clamp(self, niz_granica=(0, 0, 0), verh_granica=(255, 255, 255)):
        return Vec2(min(max(self.x, niz_granica[0]), verh_granica[0]),
                    min(max(self.y, niz_granica[1]), verh_granica[1]))

    def set(self, x=False, y=False):
        if x:
            self.x = x
        if y:
            self.y = y

    def update_val(self):
        self.vec = (self.x, self.y)
        self.mag = math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, otherVec3):
        return Vec2(self.x + otherVec3.x, self.y + otherVec3.y)

    def __sub__(self, otherVec3):
        return Vec2(self.x - otherVec3.x, self.y - otherVec3.y)

    def __mul__(self, mag):
        return Vec2(self.x * mag, self.y * mag)

    def __truediv__(self, mag):
        return Vec2(self.x / mag, self.y / mag)

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __abs__(self):
        return Vec2(abs(self.x), abs(self.y))

    def __str__(self):
        return f"{self.x} {self.y}"

    def __mod__(self, n):
        return Vec2(self.x % n, self.y % n)

    def __floordiv__(self, n):
        return Vec2(self.x // n, self.y // n)


# f = open("settings.txt", "r")
# settingZ = f.read()
# f.close()
settingZ = '10,10\n50'

fileSettings = settingZ.split("\n")
thing1 = fileSettings[0].split(",")

boardDim = Vec2(int(thing1[0]), int(thing1[1]))
blockSize = int(fileSettings[1])

score = 0
bestScore = 0

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((boardDim * blockSize + Vec2(0, 150)).vec)
clock = pygame.time.Clock()

pointScoreArray = (0, 100, 250, 400, 800, 2000, 3000, 4000, 5000, 6000)
colorArray = (COLORZ(255, 100, 100),
              COLORZ(100, 255, 100),
              COLORZ(100, 100, 255),
              COLORZ(255, 255, 100),
              COLORZ(255, 100, 255),
              COLORZ(100, 255, 255),
              COLORZ(100, 100, 100),
              )


def drawBlock(color, pos, borderSize=4, screen=screen):
    pygame.draw.rect(screen, color.vec,
                     pygame.Rect(pos.x, pos.y, blockSize, blockSize))
    pygame.draw.rect(screen, (color * 0.8).vec,
                     pygame.Rect(pos.x + borderSize, pos.y + borderSize,
                                 blockSize - borderSize * 2,
                                 blockSize - borderSize * 2))


def drawBackground():
    backgroundSurface = pygame.Surface((boardDim * blockSize).vec)
    for x in range(boardDim.x):
        for y in range(boardDim.y):
            drawBlock(COLORZ(20, 20, 20), Vec2(x, y) * blockSize,
                      screen=backgroundSurface)

    return backgroundSurface


class doska:
    def __init__(self, izmereniya_doski):
        self.dim = izmereniya_doski
        self.predstavlenie_doski = [[0 for x in range(self.dim.x)] for y in
                                    range(self.dim.y)]
        self.cvetnaya_doska = [[COLORZ(0, 0, 0) for x in range(self.dim.x)] for y
                               in range(self.dim.y)]

    def kraya_doski(self, pos):
        return pos.x >= 0 and pos.x < self.dim.x and pos.y >= 0 and pos.y < self.dim.y

    def zbroz(self):
        self.predstavlenie_doski = [[0 for x in range(self.dim.x)] for y in
                                    range(self.dim.y)]

    def mozhno_postavit_block(self, block, pos):

        relCoord = Vec2(0, 0)
        for row in block.blockShape:

            relCoord.x = 0

            for item in row:

                globalPos = pos + relCoord

                if item == 1:
                    if not self.kraya_doski(globalPos):
                        return False

                    if self.predstavlenie_doski[globalPos.y][globalPos.x] == 1:
                        return False

                relCoord += Vec2(1, 0)

            relCoord += Vec2(0, 1)

        return True

    def postavit_block(self, block, blockColor, pos):
        if self.mozhno_postavit_block(block, pos):

            for y in range(pos.y, pos.y + block.height):
                for x in range(pos.x, pos.x + block.width):
                    blockType = block.blockShape[y - pos.y][x - pos.x]

                    if blockType != 0:
                        self.predstavlenie_doski[y][x] = blockType
                        self.cvetnaya_doska[y][x] = blockColor
            return True

        return False

    def draw(self):
        screen.blit(background, (0, 0))

        for y in range(self.dim.y):
            for x in range(self.dim.x):
                if self.predstavlenie_doski[y][x] == 1:
                    drawBlock(self.cvetnaya_doska[y][x], Vec2(x, y) * blockSize)

    def clearRows(self):
        global score
        clearRowArray = []
        clearColArray = []

        # rows
        for x in range(self.dim.y):
            if sum(self.predstavlenie_doski[x]) == self.dim.x:
                clearRowArray.append(x)

        for y in range(self.dim.x):

            tempSum = 0
            for x in range(self.dim.y):
                tempSum += self.predstavlenie_doski[x][y]

            if tempSum == self.dim.y:
                clearColArray.append(y)

        for row in clearRowArray:
            self.predstavlenie_doski[row] = [0 for i in range(self.dim.x)]

        for col in clearColArray:
            for y in range(self.dim.y):
                self.predstavlenie_doski[y][col] = 0

        score += pointScoreArray[len(clearColArray) + len(clearRowArray)]

    def isGameOver(self, possibleBlocks):
        for block in possibleBlocks:

            canPlace = False
            for i in range(self.dim.x * self.dim.y):
                x = i % self.dim.x
                y = i // self.dim.y
                if self.mozhno_postavit_block(block, Vec2(x, y)):
                    canPlace = True
                    break

            if canPlace:
                return False

        return True


class Block:
    def __init__(self, blockShape):
        self.blockShape = blockShape
        self.width = len(self.blockShape[0])
        self.height = len(self.blockShape)


board = doska(boardDim)


class peretaskivanie_blokov:
    def __init__(self, blockShape, ogPos):
        self.blockShape = blockShape.blockShape
        self.blockObject = blockShape
        self.pos = ogPos
        self.prevValidPos = ogPos
        self.color = random.choice(colorArray)

    def draw(self, currBlock, pos):
        if currBlock != self:
            x_count = 0
            y_count = 0
            tempSurface = pygame.Surface((500, 500), pygame.SRCALPHA)
            for row in self.blockShape:
                x_count = 0
                for item in row:
                    blockVec = Vec2(x_count, y_count) * blockSize
                    if item != 0:
                        drawBlock(self.color, blockVec, screen=tempSurface)
                    x_count += 1

                y_count += 1
            newSurface = pygame.transform.scale_by(tempSurface, 0.5)

            screen.blit(newSurface, self.pos.vec)
            return

        cannotFit = True
        if pos.y + (
                len(self.blockShape) - 1) * blockSize >= boardDim.y * blockSize or board.mozhno_postavit_block(
            self.blockObject, pos // blockSize):
            self.prevValidPos = pos
            cannotFit = False

        x_count = 0
        y_count = 0
        for row in self.blockShape:
            x_count = 0
            for item in row:
                blockVec = pos + Vec2(x_count, y_count) * blockSize
                if item != 0:
                    if pos.y + (
                            len(self.blockShape) - 1) * blockSize < boardDim.y * blockSize and not cannotFit:
                        drawBlock(self.color, blockVec // blockSize * blockSize)
                    else:
                        drawBlock(self.color, blockVec)
                x_count += 1

            y_count += 1

    def isHoverOver(self, mousePos):
        scaleFactor = 0.5
        return mousePos.x > self.pos.x and mousePos.x < self.pos.x + len(
            self.blockShape[
                0]) * blockSize * scaleFactor and mousePos.y > self.pos.y and mousePos.y < self.pos.y + len(
            self.blockShape) * blockSize * scaleFactor


running = True
background = drawBackground()

blockTypeArray = [
    [[1, 1],
     [1, 1]],
    [[1, 1, 1],
     [1, 1, 1]],
    [[1, 1],
     [1, 1],
     [1, 1]],
    [[1, 0],
     [1, 0],
     [1, 1]],
    [[1, 1],
     [0, 1],
     [0, 1]],
    [[1, 1],
     [1, 0],
     [1, 0]],
    [[0, 1],
     [0, 1],
     [1, 1]],
    [[1, 0, 0],
     [1, 1, 1]],
    [[1, 1, 1],
     [0, 0, 1]],
    [[0, 0, 1],
     [1, 1, 1]],
    [[1, 1, 1],
     [1, 0, 0]],
    [[1, 0],
     [1, 1],
     [1, 0]],
    [[0, 1],
     [1, 1],
     [0, 1]],
    [[0, 1, 0],
     [1, 1, 1]],
    [[1, 1, 1],
     [0, 1, 0]],
    [[1, 1, 1, 1]],
    [[1],
     [1],
     [1],
     [1]],
    [[1, 1, 1, 1, 1]],
    [[1],
     [1],
     [1],
     [1],
     [1]],
    [[1, 1, 1],
     [1, 1, 1],
     [1, 1, 1]],
    [[1, 0],
     [1, 1],
     [0, 1]],
    [[0, 1],
     [1, 1],
     [1, 0]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]],
    [[0, 0, 1],
     [0, 0, 1],
     [1, 1, 1]],
    [[1, 1, 1],
     [1, 0, 0],
     [1, 0, 0]],
    [[1, 1, 1],
     [0, 0, 1],
     [0, 0, 1]],
    [[1, 0, 0],
     [1, 0, 0],
     [1, 1, 1]],
]

blockTypes = [Block(blockType) for blockType in blockTypeArray]
music = pygame.mixer.music.load('Monkeys-Spinning-Monkeys(chosic.com).mp3')
pygame.mixer.music.play(-1)
currBlock = None

blockChoiceArray = [peretaskivanie_blokov(random.choice(blockTypes),
                                          Vec2(boardDim.x / 3 * i * blockSize + 50,
                                               boardDim.y * blockSize + 50)) for i in
                    range(3)]

font = pygame.font.Font("ofont.ru_Uncage.ttf", 15)
fontSmol = pygame.font.Font("ofont.ru_Uncage.ttf", 15)
fontFat = pygame.font.Font("ofont.ru_Uncage.ttf", 25)

lost = False

while running:

    keys = pygame.key.get_pressed()
    mousePos = Vec2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if keys[pygame.K_ESCAPE]:
        running = False

    screen.fill((30, 30, 30))

    if not lost:
        if pygame.mouse.get_pressed()[0]:
            for block in blockChoiceArray:
                if block.isHoverOver(mousePos):
                    currBlock = block
                    break
        else:
            if currBlock != None:
                canPlace = board.postavit_block(currBlock.blockObject,
                                                currBlock.color,
                                                currBlock.prevValidPos // blockSize)

                if canPlace:
                    blockChoiceArray.remove(currBlock)
            currBlock = None

        board.clearRows()

        if len(blockChoiceArray) == 0:
            blockChoiceArray = [
                peretaskivanie_blokov(random.choice(blockTypes),
                                      Vec2(boardDim.x / 3 * i * blockSize + 50,
                                           boardDim.y * blockSize + 50))
                for i in range(3)]

        if board.isGameOver(blockChoiceArray):
            lost = True

    board.draw()
    for block in blockChoiceArray:
        block.draw(currBlock, mousePos)

    if score > bestScore:
        bestScore = score

    fontText = font.render(f"СЧЕТ:{score}", 1, (255, 255, 255))
    fontText2 = fontSmol.render(f"ЛУЧШИЙ СЧЕТ:{score}", 1, (255, 255, 255))

    if not lost:
        screen.blit(fontText, (0, 0))
        screen.blit(fontText2, (0, 25))
    else:
        fontText = fontFat.render("КАК МОЖНО БЫЛО ПРОИГРАТЬ?", 1, (255, 255, 255))
        fontText2 = font.render(f"ТВОЙ ПОЗОРНЫЙ СЧЕТ:{score} СТРЕМИСЬ К ЭТОМУ:{bestScore}", 1,
                                (255, 255, 255))
        fontText3 = font.render(f'РАЗРАБЫ: АЛЕКСЕЙ МИХАЙЛЮК И МИХАИЛ УЛАНОВ', 1, (255, 255, 255))
        fontText4 = font.render(
            f'ПИСАТЬ РАЗРАБАМ ПОЖЕЛАНИЯ СЮДА: @clawgmd', 1,
            (255, 255, 255))

        fontSize1 = fontText.get_size()
        fontSize2 = fontText2.get_size()

        screen.blit(fontText,
                    ((boardDim.x * blockSize - fontSize1[0]) / 2,
                     (boardDim.y * blockSize - fontSize1[1]) / 2))
        screen.blit(fontText2,
                    ((boardDim.x * blockSize - fontSize2[0]) / 2,
                     (boardDim.y * blockSize - fontSize2[1]) / 2 + 50))
        screen.blit(fontText3,
                    ((boardDim.x * blockSize - fontSize2[0]) / 2,
                     (boardDim.y * blockSize - fontSize2[1]) / 2 + 100))
        screen.blit(fontText4,
                    ((boardDim.x * blockSize - fontSize2[0]) / 2,
                     (boardDim.y * blockSize - fontSize2[1]) / 2 + 150))

        if keys[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            lost = False
            blockChoiceArray = [peretaskivanie_blokov(random.choice(blockTypes),
                                                      Vec2(
                                                          boardDim.x / 3 * i * blockSize + 50,
                                                          boardDim.y * blockSize + 50)) for
                                i
                                in range(3)]
            currBlock = None
            board.zbroz()
            score = 0

    pygame.display.flip()
    clock.tick(60)
