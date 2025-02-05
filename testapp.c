#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _MSC_VER
#include <windows.h>

static void sleep(int sec)
{
    Sleep(sec * 1000);
}
#else
#include <unistd.h>
#endif


void crash_me(int *invalid_ptr)
{
    *invalid_ptr = 0x12345678;
}


int main(int argc, char *argv[])
{
    int i;
    int timeout = 0;
    int crash = 0;
    int *invalid_ptr = NULL;

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    if (argc<=1) {
        puts("Usage:");
        puts("  testapp [-c] -t SECS");
        puts("");
        puts("where:");
        puts("   -t SECS  Sleep SECS seconds before exit or crash");
        puts("   -c       Crash the application");
    }

    for (i=1; i<argc; ++i) {
        if (!strcmp(argv[i], "-t")) {
            timeout = atoi(argv[++i]);
        } else if (!strcmp(argv[i], "-c")) {
            crash = 1;
        } else {
            printf("Error: unknown option %s\n", argv[i]);
            return 1;
        }
    }

    printf("Waiting for %d seconds..\n", timeout);
    sleep(timeout);

    if (crash) {
        puts("We're about to crash.."); fflush(stdout);
        crash_me(invalid_ptr);
    }

    puts("Exiting normally..");
    return 0;
}
