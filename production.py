# -*- coding: utf-8 -*-
import random
import re


def index():
    db.questions.answer.readable = False
    db.questions.answer.writable = False
    form = SQLFORM(db.questions).process()
    rows = db(db.questions).select(orderby=~db.questions.id, limitby=(0, 1))
    row = rows.last()
    if form.accepted:
        redirect(URL("search_lyrics", vars=dict(value=row.asked)))
    return locals()


def search_lyrics():
    question = str(request.vars["value"])
    words = question.lower()
    # Remove punctuation/random characters.
    words = re.sub("\W+", " ", question).split()
    skip_words = [
        "what",
        "whose",
        "whoever",
        "whatever",
        "whichever",
        "whomever",
        "whom",
        "which",
        "that",
    ]
    search_words = [word for word in words if len(word) > 3 and word not in skip_words]
    lyrics = list()
    rows = db(db.discography.lyrics).select()
    song_names = db(db.discography.song_name).select()
    albums = db(db.discography.album).select()
    for row in rows:
        lyrics.append(row.lyrics)
    lyric_counts = dict()
    # Take the list of search_words and get matches in lyrics by line.
    loc = dict()
    for word in search_words:
        for i, lyric in enumerate(lyrics):
            lines = list(set(lyric.split("\n")))
            for line in lines:
                line = line.strip()
                if word in line:
                    lyric_counts[line] = tuple()
                    lyric_counts[line] = (lyric_counts.get(line[0], 0) + 1, i)
                    loc[line] = i
    # Store the most matched line and # of times it matched in these variables
    most_matched_line = None
    match_count = None
    for line, lyric_count in lyric_counts.items():
        if most_matched_line is None or lyric_count > match_count:
            most_matched_line = line
            match_count = lyric_count
            i = loc[line]
            song = song_names[i]["song_name"]
            album = albums[i]["album"]
    answer = most_matched_line
    counter = count()
    try:
        line = random.choice(list(lyric_counts.keys()))
        loc = lyric_counts[line][1]
        song = song_names[loc]["song_name"]
        album = albums[loc]["album"]
        answer = line
    except IndexError:
        rows = db(db.discography).select()
        row = rows.last()
        song = row.song_name
        album = row.album
        answer = line
    db.questions.answer.readable = False
    db.questions.answer.readable = False
    db.questions.asked.writable = False
    db.questions.asked.readable = False
    form = SQLFORM(db.questions).process()
    rows = db(db.questions).select(orderby=~db.questions.id, limitby=(0, 1))
    row = rows.last()
    if form.accepted:
        redirect(URL("search_lyrics", vars=dict(value=row.asked)))
    return locals()


def count():
    session.counter = (session.counter or 0) + 1
    return dict(counter=session.counter, now=request.now)

