# prala
### Practice Language 

The aim of this project is to produce a software which can be used by a **language** learner to learn and practice new words, expressions, phrases.

The software can generate a _template dictionary_ but the **filling up** is the user's task.  
The idea is that the learner is reading a book or any other media and he collects the unknown/new words/expressions, checks it in a dictionary and write it down in the _dictionary_.  

Every **new line** in the _dictionary_ represents a new word or expression. It contains the **part of speech**, a **filter**, the **meaning** of the word/expression in the learner's language and the **word/expression** which is to be learnt.  

The **filter** is to group words by chapters or the days when it was found/collected or other freely chosen criteria. In the learning phase it is possible to concentrate on one specific **group of words** using this filter. It is also possible to concentrate on a specific **part of speech**.

On the practice phase the software shows the meaning of a word/expression from the filtered specified dictionary  and waiting for the answer. At the same time, it says out the question and the correct answer in the appropriate language.

The strategy behind showing a randomly chosen word is the following:
 - Until every word was answered shows only the not answerd words randomly
 - It is logged for every word that the answer was good or wrong. From this statistics a number is generated for the word. Higher number gives bigger chance to be asked.
 
 This number depends on
  - The last answer was good or wrong
  - How hectyc was the answer
  - The ratio between the good and wrong answers



