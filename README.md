# Prala - Language Practice

The aim of this project is to produce a software which can be used by a **language** learner to learn and practice new words, expressions, phrases. _(I will refer to them as **words**)_

<table border="0">
<blockquote><tr>
<blockquote><td>
<img src='https://github.com/dallaszkorben/hu.akoel.prala/blob/master/wiki/console-wrong-answer.png' width='300'>
<td>
<img src='https://github.com/dallaszkorben/hu.akoel.prala/blob/master/wiki/gui-good-answer-0.1.3.png' width='300'>
<td>
</blockquote><tr/></blockquote>
<blockquote><tr>
<blockquote>
<td>Console<br>
<td>GUI<br>
</blockquote><tr /></blockquote>
<table>



The main features are the following:
 - Randomly asks words
 - Saying out the question and the correct answer in the appropriate language.
 - Showing the part of the speech and the note of the asked word (if there is defined  any)
 - The words which are more difficult to learn are asked more often - depends on your answers
 - Statistics are shown about the wrong/good answers
 - Filtering words that you want to practice by part of the speech and extra filter
 - Features can be turn on/off (say out/show note/show pattern)

## Usage

### Preconditions
 - Minimum Python3.6 should be installed on your computer
 - pip (compatible to the Python version) should be installed on your computer
 - Text-to-speech synthesier should be installed on your computer. It is platform dependent.
    - Windows: **SAPI5**
    - Mac OS X: **NSSpeechSynthesizer**
    - Linux: **espeak**

### Install

1. Run a console
2. On the console type the following  
<code>pip install prala</code>

### Update

1. Run a console
2. On the console type the following  
<code>pip install prala --upgrade</code>

### Run

The software has two versions:
 - **console**  
    To run it:  
    <code>**pracon** \<dict_file_name\></code>

 - **GUI**  
    To run it:  
 <code>**pragui** \<dict_file_name\></code>


The command to run the console version:  
The command to run the gui version: **pragui**

#### Meaning of <dict_file_name>
A dict file is a simple text file which contains the words used by the application.    
You can create your own dict files from scratch or you can use the template generated by the app.  
Here is the format of the **dict** files:
- The file name should have **.dict** extension
- Every word defined in ONE line
- The definition of the words contains **5** **fields** separated by colon **:**
- The template of a word is the following:  
<code>**part of speech**:**extra filter**:**expecting answer**:**question**:**note**</code>
- The meaning of the fields:  
   - **Part of speech**: the part of speech of the word. It is **free format text**. Recommended using your language for that.  
   For example your mother language is English than it could be "verb" or "noun" or "adverb"... It is possible to filter the asking words by this **field**.
    - **extra filter**: It is free format text. It is possible to filter the asking words by this **field**.
    - **expecting answer**: this is the word in the language what you want to learn/practice. It could be en **expression** a **sentence** a **single word** or different **format of a word**. In case of the "different forms of a word" the comma "**,**" is used to separate the formats.  
    For example if you learn English and want to practice the word "go" than you can list three forms of this verb: "go, went, gone"
    - **question**: this is the "question word" in your language.
    - **note**: a note about the word for the practicing person. It is free format text. Recommended using your language for that. It is optional to show this at practicing.

Let's say you are a person speaking English and want to practice Swedish. Here is an example of a dict file:

#### 
    verb:chapter-01:göra, gör, gjorde, gjort, gör:do           
    verb:chapter-01:komma, kommer, kom, kommit, kom:arrive, come  
    verb:chapter-01:gå, går, gick, gått, gå:go, walk  
    noun:chapter-01:ett hus, huset, hus, husen:building, house
    noun:chapter-01:en katt, katten, katter, katterna:cat
    noun:chapter-01:en nyckel, nyckeln, nycklar, nycklarna:key  
    adjektiv:bibli-03:orolig, oroligt, oroliga:worried
    adjektiv:bibli-03:tung, tungt, tunga:heavy  
    adverb:chapter-01:verkligen:really  
    sentence:chapter-01:han stirrar tomt framför sig:he stares empty in front of him           
    sentence:chapter-01:han skyndar i väg:he hurries away:han  
    
Notes:  
- chapter-01, chapter-02, chapter-03 **extra filter**s are used. Presumably the person who created this dictionary got the words from different chapters of a book. Using this filter it is possible to practice a specific chapter instead of the all book.
- In the last row the "han" personal noun was used in the **note** field giving a small hint to the practicing person. (it is possible to turn off)


