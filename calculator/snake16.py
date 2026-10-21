from casioplot import *
from random import randint
from sgfx16 import *
# SNAKE v1.6 for fx-CG100 - made by Bilal Taha
# Needs sgfx16.py on the calculator too. Arrows move, OK pauses, AC quits.
# DELAY: raise it if every speed is too fast, lower it if too slow.
COLS=32;ROWS=15;DELAY=2500;POLLS=4;BUG_LIFE=30
UP=14;DOWN=34;LEFT=23;RIGHT=25;OK=24;EXE=95
DIRS={UP:(0,-1),DOWN:(0,1),LEFT:(-1,0),RIGHT:(1,0),62:(0,-1),82:(0,1),71:(-1,0),73:(1,0)}
MODES=["Classic","Wrap","Maze"]
DESC=["Walls kill you","Go through the walls","Dodge the stone walls"]
START=[(6,10),(5,10),(4,10),(3,10)]
ACH=[("Snack Time","10 apples in a game"),("Big Snake","Reach length 30"),
("Bug Hunter","3 bugs in a game"),("Speed Demon","10 apples at speed 9"),
("Feast","40 apples in a game"),("Century","Score 100"),
("Legend","Score 500"),("Maze Runner","Score 100 in Maze")]
GOT=[False]*8
STATS={"games":0,"apples":0,"bugs":0,"longest":0}
def check(g):
  t=[g["apples"]>=10,g["len"]>=30,g["bugs"]>=3,g["spd"]>=9 and g["apples"]>=10,g["apples"]>=40,
     g["score"]>=100,g["score"]>=500,g["mode"]==2 and g["score"]>=100]
  new=[]
  for i in range(8):
    if t[i] and not GOT[i]:
      GOT[i]=True;new.append(ACH[i][0])
  return new
def bar(st,col):
  draw_string(2,0,"Score "+str(st[0]),col,"small")
  draw_string(95,0,"Best "+str(st[1]),col,"small")
  draw_string(180,0,"Spd "+str(st[2]),col,"small")
  draw_string(240,0,"Apples "+str(st[3]),col,"small")
def maze(n):
  w=set();k=(n-1)%4
  if k==0:
    for x in range(8,24):
      w.add((x,4));w.add((x,12))
  elif k==1:
    for i in range(6):
      for p in ((2+i,2),(29-i,2),(2+i,14),(29-i,14)):
        w.add(p)
    for i in range(4):
      for p in ((2,2+i),(29,2+i),(2,14-i),(29,14-i)):
        w.add(p)
  elif k==2:
    for (bx,by) in ((8,4),(21,4),(8,11),(21,11),(15,6)):
      for i in range(3):
        for j in range(3):
          w.add((bx+i,by+j))
  else:
    for y in list(range(1,7))+list(range(11,16)):
      w.add((10,y));w.add((21,y))
  return w
def place(snake,walls,others):
  while True:
    p=(randint(0,COLS-1),randint(1,ROWS))
    if p not in snake and p not in walls and p not in others:
      return p
def wait_release(k):
  while getkey()==k:
    pass
def items(snake,d,cols,food,walls,bc):
  for w in walls:
    wall(w)
  apple(food)
  if bc is not None:
    bug(bc)
  draw_snake(snake,d,cols)
def board(snake,d,cols,food,walls,st):
  GRASS[0]=True;band();bar(st,WHITE);field();items(snake,d,cols,food,walls,None);show_screen()
def ready():
  draw_string(290,0,"Arrow = go",(255,220,80),"small");show_screen()
  k=getkey()
  while k not in DIRS:
    k=getkey()
  draw_string(290,0,"Arrow = go",BAND,"small");show_screen()
  return k
def pause(st):
  wait_release(OK);bar(st,BAND)
  draw_string(2,0,"PAUSED - press OK",(255,220,80),"small");show_screen()
  while getkey()!=OK:
    pass
  wait_release(OK)
  draw_string(2,0,"PAUSED - press OK",BAND,"small");bar(st,WHITE);show_screen()
def play(mode,spd,best):
  walls=maze(randint(1,4)) if mode==2 else set()
  snake=list(START);d=(1,0);cols=mkcols(3)
  food=place(snake,walls,())
  bc=None;bt=0;bw=0;bbase=5*spd;foods=0;score=0;bugs=0;tg=[];mv=0;maxlen=4
  st=[score,best,spd,foods]
  board(snake,d,cols,food,walls,st);last=ready()
  queue=[] if DIRS[last] in ((-1,0),(1,0)) else [DIRS[last]]
  while True:
    chunk=DELAY*(10-st[2])//POLLS
    for i in range(POLLS):
      wait(chunk)
      k=getkey()
      if k!=last:
        last=k
        if k==OK:
          pause(st);last=getkey()
        elif k in DIRS:
          nd=DIRS[k];ref=queue[-1] if queue else d
          if nd!=ref and (nd[0]!=-ref[0] or nd[1]!=-ref[1]) and len(queue)<2:
            queue.append(nd)
    if queue:
      d=queue.pop(0)
    mv+=1;h=snake[0];nx=h[0]+d[0];ny=h[1]+d[1]
    if mode==1:
      nx=nx%COLS;ny=(ny-1)%ROWS+1
    n=(nx,ny);grow=n==food;gotbug=bc is not None and n==bc
    rest=snake if grow else snake[:-1]
    untongue(tg);tg=[]
    if nx<0 or nx>=COLS or ny<1 or ny>ROWS or n in rest or n in walls:
      g={"apples":foods,"len":maxlen,"bugs":bugs,"spd":st[2],"score":score,"mode":mode}
      return score,snake,d,cols,g
    if not grow:
      t=snake.pop();cols.pop();cellg(t)
      tail(snake[-1],snake[-2],cols[-1],cols[-2])
    c=nextcol();seg(h,c);snake.insert(0,n);cols.insert(0,c);head(n,d);link(h,n,c)
    if len(snake)>2:
      link(snake[2],h,cols[1],10 if len(snake)>3 else 6)
    maxlen=max(maxlen,len(snake))
    f=(n[0]+d[0],n[1]+d[1])
    if mv%3==0 and f not in walls and f not in snake and f!=food and f!=bc:
      tg=tongue(n,d)
    if bc is not None:
      if gotbug:
        score+=bbase*bt//BUG_LIFE+st[2];bbase=5*st[2];bugs+=1
        box(300,3,80,6,BAND);bc=None
      else:
        bt-=1;w=80*bt//BUG_LIFE
        box(300+w,3,bw-w,6,BAND);bw=w
        cellg(bc)
        if bt<=0:
          bc=None;bbase+=2*st[2]
        else:
          bug(bc,mv%2)
    if grow:
      score+=st[2];foods+=1
      food=place(snake,walls,(bc,));apple(food)
      if foods%5==0 and bc is None:
        bc=place(snake,walls,(food,));bt=BUG_LIFE;bw=80;bug(bc);box(300,3,80,6,BUG)
    elif mv%2==0:
      cellg(food);apple(food,mv%4==0)
    if score!=st[0] or foods!=st[3]:
      bar(st,BAND);st[0]=score;st[3]=foods;bar(st,WHITE)
    show_screen()
def death(snake,d,cols):
  for i in range(3):
    head(snake[0],d,RED,True);show_screen();wait(DELAY*3)
    head(snake[0],d,None,True);show_screen();wait(DELAY*3)
  for i in range(1,len(snake)):
    inner(snake[i],WHITE)
    if i%2==0:
      show_screen()
  show_screen();wait(DELAY*3)
  for i in range(1,len(snake)):
    poof(snake[i],cols[i-1])
    if i%2==0:
      show_screen()
  poof(snake[0],CUR[0]);show_screen()
  ghost(snake[0],6,DELAY*3)
def mrow(r,v,how):
  y=58+r*20;sel=how=="sel"
  col=WHITE if how=="off" else (CUR[0] if sel else TXT)
  box(64,y+3,10,10,WHITE) if not sel else cursor(64,y+3,CUR[0])
  draw_string(84,y,["Mode","Speed","Skin"][r],col,"medium")
  draw_string(244-len(v[r])*4,y,v[r],col,"medium")
  tri(178,y+3,-1,col if sel else WHITE);tri(304,y+3,1,col if sel else WHITE)
def info(mode,spd,best,col):
  t=DESC[mode]+"  -  "+str(spd)+" pts/apple  -  Best "+str(best[mode])
  draw_string(192-len(t)*3,121,t,col,"small")
def skinparts():
  logo();draw_snake([(x,3) for x in range(19,11,-1)],(1,0),mkcols(7));apple((22,3))
  frame(48,52,288,88,LINE);frame(50,54,284,84,CUR[0])
  x=chip(58,146,"EXE",CUR[0]);draw_string(x,146,"Start",TXT,"small")
  x=chip(160,146,"OK",CUR[0]);draw_string(x,146,"Stats",TXT,"small")
  x=chip(256,146,"AC",CUR[0]);draw_string(x,146,"Quit",TXT,"small")
def menu_static():
  GRASS[0]=False;menubg()
  draw_string(286,40,"by Bilal Taha",GREY,"small")
  draw_string(88,166,"Up/Down select    Left/Right change",SOFT,"small")
def title(mode,spd,sk,best):
  skin(sk);menu_static()
  row=0;old=None
  while True:
    v=[MODES[mode],str(spd),SKINS[sk][0]]
    cur=(mode,spd,sk,row)
    if cur!=old:
      if old:
        ov=[MODES[old[0]],str(old[1]),SKINS[old[2]][0]]
        for r in range(3):
          mrow(r,ov,"off")
        info(old[0],old[1],best,WHITE)
      if old is None or old[2]!=sk:
        skin(sk);skinparts()
      for r in range(3):
        mrow(r,v,"sel" if r==row else "on")
      info(mode,spd,best,GREY)
      show_screen();old=cur
    k=getkey()
    if k==UP or k==DOWN:
      row=(row+(1 if k==DOWN else -1))%3;wait_release(k)
    elif k==LEFT or k==RIGHT:
      s=1 if k==RIGHT else -1
      if row==0:
        mode=(mode+s)%3
      elif row==1:
        spd=min(9,max(1,spd+s))
      else:
        sk=(sk+s)%len(SKINS)
      wait_release(k)
    elif k==OK:
      wait_release(k);stats(best);skin(sk);menu_static();old=None
    elif k==EXE:
      wait_release(k);skin(sk);return mode,spd,sk
def stats(best):
  clear_screen();band();h=CUR[0]
  draw_string(170,0,"STATS",WHITE,"small");draw_string(300,0,"by Bilal Taha",(170,200,170),"small")
  S=STATS
  cards=(("Games",S["games"]),("Apples",S["apples"]),("Bugs",S["bugs"]),("Longest",S["longest"]))
  for i in range(4):
    lab=cards[i][0];val=cards[i][1];x=6+i*95
    frame(x,16,88,36,LINE);box(x+1,17,86,3,h)
    v=str(val);draw_string(x+44-len(v)*5,18,v,TXT,"large")
    draw_string(x+44-len(lab)*3,39,lab,GREY,"small")
  t="Best   Classic "+str(best[0])+"    Wrap "+str(best[1])+"    Maze "+str(best[2])
  draw_string(192-len(t)*3,56,t,TXT,"small")
  n=sum(GOT)
  draw_string(6,70,"ACHIEVEMENTS",h,"medium");draw_string(132,72,str(n)+" / 8",GREY,"small")
  frame(190,74,188,8,LINE);box(191,75,186*n//8,6,GOLD)
  for i in range(8):
    x=6+(i%2)*190;y=88+(i//2)*22
    tick(x,y+2,GOT[i])
    draw_string(x+16,y,ACH[i][0],GREEN if GOT[i] else GREY,"small")
    draw_string(x+16,y+10,ACH[i][1],SOFT,"small")
  draw_string(6,178,"Stats reset when you quit or power off",RED,"small")
  x=chip(300,177,"OK",h);draw_string(x,178,"Back",TXT,"small")
  show_screen()
  while getkey()!=OK:
    pass
  wait_release(OK)
def game_over(score,best,newbest,g,new):
  panel(62,36,260,124)
  shadow(116,44,"GAME OVER",RED)
  draw_string(90,78,"Score "+str(score)+"    Best "+str(best),TXT,"medium")
  draw_string(90,98,"Length "+str(g["len"])+"   Apples "+str(g["apples"])+"   Bugs "+str(g["bugs"]),GREY,"small")
  y=112
  if newbest:
    draw_string(155,y,"NEW BEST!",GOLD,"small");y+=11
  for a in new[:2]:
    draw_string(90,y,"Unlocked: "+a,GOLD,"small");y+=11
  draw_string(95,145,"EXE = again    OK = menu",BAND,"small")
  show_screen();last=getkey()
  while True:
    k=getkey()
    if k!=last and (k==EXE or k==OK):
      wait_release(k);return k
    last=k
best=[0,0,0];mode=0;spd=5;sk=0
mode,spd,sk=title(mode,spd,sk,best)
while True:
  s,snake,d,cols,g=play(mode,spd,best[mode])
  death(snake,d,cols)
  STATS["games"]+=1;STATS["apples"]+=g["apples"];STATS["bugs"]+=g["bugs"]
  STATS["longest"]=max(STATS["longest"],g["len"])
  nb=s>best[mode]
  if nb:
    best[mode]=s
  new=check(g)
  if game_over(s,best[mode],nb,g,new)==OK:
    mode,spd,sk=title(mode,spd,sk,best)
