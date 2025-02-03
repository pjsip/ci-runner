# ci-runner

This contains Python script to setup, capture and display crash in GitHub action,
for Linux, Windows, and MacOS.

A program is run via the script, and the script does the following:

1. it sets up crash handler on the system
2. it forwards any stdout/stderr output from the program without buffering.
3. it collects and analyze crash dump and display the analysis using a debugger if the program crashes
4. it terminates the program and generate crash dump and display the analysis using a debugger
   if the program runs for too long (default is one hour)
5. it returns using the return value of the program.

For examples, see the GitHub workflows for each platform in this repository. Note that the
invocation is slightly different between platforms.
