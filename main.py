# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import random

wordSet = []
MAXSIZE = 15
BOARD = [[' ']*MAXSIZE for i in range(MAXSIZE)]

# Get word from file and sort by length, descending
def get_word_set():
    f = open('wordset.txt', 'r')
    word = f.readline()
    wordSet.append(word.strip())
    while word:
        word = f.readline()
        #단어 양 옆에 공백 채움
        #word = word.center(len(word)+2)
        wordSet.append(word.strip())
    f.close()
    random.shuffle(wordSet)
    print(wordSet)

# 예외처리(단어, 위치)
# 찾은 글자의 n번째 위치가 a,b라 할때 a-n <0 이거나 a+n > MAX이면 다음 단어 찾기
def except_row(first, last, loc):
    if loc[0] - first<0 or loc[0] + last - first > MAXSIZE:
        return False
    else:
        return True

def except_col(first, last, loc):
    if loc[1] - first<0 or loc[1] + last - first > MAXSIZE:
        return False
    else:
        return True

def except_not_empty_row(first, last, loc):
    for i in range(last):
        if i == loc[0]:
            continue
        elif BOARD[loc[0]-first+i][loc[1]] != ' ':
            return False
        else :
            return True

def except_not_empty_col(first, last, loc):
    for i in range(last):
        if i == loc[1]:
            continue
        elif BOARD[loc[1]-first+i][loc[0]] != ' ':
            return False
        else :
            return True
        # print("word 1 : {}".format(pick_1))

def col_and_row(nextWord, nextWord_loc):
    secondWord = ''
    secondWord_loc = ()
    thirdWord = ''
    thirdWord_loc = ()

    # 세로로 넣기
    # 다음단어중 random으로 문자 뽑아오기
    getrandom = random.randrange(0, len(nextWord))
    pick_1 = nextWord[getrandom]
    pick_1_loc = (nextWord_loc[0], nextWord_loc[1] + getrandom)

    #나머지 단어중 찾기
    for word in wordSet:
        loc = word.find(pick_1)
        # 단어를 찾았으면 세로로 넣기(예외처리 후)
        if loc != -1:
            if except_row(loc, len(word), pick_1_loc):
                if except_not_empty_row(loc, len(word), pick_1_loc):
                    secondWord = word
                    secondWord_loc = (pick_1_loc[0] - loc, pick_1_loc[1])
                    for letter in word:
                        BOARD[pick_1_loc[0] - loc][pick_1_loc[1]] = letter
                        loc -= 1
                    wordSet.remove(word)
        break
    #세로로 넣을수 있는 단어가 없으면 무작위 빈칸에 세로로 넣기
    if secondWord == '':
        secondWord = wordSet.pop()
        while True:
            n1 = random.randrange(0, MAXSIZE - len(secondWord))
            n2 = random.randrange(0, MAXSIZE)
            if except_not_empty_row() || except_row():
                break

            i = 0

            for letter in secondWord:
                BOARD[n1][n2 + i] = letter
                i += 1
            secondWord_loc = (n1, n2)

    print_board()

    #가로로 넣기
    # 두번째 단어에 가로로 뽑을 위치 찾기
    getrandom = random.randrange(0, len(secondWord))
    pick_2 = secondWord[getrandom]
    pick_2_loc = (secondWord_loc[0] + getrandom, secondWord_loc[1])

    # 나머지 단어중 가로로 넣을 단어 찾기
    for word in wordSet:
        loc = word.find(pick_2)
        # 단어를 찾으면 예외처리 후 가로로 넣기
        if loc != -1:
            if except_col(loc, len(word), pick_2_loc):
                if except_not_empty_col(loc, len(word), pick_2_loc):
                    thirdWord = word
                    thirdWord_loc = (pick_2_loc[0], pick_2_loc[1] - loc)
                    for letter in word:
                        BOARD[pick_2_loc[0]][pick_2_loc[1] - loc] = letter
                        loc -= 1
                    wordSet.remove(word)
    #가로로 넣을수 있는 단어가 없으면 무작위 빈칸에 넣기

    #단어가 없으면 끝냄
    if not wordSet:
        return
    else:
        col_and_row(thirdWord, thirdWord_loc)
    print_board()


def put_word():
    #단어 1개 넣기
    firstWord = wordSet.pop()
    i = 0
    n1 = random.randrange(0, MAXSIZE)
    n2 = random.randrange(0, MAXSIZE-len(firstWord))
    for letter in firstWord:
        BOARD[n1][n2+i] = letter
        i += 1
    col_and_row(firstWord,(n1,n2))

def print_board():
    for i in range(MAXSIZE):
        print(BOARD[i])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_word_set()
    put_word()
    print_board()

'''
1. Sort all the words by length, descending.
2. Take the first word and place it on the board.
3. Take the next word.
4. Search through all the words that are already on the board and see if there are any possible intersections (any common letters) with this word.
5. If there is a possible location for this word, loop through all the words that are on the board and check to see if the new word interferes.
6. If this word doesn't break the board, then place it there and go to step 3, otherwise, continue searching for a place (step 4).
7. Continue this loop until all the words are either placed or unable to be placed.
'''

