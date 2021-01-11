def resetboard():
    # 1: white, -1: black, 0: none
    return list([[0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 1,-1, 0, 0, 0],
                 [0, 0, 0,-1, 1, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0]])

#brd: board, color: 1 or -1, r: row, c: column
def legalCheck(brd, color, r, c): #returns array of number of disks that can be flipped in each direction. use sum(legalcheck(...)) to check legal moves
    #check each 8 directions
    rightCheck = 0
    if c < 6:
        flippableDisks = 0
        for i in range(c + 1, 8):
            if brd[r][i] == color:
                rightCheck = flippableDisks
                break
            elif brd[r][i] == -color:
                flippableDisks += 1    
            elif brd[r][i] == 0:
                break

    leftCheck = 0
    if c > 1:
        flippableDisks = 0
        for i in range(c - 1, -1, -1):
            if brd[r][i] == color:
                leftCheck = flippableDisks
                break
            elif brd[r][i] == -color:
                flippableDisks += 1    
            elif brd[r][i] == 0:
                break
    
    downCheck = 0
    if r < 6:
        flippableDisks = 0
        for i in range(r + 1, 8):
            if brd[i][c] == color:
                downCheck = flippableDisks
                break
            elif brd[i][c] == -color:
                flippableDisks += 1    
            elif brd[i][c] == 0:
                break

    upCheck = 0
    if r > 1:
        flippableDisks = 0
        for i in range(r - 1, -1, -1):
            if brd[i][c] == color:
                upCheck = flippableDisks
                break
            elif brd[i][c] == -color:
                flippableDisks += 1    
            elif brd[i][c] == 0:
                break

    #diagnals calculate slightly differently, but essentially the same
    uprightCheck = 0
    if c < 6 and r > 1:
        flippableDisks = 0
        for i in range(1, min(8 - c, r + 1)):
            if brd[r - i][c + i] == color:
                uprightCheck = flippableDisks
                break
            elif brd[r - i][c + i] == -color:
                flippableDisks += 1    
            elif brd[r - i][c + i] == 0:
                break

    upleftCheck = 0
    if c > 1 and r > 1:
        flippableDisks = 0
        for i in range(1, min(c + 1, r + 1)):
            if brd[r - i][c - i] == color:
                upleftCheck = flippableDisks
                break
            elif brd[r - i][c - i] == -color:
                flippableDisks += 1    
            elif brd[r - i][c - i] == 0:
                break

    downleftCheck = 0
    if c > 1 and r < 6:
        flippableDisks = 0
        for i in range(1, min(c + 1, 8 - r)):
            if brd[r + i][c - i] == color:
                downleftCheck = flippableDisks
                break
            elif brd[r + i][c - i] == -color:
                flippableDisks += 1    
            elif brd[r + i][c - i] == 0:
                break

    downrightCheck = 0
    if c < 6 and r < 6:
        flippableDisks = 0
        for i in range(1, min(8 - c, 8 - r)):
            if brd[r + i][c + i] == color:
                downrightCheck = flippableDisks
                break
            elif brd[r + i][c + i] == -color:
                flippableDisks += 1    
            elif brd[r + i][c + i] == 0:
                break

    legal = [rightCheck, leftCheck, downCheck, upCheck, uprightCheck, upleftCheck, downleftCheck, downrightCheck]
    return legal

def legalPlacements(brd, color): #returns array of legal placements
    output = []
    for i in range(8):
        for j in range(8):
            if sum(legalCheck(brd, color, i, j)) > 0:
                output.append([i, j])
    return output

def placeDisk(brd, color, r, c):
    brd[r][c] = color
    flippableDisksDirection = legalCheck(brd, color, r, c)

    if flippableDisksDirection[0] > 0:
        for i in range(c + 1, 8):
            if brd[r][i] == color:
                break
            elif brd[r][i] == -color:
                brd[r][i] = color

    if flippableDisksDirection[1] > 0:
        for i in range(c - 1, -1, -1):
            if brd[r][i] == color:
                break
            elif brd[r][i] == -color:
                brd[r][i] = color 

    if flippableDisksDirection[2] > 0:
        for i in range(r + 1, 8):
            if brd[i][c] == color:
                break
            elif brd[i][c] == -color:
                brd[i][c] = color

    if flippableDisksDirection[3] > 0:
        for i in range(r - 1, -1, -1):
            if brd[i][c] == color:
                break
            elif brd[i][c] == -color:
                brd[i][c] = color

    if flippableDisksDirection[4] > 0:
        for i in range(1, min(8 - c, r + 1)):
            if brd[r - i][c + i] == color:
                break
            elif brd[r - i][c + i] == -color:
                brd[r - i][c + i] = color

    if flippableDisksDirection[5] > 0:
        for i in range(1, min(c + 1, r + 1)):
            if brd[r - i][c - i] == color:
                break
            elif brd[r - i][c - i] == -color:
                brd[r - i][c - i] = color

    if flippableDisksDirection[6] > 0:
        for i in range(1, min(c + 1, 8 - r)):
            if brd[r + i][c - i] == color:
                break
            elif brd[r + i][c - i] == -color:
                brd[r + i][c - i] = color

    if flippableDisksDirection[7] > 0:
        for i in range(1, min(8 - c, 8 - r)):
            if brd[r + i][c + i] == color:
                break
            elif brd[r + i][c + i] == -color:
                brd[r + i][c + i] = color

    return brd



#main game board
board = resetboard()
board = placeDisk(board, 1, 0, 0)