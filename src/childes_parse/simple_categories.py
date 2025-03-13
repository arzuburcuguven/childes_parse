"""
This script analyzes a single plain text file.  

It counts the occurrences of the following structures.
"""
import sys, subprocess,re

#TODO: All "s" signifying simple should come first -.-
#Single item simple noun phrase, e.g. Mike, you, something, metal, tends to be on the subject position

NP_S1 = "(NP <: /NN|DT|PRP|CD|FW/)"

#Two item simple noun phrase, e.g. a magnet, the bear, my back tends to be on the object position

NP_S2 = "(NP<1/NN|DT|PRP|CD|UH|FW/<2/^NN|DT|PRP|CD|FW/!<3__)"

#Two item simple noun phrase, e.g. a magnet men, the pet store

NP_S3 = "(NP<1/NN|DT|PRP|CD|UH|FW/<2/^NN|DT|PRP|CD|FW/<3/^NN|DT|PRP|CD|FW/!<4__)"

#Simple NP with a JJ

NP_S_D_JJ = "(NP<1/DT|PRP|CD|UH$/<2/^JJ/<3/^NN|DT|PRP|CD/!<4__)"

NP_S_JJ = "(NP<1/^JJ/<2/^NN|DT|PRP|CD/!<3__)"

#Simple NP: the best

NP_S_JJS = "(NP<:/^JJ/)"

NP_S_D_JJS = "(NP<1/DT|PRP|CD|UH$/<2/^JJ/!<3__)"

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

VP_SO_JJ = f"(VP<1/^VB/[<2{NP_S_D_JJ}|<2{NP_S_JJ}]!<3__)"

VP_SO_JJS = f"(VP<1/^VB/[<2{NP_S_JJS}|<2{NP_S_D_JJS}]!<3__)"

## TODO:Extend punctuation
#Punctuation

P = "/^(\.|\.\.\.|!|\?)$/"
P_MID = "/^(\.|:|,|''|``|-LRB-|-RRB-|HYPH)$/"

################################################################################ The Categories ################################################################################ 

## Single item utterances

NP_1 = f"'{NP_S1}!>__'"
NP_1_P = f"'(NP <1 /^NN|DT|PRP|CD/<2{P}!<3__)!>__'" 

NP_1_JJ = f"'(NP[<1/^JJ/|<1{ADJP_S1}]!<2__)!>__'"
NP_1_JJ_P = f"'(NP[<1/^JJ/|<1{ADJP_S1}]<2{P}!<3__)!>__'"

NP_1_VB = "'(NP<:/^VB/)!>__'"
NP_1_VB_P = f"'(NP<1/^VB/<2{P}!<3__)!>__'"

VP_1 = "'(VP<:/^VB/) !>__'"
VP_1_P = f"'(VP<1/^VB/<2{P}!<3__)!>__'" 

ADJP_1 = f"'{ADJP_S1}!>__'"
ADJP_1_P = f"'(ADJP|ADJ<1/^JJ/<2{P}!<3__)!>__'"

INTJ_1 = "'(INTJ<:UH)!>__'"
INTJ_1_P = f"'(INTJ<1UH<2{P})!>__'"

## Double item utterances

# NP det Noun: a cat
NP_2_D = f"'{NP_S2}!>__'"
NP_2_D_P = f"'(NP<1/DT|PRP|CD|UH$/<2/^NN|DT|PRP|CD/<3{P}!<4__)!>__'"

# NP adjp noun: blue (a) cat (toy) oh well this can be 4 item as well
NP_2_ADJP = f"'(NP[<1/^JJ/|<1{ADJP_S1}][<2{NP_S1}|<2{NP_S2}|<2{NP_S3}|<2/^NN|DT|PRP|CD/]!<3__)!>__'"
NP_2_ADJP_P = f"'(NP[<1/^JJ/|<1{ADJP_S1}][<2{NP_S1}|<2{NP_S2}|<2{NP_S3}|<2/^NN|DT|PRP|CD/]<3{P}!<4__)!>__'"


#Imperative VP: do this 

VP_Imp = f"'{VP_SO}!>__'"
VP_Imp_P = f"'(VP<1/^VB/[<2{NP_S1}|<2{NP_S2}|<2{NP_S3}]<3{P}!<4__)!>__'"

##Triple item

# det JJ N: a blue cat 
NP_3_D_JJ_N = "'(NP<1/DT|PRP|CD|UH/<2/^JJ/<3/^NN|DT|PRP|CD/!<4__)!>__'"
NP_3_D_JJ_N_P = f"'(NP<1/DT|PRP|CD|UH/<2/^JJ/<3/^NN|DT|PRP|CD/<4{P}!<5__)!>__'"

#JJ JJ NN
NP_JJ_JJ_N = "'(NP<1/JJ/<2/^JJ/<3/^NN|DT|PRP|CD/!<4__)!>__'"
NP_JJ_JJ_N_P = f"'(NP<1/JJ/<2/^JJ/<3/^NN|DT|PRP|CD/<4{P}!<5__)!>__'"

# JJ NN NN
NP_JJ_N_N = "'(NP<1/JJ/<2/^NN|DT|PRP|CD/<3/^NN|DT|PRP|CD/!<4__)!>__'"
NP_JJ_N_N_P = f"'(NP<1/JJ/<2/^NN|DT|PRP|CD/<3/^NN|DT|PRP|CD/<4{P}!<5__)!>__'"

# det NN JJ 
NP_3_D_N_JJ = f"'(NP[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}][<2/^JJ/|<2{ADJP_S1}]!<3__)!>__'"
NP_3_D_N_JJ_P = f"'(NP[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}][<2/^JJ/|<2{ADJP_S1}]<3{P}!<4__)!>__'"

#Imperative VP: do this, Mike!

VP_Imp_S = f"'(S<1(VP<1/^VB/[<2{NP_S1}|<2{NP_S2}|<2{NP_S3}]<3{P_MID}[<4{NP_S1}|<4{NP_S2}|<4{NP_S3}]!<5__))!>__'"
VP_Imp_S_P = f"'(S<1(VP<1/^VB/[<2{NP_S1}|<2{NP_S2}|<2{NP_S3}]<3{P_MID}[<4{NP_S1}|<4{NP_S2}|<4{NP_S3}]!<5__)<2{P}!<3__)!>__'"

#Simple sentence, intranstive

S_SV = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}]<2{VP_S}<3{P})!>__'"

#Simple sentence, intranstive, w/ adjective mod on S: the cute girl runs, the best follows

S_SV_JJ = f"'(S[<1{NP_S_D_JJ}|<1{NP_S_JJ}|<1{NP_S_JJS}|<1{NP_S_D_JJS}]<2{VP_S}<3{P})!>__'"

#Simple sentence, transitive

S_SVO = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}]<2{VP_SO}<3{P})!>__'"

##Simple sentence, transitive, w/ adjective mod on 0: She is a cute girl, Mike answers the pink phone

S_SVO_OJJ = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}][<2{VP_SO_JJ}|<2{VP_SO_JJS}]<3{P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S: the cute girl answers the phone, the best follows

S_SVO_SJJ = f"'(S[<1{NP_S_D_JJ}|<1{NP_S_JJ}|<1{NP_S_JJS}|<1{NP_S_D_JJS}]<2{VP_SO}<3{P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S and O: the cute girl answers the pink phone

S_SVO_SJJ_OJJ = f"'(S[<1{NP_S_D_JJ}|<1{NP_S_JJ}|<1{NP_S_JJS}|<1{NP_S_D_JJS}][<2{VP_SO_JJ}|<2{VP_SO_JJS}]<3{P})!>__'"

#Simple sentence, ditransitive

S_SVOO = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}]<2{VP_SOO}<3{P})!>__'"

#TODO: ditrans w/ adjective modifiers

#She is smart

#TODO: other combinations e.g Smart girl is tall, smart girl is the best

S_SVC = f"'(S[<1{NP_S1}|<1{NP_S2}|<1{NP_S3}]<2{VP_SC}<3{P})!>__'"

#TODO: Ungrammatical stuff like Noun ADJP

###################################################################### Perturbed patterns with high yield ######################################################################

# Simple sentences w/ interjections

#Simple sentence, intranstive

S_U_SV = f"'(S[<1(INTJ<:UH)|<1UH][<2{NP_S1}|<2{NP_S2}|<2{NP_S3}]<3{VP_S}<4{P})!>__'"

#Simple sentence, intranstive, w/ adjective mod on S: the cute girl runs, the best follows

S_U_SV_JJ = f"'(S[<1(INTJ<:UH)|<1UH][<2{NP_S_D_JJ}|<2{NP_S_JJ}|<2{NP_S_JJS}|<2{NP_S_D_JJS}]<3{VP_S}<4{P})!>__'"

#Simple sentence, transitive

S_U_SVO = f"'(S[<1(INTJ<:UH)|<1UH][<2{NP_S1}|<2{NP_S2}|<2{NP_S3}]<3{VP_SO}<4{P})!>__'"

##Simple sentence, transitive, w/ adjective mod on 0: She is a cute girl, Mike answers the pink phone

S_U_SVO_OJJ = f"'(S[<1(INTJ<:UH)|<1UH][<2{NP_S1}|<2{NP_S2}|<2{NP_S3}][<3{VP_SO_JJ}|<3{VP_SO_JJS}]<4{P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S: the cute girl answers the phone, the best follows

S_U_SVO_SJJ = f"'(S[<1(INTJ<:UH)|<1UH][<2{NP_S_D_JJ}|<2{NP_S_JJ}|<2{NP_S_JJS}|<2{NP_S_D_JJS}]<3{VP_SO}<4{P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S and O: the cute girl answers the pink phone

S_U_SVO_SJJ_OJJ = f"'(S[<1(INTJ<:UH)|<1UH][<2{NP_S_D_JJ}|<2{NP_S_JJ}|<2{NP_S_JJS}|<2{NP_S_D_JJS}][<3{VP_SO_JJ}|<3{VP_SO_JJS}]<4{P})!>__'"

#Simple sentence, ditransitive

S_U_SVOO = f"'(S[<1(INTJ<:UH)|<1UH][<2{NP_S1}|<2{NP_S2}|<2{NP_S3}]<3{VP_SOO}<4{P})!>__'"

#TODO: ditrans w/ adjective modifiers

#She is smart

#TODO: other combinations e.g Smart girl is tall, smart girl is the best

S_U_SVC = f"'(S[<1(INTJ<:UH)|<1UH][<2{NP_S1}|<2{NP_S2}|<2{NP_S3}]<3{VP_SC}<4{P})!>__'"


#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Single item
    "NP_1": NP_1,
    "NP_1_P": NP_1_P,
    "NP_1_JJ": NP_1_JJ,
    "NP_1_JJ_P": NP_1_JJ_P,
    "NP_1_VB": NP_1_VB,
    "NP_1_VB_P": NP_1_VB_P,
    "VP_1": VP_1,
    "VP_1_P": VP_1_P,
    "ADJP_1": ADJP_1,
    "ADJP_1_P": ADJP_1_P,
    # 2 items
    "NP_2_D": NP_2_D,
    "NP_2_D_P": NP_2_D_P,
    "NP_2_ADJP": NP_2_ADJP,
    "NP_2_ADJP_P": NP_2_ADJP_P,
    "VP_Imp": VP_Imp,
    "VP_Imp_P": VP_Imp_P,
    "VP_Imp_S": VP_Imp_S,
    "VP_Imp_S_P": VP_Imp_S_P,
    # 3 items
    "NP_3_D_JJ_N": NP_3_D_JJ_N,
    "NP_3_D_N_JJ": NP_3_D_N_JJ,
    "NP_3_D_N_JJ_P": NP_3_D_N_JJ_P,
    "NP_3_D_JJ_N_P": NP_3_D_JJ_N_P,
    "NP_JJ_JJ_N": NP_JJ_JJ_N,
    "NP_JJ_JJ_N_P": NP_JJ_JJ_N_P,
    "NP_JJ_N_N": NP_JJ_N_N,
    "NP_JJ_N_N_P": NP_JJ_N_N_P,
    # Simple sentences
    "S_SV": S_SV,
    "S_SV_JJ": S_SV_JJ,
    "S_SVO": S_SVO,
    "S_SVO_SJJ": S_SVO_SJJ,
    "S_SVO_OJJ": S_SVO_OJJ,
    "S_SVO_SJJ_OJJ": S_SVO_SJJ_OJJ,
    "S_SVOO": S_SVOO,
    "S_SVC": S_SVC,
    # Simple sentences w/ 
    "S_U_SV": S_U_SV,
    "S_U_SV_JJ": S_U_SV_JJ,
    "S_U_SVO": S_U_SVO,
    "S_U_SVO_SJJ": S_U_SVO_SJJ,
    "S_U_SVO_OJJ": S_U_SVO_OJJ,
    "S_U_SVO_SJJ_OJJ": S_U_SVO_SJJ_OJJ,
    "S_U_SVOO": S_U_SVOO,
    "S_U_SVC": S_U_SVC,
    # To be discarded?
    "INTJ_1": INTJ_1,
    "INTJ_1_P": INTJ_1_P
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