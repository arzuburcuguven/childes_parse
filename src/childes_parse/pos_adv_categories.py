"""
This script analyzes a single plain text file.  

It counts the occurrences of the following structures.
"""
import sys, subprocess, re
import simple_categories as sc


#Simple possesive , e.g. Maggies's, you, something, metal, tends to be on the subject position

S_POS = "(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)"

#NP w possessive e.g. morgan's shirt

NP_POS = "(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/NN|DT|PRP|CD|UH|FW/!<3__)"

NP_POS_D = "(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/NN|DT|PRP|CD|UH|FW/!<3__)"

#NP w possessive and adjective e.g. morgan's green shirt

NP_POS_JJ = "(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/JJ/<3/NN|DT|PRP|CD|UH|FW/!<4__)"

#NP w possessive and noun e.g. morgan's living room

NP_POS_N = "(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/NN|DT|PRP|CD|UH|FW/<3/NN|DT|PRP|CD|UH|FW/!<4__)"

#Single item simple adverb , e.g. Mike, you, something, metal, tends to be on the subject position

S_ADVP = "(ADVP<:/^RB/)"
S_ADVP_2 = "(ADVP<1/^RB/<2/^RB/)"

# POS on Object

VP_SO_POS = f"(VP<1/^VB/[<2{S_POS}|<2{NP_POS}|<2{NP_POS_JJ}|<2{NP_POS_N}]!<3__)"

################################################################################ The Categories ################################################################################ 

## Fragment utterances

POS_1 = f"'({S_POS}!>__)|({NP_POS}!>__)|({NP_POS_JJ}!>__)|({NP_POS_N}!>__)'"
POS_1_P = f"'(NP<1/NN|DT|PRP|CD|UH|FW/<2POS<3{sc.P}!<4__)!>__'" 

POS_D = f"'(NP<1/NN|DT|PRP|CD|UH|FW/<2/^NN|DT|PRP|CD|FW/<3POS<4{sc.P})'"

NP_POS_P = f"'(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/NN|DT|PRP|CD|UH|FW/<3{sc.P})'"
NP_POS_JJ_P = f"'(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/JJ/<3/NN|DT|PRP|CD|UH|FW/<4{sc.P})!>__'"
NP_POS_N_P = f"'(NP<1(NP<1/NN|DT|PRP|CD|UH|FW/<2POS!<3__)<2/NN|DT|PRP|CD|UH|FW/<3/NN|DT|PRP|CD|UH|FW/<4{sc.P})!>__'"

ADVP_1 = f"'{S_ADVP}!>__'"
ADVP_1_P = f"'(ADVP<1/^RB/<2{sc.P}!<3__)!>__'" 

ADVP_2 = f"'{S_ADVP_2}!>__'"
ADVP_2_P = f"'(ADVP<1/^RB/<2/^RB/<3{sc.P}!<4__)!>__'" 

#so fun
ADJP_RB = f"'(ADJP<1/^RB/<2/^JJ/<3/\./!<4__)!>__'"

#very good

ADJP_ADJP_RB = f"'(ADJP<1(ADJP<1/^RB/<2/^JJ/)<2/\./!<3__)!>__'"

#Simple sentence w POS S, intranstive: Her cat runs.

S_SV_pos = f"'(S[<1{S_POS}|<1{NP_POS}|<1{NP_POS_JJ}|<1{NP_POS_N}]<2{sc.S_VP}<3{sc.P})!>__'"

#Simple sentence w POS S, transitive: Her cat eats an apple

S_SVO_S_pos = f"'(S[<1{S_POS}|<1{NP_POS}|<1{NP_POS_JJ}|<1{NP_POS_N}]<2{sc.S_VP_O}<3{sc.P})!>__'"

#Simple sentence, transitive, w/ possesive on 0: She is Mike's girl

S_SVO_O_pos = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2{VP_SO_POS}<3{sc.P})!>__'"

#ADVP and Imperative: Okay, go this way!

S_imp_ADVP = f"'(S<1(ADVP<:/^RB/)<2{sc.S_VP_OO}!<3__)!>__'"
S_imp_ADVP_P = f"'(S<1(ADVP<:/^RB/)<2{sc.S_VP_OO}<3{sc.P}!<4__)!>__'"

#ADVP and Imperative: try again

SV_imp_ADVP = f"'(S<:(VP<1/^VB/[<2{S_ADVP}|<2{S_ADVP_2}]))!>__'"
SV_imp_ADVP_P = f"'(S<1(VP<1/^VB/[<2{S_ADVP}|<2{S_ADVP_2}])<2{sc.P})!>__'"

#Simple sentence w ADVP under VP, intranstive: She runs fast

S_SV_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/^VB/[<2{S_ADVP}|<2{S_ADVP_2}])<3{sc.P})!>__'"

#Simple sentence w ADVP under VP, transitive: She eats the apple fast

S_SVO_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{S_ADVP}|<3{S_ADVP_2}])<3{sc.P})!>__'"

#?They are really ducks

#ADVP directly under S: you almost had it

S_SV_ADVP_direct = f"'(S|SINV[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}][<2{S_ADVP}|<2{S_ADVP_2}]<3(VP<:/^VB/)<4{sc.P})!>__'"
S_SVO_ADVP_direct = f"'(S|SINV[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}][<2{S_ADVP}|<2{S_ADVP_2}]<3{sc.S_VP_OO}<4{sc.P})!>__'"
S_SVOO_ADVP_direct = f"'(S|SINV[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}][<2{S_ADVP}|<2{S_ADVP_2}]<3{sc.S_VP_OO}<4{sc.P})!>__'"

#ADVP initial: Well I see you

S_ADV_SV = f"'(S|SINV[<1{S_ADVP}|<2{S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{sc.S_VP}<4{sc.P})!>__'"
S_ADV_SVO = f"'(S|SINV[<1{S_ADVP}|<2{S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{sc.S_VP_OO}<4{sc.P})!>__'"
S_ADV_SVOO = f"'(S|SINV[<1{S_ADVP}|<2{S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{sc.S_VP_OO}<4{sc.P})!>__'"

#ADVP as subject: here it is

#ADVP initial: Well I see you

S_ADVP_as_S_SV = f"'(S|SINV[<1{S_ADVP}|<1{S_ADVP_2}]<2{sc.S_VP}<3{sc.P})!>__'"
S_ADVP_as_S_SVO = f"'(S|SINV[<1{S_ADVP}|<1{S_ADVP_2}]<2{sc.S_VP_OO}<3{sc.P})!>__'"
S_ADVP_as_S_SVOO = f"'(S|SINV[<1{S_ADVP}|<1{S_ADVP_2}]<2{sc.S_VP_OO}<3{sc.P})!>__'"

#SINV

SINV_ADVP_VP_NP = f"'(SINV[<1{S_ADVP}|<1{S_ADVP_2}]<2(VP<:/VB/)[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}]<4{sc.P})!>__'"

## ADJP < RB

## She is very fast

S_SV_ADJP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/^VB/<2(ADJP<1/^RB/<2/^JJ/!<3__))<3{sc.P})!>__'"

# That is a pretty big boy

S_SV_C_ADJP_RB = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/VB/<2(NP<1/NN|DT|PRP|CD|UH|FW/<2(ADJP<1/^RB/<2/^JJ/)<3/NN|DT|PRP|CD|UH|FW/!<4__)!<3__)<3{sc.P})!>__'"



#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Utterance 
    "POS_1": POS_1,
    "POS_1_P": POS_1_P,
    "POS_D": POS_D,
    "NP_POS_P": NP_POS_P,
    "NP_POS_JJ_P": NP_POS_JJ_P,
    "NP_POS_N_P": NP_POS_N_P,
    "ADVP_1": ADVP_1,
    "ADVP_1_P": ADVP_1_P,
    "ADJP_RB": ADJP_RB,
    "ADJP_ADJP_RB": ADJP_ADJP_RB,
    # Simple sentences
    "S_SV_pos": S_SV_pos,
    "S_SVO_S_pos": S_SVO_S_pos,
    "S_SVO_O_pos": S_SVO_O_pos,
    "S_imp_ADVP": S_imp_ADVP,
    "S_imp_ADVP_P": S_imp_ADVP_P,
    "SV_imp_ADVP": SV_imp_ADVP,
    "SV_imp_ADVP_P": SV_imp_ADVP_P,
    "S_SV_ADVP": S_SV_ADVP,
    "S_SVO_ADVP": S_SVO_ADVP,
    "S_SV_ADVP_direct": S_SV_ADVP_direct,
    "S_SVO_ADVP_direct": S_SVO_ADVP_direct,
    "S_SVOO_ADVP_direct": S_SVOO_ADVP_direct,
    "S_ADV_SV": S_ADV_SV,
    "S_ADV_SVO": S_ADV_SVO,
    "S_ADV_SVOO": S_ADV_SVOO,
    "S_ADVP_as_S_SV": S_ADVP_as_S_SV,
    "S_ADVP_as_S_SVO": S_ADVP_as_S_SVO,
    "S_ADVP_as_S_SVOO": S_ADVP_as_S_SVOO,
    "SINV_ADVP_VP_NP": SINV_ADVP_VP_NP,
    "S_SV_ADJP": S_SV_ADJP,
    "S_SV_C_ADJP_RB": S_SV_C_ADJP_RB
}

if __name__ == "__main__":

    #input file name
    inputFile=sys.argv[1]

    #extract the name of the file being processed
    output=inputFile.split('/')[-1]

    #output file name
    outputFile=open(sys.argv[2],"w")
    print('Processing '+inputFile+'...')

    #write a list of 24 comma-delimited fields to the output file
    fields= ["Filename", "WordCount"] + [key for key in pattern_dict.keys()]
    outputFile.write(",".join(fields) + "\n")

    #list of counts of the patterns
    patterncount=[]

    # Write to a pattern file, list of the rules for UI testing 
    with open("tregex_patterns_pos_adv.txt", "w") as f:
        for name, pattern in pattern_dict.items():
            f.write(f"{name}: {pattern}\n")

    print(len(pattern_dict))
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


