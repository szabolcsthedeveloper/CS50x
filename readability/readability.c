#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include <string.h>

int count_letters(string text);
int count_sentences(string text);
int count_words(string text);

int main(void)
{
    string text = get_string("Text: \n");

    float letterscount = count_letters(text);
    float sentencescount = count_sentences(text);
    float wordscount = count_words(text);

    int index = round(0.0588 * (100 * letterscount / wordscount) - 0.296 * (100 * sentencescount / wordscount) - 15.8);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }

    if (index >= 1 && index <= 16)
    {
        printf("Grade %d\n", index);
    }

    else if (index > 16)
    {
        printf("Grade 16+\n");
    }

}

int count_letters(string text)
{
    int letterscount = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]) != 0)
        {
            letterscount++;
        }
    }

    return letterscount;
}

int count_sentences(string text)
{
    int sentencescount = 0;

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentencescount++;
        }
    }

    return sentencescount;
}

int count_words(string text)
{
    int wordscount = 1;

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            wordscount++;
        }
    }

    return wordscount;
}