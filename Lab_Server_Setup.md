# Setting Up and Using Visual Studio Code (VS Code) with SSH and Git

## Step 1: Install Visual Studio Code on Your Local Machine

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
- Reboot your machine, make sure VS Code is in your Application folder.
- Click Remote-SSH add on, enter the SSH command for your server in the format `username@hostname` (replace "username" with your username and "hostname" with the IP address or domain of your server). In the case of YES Lab, it's `ssh psych-ads\\[username]@yeslab1.psych.ucsb.edu` (could be single or double backslash)
- Press Enter. If you're connecting to the server for the first time, you'll have to confirm that you trust the server.
- Enter your password when prompted. Check bottom left, it should show "SSH: yeslab1.psych.psych.ucsb.edu"
- To show the folder, click "Explorer" on the left top panel, enter the password again, you should see the remote server folder.

Now, you should be connected to your remote server via SSH in Visual Studio Code.

## Step 4: Environment Setup
- Make sure you are connected to the lab server. 
- Note that lab members don't don't have root access or admin permission, you would want to avoid running `sudo`, `apt`, etc. Email psy help if you want to install something that needs admin permission.
### 4.1 [Anaconda](https://docs.anaconda.com/free/anaconda/install/linux/) for Programming such as Python: 
- Download the installer from [Anaconda](https://docs.anaconda.com/free/anaconda/install/linux/);
- Search for “terminal” in your applications and click to open;
- Type `cd Downloads` and press Enter (or any location the installer is downloaded to);
- Type `bash Anaconda...` (finish the installer file name or just press Tab for autocompletion) and press Enter
- Follow everything prompted and you should be set for Anaconda
### 4.2 [Git](https://docs.github.com/en/get-started/quickstart/set-up-git#setting-up-git): 
- Follow the github [instruction](https://docs.github.com/en/get-started/quickstart/set-up-git#setting-up-git);
- Once you have your github setup, let lab-manager/PI knows your username so we can add you to the lab account.

## Step 5: Use matlab (optional)
1. type `matlab` to see if it has been installed.
2. (optional) Use X11 forwarding or VNC to get GUI. 
3. (optional) After setting up X11 forwarding, open terminal, type `ssh -X username@hostname` note the "X".
If your mac is M chips and using X11 forwarding with XQuartz, do the following to fix the black background:
    - create a file "java.opts" in the home folder
    - codes inside that file:
    ```
    Dsun.java2d.xrender=false
    Dsun.java2d.pmoffscreen=false
    ```
    - restart matlab
4. To run the script without GUI, navigate to the directory containing the Matlab scripts and run, e.g.: 
    ```
    matlab -nodisplay -nosplash -r "run('kappa_estimate_aggression.m'); exit;"
    ```

## Basic Operations

### Terminal basic commands
- source: https://towardsdatascience.com/17-terminal-commands-every-programmer-should-know-4fc4f4a5e20e
- TBD

### Opening a File

To open a file in Visual Studio Code:

- Go to the File menu and click on Open File.
- Navigate to the location of your file, select it, and click Open.
- When SSH to lab server, you may need to refresh if you create/delete files to see the changes.

### Saving a File

To save changes to a file:

- Go to the File menu and click on Save. You can also use the shortcut Ctrl+S (Command+S on a Mac).
- It's recommended that you change the auto save settings to delay mode (1000ms).

Remember to save your work often and commit your changes to your version control system (like Git) if you're using one.