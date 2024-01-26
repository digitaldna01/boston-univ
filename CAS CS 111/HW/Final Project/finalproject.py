#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:17:37 2019

@author: leejaehong
"""
import math

class TextModel:
    """ blueprint for objects that model a body of text
    """
    def __init__(self,model_name):
        """ constructs a new TextModel object by accepting a string model_name
            as a parameter and initializing the following three attributes:
            name, words, word_lengths
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}
        
    def __repr__(self):
        """ Return a string representation of the TextModel.
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) +'\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of punctuation: ' + str(len(self.punctuation))
        return s 
    
    def add_string(self, s):
        """ Analyzes the string txt and adds its pieces to all of the 
            dictionaries in this text model.
        """
        
        # Add code to clean the text and split it into a list of words.
        # *Hint:* Call one of the functions you have already written!
        
        dot = s.split('. ')
        for w in dot:
            m = 1
            for z in w:
                if z == ' ':
                    m += 1
            if m not in self.sentence_lengths:
                self.sentence_lengths[m] = 1
            else:
                self.sentence_lengths[m] +=1

        
        
        word_list = clean_text(s)
        pun_list = punc_text(s)
        # Template for updating the words dictionary.
        
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
            # Update self.words to reflect w
            # either add a new key-value pair for w
            # or update the existing key-value pair.

    # Add code to update other feature dictionaries.
        for l in word_list:
            if len(l) not in self.word_lengths:
                self.word_lengths[len(l)] = 1
            else:
                self.word_lengths[len(l)] += 1
            
        for s in word_list:
            b = stem(s)
            if b not in self.stems:
                self.stems[b] = 1
            else:
                self.stems[b] += 1
                
                
        
        for p in pun_list:
            if p not in self.punctuation:
                self.punctuation[p] = 1
            else:
                self.punctuation[p] += 1 
    
                
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to 
            the model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        
        for line in f:
            line = line[:-1]
            self.add_string(line)
            
    def save_model(self):
        """ saves the TextModel object self by writing its various feature 
            dictionaries to files. There will be one file written for each 
            feature dictionaries to files.
        """
        filename = self.name + '_' + 'words'
        f = open(filename, 'w')
        f.write(str(self.words))
        f.close()
        
        filename2 = self.name + '_' + 'word_lengths'
        f1 = open(filename2, 'w')
        f1.write(str(self.word_lengths))
        f1.close()
        
        filename3 = self.name + '_' + 'stems'
        f2 = open(filename3, 'w')
        f2.write(str(self.stems))
        f2.close()
        
        filename4 = self.name + '_' + 'sentence_lengths'
        f3 = open(filename4, 'w')
        f3.write(str(self.sentence_lengths))
        f3.close()
        
        filename5 = self.name + '_' + 'punctuation'
        f4 = open(filename5, 'w')
        f4.write(str(self.punctuation))
        f4.close()
        
        
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from
            their files and assigns them to the attributes of the called 
            TextModel.
        """
        filename = self.name + '_' + 'words'
        f = open(filename, 'r')
        s_str = f.read()
        f.close()
        
        self.words = dict(eval(s_str))
        
        filename1 = self.name + '_' + 'word_lengths'
        f1 = open(filename1, 'r')
        s_str1 = f1.read()
        f1.close()
        
        self.word_lengths = dict(eval(s_str1))
        
        filename2 = self.name + '_' + 'stems'
        f2 = open(filename2, 'r')
        s_str2 = f2.read()
        f2.close()
        
        self.stems = dict(eval(s_str2))
        
        filename3 = self.name + '_' + 'sentence_lengths'
        f3 = open(filename3, 'r')
        s_str3 = f3.read()
        f3.close()
        
        self.sentence_lengths = dict(eval(s_str3))
            
        filename4 = self.name + '_' + 'punctuation'
        f4 = open(filename4, 'r')
        s_str4 = f4.read()
        f4.close()
        
        self.punctuation = dict(eval(s_str4))
        
    def similarity_scores(self, other):
        """ computes and returns a list of log similiarity scores measuring the
            similarity of self and other - one score for each type of feature
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_score = compare_dictionaries(other.punctuation, self.punctuation)
        
      
        
        
        return [word_score, word_lengths_score, stems_score, sentence_lengths_score, punctuation_score]
    
    def classify(self, source1, source2):
        """ compares the called TextModel object(self) to two other "source" 
            textModel objects (source1 and source2) and determines which of 
            these other TextModels is the more likely source of the called 
            TextModel.
        """
        scores1 = source1.similarity_scores(self)
        scores2 = source2.similarity_scores(self)
        
        print('scores for',source1.name,':',scores1)
        print('scores for',source2.name,':',scores2)
        
        sum1 = 0
        sum2 = 0
        
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                sum1 += 1
            else:
                sum2 += 1
                
        if sum1 > sum2:
            print('mystery is more likely to have come from', source1.name )
        else:
            print('mystery is more likely to have come from', source2.name )
        
    
def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list 
        containing the words in txt after it has been "cleaned"
    """
    s = txt.lower()
    new = ''
    for i in s:
        if i not in 'qwertyuiopasdfghjklzxcvbnm 1234567890':
            pass
        else:
            new += i
            
    return new.split()

def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}   # Create a sample dictionary.
    f = open(filename, 'w')      # Open file for writing.
    f.write(str(d))              # Writes the dictionary to the file.
    f.close()  

def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    f = open(filename, 'r')    # Open for reading.
    d_str = f.read()           # Read in a string that represents a dict.
    f.close()

    d = dict(eval(d_str))      # Convert the string to a dictionary.

    print("Inside the newly-read dictionary, d, we have:")
    print(d)
    
def stem(s):
    """ accepts a string as a parameter and then return the stem of s. 
        stem of a word is the root part of the word, which excludes any 
        prefixes and suffixes.
    """
    if (len(s) > 1) and (s[-1] != 's'):
        if (len(s) > 5 ) and (s[-3:] == 'ing'):
            if s[-4] == s[-5] and s[-5] == 'm':
                s = s[:-4]
            else:
                s = s[:-3]
                
        elif s[-2:] == 'er' or s[-2:] == 'al' or s[-2:] == 'ac' or s[-2:] == 'ar' or s[-2:] == 'or' or s[-2:] == 'ed':
            s = s[:-2]
            
        elif s[-4:] == 'able' or s[-4:] == 'sion' or s[-4:] == 'tion' or s[-4:] == 'ship' or s[-4:] == 'ment':
            if s[-4:] == 'sion':
                s = s[:-3]
            else:
                s = s[:-4]
                
    elif len(s) > 1:
        s = stem(s[:-1])
    
    return s
                
                
    
def punc_text(txt):
    """ takes a string of text txt as a parameter and returns a list 
        conataining the words, which is punctuation 
    """
    new = ''
    for i in txt:
        if i not in '.!?"[](),;:{}/<>-_':
            pass
        else:
            new += i
    
    return new.split()
        
def compare_dictionaries(d1, d2):  
    """ take two feature dictionaries d1 and d2 as inputs, and it should 
        compute and return their log similarity score. 
    """ 
    score = 0
    total = 0
    
    for w in d1:
        total += d1[w]
    
    for w in d2:
        if w in d1:
            score += math.log(d1[w] / total) * d2[w]
        else:
            score += math.log(0.5 / total) * d2[w]
    
    return score


def test():
    """ test the sample """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)


def run_tests():
    """ compare two texts to mystery and get which one is more likely has the 
        same author 
    """
    
    source1 = TextModel('Sherlock_Holmes')
    source1.add_file('sherlock_holmes.txt')

    source2 = TextModel('Arsene_Lupin')
    source2.add_file('Arsene_Lupin.txt')

    new1 = TextModel('Treasure_Island')
    new1.add_file('Treasure_Island.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('Life_of_Pie')
    new2.add_file('_life_of_pi_full_text_pdf.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('Moby_dick')
    new3.add_file('moby_dick.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('Bill')
    new4.add_file('Bill of Rights.txt')
    new4.classify(source1, source2)
    
    new5 = TextModel('Constitution')
    new5.add_file('Constitution.txt')
    new5.classify(source1, source2)
    
    new6 = TextModel('Trump')
    new6.add_file('Trump Election Speech.txt')
    new6.classify(source1, source2)
    
    new7 = TextModel('Arsene_Lupin')
    new7.add_file('Arsene_Lupin.txt')
    new7.classify(source1, source2)
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    