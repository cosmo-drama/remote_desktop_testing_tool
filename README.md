# remote_desktop_test_tool

this is a tool that takes in an ip or a hostname and returns whether or not that machine can be reached via ping and then connected to via rdp.

It then checks to see if the machine is in the user's big fix console and pulls information from the big fix api such as the computer name, operating system, last report time, and serial number. 

this tool is meant to be used by local support providers within the school of arts and sciences. please note: since this is a public repo, I have removed our server info. 

how-to-use the tool:
You'll need the latest version of python (python 3) to use this tool. Homebrew is a nifty package manager for mac/unix machines which can simplify the installation process. 
- head to brew.sh in your web browser
- follow the instructions to install homebrew. it involves pasting a command into your terminal. 
- once homebrew has successfully installed, you'll need to install python 3
- head to the terminal and type: 
brew install python3
- once python3  is installed:

download the project files, open an elevated terminal, navigate to the directory with the project files, and enter: pip install -r requirements.txt
You won't have to do the pip install -r requirements again on this machine. this just installs the necessary python modules to run the script.

Once that completes, run the .py file by entering python3 [name of .py file] in your terminal

to run this again later, navigate to the project folder in the terminal and just enter python3 [name of .py file] 







