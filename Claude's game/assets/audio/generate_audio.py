"""Generate independently reusable original chiptune samples for Greenlands Quest.
The HTML game synthesizes corresponding effects at runtime, so it requires no external audio files.
"""
import wave, math, pathlib, numpy as np
RATE=22050
OUT=pathlib.Path(__file__).parent

def tone(freq,dur,kind='square',sweep=1.0,amp=.4):
 n=int(dur*RATE);t=np.arange(n)/RATE
 hz=freq*np.exp(np.log(max(.01,sweep))*t/dur)
 phase=np.cumsum(hz)/RATE
 if kind=='triangle': y=2*np.abs(2*(phase%1)-1)-1
 elif kind=='sawtooth':y=2*(phase%1)-1
 else:y=np.where((phase%1)<.5,1.,-1.)
 env=np.minimum(1.,t/.01)*np.exp(-4*t/dur)
 return y*env*amp

def wav(name,a):
 arr=np.asarray(a,dtype=float);arr=np.clip(arr,-1,1);arr=(arr*26000).astype('<i2')
 with wave.open(str(OUT/name),'wb') as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(RATE);f.writeframes(arr.tobytes())
 return name,len(arr)/RATE

for nm,parts in {
 'SFX_Jump.wav':[(390,.14,'square',1.7)],
 'SFX_Coin.wav':[(750,.08,'square',1.35),(1120,.14,'square',1.)],
 'SFX_Stomp.wav':[(160,.14,'triangle',.6)],
 'SFX_Hurt.wav':[(260,.28,'sawtooth',.36)],
 'SFX_Checkpoint.wav':[(470,.13,'square',1.),(700,.20,'square',1.)],
 'SFX_Level_Clear.wav':[(523,.17,'square',1.),(659,.17,'square',1.),(784,.17,'square',1.),(1046,.40,'square',1.)]
}.items():
 a=np.concatenate([tone(*tup) for tup in parts]);print(wav(nm,a))
notes=[392,0,494,0,587,494,392,0,349,0,440,0,523,440,349,0,392,0,494,0,659,587,494,0,440,392,349,330,392,0,0,0]
unit=int(.175*RATE);out=np.zeros(len(notes)*unit)
for i,n in enumerate(notes):
 if n:
  t=tone(n,.15,'square',1.,.14);out[i*unit:i*unit+len(t)]+=t
 if i%4==0:
  t=tone(98,.09,'triangle',.77,.20);out[i*unit:i*unit+len(t)]+=t
print(wav('MUSIC_Greenlands_Theme_loop.wav',out))
