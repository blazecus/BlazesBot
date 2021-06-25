class dotsandboxes:

    player1 = ""
    player2 = ""
    current_player = player1
    
    vertical_lines = []
    horizontal_lines = []
    owned = []

    player1_score = 0
    player2_score = 0

    done = False
    tie = False
    winning_score = 0

    width = 0
    height = 0

    def __init__(self, player1_id, player2_id, widthnew, heightnew):
        self.width = widthnew
        self.height = heightnew

        self.player1 = player1_id
        self.player2 = player2_id
        self.current_player = self.player1

        #self.horizontal_lines = [[False] * (self.width-1)] * self.height
        #self.vertical_lines = [[False] * self.width] * (self.height - 1)
        #python sucks and this creates shallow copies so gg
        #time for stupid for loops
        self.horizontal_lines = [[False] * (self.width-1) for i in range(self.height)]
        self.vertical_lines = [[False] * self.width for i in range(self.height - 1)]

        self.owned = [[" " for i in range(self.width - 1)] for j in range(self.height - 1)]

        self.player1_score = 0
        self.player2_score = 0
        self.done = False
        self.tie = False
        self.winning_score = 0

    def check_valid(self,x1, y1, x2, y2):
        if(x1 < 1 or x1 > self.width or x2 < 1 or x2 > self.width or y1 < 1 or y1 > self.height or y2 < 1 or y2 > self.height):
            return False
        
        if((x1 != x2 and y1 != y2) or (x1 == x2 and y1 == y2)):
            return False

        if(abs(x1-x2) > 1 or abs(y1-y2) > 1):
            return False
        
        if(x1 != x2):
            if(x1 < x2):
                return not self.horizontal_lines[y1-1][x1-1]
            else:
                return not self.horizontal_lines[y1-1][x2-1]
        else:
            if(y1 < y2):
                return not self.vertical_lines[y1-1][x1-1]
            else:
                return not self.vertical_lines[y2-1][x1-1]
        
    def check_box(self, x, y):
        return self.horizontal_lines[y][x] and self.horizontal_lines[y+1][x] and self.vertical_lines[y][x] and self.vertical_lines[y][x+1]
    
    def boxes_to_check(self, horizontal, x, y):
        t = []
        if(horizontal):
            if(y < self.height - 1):
                t += [(x, y)]
            if(y > 0):
                t += [(x, y-1)]
        else:
            if(x < self.width - 1):
                t += [(x, y)]
            if(x > 0):
                t += [(x-1,y)]
        
        return t

    def place_line(self,x1,y1,x2,y2):
        if(x1 != x2):
            if(x1 < x2):
                self.horizontal_lines[y1-1][x1-1] = True
                px = x1-1
            else:
                self.horizontal_lines[y1-1][x2-1] = True
                px = x2-1

            for i in self.boxes_to_check(True, px, y1-1):
                if(self.check_box(i[0], i[1])):
                    print(i[0])
                    print(i[1])
                    if(self.current_player == self.player1):
                        self.player1_score += 1
                        self.owned[i[1]][i[0]] = "1"
                    else:
                        self.player2_score += 1
                        self.owned[i[1]][i[0]] = "2"

                    if(self.player1_score + self.player2_score == (self.width-1) * (self.height-1)):
                        if(self.player1_score == self.player2_score):
                            self.tie = True
                        self.winning_score = self.player1_score
                        if(self.player2_score > self.winning_score):
                            self.winning_score = self.player2_score
                        self.done = True
                    return
        else:
            if(y1 < y2):
                self.vertical_lines[y1-1][x1-1] = True
                py = y1-1
            else:
                self.vertical_lines[y2-1][x1-1] = True
                py = y2-1

            for i in self.boxes_to_check(False, x1-1, py):
                if(self.check_box(i[0], i[1])):
                    if(self.current_player == self.player1):
                        self.player1_score += 1
                        self.owned[i[1]][i[0]] = "1"
                    else:
                        self.player2_score += 1
                        self.owned[i[1]][i[0]] = "2"

                    if(self.player1_score + self.player2_score == (self.width-1) * (self.height-1)):
                        if(self.player1_score == self.player2_score):
                            self.tie = True
                        if(self.player2_score > self.winning_score):
                            self.winning_score = self.player2_score
                        self.done = True
                    return

        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        
        
    def print_board(self):
        tot_string = "```"
        for i in range(self.width):
            tot_string +=  "   " + str(i+1)
        tot_string += "\n"

        for i in range(len(self.horizontal_lines)):
            tot_string += str(i+1) + "  "
            for j in self.horizontal_lines[i]:
                if j:
                    tot_string += "*---"
                else:
                    tot_string += "*   "
            tot_string += "*\n"
            
            if i < len(self.vertical_lines):
                tot_string += "   "
                for j in range(len(self.vertical_lines[i]) - 1):
                    if self.vertical_lines[i][j]:
                        tot_string += "| " + self.owned[i][j] + " "
                    else:
                        tot_string += "  " + self.owned[i][j] + " "
                if(self.vertical_lines[i][-1]):
                    tot_string += "|\n"
                else:
                    tot_string += " \n"
        tot_string += "```"
        return tot_string

    