#isnt it, wasnt it?? tag questionss

"""
This script analyzes a single plain text file.  

It counts the occurrences of the following structures.
"""

import sys, subprocess, re
import a_simple_categories as sc
import a2_pos_adv_categories as pvc

# simple questions

# Yes/No Questions: Is she coming, can he swim?

S_SQ_yn = f"'(SQ<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{sc.S_VP}|<3{sc.S_VP_O}|<3{sc.S_VP_OO}]<4{sc.P})!>__'"

# W/ JJ: Is she sad, can you be happy?

S_SQ_yn_2 = f"'(SQ<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{sc.S_VP_C}|<3{sc.S_NP_D_JJ}|<3{sc.S_NP_JJ}|<3{sc.S_NP_JJS}|<3{sc.S_NP_D_JJS}|<3{sc.S_ADJP}]<4{sc.P})!>__'"

# W/ a demonstrative: Is that a hat


S_SQ_yn_3 = f"'(SQ<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{sc.S_NP_1}|<3{sc.S_NP_2}|<3{sc.S_NP_3}]<4{sc.P})!>__'"

#Shall we go hide

S_SQ_yn_4 = f"'(SQ<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/VB/<2(VP<:VB)!<4__)<4{sc.P})!>__'"

#Can I try now?

S_SQ_yn_5 = f"'(SQ<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/^VB/[<2{pvc.S_ADVP}|<2{pvc.S_ADVP_2}])<4{sc.P})!>__'"

#Can I try it now?

S_SQ_yn_6 = f"'(SQ<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{pvc.S_ADVP}|<3{pvc.S_ADVP_2}])<4{sc.P})!>__'"

#WHNP WHADVP WHADJP 

#What?, how long? what kind of scientist?

S_SBARQ_1 = f"'(SBARQ<1(/WH|WP|WRB/)<2{sc.P})!>__'"

#Why this?

S_SBARQ_2 = f"'(SBARQ<1/WH/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{sc.P})!>__'"

#Why not?

S_SBARQ_3 = "'(SBARQ<1/WH/<2RB)!>__'"


# What is your name, 1 verb? copula Q? What is the canonical name
S_SBARQ_4 = f"'(SBARQ<1/WH/<2((SQ|S)<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}|<2{sc.S_ADJP}]!<3__)<3{sc.P})!>__'"

#What do you do, What can you do 2 What is the canonical name
S_SBARQ_5 = f"'(SBARQ<1/WH/<2((SQ|S)<1(/VB|MD/)[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{sc.S_VP}|<3{sc.S_VP_O}|<3{sc.S_VP_OO}]!<4__)<3{sc.P})!>__'"

# like what ?

S_SBARQ_6 = f"'(SBARQ<1(VP<1/VB/<2(NP<:/WP/))<2{sc.P})!>__'"

# What she said

S_SBARQ_7 = f"'(SBARQ<1/WH/<2((SQ|S)[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}|<1{sc.S_ADJP}][<3{sc.S_VP}|<3{sc.S_VP_O}|<3{sc.S_VP_OO}]!<4__)<3{sc.P})!>__'"

# What is she doing?

################################Odd ones################################
# Which one

S_NP_Q_1 = "'(NP<1WDT<2CD<3{sc.P})!>__'"



#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Utterance 
    "S_SQ_yn": S_SQ_yn,
    "S_SQ_yn_2": S_SQ_yn_2,
    "S_SQ_yn_3": S_SQ_yn_3,
    "S_SQ_yn_4": S_SQ_yn_4,
    "S_SQ_yn_5": S_SQ_yn_5,
    "S_SQ_yn_6": S_SQ_yn_6,
    "S_SBARQ_1": S_SBARQ_1,
    "S_SBARQ_2": S_SBARQ_2,
    "S_SBARQ_3": S_SBARQ_3,
    "S_SBARQ_4": S_SBARQ_4,
    "S_SBARQ_5": S_SBARQ_5,
    "S_SBARQ_6": S_SBARQ_6,
    "S_SBARQ_7": S_SBARQ_7,
    "S_NP_Q_1": S_NP_Q_1,
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
    with open("tregex_patterns_Qs.txt", "w") as f:
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
