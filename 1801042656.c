// Author: Suleyman Golbol
// Running through gcc->  cc 1801042656.c && ./a.out

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Converting a string to its hexadecimal representation involves 
   encoding the string as a sequence of bytes, and then representing
   each byte as a two-digit hexadecimal number. */
void convert_str_to_hex(char *input, int size, char *output){
    int i;
    for(i = 0; i < size; i++){
        // %02x means that the output will be two digits long
        sprintf(output + (i * 2), "%02x", input[i]);
    }
    output[size * 2] = '\0';
    printf("%s\n", output);
}

void convert_hex_to_str(char *input, int size, char *output){
    int i = 0;
    while(i < size){
        // convert two hex digits to a byte
        // because 16 = 2^4, we can use a nibble to represent a hex digit
        char temp[3];
        temp[0] = input[i];
        temp[1] = input[i + 1];
        temp[2] = '\0';
        output[i / 2] = strtol(temp, NULL, 16);

        i = i + 2;
    }
    output[size / 2] = '\0';
    printf("%s\n", output);
}

// removes redundant characters from the string using anding with 
char* redundant_remover(char *input){
    int i = 0;
    while(input[i] != '\0'){
        input[i] = input[i] & 0x7f;
        // the reason for 0x7f is that 0x7f = 0111 1111 is the highest in ASCII
        i++;
    }
    return input;
}

void rotator(char *input, ){
    int offset = offset % 26;
    int i = 0;

    char *shifted1 = (char *)malloc(strlen(input) + 1);
    char *shifted2 = (char *)malloc(strlen(input) + 1);
    char *ored = shifted1 | shifted2;
    


}


int main(){
    char *input = "Hello World!";
    int size = strlen(input);
    char *output = (char *)malloc(size * 2 + 1);
    convert_str_to_hex(input, size, output);
    input = malloc(size * 2 + 1);
    convert_hex_to_str(output, size * 2, input);
    return 0;
}
