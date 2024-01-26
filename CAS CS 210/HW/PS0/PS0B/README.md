# PS0B: Running some UNIX commands


## Before you proceed

This assignment requires you to run some commands using our Online Unix Environment, therefore, please make sure you have gone through the steps in the following **howto posts** on Piazza. You can directly search those posts on Piazza. 

- How to join GitHub Classroom
- How to accept an assignment
- How to access and use the UNIX Environment
- How to setup SSH key for cloning
    
## Run some commands

**You are not expected to understand what all of these commands and
steps are doing yet.** But hopefully, as you do them, you will get curious
about the commands and what you observe in response to them.  A few of
the commands may even produce error messages.  This is on purpose.  We
have done this so that you can get curious about what the following
commands do to correct the error and why they are needed.

After the first few lectures and doing the readings, you should be able
to look back on the steps and commands and say, "Ah ha, that makes
sense now."  For the moment, following them more like a recipe is OK.
Doing so will get your fingers and brains familiar with the bread-and-butter steps of working in a UNIX environment.  It will also help us
ensure you are set up correctly.

Now, in the terminal, run the following commands:

1. `git clone git@github.com:CS-210-Fall-2023/ps0b-<username>.git` where you replace `<username>` with your GitHub username. Then, if you see a message **Are you sure you want to continue connecting?**, type yes in your current terminal.
2. `cd ps0b-<username>` where you replace `<username>` with your GitHub username. 
3. `ls -l`
4. `echo '#!/opt/conda/bin/python' > hello`
5. `echo 'print("Hello World!!!")' >> hello`
6. `ls -l`
7. `cat hello`
8. `./hello`
9. `chmod +x hello`
10. `ls -l`
11. `./hello`
12. `hello`
13. `export PATH=$PATH:$PWD`
14. `hello`
15. `cat testhello.sh`
16. `./testhello.sh ./hello`
17. `git add hello`
18. `git commit -m "my cool hello program"`
19. `git push`

In step 16 above you ran the same test script that the autograder will use.  It confirms that the hello "program" you wrote works as expected.  If you don't see it pass, then please carefully repeat the steps.  If you are still having trouble, check piazza and post if you need help.

## Check repository on GitHub classroom

Refresh this page and confirm that the main copy of your repository on GitHub reflects your changes (eg. you see your hello file there)

## Submit to Gradescope

1. Sign into Gradescope
2. Navigate to the PS0B submission site
3. Submit a copy of PS0B solution using your main GitHub classroom PS0B repository

For more detailed instructions, please check **How to upload your assignments to Gradescope** post on Piazza.

