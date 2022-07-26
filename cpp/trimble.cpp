#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

using namespace std;
#define max  2// define the max string  
#define PGN_SPEED_DIR "18FEE8AA"
string strings[max]; // define max string  

void splitString(char str[]){
    char *ptr; // declare a ptr pointer  
    ptr = strtok(str, " "); // use strtok() function to separate string using comma (,) delimiter.  
    cout << " \n Split string using strtok() function: " << endl;  
    // use while loop to check ptr is not null  
    while (ptr != NULL)  
    {  
        cout << ptr  << endl; // print the string token  
        ptr = strtok (NULL, " , ");  
    } 
}

// length of the string  
int len(string str)  
{  
    int length = 0;  
    for (int i = 0; str[i] != '\0'; i++)  
    {  
        length++;  
          
    }  
    return length;     
}

void split (string str, char seperator)  
{  
    int currIndex = 0, i = 0;  
    int startIndex = 0, endIndex = 0;  
    while (i <= len(str))  
    {  
        if (str[i] == seperator || i == len(str))  
        {  
            endIndex = i;  
            string subStr = "";  
            subStr.append(str, startIndex, endIndex - startIndex);  
            strings[currIndex] = subStr;  
            currIndex += 1;  
            startIndex = endIndex + 1;  
        }  
        i++;  
        }     
}

void find_speed_dir_data_store(string canMsg, string dataBytes) {
    cout << canMsg << ' ' << PGN_SPEED_DIR << endl;
    if (canMsg == PGN_SPEED_DIR)
    {
        cout << canMsg << ' ' << PGN_SPEED_DIR << endl;
    }
}

void extractDatapacket(string str) {
    char seperator = '#';
    split(str, seperator);
    string data1 = strings[0]; // Contains pgn
    string data2 = strings[1]; // Data bytes
    find_speed_dir_data_store(data1, data2);
    // cout <<" The split string is: ";  
    // for (int i = 0; i < max; i++)  
    // {  
    //     cout << "\n i : " << i << " " << strings[i];  
    // } 
}

void splitStringPython(char str[]) {
    vector<string> g1;
    char *ptr; // declare a ptr pointer  
    ptr = strtok(str, " "); // use strtok() function to separate string using comma (,) delimiter.  
    cout << "Split string using strtok() function: " << endl; 
    while (ptr != NULL)  
    {  
        g1.push_back(ptr);
        ptr = strtok (NULL, " , ");  
    } 

    string time_epoch = g1.at(0);
    string bus_channel = g1.at(1);
    string data_packet = g1.at(2);
    extractDatapacket(data_packet);
    // cout << g1.at(2) << endl; 
    // cout << "\nVector elements are: ";
    // for (auto it = g1.begin(); it != g1.end(); it++)
    //     cout << *it << " ";
}

void testSplitString(){
    string s = "(1607034637.501660) can0 18FEE8AA#BC653D00C762814D";
    int n = s.length();
    char char_array[50];
    strcpy(char_array, s.c_str());
    // splitString(char_array);
    splitStringPython(char_array);
}

int main() {
    // // Read logs
    // char filename[50];
    // ifstream fileObj;
    // cin.getline(filename, 50);
    // fileObj.open(filename);
    // if (!fileObj.is_open()) {
    //     exit(EXIT_FAILURE);
    // }

    // char line[50];
    // fileObj >> line;
    // while(fileObj.good()) {
    //     cout << line << "\n";
    //     fileObj >> line;
    // }

    // testSplitString();
    testSplitString();

    return 0;
}