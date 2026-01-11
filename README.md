# Serverless TMDB Data Lake

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-2088FF?logo=github-actions&logoColor=white)
![ETL](https://img.shields.io/badge/Pipeline-ETL-green)

A fully automated, serverless ETL pipeline that tracks daily movie trends. This project leverages **GitHub Actions** as a compute engine to extract data from the **TMDB API**, transform it using **Pandas**, and load it into a persistent CSV-based data lake.

## Project Overview

This repository acts as a self-updating database of movie trends. Instead of paying for cloud servers, it uses GitHub Actions to run a daily cron job that:
1.  **Extracts:** Fetches the daily trending movies from the The Movie Database (TMDB) API.
2.  **Transforms:** Cleans the JSON response, adds timestamping, and standardizes the schema using Pandas.
3.  **Loads:** Appends the new data to a historical CSV file (`daily_movie_trends.csv`) and generates a snapshot report.
4.  **Commits:** Automatically pushes the updated data back to the repository, creating a version-controlled history of changes.

## File Structure

* `etl.py`: The core Python script that performs the Extract, Transform, and Load logic.
* `.github/workflows/scheduler.yml`: The YAML configuration for the GitHub Actions runner. It schedules the job to run daily at 12:00 UTC.
* `daily_movie_trends.csv`: The "Data Lake." A historical record of trending movies appended daily.
* `LATEST_UPDATE.md`: A generated Markdown report showing the top 5 movies from the most recent run.

## Tech Stack

* **Language:** Python 3.9
* **Libraries:** Pandas, Requests, Tabulate
* **Orchestration:** GitHub Actions (Cron Scheduler)
* **Data Source:** TMDB API

## How It Works

### 1. The ETL Script (`etl.py`)
The script uses the `requests` library to hit the TMDB endpoint. It processes the raw JSON into a structured Pandas DataFrame, enforcing schema consistency. It handles **incremental loading** by appending only new rows to the existing CSV file, ensuring no historical data is lost.

### 2. The Scheduler (`scheduler.yml`)
The pipeline is defined as code using YAML. It sets up an Ubuntu container, installs Python dependencies, injects the API credentials securely via **GitHub Secrets**, and commits the results back to the `main` branch.

```yaml
on:
  schedule:
    - cron: '0 12 * * *' # Runs every day at 12:00 PM UTC
