# To run this script

Download python 3.12

## Maybe need to change the execution policy for this session

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

## Create and start the virtual env

python -m venv venv

.\venv\Scripts\activate

## Install dependencies

pip install -r requirements.txt

OR
pip install selenium requests webdriver-manager

## Run script

python .\scraper.py
