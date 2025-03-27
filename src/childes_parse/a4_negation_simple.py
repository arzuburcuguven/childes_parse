"""
This script analyzes a single plain text file.  

It counts the occurrences of the following structures.
"""

import sys, subprocess, re
import a_simple_categories as sc

# Captures 50: S<1NP<2ADVP<3(VP<(RB</^not|n.*t$/))

#TODO: interjection at end

# neg imperative: do nt go, do not do that, do nt worry

NEG_IMP_SV = f"'(S<1(VP<1(/MD|VB/)<2(RB</^not|n.*t$/)<3(VP<1/VB/))<2{sc.P})!>__'"
NEG_IMP_SVO = f"'(S<1(VP<1(/MD|VB/)<2(RB</^not|n.*t$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))<2{sc.P})!>__'"

# Negated copula NP: VP<1/VB/<2(RB</^not|n't|nt$/)<3NP, she is n't that, she is n't good

NEG_COP_NP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/VB/<2(RB</^not|n.*t$/)[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}])!<3__)!>__'"
NEG_COP_NP_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/VB/<2(RB</^not|n.*t$/)[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}])<3{sc.P})!>__'"

NEG_COP_JJ = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/(^VB)/<2(RB</^not|n.*t$/)<3ADJP)!<3__)!>__'"
NEG_COP_JJ_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/(^VB)/<2(RB</^not|n.*t$/)<3ADJP)<3{sc.P}!<4__)!>__'"

#she is not a good girl

NEG_SV_C_JJ = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1/VB/<2(RB</^not|n.*t$/)[<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}])<3{sc.P})!>__'"

# also with "no" at top

NEG_COP_NP_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/VB/<2(RB</^not|n.*t$/)[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}])!<4__)!>__'"
NEG_COP_NP_P_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/VB/<2(RB</^not|n.*t$/)[<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}])<4{sc.P})!>__'"

NEG_COP_JJ_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/(^VB)/<2(RB</^not|n.*t$/)<3ADJP)!<4__)!>__'"
NEG_COP_JJ_P_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/(^VB)/<2(RB</^not|n.*t$/)<3ADJP)<4{sc.P}!<5__)!>__'"

#I do not know

NEG_SV = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1(/MD|VB/)<2(RB<:/^not|n.*t$/)<3(VP<:/VB/))!<3__)!>__'"
NEG_SV_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<:/VB/))<3{sc.P}!<4__)!>__'"

# you cant have that, he does nt have a foot

NEG_SVO = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1(/MD|VB/)<2(RB<:/^not|n.*t$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))!<3__)!>__'"
NEG_SVO_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))<3{sc.P}!<4__)!>__'"

# also with "no" at top

NEG_SVO_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))!<4__)!>__'"
NEG_SVO_P_U = f"'(S[<1(INTJ<:UH)|<1UH|<1RB][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1(/MD|VB/)<2(RB<:/^(not|n.*t)$/)<3(VP<1/VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]))<4{sc.P}!<5__)!>__'"

#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Utterance 
    "NEG_IMP_SV": NEG_IMP_SV,
    "NEG_IMP_SVO": NEG_IMP_SVO,
    "NEG_COP_NP": NEG_COP_NP,
    "NEG_COP_NP_P": NEG_COP_NP_P,
    "NEG_COP_JJ": NEG_COP_JJ,
    "NEG_COP_JJ_P": NEG_COP_JJ_P,
    "NEG_SV_C_JJ": NEG_SV_C_JJ,
    "NEG_COP_NP_U": NEG_COP_NP_U,
    "NEG_COP_NP_P_U": NEG_COP_NP_P_U,
    "NEG_COP_JJ_U": NEG_COP_JJ_U,
    "NEG_COP_JJ_P_U": NEG_COP_JJ_P_U,
    "NEG_SV": NEG_SV,
    "NEG_SV_P": NEG_SV_P,
    "NEG_SVO": NEG_SVO,
    "NEG_SVO_P": NEG_SVO_P,
    "NEG_SVO_U": NEG_SVO_U,
    "NEG_SVO_P_U": NEG_SVO_P_U
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
    with open("tregex_patterns_neg.txt", "w") as f:
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



