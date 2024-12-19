import math

# TextModel Class
class TextModel:
    """ TextModel Class
    """
    def __init__(self, model_name):
        """ Initializes atributes
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.character_sequences = {} 
        
    def __repr__(self):
        """ returns a string that includes the name of the model 
            as well as the sizes of the dictionaries for each feature of the text.
        """
        text = "text model name: " + self.name + "\n"
        text += "  number of words: " + str(len(self.words)) + "\n"
        text += "  number of word lengths: " + str(len(self.word_lengths)) + "\n"
        text += "  number of stems: " + str(len(self.stems)) + "\n"
        text += "  number of sentence lengths: " + str(len(self.sentence_lengths)) + "\n"
        text += "  number of character sequences: " + str(len(self.character_sequences))
        return text
    
    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """
        
        # Do not want a clean version of the text
        sentence_lengths_counts = length_sentence(s)
        for count in sentence_lengths_counts:
            if count not in self.sentence_lengths:
                self.sentence_lengths[count] = 1
            else:
                self.sentence_lengths[count] += 1

        for chars in char_sequences(s, 3): #Length of 3
            if chars not in self.character_sequences:
                self.character_sequences[chars] = 1
            else:
                self.character_sequences[chars] += 1
         
        # Wants a clean version of text
        word_list = clean_text(s)
        
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1
                
    def add_file(self, filename):
        """ Adds content from file into model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        content = f.read()
        content = content.replace("\n", "")
        f.close()
        self.add_string(content)
        
    def save_model(self):
        """ Saves the models dictionaries to a file
        """
        word_filename = self.name + '_words'
        wordlengths_filename = self.name + '_word_lengths'
        stems_filename = self.name + '_stems'
        sentencelengths_filename = self.name + '_sentence_lengths'
        charsequence_filename = self.name + '_char_sequences'
        files = {word_filename: self.words,  wordlengths_filename: self.word_lengths,  stems_filename: self.stems,  sentencelengths_filename: self.sentence_lengths, charsequence_filename: self.character_sequences}
        for file_name in files:
            f = open(file_name + '.txt', 'w')       
            f.write(str(files[file_name]))               
            f.close() 
        
    def read_model(self):
        """ Loads the data from the files into the model
        """
        word_filename = self.name + '_words'
        wordlengths_filename = self.name + '_word_lengths'
        stems_filename = self.name + '_stems'
        sentencelengths_filename = self.name + '_sentence_lengths'
        charsequence_filename = self.name + '_char_sequences'
        
        #Read files
        f = open(word_filename + '.txt', 'r')    
        word_str = f.read()          
        f.close()
        
        f = open(wordlengths_filename + '.txt', 'r') 
        word_lengths_str = f.read()
        f.close()
        
        f = open(stems_filename + '.txt', 'r') 
        stems_str = f.read()
        f.close()
        
        f = open(sentencelengths_filename + '.txt', 'r') 
        sentence_lengths_str = f.read()
        f.close()
        
        f = open(charsequence_filename + '.txt', 'r') 
        char_seq_str = f.read()
        f.close()
        
        self.words = dict(eval(word_str))
        self.word_lengths = dict(eval(word_lengths_str))
        self.stems = dict(eval(stems_str))
        self.sentence_lengths = dict(eval(sentence_lengths_str))
        self.character_sequences = dict(eval(char_seq_str))
        
    def similarity_scores(self, other):
        """ Scores each feature compared to the other object and returns a list of the scores
        """
        score_words = compare_dictionaries(other.words, self.words)
        score_word_lengths = compare_dictionaries(other.word_lengths, self.word_lengths)
        score_stems = compare_dictionaries(other.stems, self.stems)
        score_sentence_lengths = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        score_character_sequences = compare_dictionaries(other.character_sequences, self.character_sequences)
        return [score_words, score_word_lengths, score_stems, score_sentence_lengths, score_character_sequences]
      
    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to two other “source” TextModel objects (source1 and source2) 
            and determines which of these other TextModels is the more likely source of the called TextModel.
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        text = "scores for " + source1.name + ": " + str(scores1) + "\n"
        text += "scores for " + source2.name + ": " + str(scores2)
        print(text)
        weighted_sum1 = 10*scores1[0] + 10*scores1[1] + 10*scores1[2] + 10*scores1[3] + 10*scores1[4] # We can change the weighting of each feature
        weighted_sum2 = 10*scores2[0] + 10*scores2[1] + 10*scores2[2] + 10*scores2[3] + 10*scores2[4]
        if weighted_sum1 > weighted_sum2:
            print(self.name + " is more likely to have come from " + source1.name)
        else:
            print(self.name + " is more likely to have come from " + source2.name)
    
    
    
# Outside Class (Helper Functions)
def clean_text(txt):
    """ returns a list containing the words in txt after it has been “cleaned”
        input txt: string
    """
    s = txt.lower()
    for symbol in """.,?"'!;:""":
        s = s.replace(symbol, '')
        
    word_list = s.split()
    return word_list

def length_sentence(s):
    """ retuns a list of the length of each setence in the text.
    """
    sentence_counts = []
    count = 0
    word_list = s.split()
    for word in word_list:
        if word[-1] in "!.?":
            count+=1
            sentence_counts += [count]
            count = 0
        else:   
            count +=1
    return sentence_counts

def stem(s):
    """ returns the stem of the string
        input s: string
    """
    
    if len(s) <= 3:
        return s
    elif s[-3:] == "ies":
        return s[:-2]
    elif s[-3:] == "ing" and len(s) > 5:
        if s[-4] == s[-5]:
            return s[:-4]
        else:
            return s[:-3]
    elif s[-2:] == "er":
        return s[:-2]
    elif s[-2:] == "ed":
        return s[:-2]
    elif s[-1] == "y":
        return s[:-1] + "i"
    elif s[-1] == "e":
        return s[:-1]
    elif s[-1] == "s":
        if s[-3:-1] == 'er':
            return s[:-3]
        else:
            return s[:-1]
    else:
        return s
    
def char_sequences(txt, length):
    """ returns a list of all the sequences of chars of length "length"
        input txt: string
        input length: int (length of seq)
    """
    s = txt.lower()
    s = s.replace(' ', '') 
    for symbol in """.,?"'!;-:""":
        s = s.replace(symbol, '') 
    sequences = []
    for i in range(len(s) - length + 1):
        sequences += [s[i:i+length]]
        
    return sequences


def compare_dictionaries(d1, d2):
    """ returns their log similarity score
        input d1: source dictionary
        input d2: mystery dictionary
    """
    if d1 == {}:
        return -50
    score = 0
    total = 0
    for word in d1:
        total += d1[word]
    for word in d2:
        if word in d1:
            score += d2[word] * math.log(d1[word]/total)
        else:
            score += d2[word] * math.log(0.5/total)
    return score