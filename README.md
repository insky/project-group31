# project-group31

## Installation
Clone the repository to your local machine.

Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the main script to start the assistant bot:
```bash
python3 -m src.main
```

## Features
- Chat-based assistant bot.
- Address book management with birthday reminders.
- Phone number validation (10 digits).
- Email validation.
- Birthday management and upcoming birthday notifications.
- Note-taking with tagging functionality.
- Command suggestion based on user input.
- Command history and autocompletion.

## Data Seeding
To seed the application with initial data, run:
```bash
python3 -m src.data_seed
```

## Tests
To run the tests, use the following command:
```bash
python3 -m unittest
```
## Benchmarks
To run the benchmarks, use the following command:
```bash
python3 -m src.benchmark_suggest_command
```
