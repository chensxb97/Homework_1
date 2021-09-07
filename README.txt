This is the README file for A0228375X's submission 
Email: e0673208@u.nus.edu

== Python Version ==

I'm using Python Version 3.7.4 for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general. A few paragraphs 
are usually sufficient.

This program serves to build a 4-gram language model that is able to predict the language used in a line of text. 

= Building the model =

The 4-grams are extracted from each line of text in the training input file.
Each 4-gram, together with their corresponding counts and after applying add-one smoothing, 
are pushed into a dictionary of dictionaries. An additional dictionary is created to track 
the total number of 4-grams recorded per language. After storing all the 4-grams and their 
individual counts, each count is converted to its probability by dividing each count 
by the total number of 4-grams per language as tracked by the additional dictionary. 

Below is the skeleton of the language model.

{
  'malaysian':{ (4-gram-1): probability of 4-gram-1, 
		(4-gram-2): probability of 4-gram-2,
		... ,
		(4-gram-n): probability of 4-gram-n
	      },

 'indonesian':{
		 ...

	      },

 'tamil':{ 
		...
	  } 

}

= Testing the model =

To test the model, we extract 4-grams from each line of text in the test input file and obtain the
product of probabilities for the observed n-grams for each language. As each 4-gram's 
probability value is very small(of orders -5 to -7), the final product can become so small till it gets
read as 0 in the program which is undesirable for comparison.

To resolve this problem, we will perform logarithmic normalisation on the probabilities 
using a common base-10. We will be comparing the logarithmic of the product of probabilities. 
An example of the normalisation is as follows:

Before: P('Hello') = P(('H,'e','l','l')) * P('e','l',' l','o')

After: log10(P('Hello')) = log10(P(('H,'e','l','l'))) + log10(P('e','l',' l','o'))

The language with the highest logarithmic product will be assigned as the prediction to the line of text. 
The output predictions file will contain the list of predictions using the following format:

[Prediction][Space][Line of text]

To classify lines of text that do not belong to any of the 3 languages, we can first check if 
the 3 logarithmic products are the same, where there is no clear winner. Another condition to check 
is the percentage of (unknown ngrams/ngrams in language model). This determines the proportion of 
alien language in the line of text. After some experimentation, I have arrived at an optimal threshold 
of (>75%) to classify these lines as 'other' languages.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

build_test_LM.py: Python script containing two functions(build_LM and test_LM) that each builds 
and tests the language model respectively
README.txt: Documentation text file

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0228375X, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[] I, A0228375X, did not follow the class rules regarding homework
assignment, because of the following reason:

NIL

I suggest that I should be graded as follows:

NIL

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

NIL