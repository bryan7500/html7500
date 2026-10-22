# Generates NES-style assets: sprites.png (8x8 tiles, 4-colour palette) + chiptune WAVs.
import zlib, struct, wave, math, random, os
here = os.path.dirname(os.path.abspath(__file__))
PAL = {'.':(0,0,0,0),'1':(252,252,252,255),'2':(0,120,248,255),'3':(248,56,0,255),'4':(252,216,56,255)}
SPR = [  # player, enemy A, enemy B, bullet, enemy bullet, boom1, boom2, star
 ["...11...","...11...","..1221..","..1221..",".122221.","12222221","13.22.31","4..33..4"],
 ["33....33","3333333.","33.33.33","3333333.",".33333..","..3.3...",".3...3..","3.....3."],
 [".4444444","44.44.44","4444444.","44444444",".4....4.","4.4..4.4","........","........"],
 ["........","...44...","...44...","...44...","...44...","........","........","........"],
 ["........","...33...","..3333..","...33...","........","........","........","........"],
 ["........","..4..4..","...44...",".4.44.4.","...44...","..4..4..","........","........"],
 ["4..3..4.","..4..3..","3..44..4","..4..3..","4..3..4.","..4..3..",".3..4..3","........"],
 ["........","........","........","...1....","........","........","........","........"]]
W=8*len(SPR); H=8
rows=[]
for y in range(H):
    r=b'\x00'
    for t in SPR:
        for x in range(8): r+=bytes(PAL[t[y][x]])
    rows.append(r)
def chunk(t,d): c=struct.pack('>I',len(d))+t+d; return c+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,6,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(rows)))+chunk(b'IEND',b'')
open(os.path.join(here,'sprites.png'),'wb').write(png)

SR=22050
def sq(f,t,duty=.5): return 1 if (f*t)%1<duty else -1
def tri(f,t): p=(f*t)%1; return 4*abs(p-.5)-1
def save(name,samples):
    w=wave.open(os.path.join(here,name),'wb'); w.setnchannels(1); w.setsampwidth(1); w.setframerate(SR)
    w.writeframes(bytes(int(128+max(-1,min(1,s))*100) for s in samples)); w.close()
def sweep(f0,f1,dur,vol=.6,noise=False):
    out=[];n=int(SR*dur);ph=0
    for i in range(n):
        k=i/n; f=f0+(f1-f0)*k; ph+=f/SR
        v=(random.uniform(-1,1) if noise else sq(ph,1,.25))
        out.append(v*vol*(1-k))
    return out
random.seed(7)
save('sfx_shoot.wav',sweep(1400,300,.12))
save('sfx_hit.wav',sweep(300,60,.25,.7,True))
save('sfx_explode.wav',sweep(200,20,.6,.8,True))
save('sfx_gameover.wav',sweep(600,80,.9,.6))
# music: 16-step loop, square lead + triangle bass
N={'C':261.6,'D':293.7,'E':329.6,'F':349.2,'G':392,'A':440,'B':493.9,'c':523.3}
lead="E G A G E G c B A G E D E G A G".split()
bass="C C G G A A F F C C G G F F G G".split()
step=.15;m=[]
for rep in range(2):
    for l,b in zip(lead,bass):
        n=int(SR*step)
        for i in range(n):
            t=i/SR; env=1-i/n*.5
            m.append((sq(N[l],t,.25)*.35*env+tri(N[b]/2,t)*.45))
save('music.wav',m)
print('assets written')
