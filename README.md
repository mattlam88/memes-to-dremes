
Desktop app which allows the user to select twitter users to monitor for tweets related to the cryptocurrency of their choice. Our desktop app will use sentiment analysis to give an immediate buy/sell notification when one of the selected influencers sends a tweet about the chosen cryptocurrency. In addition to notifications, users can open the desktop app to scroll through a history of previous crypto-related tweets.

## Demo

#### API Query

![App Demo](https://github.com/sbmm/memes-to-dremes/blob/main/media/demo.gif)

#### Settings Window

![Settings Window](https://github.com/sbmm/memes-to-dremes/blob/main/media/settings_blank.PNG)

## Installation

#### Linux (Ubuntu 20.04):

#### Step 1: Clone the project.
```bash
git clone https://github.com/sbmm/memes-to-dremes.git && cd memes-to-dremes
```

#### Step 2: Check your current version of Python and pip. 
Python 3.6+ is required to run this app.

```bash
python --version
```

```bash
pip --version
```

OR

```bash
python3 --version
```

```bash
pip3 --version
```

From this point forward we will assume python3 and pip3 are the correct aliases. 

#### Step 3: Create a virtual environment for Python.
```bash
python3 -m venv demo && source ./demo/bin/activate
```

#### Step 4: Install app packages.
```bash
npm install && pip3 install -r requirements.txt
```

#### Step 4: Create app database.
```bash
python3 database/seed.py
```

#### Step 5 (optional): Install required packages for Qt 5.15+
If you skip this step and run into the following error when trying to run the app:
```bash
qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, wayland-egl, wayland, wayland-xcomposite-egl, wayland-xcomposite-glx, xcb.

Aborted (core dumped)
```

you will need to run the following command:
```bash
sudo apt install libxcb-xinerama0
```

and try running the app again.

#### Step 5: Run the app.
```bash
python3 main.py
```

#### Windows 10:
**NOTE:** We will be using PowerShell 5.1+ for this demo. To check your version of PowerShell, run the following command:

```bash
$PSVersionTable
```

#### Step 1: Clone the project.
```bash
git clone https://github.com/sbmm/memes-to-dremes.git; cd memes-to-dremes
```

#### Step 2: Check your current version of Python and pip. 
Python 3.6+ is required to run this app.

```bash
python --version
```

```bash
pip --version
```

OR

```bash
python3 --version
```

```bash
pip3 --version
```

From this point forward we will assume python3 and pip3 are the correct aliases. 

#### Step 3: Create a virtual environment for Python.
```bash
python3 -m venv demo; ./demo/Scripts/activate.ps1
```

#### Step 3: Install app packages.
```bash
npm install; pip3 install -r requirements.txt
```

#### Step 4: Create app database.
```bash
python3 database/seed.py
```

#### Step 5: Run the app.
```bash
python3 main.py
```

## Setup

#### Step 1: Visit the app's settings page. 

On Windows and Ubuntu, this will be under File > Settings. 

On MacOS, you will find this under Preferences > Settings.

#### Step 2: Create a new [Twitter developer account](https://developer.twitter.com/en/apply-for-access). 

You will need this to be able to generate tokens for the API.

#### Step 3: Visit the [Developer Portal](https://developer.twitter.com/en/portal/projects-and-apps) dashboard.

#### Step 4: Create a new project. 

Then under the project tab, click the key icon beside your project name.

#### Step 5: Regenerate your API Key and Secret. 

Copy the values to the app's settings fields.

#### Step 6: Regenerate your Access Token and Secret. 

Copy the values to the app's settings fields.

#### Step 7: Add the database name. 

By default, this should be `memesToDremes.db`.

#### Step 8: Add the database path. 

This should be the full path to the project's root directory. 

If you cloned the repo to you C drive, then your config would look like this:

![Settings DB Config](https://github.com/sbmm/memes-to-dremes/blob/main/media/settings_defaults.PNG)

#### Step 9: Save settings and close to return to the app. 

You're done! You can now start using the app to make API calls. 

## Tech Stack
* Python 3.6+
* sqlite3
* PyQt 5.15+
* MATLAB Plot

# Visuals

# Maintainers
* Mohamed Al-Hussein
* Bryan Zierk
* Shaun Gannon
* Matt Lam
