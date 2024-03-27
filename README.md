# Finance Calculator

## The Problem

You are creating a loan payment calculator using Django, SQLite, and Vue (optionally Vuex). The user will be able to try out different scenarios to see how each one affects their payments. They will be able to view each scenario they have run in a basic table in the UI. No authentication is necessary.


The user will input the purchase price, down payment, mortgage term, and interest rate into a form and your program will display the total loan amount, monthly payment, total amount paid over the course of the loan, and total interest paid over the course of the loan. All of that data should be displayed in the table.
The user should be able to enter the purchase price in dollars, the down payment in percent or dollars, the mortgage term in years or months, and the interest rate in percent.

## Prerequisites
* Python 3.11.x
* Pipenv
* Docker
* Docker compose

#### Tested with versions

* Python — 3.11.2
* Pipenv — 2023.3.20
* Docker — 25.0.4
* Docker compose — 2.24.7
* OS — Ubuntu 22.04

## How to run
### Locally

To run the backend application locally, enter:
```shell
cd scripts
./start-locally.sh
```

To run the frontend application locally, enter:
```shell
cd frontend
npm install
npm run dev
```
Then access `http://localhost:5173/`.

#### How to run tests
To run tests locally, enter:
```shell
cd finance_calculator
pytest
```

### Using Docker Compose

You can run both applications (backend & frontend) with Docker Compose just entering:
```shell
make start-server
```
Then access `http://localhost:8080/`.

#### How to run tests
To run tests in Docker Compose, enter:
```shell
make test
```
