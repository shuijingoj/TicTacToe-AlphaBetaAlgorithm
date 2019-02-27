#-*-coding:utf-8-*-

import tkinter as tk
import os
import time 
from copy import deepcopy

def Evaluate(player, chessboard): 
    # 评估函数，计算player在给定局面的得分。player=‘O’代表圈玩家，player=‘X’代表X玩家
    # chessboard为长度9的list，记录从左上到右下的棋盘状态(0：空，1：圈，10：X)

    # 己方达到胜利：1000，对方达到胜利：-1000
    # 单棋子占有某行、列、对角线：10
    # 双棋子占有某行、列、对角线：50
    score = 0    
    if player=='O':
        score_dict = {1:10, 2:50, 3:1000, 30:-1000}     # 圈玩家局面得分映射
    else:
        score_dict = {10:10, 20:50, 30:1000, 3:-1000}  # X玩家局面得分映射 

    cb = chessboard[0]+chessboard[1]+chessboard[2]       # 第一行
    score += score_dict.get(cb) if score_dict.get(cb) else 0
    cb = chessboard[3]+chessboard[4]+chessboard[5]       # 第二行
    score += score_dict.get(cb) if score_dict.get(cb) else 0   
    cb = chessboard[6]+chessboard[7]+chessboard[8]       # 第三行
    score += score_dict.get(cb) if score_dict.get(cb) else 0   
    cb = chessboard[0]+chessboard[3]+chessboard[6]       # 第一列
    score += score_dict.get(cb) if score_dict.get(cb) else 0   
    cb = chessboard[1]+chessboard[4]+chessboard[7]       # 第二列
    score += score_dict.get(cb) if score_dict.get(cb) else 0   
    cb = chessboard[2]+chessboard[5]+chessboard[8]       # 第三列
    score += score_dict.get(cb) if score_dict.get(cb) else 0      
    cb = chessboard[0]+chessboard[4]+chessboard[8]       # 左上右下对角线
    score += score_dict.get(cb) if score_dict.get(cb) else 0                
    cb = chessboard[2]+chessboard[4]+chessboard[6]       # 左下右上对角线
    score += score_dict.get(cb) if score_dict.get(cb) else 0    
    return score

def MinMaxGameTree(player, chessboard, strategy='max', max_depth=-1):
    # MinMax博弈树推演，根据chessboard为player计算各着点的终局得分(达到最大搜索深度或某一方胜利)，返回[(着点,得分)]列表
    # 由于井字棋推演比较简单，可以穷尽各种情况，max_depth==-1不限制搜索深度
    scores = []
    for pos in range(len(chessboard)):
        if chessboard[pos] != 0:   # 已有棋子，不能选为着点
            continue
        next_chessboard = deepcopy(chessboard)
        if player=='O':   # 模拟下子
            next_chessboard[pos]= 1 if strategy=='max' else 10    
        else:
            next_chessboard[pos]= 10 if strategy=='max' else 1  
        if 0 not in next_chessboard or max_depth==0:    # 棋盘已满，或达到最大搜索深度
            scores.append((pos, Evaluate(player, next_chessboard)))
            return scores
        elif strategy == 'max': # max方
            if Evaluate(player, next_chessboard)>=1000: # 已达到胜利条件
                scores.append((pos, Evaluate(player, next_chessboard)))
                return scores
            else:
                children_scores = MinMaxGameTree(player, next_chessboard, 'min', (max_depth-1 if max_depth!=-1 else -1)) # 未达到胜利条件，向前推演
                children_scores.sort(key=lambda x:x[1], reverse=False)  # 选出子局面极小方所有得分中最小的一个，作为当前着点最终得分 
                scores.append((pos, children_scores[0][1]))
        elif strategy == 'min':
            if Evaluate(player, next_chessboard)<0:  # min方
                scores.append((pos, Evaluate(player, next_chessboard)))
                return scores
            else:  
                children_scores = MinMaxGameTree(player, next_chessboard, 'max', (max_depth-1 if max_depth!=-1 else -1)) # 未达到胜利条件，向前推演
                children_scores.sort(key=lambda x:x[1], reverse=True)  # 选出子局面极大方所有得分中最大的一个，作为当前着点最终得分 
                scores.append((pos, children_scores[0][1]))
    return scores

def GameOver(chessboard):
    player_O_score = Evaluate('O', chessboard)
    if player_O_score >= 1000:
        return 'O_win'
    elif player_O_score < 0:
        return 'X_win'
    elif 0 not in chessboard:
        return 'draw'
    else:
        return False

def Printchessboard(chessboard):
    chessboard_symbols = []
    for i in range(len(chessboard)):
        if chessboard[i] == 1:
            chessboard_symbols.append('○')
        elif chessboard[i] == 10:
            chessboard_symbols.append('X')
        else:
            chessboard_symbols.append(i)
    print(' %s | %s | %s'%(chessboard_symbols[0], chessboard_symbols[1], chessboard_symbols[2]))
    print('———————————')
    print(' %s | %s | %s'%(chessboard_symbols[3], chessboard_symbols[4], chessboard_symbols[5]))
    print('———————————')
    print(' %s | %s | %s\n'%(chessboard_symbols[6], chessboard_symbols[7], chessboard_symbols[8]))

def main():
    chessboard = [0]*9
    first_side = int(input('Please choose the first side: 1.Plyaer(○) 2.Computer(X): ')) # 选择先手方，玩家执圈，计算机执X
    while(first_side not in (1,2)):
        print('You should input 1 or 2 to choose the first side.')
        first_side = int(input('Please choose the first side: 1.Plyaer(○) 2.Computer(X): '))
    if first_side == 2:   # 计算机先手，先下一子
        player = 'X'
        computer = 'O'
        candidates = MinMaxGameTree(computer, chessboard, 'max')  # 候选着点及得分列表
        candidates.sort(key=lambda x:x[1], reverse=True) # 按终局得分排序
        computer_next = candidates[0][0]
        chessboard[computer_next] = 1
        print('Computer\'s turn(%s): %d'%(('○' if computer == 'O' else 'X'), computer_next))
    else:
        player = 'O'
        computer = 'X'
    Printchessboard(chessboard)
    while(not GameOver(chessboard)):    # 游戏主循环
        input_msg = 'Your turn(%s): '%('○' if player == 'O' else 'X')
        player_next = int(input(input_msg))
        while(player_next not in range(9) or chessboard[player_next]!=0):
            print('Invalid position!')
            player_next = int(input(input_msg))
        chessboard[player_next] = 1 if player == 'O' else 10
        Printchessboard(chessboard)
        if GameOver(chessboard):
            break

        candidates = MinMaxGameTree(computer, chessboard, 'max')  # 候选着点及得分列表
        candidates.sort(key=lambda x:x[1], reverse=True) # 按终局得分排序
        computer_next = candidates[0][0]
        chessboard[computer_next] = 1 if computer == 'O' else 10
        time.sleep(1)
        print('Computer\'s turn(%s): %d'%(('○' if computer == 'O' else 'X'), computer_next))
        Printchessboard(chessboard)

    if GameOver(chessboard) == 'draw':
        msg = 'Draw.'
    elif GameOver(chessboard) == 'O_win':
        msg = 'You win!' if player == 'O' else 'Computer win!'
    else:
        msg = 'You win!' if player == 'X' else 'Computer win!'
    print('Game over.\n%s\n'%msg)
    restart = int(input('1.Restart 2.Exit: '))
    if restart == 1:
        main()

if __name__ == '__main__':
    main()