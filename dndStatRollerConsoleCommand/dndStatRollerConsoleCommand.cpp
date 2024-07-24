/*
created by: GreifOfUs
updates:
11/1/2023: added roll(), roll_stats(), roll_stats_simple(), print_stats(), print_average()

*/

#include <iostream>
#include <stdlib.h> //adds rand and srand
#include <time.h> //time

using namespace std;

int no_ones = 0;                    //tells function to change the dice size and the floor
int stats[] = { 0, 0, 0, 0, 0, 0 }; //the stat array that will hold the sum of the accepted rolls
const int number_of_stats = 6;
int number_of_dice_rolled = 3;
int number_of_dice_accepted = 3;
int size_of_dice = 6; //you want rand()%size_of_dice + 1

//prototypes
int roll();
int roll_stats();
int roll_stats_simple();
int print_stats();
int print_average();

int main()
{
    cout << "STARTING STAT ROLLER\n";
    srand(time(NULL));//sets seed
    int repeat = 1;
    cout << "Do you wish to have no ones?" << endl;
    cout << "1 to have no ones\n0 to have ones\nChoice 1/0:\t";
    cin >> no_ones;
    if (no_ones != 1)
    {
        no_ones = 0;
    }
    do {
        cout << "CURRENT STATS:\n";
        roll_stats_simple();//roll for stats
        print_stats();  //print stats function //| % d | % d | % d | % d | % d | % d |
        print_average();
        cout << "\nDO YOU WISH TO REROLL ? \n";
        //get user input
        cout << "1 to continue\n0 to quit\nChoice 1/0:\t";
        cin >> repeat;
        if (repeat != 1)
        {
            repeat = 0;
        }
        //////
    } while (repeat);
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

int roll()
{
    //roll one dice
    int temp = 0;
    if (no_ones == 0)
    {
        temp = rand() % size_of_dice + 1;
    }
    else
    {
        temp = rand() % (size_of_dice - 1) + 2;
    }
    return temp;
}

int roll_stats_simple()
{
    //no maximization of stats here
    int temp = 0;
    for (int i = 0; i < number_of_stats; i++)
    {
        for (int j = 0; j < number_of_dice_accepted; j++)
        {
            temp += roll();
        }
        stats[i] = temp;
        temp = 0;
    }
    return 0;
}

int roll_stats()//incomplete
{
    //no return needed
    //incomplete
    if (number_of_dice_accepted > number_of_dice_rolled)
    {
        cout << "CANNOT ROLL DICE TOO FEW TO ACCEPT" << endl;
        return 0;
    }
    //need to create an array dynamically based on dice to roll to hold the results
    int* held_rolls = NULL;
    held_rolls = new int[number_of_dice_rolled];
    int* accepted_rolls = NULL;
    accepted_rolls = new int[number_of_dice_accepted];
    //deallocate memory used
    delete[] held_rolls;
    delete[] accepted_rolls;
    return 0;
}

int print_stats()
{
    for (int i = 0; i < number_of_stats; i++)
    {
        cout << "|" << stats[i];
    }
    cout << "|";
    return 0;
}

int print_average()
{
    float temp = 0;
    for (int i = 0; i < number_of_stats; i++)
    {
        temp += stats[i];
    }
    temp = temp / number_of_stats;
    cout << "average = " << temp << endl;
    return 0;
}