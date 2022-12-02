moves = []
with open("day2input.txt") as f:
    for x in f.readlines():
        moves.append(x.strip().split(' '))
cipher = {'A': "Rock", 'B': "Paper", 'C': "Scissors",
          'X': "Rock", 'Y': "Paper", 'Z': "Scissors"}
scoring = {"Rock": 1, "Paper": 2, "Scissors": 3}
sum_score = 0
for m in moves:
    a = scoring[cipher[m[0]]]
    b = scoring[cipher[m[1]]]
    sum_score += b
    if a == b:
        sum_score += 3
    elif (a % 3) == b-1:
        sum_score += 6
print("The first answer is: ", sum_score)

cipher['X'] = 0
cipher['Y'] = 3
cipher['Z'] = 6
sum_score = 0
for m in moves:
    sum_score += cipher[m[1]]
    if cipher[m[1]] == 0:
        sum_score += ((scoring[cipher[m[0]]]+1) % 3)+1
    elif cipher[m[1]] == 3:
        sum_score += scoring[cipher[m[0]]]
    elif cipher[m[1]] == 6:
        sum_score += (scoring[cipher[m[0]]] % 3)+1
print("The second answer is: ", sum_score)
