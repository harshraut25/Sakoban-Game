from flask import *
from collections import deque
import json


data = [] #list containing row as each item
nrows = 0 #length of longest row
px = py = 0 #player position
sdata = "" #source data
ddata = "" #destinaton data

#initialize the data
def init(board):
    global data, nrows, sdata, ddata, px, py
    data = [_f for _f in board.split('x') if _f]
    nrows = max(len(r) for r in data)
 
    maps = {' ':' ', '.': '.', '@':' ', '#':'#', '$':' '}
    mapd = {' ':' ', '.': ' ', '@':'@', '#':' ', '$':'*'}
 
    for r, row in enumerate(data):
        for c, ch in enumerate(row):
            sdata += maps[ch]
            ddata += mapd[ch]
            if ch == '@':
                px = c
                py = r

#to make next move
def push(x, y, dx, dy, data):

    #if player or box runs into wall then dont make move
    if sdata[(y+2*dy) * nrows + x+2*dx] == '#' or \
       data[(y+2*dy) * nrows + x+2*dx] != ' ':
        return None
    #else make move
    data2 = list(data)
    data2[y * nrows + x] = ' ' #set current player position to blank
    data2[(y+dy) * nrows + x+dx] = '@' #move player to next position
    data2[(y+2*dy) * nrows + x+2*dx] = '*' #move box to goal
    return "".join(data2)
 
def is_solved(data):
    for i in range(len(data)):
        if (sdata[i] == '.') != (data[i] == '*'):
            return False
    return True
 
def solve():
    open = deque([(ddata, "", px, py)])
    visited = set([ddata])
    dirs = ((0, -1, 'u', 'U'), ( 1, 0, 'r', 'R'),  #possilble directions and their corresponding coordinates
            (0,  1, 'd', 'D'), (-1, 0, 'l', 'L'))
 
    lnrows = nrows
    while open:
        cur, csol, x, y = open.popleft()
 
        for di in dirs: #exploring the result of each direction
            temp = cur
            dx, dy = di[0], di[1]
 
            if temp[(y+dy) * lnrows + x+dx] == '*': #checks if the move places a block to goal
                temp = push(x, y, dx, dy, temp) #make the move
                if temp and temp not in visited:
                    if is_solved(temp):
                        #if solved then add the last move to soultion and return
                        return csol + di[3]
                    #if not solved then append new state to explore
                    open.append((temp, csol + di[3], x+dx, y+dy))
                    visited.add(temp)
            else:
                #if player runs into a wall then ignore
                if sdata[(y+dy) * lnrows + x+dx] == '#' or \
                   temp[(y+dy) * lnrows + x+dx] != ' ':
                    continue
                
                #else if player does legal move then perform it
                data2 = list(temp)
                data2[y * lnrows + x] = ' '
                data2[(y+dy) * lnrows + x+dx] = '@'
                temp = "".join(data2)
 
                if temp not in visited:
                    if is_solved(temp):
                        return csol + di[2]
                    open.append((temp, csol + di[2], x+dx, y+dy))
                    visited.add(temp)
 
    return "No solution"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/index' ,methods=['GET','POST'])
def index_page():
    name=request.form["username"]
    return redirect(url_for("user",usr=name))

@app.route('/<usr>')
def user(usr):
    return render_template('index.html',usr=usr)



@app.route('/processUserInfo/<string:userInfo>', methods=['POST'])
def processUserInfo(userInfo):
    userInfo=json.loads(userInfo)
    level=userInfo['level']
    level=level.replace('w','#')

    init(level)
    answer=solve()
    return answer

if (__name__=='__main__'):
    app.run(debug=True)
