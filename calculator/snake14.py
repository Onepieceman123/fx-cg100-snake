from casioplot import *
from random import randint
from sgfx14 import *
# SNAKE v1.4 for fx-CG100 - made by Bilal Taha
# Needs sgfx14.py on the calculator too. Arrows move, OK pauses, AC quits.
# DELAY: raise it if every speed is too fast, lower it if too slow.
COLS=32;ROWS=15;DELAY=2500;POLLS=4;BUG_LIFE=30
UP=14;DOWN=34;LEFT=23;RIGHT=25;OK=24;EXE=95
DIRS={UP:(0,-1),DOWN:(0,1),LEFT:(-1,0),RIGHT:(1,0),62:(0,-1),82:(0,1),71:(-1,0),73:(1,0)}
MODES=["Classic","Wrap","Maze"]
START=[(6,10),(5,10),(4,10),(3,10)]
ACH=[("Snack Time","Eat 10 apples in one game"),("Big Snake","Reach length 30"),
("Bug Hunter","Catch 3 bugs in one game"),("Speed Demon","Reach speed 9"),
("Explorer","Reach level 4"),("Century","Score 100 points"),
("Legend","Score 500 points"),("Maze Runner","Reach level 3 in Maze")]
GOT=[False]*8
STATS={"games":0,"apples":0,"bugs":0,"longest":0}
def check(g):
  t=[g["apples"]>=10,g["len"]>=30,g["bugs"]>=3,g["spd"]>=9,g["lvl"]>=4,
     g["score"]>=100,g["score"]>=500,g["mode"]==2 and g["lvl"]>=3]
  new=[]
  for i in range(8):
    if t[i] and not GOT[i]:
      GOT[i]=True;new.append(ACH[i][0])
  return new
def bar(st,col):
  draw_string(2,0,"Score "+str(st[0]),col,"small")
  draw_string(95,0,"Best "+str(st[1]),col,"small")
  draw_string(180,0,"Spd "+str(st[2]),col,"small")
  draw_string(240,0,"Lv "+str(st[3]),col,"small")
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
def overlay(lines,dl,snake,d,cols,food,walls,bc):
  panel(92,64,200,64)
  for (s,y,col,size) in lines:
    draw_string(192-len(s)*(9 if size=="large" else 4),y,s,col,size)
  show_screen();wait(dl)
  ground(92,64,200,64);items(snake,d,cols,food,walls,bc);show_screen()
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
  lvl=1;walls=maze(1) if mode==2 else set()
  snake=list(START);d=(1,0);cols=mkcols(3)
  food=place(snake,walls,())
  bc=None;bt=0;bw=0;bbase=5*spd;foods=0;score=0;bugs=0;tg=[];mv=0;maxlen=4
  st=[score,best,spd,lvl]
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
      g={"apples":foods,"len":maxlen,"bugs":bugs,"spd":st[2],"lvl":lvl,"score":score,"mode":mode}
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
    if score!=st[0]:
      bar(st,BAND);st[0]=score;bar(st,WHITE)
    if grow and foods%10==0:
      bar(st,BAND);lvl+=1;st[3]=lvl
      if st[2]<9:
        st[2]+=1
      bar(st,WHITE);untongue(tg);tg=[]
      if bc is not None:
        cellg(bc);bc=None;box(300,3,80,6,BAND)
      overlay([("LEVEL "+str(lvl),72,BAND,"large"),("Speed "+str(st[2])+" - food = "+str(st[2])+" pts",106,TXT,"small")],
              DELAY*40,snake,d,cols,food,walls,None)
      if mode==2:
        walls=maze(lvl);snake=list(START);d=(1,0);queue=[];cols=mkcols(3)
        food=place(snake,walls,());board(snake,d,cols,food,walls,st)
        last=ready()
        if DIRS[last] not in ((-1,0),(1,0)):
          queue=[DIRS[last]]
      else:
        last=getkey()
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
def menu_text(mode,spd,sk,row,best):
  t=[("> " if r==row else "  ")+["Mode   <  "+MODES[mode]+"  >","Speed  <  "+str(spd)+"  >","Skin   <  "+SKINS[sk][0]+"  >"][r] for r in range(3)]
  t.append("Food = "+str(spd)+" pts     Best: "+str(best[mode]))
  return t
def title(mode,spd,sk,best):
  skin(sk);GRASS[0]=False;menubg()
  draw_string(286,40,"by Bilal Taha",GREY,"small")
  frame(56,52,272,92,LINE);frame(58,54,268,88,BAND)
  draw_string(28,152,"Up/Down choose  Left/Right change",GREY,"small")
  draw_string(30,166,"EXE = start",BAND,"medium");draw_string(230,166,"OK = stats",BAND,"medium")
  row=0;old=None
  while True:
    txt=menu_text(mode,spd,sk,row,best)
    if txt!=old:
      for r in range(4):
        sz="medium" if r<3 else "small"
        if old:
          draw_string(68,60+r*21,old[r],WHITE,sz)
        draw_string(68,60+r*21,txt[r],(RED if r==row else TXT) if r<3 else GREY,sz)
      if old is None or old[2]!=txt[2]:
        skin(sk);logo();draw_snake([(x,3) for x in range(19,11,-1)],(1,0),mkcols(7));apple((22,3))
      show_screen();old=txt
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
      wait_release(k);stats(best);return title(mode,spd,sk,best)
    elif k==EXE:
      wait_release(k);skin(sk);return mode,spd,sk
def stats(best):
  clear_screen();band();draw_string(150,0,"STATS",WHITE,"small")
  S=STATS
  draw_string(10,18,"Games "+str(S["games"])+"   Apples "+str(S["apples"])+"   Bugs "+str(S["bugs"]),TXT,"small")
  draw_string(10,32,"Longest "+str(S["longest"])+"   Best  C:"+str(best[0])+"  W:"+str(best[1])+"  M:"+str(best[2]),TXT,"small")
  draw_string(10,50,"ACHIEVEMENTS  "+str(sum(GOT))+"/8",BAND,"medium")
  for i in range(8):
    draw_string(10,68+i*12,("[x] " if GOT[i] else "[ ] ")+ACH[i][0]+" - "+ACH[i][1],GOLD if GOT[i] else GREY,"small")
  draw_string(10,164,"Note: stats reset when you quit or power off!",RED,"small")
  draw_string(10,178,"made by Bilal Taha",GREY,"small");draw_string(280,178,"OK = back",BAND,"small")
  show_screen()
  while getkey()!=OK:
    pass
  wait_release(OK)
def game_over(score,best,newbest,g,new):
  panel(62,36,260,124)
  shadow(116,44,"GAME OVER",RED)
  draw_string(90,78,"Score "+str(score)+"    Best "+str(best),TXT,"medium")
  draw_string(90,98,"Length "+str(g["len"])+"   Level "+str(g["lvl"])+"   Bugs "+str(g["bugs"]),GREY,"small")
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
