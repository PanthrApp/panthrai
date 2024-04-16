# PantherAI

**Please note that this README file is still a work in progress.**

# PantherAI

An easy to setup chatbot for any school's lunch menu, schedule, etc.

## Features

- Fetch the lunch menu
- Fetch the schedule
- Easy-to-use user interface
- Integrated with GPT-3.5 for optimal performance
- Themes powered by [Arc](https://arc.net/gift/a06241b3)

You can access this chatbot at [panthr.app](https://panthr.app/).
Please note that if you are self-hosting this, you will need an OpenAI API Key with sufficient balance to run GPT-3.5 Turbo.

## Themes

You can access a secret "themes" option. First, you will need to download [Arc](https://arc.net/gift/a06241b3). During the setup of Arc, you can personalize your theme. Now visit PanthrAI through Arc and you can view the website with your theme. To change your theme, right-click an empty section of the sidebar and click `Theme...`. Then, you can change your theme, and the color of PanthrAI will change as you drag the color picker around. As of right now, changing between light and dark theme does not do anything.

## Setup

The first step is to clone this repository:

```
git clone https://github.com/panthrapp/panthrai
cd panthrai
```

By default, the code on this repository contains everything needed to get the lunch menu and schedule for J.L. Stanford Middle school in Palo Alto, CA. This makes it incredibly easy to setup. If you would just like to locally host this service, skip to [Configuration](#configuration).

## Lunch Menu

There is a directory inside of this repository called `lunchmenus`. First, enter the directory, and take a look at the files inside.

```
cd lunchmenus
ls
```

There will be JSON files stored inside. The format for the name of the JSON is `[month][year].json`. If you see the JSON file for the month you want to edit, open it in your favorite JSON editor.

```
vi may2024.json
```

Otherwise, copy an existing JSON and rename it to the current month and year.

```
cp april2024.json may2024.json
vi may2024.json
```

Now, follow the steps below:

1. Make sure that the weeks are aligned properly. You will need access to a calendar tool. If the month is not aligned properly, you will have to manually go through the file and align the dates properly.
2. Edit each individual lunch menu section. You will need access to your school's lunch menu for the month. If there is no school, type in one entry saying "No School - [Reason]".
3. Save the file

Now, you will need to go back to the `panthrai` directory. Open the Python script `lunchmenu.py`.

```
cd ../
vi lunchmenu.py
```

There is a dictionary near the top containing the years and months. If your file already exists inside, then no action is required. Otherwise, add the name of your JSON file into the dictionary with the correct year.

## Schedule

There is a directory inside of this repository called `lunchmenus`. First, enter the directory, and take a look at the files inside.

```
cd schedules
ls
```

The most important file is `scheduletemplates.json`. This contains the schemas for all of your schedules. First, open the file. Then, add your own block schedules on, following the format given.

```
vi scheduletemplates.json
```

Now look at the other JSON files. The format for the name of the other JSON files are `[month][year].json`. If you see the JSON file for the month you want to edit, open it in your favorite JSON editor.

```
vi may2024.json
```

Otherwise, copy an existing JSON and rename it to the current month and year.

```
cp april2024.json may2024.json
vi may2024.json
```

Now, follow the steps below:

1. Make sure that the weeks are aligned properly. You will need access to a calendar tool. If the month is not aligned properly, you will have to manually go through the file and align the dates properly.
2. Edit each day, and enter the correct template id from `scheduletemplates.json`.
3. Save the file

Now, you will need to go back to the `panthrai` directory. Open the Python script `schedule.py`.

```
cd ../
vi schedule.py
```

There is a dictionary near the top containing the years and months. If your file already exists inside, then no action is required. Otherwise, add the name of your JSON file into the dictionary with the correct year.

## Configuration

Now, make a copy of `config.yaml.example` to `config.yaml` and enter the file.

```
cp config.yaml.example config.yaml
vi config.yaml
```

Now, you will need to fill in the configuration file. Follow the steps below:

1. OpenAI API Key
   1. Go to [platform.openai.com](https://platform.openai.com)
   2. Sign up for an account
   3. In the sidebar on the left, click API Keys
   4. Click generate and API key
   5. Paste it into config.yaml
2. Google Cloud Platform Client ID & Secret
   1. Go to [console.cloud.google.com/apis/credentials](console.cloud.google.com/apis/credentials)
   2. Sign in with your Google account if prompted to do so
   3. Click Create Credentials near the top
   4. Create OAuth client ID
   5. Fill out the details
   6. For redirect URL, put the domain you will be hosting on but with /google/auth appended to the end (e.g. [https://panthr.app/google/auth](https://panthr.app/user))
   7. Copy the Client ID and Secret into config.yaml

## Running

First, create a virtual environment, and install all dependencies.

```
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
```

Now, you can run the app via gunicorn. Replace 8080 with the port you want to use.

```
gunicorn --bind 0.0.0.0:8080 app:app
```

Now, navigate to `localhost:8080` to view your app!

## Contributing

Just start an issue or pull request and I'll be in contact with you.

## Support

Email me at [contact@adamxu.net](mailto:contact@adamxu.net).
Alternatively, DM me on Discord. My username is [@thetnter](https://discordapp.com/users/773996537414942763).
You can also [start an issue](https://github.com/PanthrApp/panthrai/issues/new) and I will try to get back to you ASAP
