import pygame
import time
import pygame_gui
import hashlib
pygame.init()




global board
board = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]

clock = pygame.time.Clock()
screen_width = 1800
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
font = pygame.font.SysFont("Arial",50,bold=True)
global dark_mode
dark_mode = False
run = True
clicked = False
MouseTempNumber = 0
MANAGER = pygame_gui.UIManager((1800, 1000))
usernameInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (900, 50)), manager=MANAGER, object_id="#username_text_entry")
passwordInput = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 400), (900, 50)), manager=MANAGER, object_id="#password_text_entry")
active = False
file = open("Default_boards.txt", "r")
read = file.readlines()
file_text = []
for line_in_file in read:
    if line_in_file[-1] == "\n":
        file_text.append(line_in_file[:-1])
    else:
        file_text.append(line_in_file)
#reads the text file "Default_boards.txt" and 
# stores it in the variable "file_text"

def next_empty(board_temp):
    for i in range(0,9):
        for j in range(0,9):
            if board_temp[i][j] == 0:
                return (i,j)
#finds the next empty slot in the grid and returns the coordinates of it          


    return False
def check_if_valid(board_temp, number, coords):
    
    for i in range(0,9):
        if board_temp[coords[0]][i] == number and coords[1] != i:
            return False
    
    for i in range(0,9):
        if board_temp[i][coords[1]] == number and coords[0] != i:
            return False
    
    x = (coords[1] // 3)*3
    y = (coords[0] // 3)*3
    for i in range(y, y + 3):
        for j in range(x, x + 3):
            if board_temp[i][j] == number and (i,j) != coords:
                return False
    return True    
#This function uses the rules of sudoku to check if the number stored in "number"
#can be legally placed in the coordinates "coords" on the board stored in "board_temp"


def solve(board_temp):
    if next_empty(board_temp) == False:
        return True
    else:
        row, col = next_empty(board_temp)
        
    for i in range(1,10):
        if check_if_valid(board_temp, i, (row, col)):
            board_temp[row][col] = i
            if solve(board_temp) == True:
                return True
            else:
                board_temp[row][col] = 0
            
    return False
#This function uses the two other functions to find the 
#next empty tile in the board and to place the first number
#that can be legally placed there into that tile.
#The function then uses reccursion to call itself and repeat
#the process for the next empty tile until the grid is full.






#checks if the board has a possible solution
def tile_solveable(board_temp, number, coords):
    if number == 0:
        return True


    for i in range(0,9):
        if board_temp[coords[0]][i] == number and coords[1] != i:
            return False
    
    for i in range(0,9):
        if board_temp[i][coords[1]] == number and coords[0] != i:
            return False
    
    x = (coords[1] // 3)*3
    y = (coords[0] // 3)*3
    for i in range(y, y + 3):
        for j in range(x, x + 3):
            if board_temp[i][j] == number and (i,j) != coords:
                return False
    return True    
#Checks to see if a tile is solveable or not


def board_solveable():
    for i in range(0,9):
        for j in range(0,9):
            m = board[i]
            n = m[j]
            if n == " ":
                n = 0
            n = int(n)
            m[j] = n
            board[i] = m
            temp = board[i]
            if tile_solveable(board, temp[j], (i,j)) == False:
                return False
    return True  
#checks to see if the board is solveable


#######################################################################################################################################################################
#button = pygame.Rect(TOPLEFTx, TOPLEFTy, WIDTH, HEIGHT)



class super_draw:
    
    def __init__(self,x,y,width,height,dark):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dark = dark
#Initialises 5 parameters 
class button(super_draw):

    def __init__(self,x,y,text,width,height,dark):
        super().__init__(x,y,width,height,dark)
        self.text = str(text)

        

        if self.dark == False:
            self.button_col = (255, 255, 255)
            self.hover_col = (242, 109, 7)
            self.click_col = (50, 150, 255)
            self.text_col = (0, 0, 0)
        else:
            self.button_col = (0, 0, 0)
            self.hover_col = (50, 180, 55)
            self.click_col = (180, 50, 50)
            self.text_col = (255, 255, 255)

        if self.text == 0:
            self.text = ""



    def draw(self):
        global clicked
        action = False

        pos = pygame.mouse.get_pos() #get position of mouse

        button_rect = pygame.Rect(self.x, self.y, self.width, self.height) #create pygame rectangle for button

        if button_rect.collidepoint(pos): #checks if the mouse is hovering over the button
            if pygame.mouse.get_pressed()[0] == 1: #checks if left mouse button has been clicked
                clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect) #draws the buttton without text as the click colour
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True: #this line prevents the button from being repeatedly clicked if the user holds left click
                clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect) #draws button without text as the hover colour
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)  #draws button without text
        text_img = font.render(self.text, True, self.text_col) #turns text into an img
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 20)) #pastes the text_img into the button 
        return action #returns "True" if the button has been clicked and "False" if the button hasn't been clicked

class line(super_draw):
    def __init__(self, x, y, width, height, bold, dark):
        super().__init__(x,y,width,height,dark)
        self.bold = bold

        if self.dark:
            self.line_col = (255,255,255)
        else:
            self.line_col = (0,0,0)
    
    
    def draw_line(self):
        pygame.draw.line(screen, self.line_col, (self.x, self.y), (self.x +self.width, self.y + self.height), self.bold)
        #draws the line with the values stored to that object



#Changes the number on the grid that has been clicked into the number in the variable "MouseTempNumber"




def board_UI(dark_mode):
    for i in range(0,9):
        for j in range(0,9):
            m = board[i]
            n = m[j]
            if n == 0:
                n = ""
            y = (i*105)+25
            x = (j*105)+25
            exec(f"board_button_{i}_{j} = button(x,y,n,102,102, dark_mode)")
            exec(f"change_number(j,i,MouseTempNumber,board_button_{i}_{j})")
#Uses the class "button" to generate 81 buttons in a 9X9 board. 
#It uses the built in "exec()" function to create and call 81 variables, because 
# without the function it would need to create 81 buttons one line at a time.
#This board is a copy of the "board" array 
#It then calls the function "change_number" for every button in the board

def change_number(x,y,number,varName):
    global board
    temp = varName.draw()
    if temp:
        m = board[y]
        m[x] = number
        board[y] = m
        for i in range(0,9):
            for j in range(0,9):
                m = board[i]
                n = m[j]
                exec(f"board_button_{i}_{j} = button(j,i,n,100,100, dark_mode)")
        return board
#Changes the number in tile with coords (x,y) in the board to the value in "number"



def one_to_nine_UI(dark_mode):
    n=0
    for i in range(0,3):
        for j in range(0,3):
            n +=1
            b = (105*i) + 27
            a = (105*j) + 1100
            exec(f"one_to_nine_{i}_{j} = button(a,b,n,100,100, dark_mode)")
            exec(f"mouse_number(one_to_nine_{i}_{j})")
#Uses the class "button" to generate 9 buttons, which are labled 1-9 and are in a 3X3 grid
            

def mouse_number(varName):
    global MouseTempNumber
    temp = varName.draw()
    if temp:
        MouseTempNumber = varName.text
#Uses the function "draw()" to change the variable "MouseTempNumber" 
# into the number that the user clicked on in the 3X3 grid


def clear_board(board):
    board = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]
    return board
        

def clear_board_button_generator(dark_mode):
    global board
    clear_board_button = button(1095, 485, "Clear Board", 315, 100, dark_mode)
    if clear_board_button.draw():
        board = [[0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0],
                 [0,0,0,0,0,0,0,0,0]]
        return board
#Creates one button with the text "Clear Board" which changes the 2D array "board"
# back to an empty board (all 0s)
    

def clear_tile_button_generator(dark_mode):
    global MouseTempNumber
    clear_tile_button = button(1095, 610, "Clear Tile", 315, 94, dark_mode)
    if clear_tile_button.draw():
        MouseTempNumber = 0
#Creates a button called "Clear Tile" which changes the variable "MouseTempNumber" to 0 when clicked
#This allows the user to then click any button on the board and change the number in it to 0
        
def board_solve_button_generator(dark_mode):
    import pygame
    pygame.init()
    board_solve_button = button(1100, 360, "Solve", 315, 100, dark_mode)
    temp = board_solve_button.draw()
    if temp:
        temp_solvable = (board_solveable())
        if temp_solvable:
            solve(board)
        else:
            for i in range(0,9):
                for j in range(0,9):
                    a = board[i]
                    b = a[j]
                    if tile_solveable(board,b,(i,j)) == False:
                        temp_Rect = pygame.Rect((j*105)+25, (i*105)+25, 102, 102)
                        pygame.draw.rect(screen, (240, 20, 20), temp_Rect)
                        clear_board_button_generator(dark_mode)
                        clear_tile_button_generator(dark_mode)
                        choose_board_buttons(dark_mode)
                        images(dark_mode)
                        board_solve_button_generator(dark_mode)
                        grid_lines(dark_mode)
                        if dark_mode:
                            temp_img = font.render(str(b), True, (255,255,255))
                        else:
                            temp_img = font.render(str(b), True, (0,0,0))
                        temp_len = temp_img.get_width()
                        screen.blit(temp_img, ((j*105)+20 + int(56) - int(temp_len / 2), (i*105) + 45))
            pygame.display.update()
            time.sleep(2)
#creates a button with the text "Solve" in it which, when clicked, checls to see if the board is solveable. 
#If the board is solveable, it will be solve. If the board is not solveable then the tiles that are breaking 
#the sudoku rules will be highlighted red for 2 seconds.
            
def dark_mode_button_generator(dark_mode):
    dark_mode_button = button(1675, 27, "", 100, 100, dark_mode)
    if dark_mode_button.draw():
        if dark_mode:
            dark_mode = False
        else:
            dark_mode = True
    return dark_mode
#Draws a button with no text which changes the boolean variable "dark_mode" 
# whenever it is clicked, this causes almost all of the colours on the screen 
# to change


def grid_lines(dark_mode):
    for i in range(0,10):
        if i == 0 or i == 3 or i == 6 or i == 9:
            j = 8
        else:
            j = 4
        exec(f"horizontal_grid_line_{i} = line(21, (i*105)+23, 950, 0, j, dark_mode)")
        exec(f"horizontal_grid_line_{i}.draw_line()")
        exec(f"vertical_grid_line_{i} = line((i*105)+23, 21, 0, 950, j, dark_mode)")
        exec(f"vertical_grid_line_{i}.draw_line()")
    for i in range(0,4):
        exec(f"horizontal_number_line_{i} = line(1094, (i*105)+23, 320, 0, 6, dark_mode)")
        exec(f"horizontal_number_line_{i}.draw_line()")
        exec(f"vertical_number_line_{i} = line((i*105)+1096, 23, 0, 315, 6, dark_mode)")
        exec(f"vertical_number_line_{i}.draw_line()")
    for i in range(0,3):
        exec(f"horizontal_button_line_{i} = line(1096, (i*125)+356, 315, 0, 6, dark_mode)")
        exec(f"horizontal_button_line_{i}.draw_line()")
        exec(f"horizontal_button2_line_{i} = line(1096, (i*125)+456, 315, 0, 6, dark_mode)")
        exec(f"horizontal_button2_line_{i}.draw_line()")
        exec(f"vertical_button_line_{i} = line(1096, (i*125)+354, 0, 105, 6, dark_mode)")
        exec(f"vertical_button_line_{i}.draw_line()")
        exec(f"vertical_button2_line_{i} = line(1412, (i*125)+354, 0, 105, 6, dark_mode)")
        exec(f"vertical_button2_line_{i}.draw_line()")
    for i in range(0,4):
        for j in range(0,4):
            exec(f"Difficulty_line_vertical_{i}_{j} = line(1451 + (i*105), 183 + (150*j), 0, 105, 6, dark_mode)")
            exec(f"Difficulty_line_vertical_{i}_{j}.draw_line()")
        exec(f"Difficulty_line_horizontal1_{i} = line(1449 , 183 + (150*i), 320, 0, 6, dark_mode)")
        exec(f"Difficulty_line_horizontal1_{i}.draw_line()")
        exec(f"Difficulty_line_horizontal2_{i} = line(1449 , 285 + (150*i), 320, 0, 6, dark_mode)")
        exec(f"Difficulty_line_horizontal2_{i}.draw_line()")
             


def images(dark_mode):
    light_mode_image = pygame.image.load("Light_Mode.png")
    light_mode_image = pygame.transform.scale(light_mode_image, (100, 100))
    dark_mode_image = pygame.image.load("Dark_Mode.png")
    dark_mode_image = pygame.transform.scale(dark_mode_image, (100, 100))
    if dark_mode:
        screen.blit(dark_mode_image, (1675, 27))
    else:
        screen.blit(light_mode_image, (1675, 27))
#Pastes a png image from the PC files over the dark mode button.
#The image pasted on the screen is dependant on the value stored
#in the variable "dark_mode"



def choose_board_buttons(dark):
    for i in range(1,4):
        for j in range(0,4):
             if j == 0:
                temp_letter = "E"
                temp_letter = str(temp_letter) + str(i)
                exec(f"Default_board{temp_letter} = button(1350 + (105*i), 187 + (150*j), temp_letter, 100, 100, dark)")
                exec(f"Default_board{temp_letter}.button_col = (0, 255, 0)")
             elif j == 1:
                temp_letter = "M"
                temp_letter = str(temp_letter) + str(i)
                exec(f"Default_board{temp_letter} = button(1350 + (105*i), 187 + (150*j), temp_letter, 100, 100, dark)")
                exec(f"Default_board{temp_letter}.button_col = (255, 255, 0)")
             elif j == 2:
                temp_letter = "H"
                temp_letter = str(temp_letter) + str(i)
                exec(f"Default_board{temp_letter} = button(1350 + (105*i), 187 + (150*j), temp_letter, 100, 100, dark)")
                exec(f"Default_board{temp_letter}.button_col = (255, 128, 0)")
             else:   
                temp_letter = "I"
                temp_letter = str(temp_letter) + str(i)
                exec(f"Default_board{temp_letter} = button(1350 + (105*i), 187 + (150*j), temp_letter, 100, 100, dark)")
                exec(f"Default_board{temp_letter}.button_col = (255, 0, 0)")
             exec(f"Default_board{temp_letter}.hover_col = (0, 255, 255)")
             exec(f"Default_board{temp_letter}.text_col = (0, 0, 0)")
             exec(f"choose_board_clicked(Default_board{temp_letter})")
#draws 12 buttons which have different colours and text.






def choose_board_clicked(button_name):
    if button_name.draw():
        temp = str(button_name.text[0]).lower()
        temp1 = str(button_name.text[-1])
        temp = temp + temp1
        for i in file_text:
            if temp == i[:2]:
                temp_board = (i[3:])
                global board
                board = []
                for b in range(0,9):
                    j = b+1
                    temp_line = list(temp_board[b*10:(j*10)-1])
                    board.append(temp_line)
#if the button is clicked, the board changes to the corresponding 
# stored board from the variable file_text

def hash_password(password):
    password_bytes = password.encode("utf-8")
    hash_object = hashlib.sha256(password_bytes)
    return hash_object.hexdigest()



def check_login(username, password):
    users_file = open("Users.txt", "r")
    read_file = users_file.readlines()
    users_text = []
    for line_in_file in read_file:
        if line_in_file[-1] == "\n":
            users_text.append(line_in_file[:-1])
        else:
            users_text.append(line_in_file)
    usernames = []
    passwords = []

    for i in users_text:
        temp = 0
        for j in i:
            if j == ",":
                usernames.append(i[:temp])
                passwords.append(i[temp+1:])
            temp +=1
    temp1 = 0
    for i in usernames:
        if i == username:
            if passwords[temp1] == hash_password(password):
                return True
            return "P"
        temp1 +=1
    return "U"


def logIn(dark_mode):
    pygame.display.set_caption("Log In")
    username = ""
    password = ""
    temp_text = ""
    while True:
        if dark_mode:
            screen.fill((84, 82, 82))
        else:
            screen.fill((210, 200, 200))
        username, password = get_user_name(dark_mode, username, password)
        dark_mode = dark_mode_button_generator(dark_mode)
        images(dark_mode)
        if dark_mode:
            text_img = font.render("Username", True, (255, 255, 255))
            text_img2 = font.render("Password", True, (255, 255, 255))
        else:
            text_img = font.render("Username", True, (0, 0, 0))
            text_img2 = font.render("Password", True, (0, 0, 0))
        screen.blit(text_img, (350, 225))
        screen.blit(text_img2, (350, 350))
        confirm_log_in = button(1000, 500, "Confirm", 300, 100, dark_mode)
        cant_log_in = button(1000, 600, "Back", 300, 100, dark_mode)
        if cant_log_in.draw():
            sign_in_menu(dark_mode)
        if confirm_log_in.draw():
            if check_login(username, password) == True:
                temp_text = ("Welcome back " + str(username))
                if dark_mode:
                    screen.fill((84, 82, 82))
                    text_img = font.render(temp_text, True, (255, 255, 255))
                else:
                    screen.fill((210, 200, 200))
                    text_img = font.render(temp_text, True, (0, 0, 0))
                screen.blit(text_img, (400, 200))
                pygame.display.update()
                time.sleep(1.5)
                sudoku_game(dark_mode)
            elif check_login(username, password) == "U":
                if dark_mode:
                    screen.fill((84, 82, 82))
                    text_img = font.render("Username not found", True, (255, 255, 255))
                else:
                    screen.fill((210, 200, 200))
                    text_img = font.render("Username not found", True, (0, 0, 0))
            else:
                if dark_mode:
                    screen.fill((84, 82, 82))
                    text_img = font.render("Password incorrect", True, (255, 255, 255))
                else:
                    screen.fill((210, 200, 200))
                    text_img = font.render("Password incorrect", True, (0, 0, 0))
            screen.blit(text_img, (400, 200))
            pygame.display.update()
            time.sleep(1.5)
        pygame.display.update()
        clock.tick(60)



def signUp(dark_mode):
   
    pygame.display.set_caption("Sign Up")
    username = ""
    password = ""
    while True:
        if dark_mode:
            screen.fill((84, 82, 82))
        else:
            screen.fill((210, 200, 200))
        username, password = get_user_name(dark_mode, username, password)
        dark_mode = dark_mode_button_generator(dark_mode)
        images(dark_mode)
        if dark_mode:
            text_img = font.render("Username", True, (255, 255, 255))
            text_img2 = font.render("Password", True, (255, 255, 255))
        else:
            text_img = font.render("Username", True, (0, 0, 0))
            text_img2 = font.render("Password", True, (0, 0, 0))
        screen.blit(text_img, (350, 225))
        screen.blit(text_img2, (350, 350))
        confirm_sign_in = button(1000, 500, "Confirm", 300, 100, dark_mode)
        if confirm_sign_in.draw():
            if check_if_username_free(username):
                add_user_to_file(username, password)
                if dark_mode:
                    screen.fill((84, 82, 82))
                    text_img = font.render("New User Added", True, (255, 255, 255))
                else:
                    screen.fill((210, 200, 200))
                    text_img = font.render("New User Added", True, (0, 0, 0))
                screen.blit(text_img, (400, 200))
                pygame.display.update()
                time.sleep(1.5)
                sudoku_game(dark_mode)
            else:
                if dark_mode:
                    screen.fill((84, 82, 82))
                    text_img = font.render("Username already exists, please use another", True, (255, 255, 255))
                else:
                    screen.fill((210, 200, 200))
                    text_img = font.render("Username already exists, please use another", True, (0, 0, 0))
            screen.blit(text_img, (400, 200))
            pygame.display.update()
            time.sleep(1.5)
        pygame.display.update()
        clock.tick(60)
    


def get_user_name(dark_mode, username, password):
    UserName = username
    Password = password
    UI_refresh_rate = clock.tick(60)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#username_text_entry":
            UserName = event.text
            print(UserName)
        elif event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED and event.ui_object_id == "#password_text_entry":
            Password = event.text
            print(Password)
        MANAGER.process_events(event)
    MANAGER.update(UI_refresh_rate)
    MANAGER.draw_ui(screen)
    return UserName, Password

def add_user_to_file(username, password):
    hashed_password = hash_password(password)
    users_file = open("Users.txt", "a")
    text_for_file =("\n"+str(username) +"," + str(hashed_password))
    users_file.write((text_for_file))

def check_if_username_free(username):
    users_file = open("Users.txt", "r")
    read_file = users_file.readlines()
    users_text = []
    for line_in_file in read_file:
        if line_in_file[-1] == "\n":
            users_text.append(line_in_file[:-1])
        else:
            users_text.append(line_in_file)
    usernames = []
    for i in users_text:
        temp = 0
        for j in i:
            if j == ",":
                usernames.append(i[:temp])
            temp +=1
    for i in usernames:
        if i == username:
            return False
    return True




def sign_in_menu(dark_mode):
    run = True
    while run:
        signUpButton = button(800, 400, "Sign up", 300, 100, dark_mode)    
        logInButton = button(800, 250, "Log In", 300, 100, dark_mode)
        if dark_mode:
            screen.fill((84, 82, 82))
        else:
            screen.fill((210, 200, 200))
        dark_mode = dark_mode_button_generator(dark_mode)
        images(dark_mode)
        if signUpButton.draw():
            signUp(dark_mode)
            quit()
            i = 1
        if logInButton.draw():
            logIn(dark_mode)
            quit()
            i = 1
        clock.tick(60)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit
def sudoku_game(dark_mode):
    pygame.display.set_caption("Sudoku Puzzle")
    run = True
    while run:
        if dark_mode:
            screen.fill((84, 82, 82))
        else:
            screen.fill((210, 200, 200))
        board_UI(dark_mode)
        one_to_nine_UI(dark_mode)
        board_solve_button_generator(dark_mode)
        clear_board_button_generator(dark_mode)
        clear_tile_button_generator(dark_mode)
        choose_board_buttons(dark_mode)
        grid_lines(dark_mode)
        dark_mode = dark_mode_button_generator(dark_mode)
        images(dark_mode)
        clock.tick(60)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
        pygame.display.update()

    pygame.quit()   


sign_in_menu(dark_mode)
