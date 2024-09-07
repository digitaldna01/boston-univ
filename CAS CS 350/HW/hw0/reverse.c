/* C input (printf) example */
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    // Check if the number of arguments is correct
    if (argc != 2) // passed arguments are more than two 
    {
        printf("Usage: %s <string>\n", argv[0]);
        return 1;
    }

    // Print the provided argument backwards
    int length, i;
    length = strlen(argv[1]);

    for(i = length - 1; i >= 0; i--){
        printf("%c", argv[1][i]);
    }

    return 0;
}
