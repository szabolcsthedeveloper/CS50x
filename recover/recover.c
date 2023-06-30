#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    char *input = argv[1];
    FILE *inptr = fopen(input, "r");
    if (inptr == NULL)
    {
        printf("Unable to open file\n");
        return 1;
    }

    int block_counter = 0;
    FILE *outptr = NULL;
    char filename[8];
    uint8_t buffer[512];

    while (fread(buffer, 512, 1, inptr))
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (outptr != 0)
            {
                fclose(outptr);
            }

            sprintf(filename, "%03i.jpg", block_counter);
            outptr = fopen(filename, "w");
            block_counter++;
        }
        if (outptr != 0)
        {
            //if already found, continue writing
            fwrite(buffer, 512, 1, outptr);
        }
    }

    fclose(inptr);
    fclose(outptr);
    return 0;
}