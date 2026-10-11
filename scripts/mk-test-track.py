import math, random, struct, wave, sys
sr=44100; bpm=124; dur=40.0; n=int(sr*dur); beat=60/bpm
L=[0.0]*n; R=[0.0]*n
random.seed(3)
def add(i,v,pan=0.5):
    if 0<=i<n: L[i]+=v*(1-pan)*2*0.5; R[i]+=v*pan*2*0.5
notes=[41,41,44,39]  # F, F, Ab, Eb bass roots
for b in range(int(dur/beat)):
    t0=int(b*beat*sr); bar=b//4
    if not (16<=b<24):  # breakdown without kick
        for k in range(int(0.25*sr)):
            t=k/sr; f=45+120*math.exp(-t*30); ph=2*math.pi*(45*t+120*(1-math.exp(-t*30))/30)
            add(t0+k, 0.9*math.sin(ph)*math.exp(-t*9))
    # offbeat hat
    h0=t0+int(beat/2*sr)
    for k in range(int(0.05*sr)):
        add(h0+k, 0.25*(random.random()*2-1)*math.exp(-k/sr*80), 0.7)
    # bass on offbeats
    f=440*2**((notes[bar%4]-69)/12)
    for k in range(int(beat/2*sr*0.9)):
        t=k/sr; v=0.35*(2*((f*t)%1)-1)*math.exp(-t*4)
        add(h0+k, v)
# pad: slow chord with LFO, swells over time
for i in range(n):
    t=i/sr; sw=0.5-0.5*math.cos(2*math.pi*t/16)
    v=sum(math.sin(2*math.pi*fr*t+math.sin(t*0.7+j)) for j,fr in enumerate([349.2,415.3,523.3,622.3]))
    L[i]+=0.05*sw*v; R[i]+=0.05*sw*sum(math.sin(2*math.pi*fr*1.003*t) for fr in [349.2,415.3,523.3,622.3])
m=max(max(map(abs,L)),max(map(abs,R)))
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
w.writeframes(b''.join(struct.pack('<hh',int(l/m*30000),int(r/m*30000)) for l,r in zip(L,R)))
