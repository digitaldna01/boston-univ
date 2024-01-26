#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 17:06:38 2019

@author: leejaehong
"""

#
# Lab 7
#
# Computer Science 111
#

def display_menu():
    """ prints a menu of options
    """  
    print()
    print('0) Input new goal lists')
    print('1) Get the latest score')
    print('2) Find the max number of goals')
    print('3) Find the number of wins')
    print('4) Print the results')
    
    ## Add any new menu options here.


    print('7) Quit')
    print()

def latest_score(terriers, opponents):
    """ returns the score of the latest (i.e., most recent) game
        inputs: terriers - a list of goals scored by the Terriers in a 
                  set of games
                opponents - a list of goals scored by their opponents
        We assume that both lists contain the same number of integers,
        and that they each contain at least one integer.
    """
    score = str(terriers[-1]) + '-' + str(opponents[-1])
    return score

## Add your helper functions for the remaining options below.
def find_max_goals(goals):
    """ returns the largest number of goals in the specified 
        list of goals, which we assume contains at least one integer
    """
    maxg = goals[0]

    for g in goals:
        if maxg < g:
            maxg = g

    return maxg     

def find_num_wins(s1,s2):
    """ returns the numbers of wins of terriers compare the score of both teams
        list of goals
    """
    num_of_wins = 0
    for i in range(len(s1)):
        if s1[i] > s2[i]:
            num_of_wins += 1
    return num_of_wins

def print_result(terriers, opponents):
    """ takes two lists of integers containing the goals scored by the Terriers
        and their opponents
        list of two goals
    """
    for i in range(len(terriers)):
        if terriers[i] > opponents[i]:
            print("win", terriers[i],'-',opponents[i])
        elif terriers[i] < opponents[i]:
            print("lose",terriers[i],'-',opponents[i])
        else:
            print("tie",terriers[i],'-',opponents[i])
            
def main():
    """ the main user-interaction loop
    """
    terriers = []
    opponents = []

    while True:
        display_menu()
        choice = int(input('Enter your choice: '))

        if choice == 0:
            terriers = eval(input('Enter the Terriers list of goals: '))
            opponents = eval(input('Enter their opponents list of goals: '))
            if len(terriers) != len(opponents):
                print('The lists must have the same length.')
                print('Please select menu option 0 to try again.')
                terriers = []
                opponents = []
        elif choice == 7:
            break
        elif choice < 7 and len(terriers) == 0:
            print('You need to first enter the goal lists.')
            print('Please select menu option 0 to do so.')
        elif choice == 1:
            score = latest_score(terriers, opponents)
            print('The score of the latest game was', score)
        ## add code to process the other choices here
        elif choice == 2:
            max_goals_terriers = find_max_goals(terriers)
            max_goals_opponents = find_max_goals(opponents)
            print('maximun goals of terriers', max_goals_terriers)
            print('maximun goals of opponents', max_goals_opponents)
        elif choice == 3:
            num_win = find_num_wins(terriers, opponents)
            print("Number of wins", num_win)
        elif choice == 4:
            print(print_result(terriers, opponents))
        else:
            print('Invalid choice. Please try again.')

    print('Goodbye!')