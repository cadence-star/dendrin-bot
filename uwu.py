import random

joy = [" (\\* ^ ω ^)", " (o^▽^o)", " (≧◡≦)", " ☆⌒ヽ(\\*\"､^\\*)chu", " ( ˘⌣˘)♡(˘⌣˘ )", " xD"]
embarrassed = [" (⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)..", " (\\*^.^\\*)..,", "..,", ",,,", "... ", ".. ", " mmm..", "O.o"]
confused = [" (o_O)?", " (°ロ°) !?", " (ーー;)?", " owo?"]
sparkles = [" \\*:･ﾟ✧\\*:･ﾟ✧ ", " ☆\\*:・ﾟ ", "〜☆ ", " uguu.., ", "-.-"]


async def uwu_word(word):
    end = ''
    # randomly change punctuation to kaomoji
    if word[-1] in ',.?!':
        end = word[-1]
        word = word[:-1]
        if end in ',.':
            chance = 0.33
        else:
            chance = 0.50
        if random.random() < chance:
            if end == ',':
                end = random.choice(embarrassed)
            elif end == '?':
                end = random.choice(confused)
            else:
                end = random.choice(joy)
        if random.random() < 0.25:
            end = random.choice(sparkles)
    # don't change some endings
    if word.endswith(('le', 'll', 'er', 're')):
        end = word[-2:] + end
        word = word[:-2]
    elif word.endswith(('les', 'lls', 'ers', 'res')):
        end = word[-3:] + end
        word = word[:-3]
    # uwu
    word = word.replace('l', 'w').replace('r', 'w') + end
    # random stutter
    if len(word) > 2 and word[0].isalpha() and random.random() < 0.17:
        word = word[0] + '-' + word
    return word
