/* C input (printf) example */
#include <stdio.h>

int main(int argc, char *argv[]) {
    // Check if the number of arguments is correct
    if (argc != 2) // passed arguments are more than two 
    {
        printf("Usage: %s <string>\n", argv[0]);
        return 1;
    }

    // Print the provided argument
    printf("%s\n", argv[1]);

    return 0;
}