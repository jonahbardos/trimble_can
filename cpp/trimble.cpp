#include <iostream>
#include <fstream>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>
#include <ctime>
#include <iomanip>

using namespace std;
#define max  2// define the max string  
#define PGN_SPEED_DIR "18FEE8AA"
string strings[max]; // define max string  

// Offsets for slicing
#define PGN_DIR_OFFSET       4
#define PGN_SPEED_OFFSET 4
#define PGN_SPEED_OFFSET_END   8

int convertToLilEndianTwoBytes(string data_byte) {
    string lsb = data_byte.substr(2, 2);
    string msb = data_byte.substr(0,2);
    string little_endian = lsb + msb;
    // cout << "Old: " << data_byte << " New: " << little_endian << endl;
    return stoi(little_endian, 0, 16);
}

void splitString(char str[]){
    char *ptr; // declare a ptr pointer  
    ptr = strtok(str, " "); // use strtok() function to separate string using comma (,) delimiter.  
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

void get_machine_direction(string data_bytes){
    string dir_hex = data_bytes.substr(0, PGN_DIR_OFFSET);
    float scale = 1.0 / 128.0;
    int data = convertToLilEndianTwoBytes(dir_hex);
    float direction = scale * data;
    cout << "Heading: " << direction << " Degrees" << endl;
    // cout << "Machine Direction in degrees " << direction << endl;
    // cout << "Machine Direction data " << data << endl;
}

void get_machine_speed(string dataBytes){
    string speedHex = dataBytes.substr(PGN_SPEED_OFFSET, 4);
    int data = convertToLilEndianTwoBytes(speedHex);
    float rpm = 0.125 * data;
    float mm_tire = 0.250;
    float speed = 0.1885 * rpm * mm_tire;
    cout << "Machine Speed: " << speed << " Km/h" << endl;
    // cout << "Machine Speed data " << data << endl;
}

void find_speed_dir_data_store(string canMsg, string dataBytes, string timeEpoch) {
    if (canMsg == PGN_SPEED_DIR)
    {
        cout << canMsg << ' ' << PGN_SPEED_DIR << endl;
        cout << dataBytes << " data bytes"<< endl;
        time_t datetime = stod(timeEpoch);
        cout << "Time: " << put_time(localtime(&datetime), "%H:%M") << endl;
        get_machine_direction(dataBytes);
        get_machine_speed(dataBytes);
    }
}

void extractDatapacket(string str, string timeEpoch) {
    char seperator = '#';
    split(str, seperator);
    string data1 = strings[0]; // Contains pgn
    string data2 = strings[1]; // Data bytes
    find_speed_dir_data_store(data1, data2, timeEpoch);
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
    while (ptr != NULL)  
    {  
        g1.push_back(ptr);
        ptr = strtok (NULL, " , ");  
    } 

    string time_epoch = g1.at(0).substr(1, g1.at(0).size() -2);
    string bus_channel = g1.at(1);
    string data_packet = g1.at(2);
    
    extractDatapacket(data_packet, time_epoch);
   
    // cout << datetime<< endl; 
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

void testSplitStringV2(string s){
    int n = s.length();
    char char_array[50];
    strcpy(char_array, s.c_str());
    splitStringPython(char_array);
}

int main() {
    // Read logs
    // ifstream file("test.log");
    ifstream file("2020-12-03T22_30_35.121930_nav900.log");
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            testSplitStringV2(line.c_str());
        }
        file.close();
    }

    return 0;
}