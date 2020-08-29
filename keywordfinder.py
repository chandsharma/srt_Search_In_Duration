import argparse
import pysrt
from PyDictionary import PyDictionary

parser = argparse.ArgumentParser()
parser.add_argument('Keywords',
                       metavar='keywords',
                       type=str,
                       help='answer keywords')
parser.add_argument('Choice',
                       metavar='choice',
                       type=int,
                       help='exact = 0 , related = 1')
args = parser.parse_args()
#print(args.Keywords)

subs = pysrt.open("subtitles.srt")
ans = pysrt.open(args.Keywords)

def findinsrt(sm,ss,em,es):
    string = ""
    for i in range(0,len(subs)):
        s = subs[i]

        if (s.start.minutes >= sm and s.start.seconds >= ss and s.end.minutes <= em and s.end.seconds <=es):
            string = string + s.text

    return string

for ke in range(0,len(ans)):
    an = ans[ke]
    foundkeys = []
    keywords = an.text.split()
    nums = len(keywords)
    sm =int(an.start.minutes)
    ss =int(an.start.seconds)
    em =int(an.end.minutes)
    es =int(an.end.seconds)
    comp = findinsrt(sm,ss,em,es)
    found  = 0
    for key in keywords:
        if args.Choice == 1:
            dictionary=PyDictionary(key)
            syns = dictionary.getSynonyms()
            if syns == [None]:
                if key in comp:
                    found += 1
                    foundkeys.append(key)
            else:
                syns = syns[0]
                syns = list(syns.values())
                syns = syns[0]
                syns.append(key)
                fou = 0
                for syn in syns:
                    if syn in comp:
                        fou += 1
                if fou != 0:
                    found +=1
                    foundkeys.append(key)
            #syns = syns.split()
            #print(syns)

        else:
            if key in comp:
                found += 1
                foundkeys.append(key)
    print ("found total of "+str(found)+" keywords from "+str(nums)+" in answer "+str(ke+1))
    print("Found keywords : "+str(foundkeys))
    print("")
