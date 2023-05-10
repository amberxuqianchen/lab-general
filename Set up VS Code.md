# Setting Up and Using Visual Studio Code (VS Code) with SSH

## Step 1: Install Visual Studio Code

First, you need to install Visual Studio Code on your local machine. 

- Visit the [Visual Studio Code](https://code.visualstudio.com/download) website.
- Choose the installation package that corresponds to your operating system (Windows, macOS, or Linux).
- Follow the installation steps to install Visual Studio Code on your machine.

## Step 2: Install the SSH Extension in VS Code

Once Visual Studio Code is installed, you can add the SSH extension.

- Open Visual Studio Code.
- On the left-hand side, click on the Extensions button (it looks like four squares).
- In the search bar, type "Remote - SSH" and press Enter.
- Click on the first result in the list (it should be created by Microsoft) and press the Install button.

## Step 3: Connect to a Remote Server via SSH in VS Code

After the SSH extension is installed, you can use it to connect to a remote server.

- Click on the green button in the bottom left corner (it should look like "><").
- Choose "Remote-SSH: Connect to Host..." from the drop-down list.
- Enter the SSH command for your server in the format `username@hostname` (replace "username" with your username and "hostname" with the IP address or domain of your server). In the case of YES Lab, it's psych-ads\\[username]@yeslab1.psych.ucsb.edu (could be single or double backslash)
- Press Enter. If you're connecting to the server for the first time, you'll have to confirm that you trust the server.
- Enter your password when prompted.

Now, you should be connected to your remote server via SSH in Visual Studio Code.

## Basic Operations

### Opening a File

To open a file in Visual Studio Code:

- Go to the File menu and click on Open File.
- Navigate to the location of your file, select it, and click Open.

### Saving a File

To save changes to a file:

- Go to the File menu and click on Save. You can also use the shortcut Ctrl+S (Command+S on a Mac).

### Running a Python Script

To run a Python script in Visual Studio Code:

- Open the Python file you want to run.
- Click on the green play button in the top-right corner of the code editor.

Remember to save your work often and commit your changes to your version control system (like Git) if you're using one.
