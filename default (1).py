# -*- coding: utf-8 -*-

def index():
    db.questions.answer.readable=False
    db.questions.answer.writable=False
    form = SQLFORM(db.questions, submit_button=T('Tame Advice')).process()
    rows = db(db.questions).select(orderby=~db.questions.id, limitby=(0,1))
    row = rows.last()
    #redirect(URL('search_lyrics', vars=dict(value = row.asked)))
    if form.accepted: 
        redirect(URL('search_lyrics', vars=dict(value = row.asked)))  
        #response.view = default/index.html
        #counter = count()
        redirect(URL('index'))
    return locals()
    #return dict(form=form, vars=form.vars)

# analyzing the question - split the analysis and database querying into two functions? 
def analyze_question():
    return locals()

def search_lyrics():
    question = str(request.vars['value'])
    import random
    import re
    
    # Ask Kevin Question Sorting
    question = question.lower()
    
    # Remove punctuation/random characters
    cleanstring = re.sub('\W+'," ", question )

    # Put the question string into a list called "words"
    words = cleanstring.split()
      
    # question starters ==[how, what, why, is, am, are, who, which, when, should, will, can]
    # typical question second words == [much, long, many, do, did, will, is, are, am, I, do, this, your, my, the, does, we]
    probable_first_words = ["how", "what", "why", "is", "am", "are", "who", "which", "when", "should", "will", "can", "was"]
    probable_second_words = ["much", "long", "many", "do", "did", "will", "is", "are", "am", "I", "do", "this", "your", "my", "the", "does", "we"]

    # Determine how to sort lyrics based on the branch that they fall into based on the first two words

    # 1) Check first and second word of question to get an idea of what the person is asking for.
    # Loop through the question and see if the first two words tip what kind of question it i
    
    # create a list to track analysis of the question
    analysis = list()
    # create a list contianing the first two words
    first_two_words = list()
    first_two_words.append(words[0])
    first_two_words.append(words[1])

    while not analysis:
        if (words[0] in probable_first_words) and (words[1] in probable_second_words):
            analysis.append("I recognize the first two words.")
            break
        elif words[0] in probable_first_words:
            analysis.append("At least the first word tells us something.")
        elif words[1] in probable_first_words:
            analysis.append("The first word is unfamiliar, but the second word is familiar.")
        else:
            analysis.append("Neither of the first words look familiar.")
     
    # 2) Check for indicators of who or what the object of the question is.
    probable_objects = ["i", "kevin","kevin parker", "tame", "tame impala", "impala", "us", "we", "you", "our", "my"]
    # prob_categories == [user, Kevin, Tame, user and Kevin, user and someone they know]
    kevin_indicators = ["you", "your"]
    about_user_indicators = ["i", "me", "my"]
    user_plus_kevin_indicators = ["us", "we", "our", "together"]
    philosophy_indicator = ["why"]
    yes_no_indicators = ["can i", "will i", "can we", "can you", "will i", "will you", "will my", "will we", "should i", "should we", "is this", "is your", "is my", "is the", "are we"] #removed "am i"
    number_indicators = ["how much", "how long", "how many"]
    choice_between_options = ["which", "or"]

    for word in words:
        if word in user_plus_kevin_indicators:
            analysis.append("The question is about the user and Kevin.")
        elif word in kevin_indicators:
            analysis.append("The question is about kevin.")
            break
        elif word in about_user_indicators:
            analysis.append("The question is about the user.")
            break
        else:
            analysis.append("No clue what this question is about.")
   
    # check to see if a which or why question?
    for word in words:    
        if word in choice_between_options:
            # Try to find options? (blank) or (blank) which (blank) is (blank)
            analysis.append("This is a 'which' question, about a choice between options.")
            break
        elif word == "why":
            analysis.append("Why question - we're gonna get deep here.")
            break
        else:
            analysis.append("Not a which or why question.")

    for first_two_words in yes_no_indicators:
        first_two_words = str(words[0] + " " + words[1])
        if first_two_words in yes_no_indicators:
            analysis.append("This question could be answered with a yes or no.")
            break
        else:
            analysis.append("The answer should not be yes/no oriented.")

    for first_two_words in number_indicators:
        first_two_words = str(words[0] + " " + words[1])
        if first_two_words in number_indicators:
            analysis.append("This question could be answered with a number.")
            break
        else:
            analysis.append("The answer should not be a number.")

    # 3) Check if there are words that indicate the question is about the past, present or future.
    past_indicators = ["did", "was"]
    future_indicators = ["until", "will", "should", "when"]
    present_indicators = ["is", "are", "do", "does", "am"] 

    for word in words:
        if word in future_indicators:
            analysis.append("Answer should be a prediction.")
            break
        elif word in past_indicators:
            analysis.append("Answer should be about the past.")
            break
        else:
            analysis.append("Answer should be about the present.")
    lyrics = list()
    rows = db(db.discography.lyrics).select()
    for row in rows:
        lyrics.append(row.lyrics)
    answer = "temporary"
    
    # Goal: Find a noun and see if there is a line in lyrics that contains it.
    nouns = list()
    lyric_counts = dict()
    # Assumption: if the word is 5 letters or longer, it is likely to be a noun or subject.
    # Add possible words to a list of "nouns"
    for word in words:
        if len(word) > 3:
            nouns.append(word)
            print("we may have found a noun.")
        else:
            print("Not sure about nouns here.")
    
    # Store the most matched line and # of times it matched in these variables
    most_matched_line = None
    match_count = None
     
    # Take the list of nouns and get matches in lyrics by line.
    for noun in nouns:
            for lyric in lyrics:
                lines = lyric.split('\n')
                for line in lines:
                    if noun in line:
                        lyric_counts[line] = lyric_counts.get(line,0)+1
    
    # Keep track of the line with the most matches
    for line,lyric_count in lyric_counts.items():
        if most_matched_line is None or match_count > match_count:
            most_matched_line = line
            match_count = lyric_count  
        else:
            pass
    # store the most relevant line in answer variable    
    answer = most_matched_line
    answer = " ".join(answer.split())
    return locals()


def count():
    session.counter = (session.counter or 0) + 1
    return dict(counter=session.counter, now=request.now)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
