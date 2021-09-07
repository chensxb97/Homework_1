#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re
import nltk
import sys
import getopt
import math

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print("building language models...")

    #Language model and counts
    LM = {'malaysian':{},'indonesian':{},'tamil':{}} 
    LM_counts = {'malaysian':0,'indonesian':0,'tamil':0} 

    input_text = open(in_file,encoding='utf8')

    #Format of line of text: [label][space][sentence]
    for line in input_text: 
        list_words = line.split()
        label = list_words[0] 
        sentence = (' '.join(list_words[1:])).strip()
        grams = []

        #Generate 4-grams, each stored in a tuple
        for i in range(len(sentence) - 3):
            grams.append((tuple(sentence[i:i+4]))) 

        #Add counts and perform add-one smoothing
        for gram in grams:
            for language in LM:
                if gram not in LM[language]: 
                    LM[language][gram] = 1
                    LM_counts[language] += 1
            LM[label][gram] += 1
            LM_counts[label] += 1

    #Convert each 4-gram counts to probabilities
    for language in LM:
        total = float(LM_counts[language])
        for gram in LM[language]:
            LM[language][gram]/=total

    input_text.close()

    return LM

def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")

    #Input test, output predictions, model files
    input_test = open(in_file,encoding='utf8')
    output_pred = open(out_file,'w')
    model = LM

    for line in input_test:
        sentence = line.strip()
        grams = []
        total_grams = 0
        grams_not_in_model=[]
        total_not_in_model = 0
        probability = {}

        # Obtaining all 4-grams and checking if gram exist in the model
        for i in range(len(sentence) - 3):
            new_gram = tuple(sentence[i:i+4])
            total_grams += 1
            if new_gram not in model['malaysian']:
                total_not_in_model += 1
                grams_not_in_model.append(new_gram)
            else:
                grams.append(new_gram)
                
        # Calculate probability for each language
        for language in model:
            calc=[]
            for gram in grams:
                if gram in grams_not_in_model:
                    continue
                else: calc.append(model[language][gram])
            probability[language]=0.0 
            #Normalise product of probabilities to log-10 scale
            if calc: 
                for value in calc:
                    probability[language]+=math.log10(value) 

        #Making the prediction
        highest_score = probability['malaysian']
        prediction = 'malaysian'
        for key,value in probability.items():
            if value > highest_score:
                highest_score= value
                prediction = key

        #Threshold of 75% unknown text and checking if all the probability values are equal, classify as 'other'
        if (total_not_in_model/float(total_grams) > 0.75) or (probability['malaysian']==probability['indonesian'] and probability['indonesian'] == probability['tamil']):
            prediction = 'other'

        #Output predictions
        output_pred.write("{} {}".format(prediction,line))

    output_pred.close()
    input_test.close()

def usage():
    print(
        "usage: "
        + sys.argv[0]
        + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"
    )


input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "b:t:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-b":
        input_file_b = a
    elif o == "-t":
        input_file_t = a
    elif o == "-o":
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)