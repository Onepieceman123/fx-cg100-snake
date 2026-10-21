from casioplot import *
from random import randint
# Graphics + skins for snake15.py v1.5 (keep both files on the calculator)
CELL=12
G1=(132,204,82);G2=(116,190,70);GB=(88,158,54);GL=(160,222,110)
BL=((2,3),(3,2),(8,7),(9,6),(5,9));HL=((3,3),(9,7))
BLS=set(BL);GRASS=[True]
BAND=(26,66,30);WHITE=(255,255,255);EYE=(0,0,0);TXT=(0,0,0);GREY=(120,120,120)
RED=(200,0,0);GOLD=(230,170,0);LINE=(70,70,70)
APPLE=(225,35,35);APPLE2=(150,10,10);LEAF=(40,130,30);STEM=(90,55,20)
BUG=(140,50,190);BUG2=(90,20,130)
WALL=(125,125,135);WALL2=(85,85,95);WALL3=(170,170,180)
# name, head, colours (repeat along body), pattern, pupil, accent (None = darker shade)
# patterns: 0 plain, 1 spot, 2 diamond, 3 scales, 4 dots
SKINS=[("Classic",(25,60,160),[(70,120,235)],3,EYE,(40,85,195)),
("Python",(90,60,20),[(205,175,70),(120,85,35)],2,EYE,None),
("Royal",(15,25,95),[(45,75,200),(35,60,175)],2,EYE,(245,195,45)),
("Fire",(160,25,10),[(240,100,20),(250,170,40)],3,(240,200,0),(205,45,10)),
("Ice",(20,70,160),[(110,190,245),(200,232,255)],4,EYE,(40,110,200)),
("Gold",(150,100,0),[(240,190,30),(250,215,90)],2,EYE,(185,125,0)),
("Grape",(70,20,110),[(135,65,205),(165,105,230)],4,EYE,(85,30,145)),
("Pink",(150,15,85),[(235,55,145),(245,105,175)],3,EYE,(255,200,225)),
("Rainbow",(80,30,130),[(230,40,40),(245,140,20),(240,215,20),(60,190,70),(40,120,230),(150,60,210)],1,EYE,None)]
CUR=[None,None,0,EYE,0,None]
def skin(i):
  s=SKINS[i];CUR[0]=s[1];CUR[1]=s[2];CUR[2]=s[3];CUR[3]=s[4];CUR[5]=s[5]
def nextcol():
  CUR[4]+=1
  return CUR[1][CUR[4]%len(CUR[1])]
def mkcols(n):
  p=CUR[1]
  return [p[(n-j)%len(p)] for j in range(n)]
def dk(c):
  return (c[0]*3//5,c[1]*3//5,c[2]*3//5)
def lt(c):
  return (c[0]+(255-c[0])*2//5,c[1]+(255-c[1])*2//5,c[2]+(255-c[2])*2//5)
def box(x0,y0,w,h,col):
  for y in range(y0,y0+h):
    for x in range(x0,x0+w):
      set_pixel(x,y,col)
def frame(x0,y0,w,h,col):
  for x in range(x0,x0+w):
    set_pixel(x,y0,col);set_pixel(x,y0+h-1,col)
  for y in range(y0,y0+h):
    set_pixel(x0,y,col);set_pixel(x0+w-1,y,col)
def gcol(x,y):
  if not GRASS[0]:
    return WHITE
  if (x%12,y%12) in BLS:
    return GB
  if (x%12,y%12) in HL:
    return GL
  return G1 if (x//12+y//12)%2==0 else G2
def ground(x0,y0,w,h):
  for y in range(max(y0,12),y0+h):
    for x in range(x0,x0+w):
      set_pixel(x,y,gcol(x,y))
def cellg(c):
  x=c[0]*CELL;y=c[1]*CELL
  if not GRASS[0]:
    box(x,y,12,12,WHITE);return
  box(x,y,12,12,G1 if (c[0]+c[1])%2==0 else G2)
  for (a,b) in BL:
    set_pixel(x+a,y+b,GB)
  for (a,b) in HL:
    set_pixel(x+a,y+b,GL)
def field(r0=1):
  for cy in range(r0,16):
    for cx in range(32):
      cellg((cx,cy))
def band():
  box(0,0,384,12,BAND)
def inner(c,col):
  box(c[0]*CELL+1,c[1]*CELL+1,10,10,col)
def wall(c):
  x=c[0]*CELL;y=c[1]*CELL
  box(x,y,12,12,WALL2);box(x,y,11,11,WALL3);box(x+1,y+1,10,10,WALL)
  set_pixel(x+4,y+4,WALL2);set_pixel(x+7,y+8,WALL2)
def adj(a,b):
  return abs(a[0]-b[0])+abs(a[1]-b[1])==1
def link(a,b,col,th=10):
  if not adj(a,b):
    return
  o=(CELL-th)//2;e=dk(col) if th==10 else col
  if a[1]==b[1]:
    x=max(a[0],b[0])*CELL-2;y=a[1]*CELL+o
    box(x,y,4,th,e);box(x,y+1,4,th-2,col)
    if th==10:
      box(x,y+1,4,1,lt(col))
  else:
    x=a[0]*CELL+o;y=max(a[1],b[1])*CELL-2
    box(x,y,th,4,e);box(x+1,y,th-2,4,col)
    if th==10:
      box(x+1,y,1,4,lt(col))
def seg(c,col):
  x=c[0]*CELL+1;y=c[1]*CELL+1;d=dk(col);a=CUR[5] or d;p=CUR[2]
  box(x,y,10,10,d);box(x+1,y+1,8,8,col)
  box(x+1,y+1,7,1,lt(col));box(x+1,y+2,1,6,lt(col))
  box(x+2,y+8,7,1,dk(lt(col)) if p else col)
  if p==1:
    box(x+3,y+3,4,4,a);set_pixel(x+3,y+3,lt(a))
  elif p==2:
    for j in range(4):
      w=4 if j in (1,2) else 2
      box(x+5-w//2,y+3+j,w,1,a)
    set_pixel(x+4,y+4,lt(a))
  elif p==3:
    for (u,v) in ((2,3),(6,3),(4,6)):
      set_pixel(x+u,y+v,a);set_pixel(x+u+1,y+v+1,a);set_pixel(x+u+2,y+v,a)
  elif p==4:
    for (u,v) in ((3,3),(6,3),(3,6),(6,6)):
      box(x+u,y+v,2,2,a)
def tail(c,nb,col,ncol=None):
  cellg(c);x=c[0]*CELL;y=c[1]*CELL
  if ncol and adj(c,nb):
    nx=nb[0]*CELL;ny=nb[1]*CELL
    if c[1]==nb[1]:
      gx=nx+11 if nb[0]<c[0] else nx
      for yy in range(ny,ny+12):
        set_pixel(gx,yy,gcol(gx,yy))
      box(nx+10 if nb[0]<c[0] else nx+1,ny+1,1,10,dk(ncol))
    else:
      gy=ny+11 if nb[1]<c[1] else ny
      for xx in range(nx,nx+12):
        set_pixel(xx,gy,gcol(xx,gy))
      box(nx+1,ny+10 if nb[1]<c[1] else ny+1,10,1,dk(ncol))
  if adj(c,nb) and c[1]==nb[1]:
    box(x+3 if nb[0]>c[0] else x+1,y+3,8,6,col)
  elif adj(c,nb):
    box(x+3,y+3 if nb[1]>c[1] else y+1,6,8,col)
  else:
    box(x+3,y+3,6,6,col)
  link(c,nb,col,6);set_pixel(x+5,y+5,dk(col));set_pixel(x+6,y+6,dk(col))
def head(c,d,col=None,dead=False):
  col=col or CUR[0];x=c[0]*CELL+1;y=c[1]*CELL+1
  box(x,y,10,10,col);box(x+1,y+1,8,1,lt(col));box(x+1,y+2,1,7,lt(col))
  for p in ((x,y),(x+9,y),(x,y+9),(x+9,y+9)):
    set_pixel(p[0],p[1],gcol(p[0],p[1]))
  if d[0]!=0:
    ex=x+5 if d[0]>0 else x+1;eyes=((ex,y+1),(ex,y+6))
  else:
    ey=y+5 if d[1]>0 else y+1;eyes=((x+1,ey),(x+6,ey))
  for (a,b) in eyes:
    box(a,b,4,3,WHITE)
    if dead:
      for (u,v) in ((0,0),(2,0),(1,1),(0,2),(2,2)):
        set_pixel(a+u,b+v,EYE)
    else:
      box(a+1+(d[0]>0),b+(d[1]>0),2,2,CUR[3])
def tongue(c,d):
  x=c[0]*CELL+1;y=c[1]*CELL+1
  fx=x+9 if d[0]>0 else (x if d[0]<0 else x+4)
  fy=y+9 if d[1]>0 else (y if d[1]<0 else y+4)
  px=[]
  for (f,s) in ((1,0),(2,0),(3,-1),(3,1)):
    p=(fx+f*d[0]+s*d[1],fy+f*d[1]+s*d[0])
    if 12<=p[1]<=191 and 0<=p[0]<=383:
      set_pixel(p[0],p[1],RED);px.append(p)
  return px
def untongue(px):
  for p in px:
    set_pixel(p[0],p[1],gcol(p[0],p[1]))
def apple(c,big=True):
  x=c[0]*CELL;y=c[1]*CELL;o=0 if big else 1
  box(x+3+o,y+3+o,7-2*o,7-2*o,APPLE);box(x+2+o,y+4+o,9-2*o,5-2*o,APPLE)
  box(x+3+o,y+9-o,7-2*o,1,APPLE2)
  set_pixel(x+6,y+2+o,STEM);box(x+7,y+1+o,2,2,LEAF);box(x+4+o,y+4+o,2,2,WHITE)
def bug(c,ph=0):
  x=c[0]*CELL;y=c[1]*CELL
  box(x+3,y+3,6,7,BUG);box(x+4,y+1,4,2,BUG2);box(x+5,y+4,2,5,BUG2)
  for i in (4,6,8):
    o=(i//2+ph)%2
    set_pixel(x+1,y+i+o,BUG2);set_pixel(x+2,y+i,BUG2);set_pixel(x+9,y+i,BUG2);set_pixel(x+10,y+i+o,BUG2)
  set_pixel(x+4,y+1,WHITE);set_pixel(x+7,y+1,WHITE)
def draw_snake(snake,d,cols):
  for i in range(1,len(snake)-1):
    seg(snake[i],cols[i-1]);link(snake[i],snake[i-1],cols[i-1])
  tail(snake[-1],snake[-2],cols[-1],cols[-2] if len(cols)>1 else None);link(snake[1],snake[0],cols[0])
  head(snake[0],d)
def panel(x,y,w,h):
  box(x,y,w,h,WHITE);frame(x,y,w,h,LINE);frame(x+2,y+2,w-4,h-4,BAND)
def shadow(x,y,s,col,size="large"):
  draw_string(x+2,y+2,s,BAND,size);draw_string(x,y,s,col,size)
def wait(n):
  for i in range(n):
    pass
def ghost(c,steps,dl):
  x0=c[0]*CELL+1;y0=c[1]*CELL
  for k in range(steps):
    y=y0-k*5
    if y<13:
      break
    save=[get_pixel(x,yy) for yy in range(y,y+11) for x in range(x0,x0+10)]
    box(x0+1,y,8,8,WHITE);box(x0,y+3,10,6,WHITE)
    for i in range(0,10,3):
      box(x0+i,y+9,2,2,WHITE)
    box(x0+2,y+3,2,2,EYE);box(x0+6,y+3,2,2,EYE)
    show_screen();wait(dl)
    i=0
    for yy in range(y,y+11):
      for x in range(x0,x0+10):
        set_pixel(x,yy,save[i]);i+=1
  show_screen()
def poof(c,col):
  x=c[0]*CELL;y=c[1]*CELL
  cellg(c)
  for i in range(4):
    set_pixel(x+randint(1,10),y+randint(1,10),col)
  set_pixel(x+5,y+5,WHITE);set_pixel(x+6,y+6,WHITE)
LET=[["01111","10000","01110","00001","11110"],["10001","11001","10101","10011","10001"],
["01110","10001","11111","10001","10001"],["10001","10010","11100","10010","10001"],
["11111","10000","11110","10000","11111"]]
def logo():
  p=CUR[1];h=CUR[0];x0=105;y0=4
  rows=["".join(L[r] for L in LET) for r in range(5)]
  for r in range(5):
    for i in range(25):
      if rows[r][i]=="1":
        x=x0+i*6+(i//5)*6;y=y0+r*6
        box(x+2,y+2,6,6,h)
  for r in range(5):
    for i in range(25):
      if rows[r][i]=="1":
        x=x0+i*6+(i//5)*6;y=y0+r*6;col=p[(i+r)%len(p)]
        box(x,y,6,6,dk(col));box(x,y,5,5,col);set_pixel(x+1,y+1,lt(col))
def menubg():
  clear_screen()
  for y in range(4,186,8):
    for x in range((y//8)%2*4+2,384,8):
      if not (44<=x<=340 and 48<=y<=178):
        set_pixel(x,y,(200,225,190))
  for x in range(384):
    for y in range(186,192):
      set_pixel(x,y,G1 if (x//12)%2==0 else G2)
    if x%7==0:
      set_pixel(x,185,G2);set_pixel(x,184,GB)
      set_pixel(x+2 if x<382 else x,185,G1)
GREEN=(35,150,55);SOFT=(150,150,150)
def tri(x,y,dr,col):
  for i in range(5):
    box(x+(i if dr>0 else 4-i),y+i,1,9-2*i,col)
def chip(x,y,lab,col):
  w=len(lab)*6+8
  box(x,y,w,13,col);draw_string(x+4,y+1,lab,WHITE,"small")
  return x+w+5
def cursor(x,y,col):
  box(x,y,10,10,col);box(x+5,y+2,4,3,WHITE);box(x+7,y+3,2,2,EYE)
def tick(x,y,ok):
  if ok:
    box(x,y,10,10,GREEN)
    for (u,v) in ((2,5),(3,6),(4,7),(5,6),(6,5),(7,4),(8,3)):
      set_pixel(x+u,y+v,WHITE)
  else:
    frame(x,y,10,10,SOFT)
