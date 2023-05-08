## App setup
In this cloned version of the app everything should be set up and ready to go.
But if you want to set up the app from scratch, you can follow the instructions below.

### Backend setup
Run the described commands from the root directory of the project (cwd: `app/`)

For local development you need to have Python 3.8 installed.
To install the needed packages, run:
```bash
pip install -r requirements.txt
```


To setup local databases app uses docker-compose. To create and start the containers run:
```bash
docker-compose up -d
```
After this step PRODUCTION DB should be running on port 5522 and all the data should be loaded.
If you want to load the data manually, the dump.sql file is located in the `app/production_database_data/db` directory.

After the database is running, you can run the backend server.
To run the backend locally, run:
```bash
# from cwd: app/
uvicorn app.main:app --reload
```

### Optional db setup
If you want to setup a db for local development, you can run:
```bash
docker-compose up -d
```
After this step DEVELOPMENT, TEST and PRODUCTION DBs should be running. Ports can be found in .env file.
PRODUCTION DB has already been loaded with data, but DEVELOPMENT and TEST DBs are empty.

To change the db backend is using, change the variable ENVIRONMENT variable in .env file (uncomment).

To run alembic migrations, run:
```bash
# from cwd: app/
alembic upgrade head
```

## Frontend setup 
Instructions on how to run or setup the frontend app can be found in the README.md file in the app/frontend directory.


## Scraping Game Reviews using CLI (and other metadata)
Module is located in the `app/app/services/scraper` directory.

The provided code is a Python script that scrapes video game reviews and game data from different sources (such as Steam, Gamespot, and Doupe). The data is then processed and stored in a database.

This guide will help you run the scraping process using CLI (Command Line Interface). The script should be run from the `app` directory (project root directory) with the following command:
```bash
python -m app.services.scraper.db_scraper
```

### Prerequisites

Before running the script, make sure you have Python 3.8+ installed on your system.
You should also have the necessary Python libraries installed, as specified in the project's `requirements.txt` file.



### Command Line Arguments

The script supports several command-line arguments to control its behavior. Below is a list of the available arguments:

- `--steam-games`: Scrape all games from Steam.
- `--steam-reviews`: Scrape all reviews from Steam for scraped games.
- `--doupe-reviews`: Scrape all reviews from Doupe.cz.
- `--gamespot-reviews`: Scrape all reviews from Gamespot.
- `--rate-limit`: Use rate limit for scraper in requests/sec (default: None).
- `--check-interval`: Check interval for scraper in days (default: 7).
- `--max-reviews`: Maximum number of reviews to scrape (default: None).
- `--game-id`: Game ID to scrape reviews for (default: None).
- `--source-game-id`: Game ID based on source (e.g., review URL or ID on the actual site) to scrape reviews for (default: None).
- `--max-games`: Maximum number of games to scrape (default: None).
- `--page-size`: Page size for scraper (default: 1).
- `--language`: Language of the reviews (default: 'english,czech').

### Example Usage

Below are some example commands demonstrating how to use the provided script:

1. Scrape all games from Steam:
   ```bash
   python -m app.services.scraper.db_scraper --steam-games
   ```

2. Scrape all reviews from Steam for a specific game:
   ```bash
   python -m app.services.scraper.db_scraper --steam-reviews --game-id 12345
   ```

3. Scrape all reviews from Doupe.cz:
   ```bash
   python -m app.services.scraper.db_scraper --doupe-reviews
   ```

4. Scrape all reviews from Gamespot:
   ```bash
   python -m app.services.scraper.db_scraper --gamespot-reviews
   ```

For more information on the available command-line arguments, run the script with the `--help` flag:

```bash
python -m app.services.scraper.db_scraper --help
```

## Analyzing Game Reviews using CLI

This project analyzes game reviews using a command-line interface (CLI) and stores the results in a database or file, depending on the chosen configuration. It is designed to run from the project root directory (`app`).

## Requirements

- Python 3.8 or higher
- Required packages from `requirements.txt`

This project relies on several libraries for its core functionality:

- **PyABSA**: A library for aspect-based sentiment analysis (ABSA) that provides the core functionality for analyzing reviews.
- **Transformers**: A library for state-of-the-art natural language processing (NLP) models, such as the MT5 model used in this project.
- **NLTK**: A library for natural language processing that is used for sentence tokenization of long reviews.

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```


### Usage

The script can be executed from the project root directory with the following command:

```bash
python -m app.services.scraper.db_scraper [options]
```

#### Options

- `--dump`: Dump the analysis results to a file instead of a database (faster).
- `--insert`: Insert the dumped analysis results from files.
- `--analyze`: Analyze reviews in the database for a specific game (`--game_id` ID) or all games (`--all`).
- `--game_id` ID: Specify the game ID for analyzing its reviews.
- `--task` TASK: Specify the task to perform, e.g., "joint-acos". Default: "joint-acos".
- `--model` MODEL: Specify the model to use, e.g., "mt5-acos-1.0". Default: "mt5-acos-1.0".
- `--batch_size` SIZE: Specify the batch size for processing reviews. Default: 32.
- `--all`: Analyze all games that have unprocessed reviews.

#### Example

Analyze all unprocessed reviews for a specific game (game_id=1234) using the "mt5-acos-1.0" model, with a batch size of 32:

```bash
python -m app.services.scraper.db_scraper --analyze --game_id 1234 --model mt5-acos-1.0 --batch_size 32
```

Analyze all unprocessed reviews for all games using the default model and batch size:

```bash
python -m app.services.scraper.db_scraper --analyze --all
```

Dump analysis results to a file instead of a database:

```bash
python -m app.services.scraper.db_scraper --analyze --game_id 1234 --dump
```

Insert dumped analysis results from files:

```bash
python -m app.services.scraper.db_scraper --insert
```

## Setting Up a Cron Job

1. Open the terminal on your system.
2. Enter the following command to open the cron table for editing:
   
   ```bash
   crontab -e
   ```
3. In the opened file, add a new line for the script you want to run periodically. The line should follow this format:

   ```
   * * * * * /path/to/python /path/to/script.py --arg1 --arg2
   ```

   Replace `/path/to/python` with the path to your Python interpreter, `/path/to/script.py` with the path to the `db_scraper` script, and `--arg1 --arg2` with the desired command-line arguments for the script.

   The cron line consists of five time and date fields, followed by the command to execute. The fields represent minutes (0-59), hours (0-23), days of the month (1-31), months (1-12), and days of the week (0-7, where both 0 and 7 represent Sunday).

   For example, to run the script every day at 3:00 AM to scrape all reviews from Steam, you could add the following line:

   ```bash
   0 3 * * * /usr/bin/python /home/user/app/services/scraper/db_scraper.py --steam-reviews
   ```

   Adjust the paths and arguments according to your requirements.

4. Save the file and exit the editor. The cron job will now run according to the specified schedule.
