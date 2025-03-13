"""
This script analyzes a single plain text file.  

It counts the occurrences of the following structures.
"""
import sys, subprocess,re

#Single item simple noun phrase, e.g. Mike, you, something, metal, tends to be on the subject position

NP_S1 = "(NP <: /NN|DT|PRP|CD|FW/)"

#Two item simple noun phrase, e.g. a magnet, the bear, my back tends to be on the object position

NP_S2 = "(NP<1/NN|DT|PRP|CD|UH|FW/<2/^NN|DT|PRP|CD|FW/!<3__)"

#Two item simple noun phrase, e.g. a magnet men, the pet store

NP_S3 = "(NP<1/NN|DT|PRP|CD|UH|FW/<2/^NN|DT|PRP|CD|FW/<3/^NN|DT|PRP|CD|FW/!<4__)"

#Simple NP with a JJ
## TODO: Optional determiner

NP_SJJ_1 = "(NP<1/DT|PRP|CD|UH$/<2/^JJ/<3/^NN|DT|PRP|CD/!<4__)"

NP_SJJ_2 = "(NP<1/^JJ/<2/^NN|DT|PRP|CD/!<3__)"

#Simple NP: the best

NP_JJS_1 = "(NP<:/^JJ/)"

NP_JJS_2= "(NP<1/DT|PRP|CD|UH$/<2/^JJ/!<3__)"

#Simple ADJP
#TODO: ADJP RB JJ & ADJP VBZ variants ADJP RB VBN PRT
ADJP_S1 = "(ADJP|ADJ <:/^JJ/)"

#simple VP

VP_S = "(VP<:/^VB/)"

#simple VP w/ simple NP child

VP_SO = f"(VP<1/^VB/[<2{NP_S1}|<2{NP_S2}|<2{NP_S3}]!<3__)"

#simple VP w/ 2 simple NP child

VP_SOO = f"(VP<1/^VB/[<2{NP_S1}|<2{NP_S2}|<2{NP_S3}][<3{NP_S1}|<3{NP_S2}|<3{NP_S3}]!<4__)"

#simple VP w/ simple ADJP child

VP_SC = f"(VP<1/^VB/<2{ADJP_S1}!<3__)"

#simple VP w/ simple JJ child

VP_NP_jj = f"(VP<1/^VB/[<2{NP_SJJ_1}|<2{NP_SJJ_1}]!<3__)"

VP_NP_jjs = f"(VP<1/^VB/[<2{NP_JJS_1}|<2{NP_JJS_1}]!<3__)"

#Simple WHNP

## TODO:Extend punctuation
#Punctuation

P = "/^(\.|\.\.\.|!|\?)$/"

################################################################################ The Categories ################################################################################ 

## Single item utterances

NP_1 = f"'{NP_S1}!>__'"
NP_1p = f"'(NP <1 /^NN|DT|PRP|CD/<2{P}!<3__)!>__'" 

NP_1jj = f"'(NP[<1/^JJ/|<1{ADJP_S1}]!<2__)!>__'"
NP_1jjp = f"'(NP[<1/^JJ/|<1{ADJP_S1}]<2{P}!<3__)!>__'"

NP_1vb = "'(NP<:/^VB/)!>__'"
NP_1vbp = f"'(NP<1/^VB/<2{P}!<3__)!>__'"

VP_1 = "'(VP<:/^VB/) !>__'"
VP_1p = f"'(VP<1/^VB/<2{P}!<3__)!>__'" 

ADJP_1 = f"'{ADJP_S1}!>__'"
ADJP_1p = f"'(ADJP|ADJ<1/^JJ/<2{P}!<3__)!>__'"

INTJ_1 = "'(INTJ<:UH)!>__'"
INTJ_1p = f"'(INTJ<1UH<2{P})!>__'"

## Double item utterances

# NP det Noun: a cat
NP_2_det = f"'{NP_S2}!>__'"
NP_2_det_p = f"'(NP<1/DT|PRP|CD|UH$/<2/^NN|DT|PRP|CD/<3{P}!<4__)!>__'"

# NP adjp noun: blue (a) cat (toy) oh well this can be 4 item as well
NP_2_ADJP = f"'(NP[<1/^JJ/|<1{ADJP_S1}][<2{NP_S1}|<2{NP_S2}|<2{NP_S3}|<2/^NN|DT|PRP|CD/]!<3__)!>__'"
NP_2_ADJP_p = f"'(NP[<1/^JJ/|<1{ADJP_S1}][<2{NP_S1}|<2{NP_S2}|<2{NP_S3}|<2/^NN|DT|PRP|CD/]<3{P}!<4__)!>__'"

#

#Subjectless VP: do this 

#Subjectless VP: do this

VP_Sless = f"'{VP_SO}!>__'"
VP_Sless_p = f"'(VP<1/^VB/[<2{NP_S1}|<2{NP_S2}|<2{NP_S3}]<3{P}!<4__)!>__'"

##Triple item

# det JJ N: a blue cat 
NP_3_ADJP = "'(NP<1/DT|PRP|CD|UH/<2/^JJ/<3/^NN|DT|PRP|CD/!<4__)!>__'"
NP_3_ADJP_p = f"'(NP<1/DT|PRP|CD|UH/<2/^JJ/<3/^NN|DT|PRP|CD/<4{P}!<5__)!>__'"

#JJ JJ NN
NP_JJ_JJ_NN = "'(NP<1/JJ/<2/^JJ/<3/^NN|DT|PRP|CD/!<4__)!>__'"
NP_JJ_JJ_NN_p = f"'(NP<1/JJ/<2/^JJ/<3/^NN|DT|PRP|CD/<4{P}!<5__)!>__'"

# JJ NN NN
NP_JJ_NN_NN = "'(NP<1/JJ/<2/^NN|DT|PRP|CD/<3/^NN|DT|PRP|CD/!<4__)!>__'"
NP_JJ_NN_NN_p = f"'(NP<1/JJ/<2/^NN|DT|PRP|CD/<3/^NN|DT|PRP|CD/<4{P}!<5__)!>__'"

# det NN JJ 
NP_3_ADJP_r = f"'(NP[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}][<2/^JJ/|<2{ADJP_S1}]!<3__)!>__'"
NP_3_ADJP_rp = f"'(NP[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}][<2/^JJ/|<2{ADJP_S1}]<3{P}!<__)!>__'"


#Simple sentence, intranstive

SV_S = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}]<2{VP_S}<3{P})!>__'"

#Simple sentence, intranstive, w/ adjective mod on O: the cute girl runs, the best follows

SV_S_a = f"'(S[<1{NP_SJJ_1}|<1{NP_SJJ_1}|<1{NP_JJS_1}|<1{NP_JJS_1}]<2{VP_S}<3{P})!>__'"

#Simple sentence, transitive

SVO_S = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}]<2{VP_SO}<3{P})!>__'"

##Simple sentence, transitive, w/ adjective mod on 0: She is a cute girl, Mike answers the pink phone

SVO_Sjj = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}][<2{VP_NP_jj}|<2{VP_NP_jjs}]<3{P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S: the cute girl answers the phone, the best follows

SVO_Ojj = f"'(S[<1{NP_SJJ_1}|<1{NP_SJJ_1}|<1{NP_SJJ_1}|<1{NP_SJJ_1}]<2{VP_SO}<3{P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S and O: the cute girl answers the pink phone

SVO_jj = f"'(S[<1{NP_SJJ_1}|<1{NP_SJJ_1}|<1{NP_SJJ_1}|<1{NP_SJJ_1}][<2{VP_NP_jj}|<2{VP_NP_jjs}]<3{P})!>__'"

#Simple sentence, ditransitive

SVOO_S = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}]<2{VP_SOO}<3{P})!>__'"

#TODO: ditrans w/ adjective modifiers

#She is smart

#TODO: other combinations e.g Smart girl is tall, smart girl is the best

SVC = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}]<2{VP_SC}<3{P})!>__'"

#This is the best, She likes the pinkest

SVO_jjs = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}]<2{VP_NP_jjs}<3{P})!>__'"

#TODO: Ungrammatical stuff like Noun ADJP

#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    "NP_1": NP_1,
    "NP_1p": NP_1p,
    "NP_1jj": NP_1jj,
    "NP_1jjp": NP_1jjp,
    "NP_1vb": NP_1vb,
    "NP_1vbp": NP_1vbp,
    "VP_1": VP_1,
    "VP_1p": VP_1p,
    "ADJP_1": ADJP_1,
    "ADJP_1p": ADJP_1p,
    "SV_S_a": SV_S_a,
    "NP_2_det": NP_2_det,
    "NP_2_det_p": NP_2_det_p,
    "NP_2_ADJP": NP_2_ADJP,
    "NP_2_ADJP_p": NP_2_ADJP_p,
    "VP_Sless": VP_Sless,
    "VP_Sless_p": VP_Sless_p,
    "NP_3_ADJP": NP_3_ADJP,
    "NP_3_ADJP_r": NP_3_ADJP_r,
    "NP_3_ADJP_rp": NP_3_ADJP_rp,
    "NP_3_ADJP_p": NP_3_ADJP_p,
    "NP_JJ_JJ_NN": NP_JJ_JJ_NN,
    "NP_JJ_JJ_NN_p": NP_JJ_JJ_NN_p,
    "NP_JJ_NN_NN": NP_JJ_NN_NN,
    "NP_JJ_NN_NN_p": NP_JJ_NN_NN_p,
    "SV_S": SV_S,
    "SVO_S": SVO_S,
    "SVO_Sjj": SVO_Sjj,
    "SVO_Ojj": SVO_Ojj,
    "SVO_jj": SVO_jj,
    "SVOO_S": SVOO_S,
    "SVC": SVC,
    "SVO_jjs": SVO_jjs,
    "INTJ_1": INTJ_1,
    "INTJ_1p": INTJ_1p
}

# Write to a pattern file, list of the rules for UI testing 
with open("tregex_patterns_simple_?.txt", "w") as f:
    for name, pattern in pattern_dict.items():
        f.write(f"{name}: {pattern}\n")

#input file name
inputFile=sys.argv[1]

#extract the name of the file being processed
output=inputFile.split('/')[-1]

#output file name
outputFile=open(sys.argv[2],"w")
print('Processing '+inputFile+'...')

#write a list of 24 comma-delimited fields to the output file
fields= ["Filename", "WordCount"] + [key for key in pattern_dict]
outputFile.write(",".join(fields) + "\n")

#list of counts of the patterns
patterncount=[]

#query the parse trees using the tregex patterns
for name, pattern in pattern_dict.items():
        command = "./tregex.sh " + pattern + " " + inputFile + " -C -o"
        print(command)
        count = subprocess.getoutput(command).split('\n')[-1]
        patterncount.append(int(count))
        
#update frequencies of complex nominals, clauses, and T-units
#patterncount[7]=patterncount[-4]+patterncount[-5]+patterncount[-6]
#patterncount[2]=patterncount[2]+patterncount[-3]
#patterncount[3]=patterncount[3]+patterncount[-2]
#patterncount[1]=patterncount[1]+patterncount[-1]

#word count
infile=open(inputFile,"r")
content=infile.read()
w=len(re.findall("\([A-Z]+\$? [^\)\(-]+\)",content))
infile.close()

#add frequencies of words and other structures to output string
output+=","+str(w) #number of words
for count in patterncount:
    output+=","+str(count)
    

#write output string to output file
outputFile.write(output+"\n")