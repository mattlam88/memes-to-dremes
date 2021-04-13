# memes-to-dremes
Desktop app which allows the user to select twitter users to monitor for tweets related to the cryptocurrency of their choice. Our desktop app will use sentiment analysis to give an immediate buy/sell notification when one of the selected influencers sends a tweet about the chosen cryptocurrency. In addition to notifications, users can open the desktop app to scroll through a history of previous crypto-related tweets.

## Installation

#### Step 1: Clone the project.
```bash
git clone https://github.com/sbmm/memes-to-dremes.git && cd memes-to-dremes
```

#### Step 2: Create a virtual environment for Python.
```bash
python -m venv demo && source ./demo/Scripts/activate
```

#### Step 3: Install app packages and setup database.
```bash
npm install && pip install -r requirements.txt
```

#### Step 4: Run the app.
```bash
python main.py
```

#### Step 5: Visit the app's settings page. On Windows, this will be under File > Settings. On MacOS, you will find this under Preferences > Settings.
#### Step 6: Create a new [Twitter developer account](https://developer.twitter.com/en/apply-for-access). You will need this to be able to generate tokens for the API.
#### Step 7: Visit the [Developer Portal](https://developer.twitter.com/en/portal/projects-and-apps) dashboard.
#### Step 8: Create a new project. Then under the project tab, click the key icon beside your project name.
#### Step 9: Regenerate your API Key and Secret. Copy the values to the app's settings fields.
#### Step 10: Regenerate your Access Token and Secret. Copy the values to the app's settings fields.
#### Step 11: Add the database name. By default, this should be `memesToDremes.db`.
#### Step 12: Add the database path. This should be the full path to the project's root directory.
#### Step 13: Save settings and close to return to the app. 

You're done! You can now start using the app to make API calls. 

## Tech Stack
* Python
* sqlite3
* PyQt
* MATLAB Plot

# Visuals

# Maintainers
* Mohamed Al-Hussein
* Bryan Zierk
* Shaun Gannon
* Matt Lam
