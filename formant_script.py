### Author: Niklas Thielking ###
### Date:23.09.2018 ###
### Formant extraction based on three-tier-annotated TextGrid###

## import relevant libraries###
import parselmouth
from parselmouth.praat import call
#import tgt
import pandas as pd
import glob
import os


#specify vowel labels for extraction
vowel_list = ["ae","e"]

# phone tier containing phone annotations
phon_tier = 1

#word tier containing word annotations
word_tier = 2

#speaker tier containing speaker annotations
speaker_tier = 3

### create dict for data to be saved###
data= {}

## create lists for variables to be saved###
vowel = []
dura = []
speak = []
style = []
wor = []
ff1 = []
ff2 =[]
ff3 = []

### run through all files in the same dir##
### .wav and .TextGrid must have same name##
for wave_file in glob.glob("/Path/to/folder/*.wav"):
    print("Processing {}...".format(wave_file))
    sound = os.path.splitext(wave_file)[0]+ ".wav"
    tgt = os.path.splitext(wave_file)[0]+ ".TextGrid"
    base = os.path.basename(wave_file)

## read in TextGrid###
    text_g = call("Read from file", tgt)
## read in sound file##
    snd = parselmouth.Sound(sound)
## create formant object##
    formant = snd.to_formant_burg(0.01, 4, 5500, 0.025, 50)
    nIntervals = call(text_g, "Get number of intervals", phon_tier)

    #print(nIntervals)

    i=1
    while i < nIntervals:
        lab = call(text_g, "Get label of interval", phon_tier, i)
        if lab != None and lab in vowel_list:
            word = call(text_g, "Get label of interval", word_tier, i)
            speaker = call(text_g, "Get label of interval", speaker_tier, i)
            beg = float(call(text_g,"Get starting point", phon_tier, i))
            end = float(call(text_g,"Get end point", phon_tier, i))

            #print(lab)
            #print(word)
            #print(speaker)
            dur= end-beg
            mid = (dur/2)+beg
            durms = dur*1000

            f1 = formant.get_value_at_time(1, mid)
            f2 = formant.get_value_at_time(2, mid)
            f3 = formant.get_value_at_time(3, mid)

            vowel.append(lab)
            wor.append(word)
            speak.append(speaker)
            dura.append(durms)
            ff1.append(f1)
            ff2.append(f2)
            ff3.append(f3)
        i =i+1
## append data from lists to dict###
    data["speaker"]= speak
    data["word"]= wor
    data["vowel"]= vowel
    data["Duration"]= dura
    data["F1"]= ff1
    data["F2"]= ff2
    data["F3"]= ff3
    #data["style"] = style

#print(data)
### save data in specified file###
df=pd.DataFrame(data, columns=["speaker","vowel","word","style","Duration","F1","F2","F3"])
df.to_csv("/Path/to/save/data/formants.csv",index=False, sep = ";")
