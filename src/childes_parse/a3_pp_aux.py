"""
This script analyzes a single plain text file.  

It counts the occurrences of the following structures.


Verb Phrase (VP) – PPs often function as adjuncts or arguments of verbs.
Example: "She looked [at the painting]."
Noun Phrase (NP) – PPs can modify nouns (often expressing possession, description, or location).
Example: "The book [on the table] is mine."
Adjective Phrase (ADJP) – Some adjectives take PP complements.
Example: "He is proud [of his work]."
Another Prepositional Phrase (PP) – PPs can be recursively embedded.
Example: "He sat [next to the chair [by the window]]."
Clause (S or CP) – PPs can appear as adjuncts in clauses.
Example: "[After the meeting], we left."
Adverbial Phrase (ADVP) – Less common, but possible in complex modification.
Example: "Soon [after the event], he arrived."

"""
import sys, subprocess, re
import a_simple_categories as sc
import a2_pos_adv_categories as pa

#Single preposition

S_PP = "(PP<:/IN|RB|TO/)"

#Simple prepositional phrase IN + NP , e.g. on you, for something, at the table

S_PP_NP = f"(PP<1/IN|RB|TO/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]!<3__)"

# PP → IN ADJP, e.g for dead

S_PP_ADJP = f"(PP<1/IN|RB|TO/[<2{sc.S_ADJP}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}<2{sc.S_NP_JJS}<2{sc.S_NP_D_JJS}]!<3__)"

# PP → IN ADVP, e.g until recently

S_PP_ADVP = f"(PP<1/IN|RB|TO/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]!<3__)"

# PP over POS

S_PP_POS = f"(PP<1/IN|RB|TO/[<2{pa.S_POS}|<2{pa.NP_POS}|<2{pa.NP_POS_D}<2{pa.NP_POS_JJ}<2{pa.NP_POS_N}]!<3__)"

# PP over PP e.g from behind the curtain

S_PP_PP = f"(PP<1/IN|RB|TO/[<2{S_PP}|<2{S_PP_NP}|<2{S_PP_ADJP}|<2{S_PP_ADVP}|<{S_PP_POS}]!<3__)"

# ADJP

# ADJP -> JJ PP : good at that

#S_ADJP_PP = (ADJP|ADJ<1/^JJ/) < JJ < PP

# ADJP -> RB JJ PP : very familiar with eggs

# VPs

#simple VP w/ PP child

S_VP_PP = f"(VP<1/^VB/[<2{S_PP}|<2{S_PP_NP}|<2{S_PP_ADJP}|<2{S_PP_ADVP}|<2{S_PP_PP}|<2{S_PP_POS}]!<3__)"

#simple VP w/ a simple NP and PP child

S_VP_O_PP = f"(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{S_PP}|<3{S_PP_NP}|<3{S_PP_ADJP}|<3{S_PP_ADVP}|<3{S_PP_PP}|<3{S_PP_POS}]!<4__)"

#simple VP w/ simple ADJP child

S_VP_C_PP = f"(VP<1/^VB/<2{sc.S_ADJP}[<3{S_PP}|<3{S_PP_NP}|<3{S_PP_ADJP}|<3{S_PP_ADVP}|<3{S_PP_PP}|<3{S_PP_POS}]!<4__)"

#simple VP w/ simple JJ child

S_VP_O_JJ_PP = f"(VP<1/^VB/[<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}][<3{S_PP}|<3{S_PP_NP}|<3{S_PP_ADJP}|<3{S_PP_ADVP}|<3{S_PP_PP}|<3{S_PP_POS}]!<4__)"

S_VP_O_JJS_PP = f"(VP<1/^VB/[<2{sc.S_NP_JJS}|<2{sc.S_NP_D_JJS}][<3{S_PP}|<3{S_PP_NP}|<3{S_PP_ADJP}|<3{S_PP_ADVP}|<3{S_PP_PP}|<3{S_PP_POS}]!<4__)"

# VP -> VB ADVP PP: walked slowly to me
 
S_VP_ADVP_PP = f"(VP<1/^VB/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}][<3{S_PP}|<3{S_PP_NP}|<3{S_PP_ADJP}|<3{S_PP_ADVP}|<3{S_PP_PP}|<3{S_PP_POS}]!<4__)"

# VP -> VB NP ADVP PP: walked him slowly to me

S_VP_NP_ADVP_PP = f"(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}][<4{S_PP}|<4{S_PP_NP}|<4{S_PP_ADJP}|<4{S_PP_ADVP}|<4{S_PP_PP}|<4{S_PP_POS}]!<5__)"

# VP -> VB PP ADVP: walk to me please

S_VP_PP_ADVP = f"(VP<1/^VB/[<2{S_PP}|<2{S_PP_NP}|<2{S_PP_ADJP}|<2{S_PP_ADVP}|<2{S_PP_PP}|<2{S_PP_POS}][<3{pa.S_ADVP}|<3{pa.S_ADVP_2}]!<4__)"

# VP -> VB NP ADVP PP: walked him to me again

S_VP_NP_PP_ADVP = f"(VP<1/^VB/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}][<3{S_PP}|<3{S_PP_NP}|<3{S_PP_ADJP}|<3{S_PP_ADVP}|<3{S_PP_PP}|<3{S_PP_POS}][<4{pa.S_ADVP}|<4{pa.S_ADVP_2}]!<5__)"

# VP -> VB ADJP, then PP mod on JJ

#S_VP_C = f"(VP<1/^VB/<2{S_ADJP}!<3__)"


################################################################################ The Categories ################################################################################ 

########## Utterances 

#Simple prepositional phrase IN + NP , e.g. on you, for something, at the table

PP_NP = f"'(PP<1/IN|RB|TO/[<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{sc.P}!<4__)!>__'"

# PP → IN ADJP, e.g for dead

PP_ADJP = f"'(PP<1/IN|RB|TO/[<2{sc.S_ADJP}|<2{sc.S_NP_D_JJ}|<2{sc.S_NP_JJ}<2{sc.S_NP_JJS}<2{sc.S_NP_D_JJS}]<3{sc.P}!<4__)!>__'"

# PP → IN ADVP, e.g until recently

PP_ADVP = f"'(PP<1/IN|RB|TO/[<2{pa.S_ADVP}|<2{pa.S_ADVP_2}]<3{sc.P}!<4__)!>__'"

# PP over POS

PP_POS = f"'(PP<1/IN|RB|TO/[<2{pa.S_POS}|<2{pa.NP_POS}|<2{pa.NP_POS_D}<2{pa.NP_POS_JJ}<2{pa.NP_POS_N}]<3{sc.P}!<4__)!>__'"

# PP over PP e.g from behind the curtain

PP_PP = f"'(PP<1/IN|RB|TO/[<2{S_PP}|<2{S_PP_ADJP}|<2{S_PP_ADVP}|<{S_PP_POS}]<3{sc.P}!<4__)!>__'"

# Subjectless 

VP_PP_all = f"'(S[<1{S_VP_PP}|<1{S_VP_O_PP}|<1{S_VP_C_PP}|<1{S_VP_O_JJ_PP}|<1{S_VP_O_JJS_PP}|<1{S_VP_ADVP_PP}|<1{S_VP_NP_ADVP_PP}|<1{S_VP_PP_ADVP}|<1{S_VP_NP_PP_ADVP}]<2{sc.P})!>__'"

########## Sentences

#Imperative VP: put this back, Mike!

S_Imp_PP = f"'(S<1{S_VP_O_PP}<2{sc.P}!<3__)!>__'"

# Intransitive w/ adjunct: She runs for me

S_SV_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2{S_VP_PP}<3{sc.P})!>__'"

#Simple sentence, intranstive, w/ adjective mod on S: the cute girl runs for me, the best follows at the road

S_SV_JJ_PP = f"'(S[<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2{S_VP_PP}<3{sc.P})!>__'"

#Simple sentence, transitive

S_SVO_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2{S_VP_O_PP}!<3__)!>__'"
S_SVO_PP_P = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2{S_VP_O_PP}<3{sc.P})!>__'"

##Simple sentence, transitive, w/ adjective mod on 0: She is a cute girl, Mike answers the pink phone

S_SVO_OJJ_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}][<2{S_VP_O_JJ_PP}|<2{S_VP_O_JJS_PP}]<3{sc.P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S: the cute girl answers the phone, the best follows

S_SVO_SJJ_PP = f"'(S[<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}]<2{S_VP_O_PP}<3{sc.P})!>__'"

#Simple sentence, transitive, w/ adjective mod on S and O: the cute girl answers the pink phone

S_SVO_SJJ_OJJ = f"'(S[<1{sc.S_NP_D_JJ}|<1{sc.S_NP_JJ}|<1{sc.S_NP_JJS}|<1{sc.S_NP_D_JJS}][<2{S_VP_O_JJ_PP}|<2{S_VP_O_JJS_PP}]<3{sc.P})!>__'"

#Simple sentence, ditransitive

#S_SVOO = f"'(S[<1{S_NP_1}|<1{S_NP_2}|<1{S_NP_3}]<2{S_VP_OO}<3{P})!>__'"

# She walked slowly to me

S_SV_ADVP_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2{S_VP_ADVP_PP}<3{sc.P})!>__'"

#She walked him slowly to me S_VP_NP_ADVP_PP
S_SV0_ADVP_PP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2{S_VP_NP_ADVP_PP}<3{sc.P})!>__'"

# She walked to me slowly
S_SV_PP_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2{S_VP_PP_ADVP}<3{sc.P})!>__'"


# She walked him to me slowly
S_SVO_PP_ADVP = f"'(S[<1{sc.S_NP_1}|<1{sc.S_NP_2}|<1{sc.S_NP_3}]<2{S_VP_NP_PP_ADVP}<3{sc.P})!>__'"

# ADVP Initial

S_ADVP_SVO_PP_P = f"'(S|SINV[<1{pa.S_ADVP}|<1{pa.S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{S_VP_O_PP}<4{sc.P})!>__'"

S_ADVP_SV_PP_P = f"'(S|SINV[<1{pa.S_ADVP}|<1{pa.S_ADVP_2}][<2{sc.S_NP_1}|<2{sc.S_NP_2}|<2{sc.S_NP_3}]<3{S_VP_PP}<4{sc.P})!>__'"

# You are good at that





#list of patterns to search for
#here we can combine the cats by item count, but maybe seperate the ADJP_1p as the "okay" confounds the counts
pattern_dict = {
    #Single item
    "PP_NP": PP_NP,
    "PP_ADJP": PP_ADJP,
    "PP_ADVP": PP_ADVP,
    "PP_POS": PP_POS,
    "PP_PP": PP_PP,
    "VP_PP_all": VP_PP_all,
    "S_Imp_PP": S_Imp_PP,
    "S_SV_PP": S_SV_PP,
    "S_SVO_PP": S_SVO_PP,
    "S_SVO_PP_P": S_SVO_PP_P,
    "S_SVO_OJJ_PP": S_SVO_OJJ_PP,
    "S_SVO_SJJ_PP": S_SVO_SJJ_PP,
    "S_SVO_SJJ_OJJ": S_SVO_SJJ_OJJ,
    "S_SV_ADVP_PP": S_SV_ADVP_PP,
    "S_SV0_ADVP_PP": S_SV0_ADVP_PP,
    "S_SV_PP_ADVP": S_SV_PP_ADVP,
    "S_SV0_PP_ADVP": S_SV_PP_ADVP,
    "S_ADVP_SVO_PP_P": S_ADVP_SVO_PP_P,
    "S_ADVP_SV_PP_P": S_ADVP_SVO_PP_P
}

if __name__ == "__main__":

    # Write to a pattern file, list of the rules for UI testing 
    with open("tregex_patterns_pp_aux.txt", "w") as f:
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
