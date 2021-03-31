# Import all the utilities from alles_util needed to make sounds
from alles_util import send, sync, lowpass, volume, note_on, note_off, reset, connect, disconnect, millis, ALLES_LATENCY_MS
import time

# Some constants shared with the synth that help
ALLES_VOICES = 10
[SINE, PULSE, SAW, TRIANGLE, NOISE, FM, KS, PCM, OFF] = range(9)
TARGET_AMP, TARGET_DUTY, TARGET_FREQ, TARGET_FILTER_FREQ, TARGET_RESONANCE = (1, 2, 4, 8, 16)


"""
    A bunch of useful presets using the oscillators
"""
def preset(which,voice=0, client=-1):
    # Reset the voice first
    reset(voice=voice)
    if(which==0): # simple note
        send(voice=voice, wave=SINE, envelope="10,250,0.7,250", adsr_target=TARGET_AMP)
    if(which==1): # filter bass
        filter(1000, 2)
        send(voice=voice, wave=SAW, envelope="10,100,0.5,25", adsr_target=TARGET_AMP+TARGET_FILTER_FREQ)
    if(which==2): # long square pad to test ADSR
        send(voice=voice, wave=PULSE, envelope="500,1000,0.25,750", adsr_target=TARGET_AMP)
    if(which==3): # amp LFO example
        reset(voice+1)
        send(voice=voice+1, wave=SINE, vel=0.50, freq=1.5)
        send(voice=voice, wave=PULSE, envelope="150,250,0.25,250", adsr_target=TARGET_AMP, lfo_target=TARGET_AMP, lfo_source=voice+1)
    if(which==4): # pitch LFO going up 
        reset(voice+1)
        send(voice=voice+1, wave=SINE, vel=0.50, freq=0.25)
        send(voice=voice, wave=PULSE, envelope="150,400,0,0", adsr_target=TARGET_AMP, lfo_target=TARGET_FREQ, lfo_source=voice+1)
    if(which==5): # bass drum
        reset(voice+1)
        send(voice=voice+1, wave=SINE, vel=0.50, freq=0.25, phase=0.5)
        send(voice=voice, wave=SINE, vel=0, envelope="0,500,0,0", adsr_target=TARGET_AMP, lfo_target=TARGET_FREQ, lfo_source=voice+1)
    if(which==6): # noise snare
        send(voice=voice, wave=NOISE, vel=0, envelope="0,250,0,0", adsr_target=TARGET_AMP)
    if(which==7): # closed hat
        send(voice=voice, wave=NOISE, vel=0, envelope="25,75,0,0", adsr_target=TARGET_AMP)

"""
    Run a scale through all the synth's sounds
"""
def test():
    while True:
        for wave in [SINE, SAW, PULSE, TRIANGLE, FM, NOISE]:
            for i in range(12):
                note_on(voice=0, wave=wave, note=40+i, patch=i)
                time.sleep(0.5)


"""
    Play all of the FM patches in order
"""
def play_patches(wait=0.500, patch_total = 100, **kwargs):
    once = True
    patch_count = 0
    while True:
        for i in range(24):
            patch = patch_count % patch_total
            patch_count = patch_count + 1
            note_on(voice=i % ALLES_VOICES, note=i+50, wave=FM, patch=patch, **kwargs)
            time.sleep(wait)
            note_off(voice=i % ALLES_VOICES)

"""
    Play up to VOICES FM patches at once
"""
def polyphony():
    voice = 0
    note = 0
    while(1):
        note_on(voice=voice, wave=FM, patch=note, note=50+note, client = -1)
        time.sleep(0.5)
        voice =(voice + 1) % ALLES_VOICES
        note =(note + 1) % 24

"""
    Sweep the filter
"""
def sweep(speed=0.100, res=0.5, loops = -1):
    end = 2000
    cur = 0
    while(loops != 0):
        for i in [0, 1, 4, 5, 1, 3, 4, 5]:
            cur = (cur + 100) % end
            filter(cur, res)
            note_on(voice=0,wave=PULSE, note=50+i, duty=0.50)
            note_on(voice=1,wave=PULSE, note=50+12+i, duty=0.25)
            note_on(voice=2,wave=PULSE, note=50+6+i, duty=0.90)
            time.sleep(speed)

"""
    An example drum machine using oscillator presets
"""
def drums(speed=0.250):
    preset(5, voice=0) # bass
    preset(6, voice=2) # snare
    preset(7, voice=3) # hat
    [bass, snare, hat, silent] = [1, 2, 4, 8]
    pattern = [bass+hat, hat, bass+hat+snare, hat, hat, hat+bass, snare+hat, hat]
    while True:
        for i,x in enumerate(pattern):
            if(x & bass): note_on(voice=0, note=50, vel=1.5)
            if(x & snare): note_on(voice=2, note=60, vel=0.5)
            if(x & hat): note_on(voice=3, note=70, vel=0.3)
            time.sleep(speed)

"""
    A small pattern using FM + sine oscillators
"""    
def complex(speed=0.250, vol=1, client =-1, loops=-1):
    while(loops != 0): # -1 means forever 
        for i in [0,2,4,5, 0, 4, 0, 2]:
            note_on(voice=0, wave=FM, vel=0.8, note=50+i, patch=15, client=client)
            time.sleep(speed)
            note_on(voice=1, wave=FM, vel=0.6, note=50+i, patch=8, client=client)
            time.sleep(speed)
            note_on(voice=2, wave=SINE, vel=0.5, note=62+i, patch=2, client=client)
            time.sleep(speed)
            note_on(voice=2, wave=SINE, vel=1, freq = 20, client=client)
            time.sleep(speed)
        loops = loops - 1


"""
    C-major chord
"""
def c_major(octave=2,wave=SINE):
    note_on(voice=0, freq=220.5*octave, wave=wave)
    note_on(voice=1, freq=138.5*octave, wave=wave)
    note_on(voice=2, freq=164.5*octave, wave=wave)



# Setup the sock on module import
connect()


