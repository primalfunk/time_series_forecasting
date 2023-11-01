# Linear Regression Forecaster for Sales and Quantity

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Structure](#structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This repository contains a Python application that performs sales and quantity forecasting using linear regression. The application is designed to handle multiple customer groups and product models. 

## Features
- Uses `sklearn` for implementing the Linear Regression model.
- Groups data by Customer Groups and Models to train individual forecasts.
- Supports sales and quantity predictions for each group.
- Designed to work with dataframes for easy data manipulation and storage.

## Installation
To get started, clone the repository and install the requirements:
\```bash
git clone https://github.com/your_username/your_repository_name.git
cd your_repository_name
pip install -r requirements.txt
\```

## Usage

### Fitting the Model
To fit the model, you would typically call the `fit` method with a dataframe containing at least the following columns:
- `CustomerGroup`
- `Model`
- `Date`
- `Quantity`
- `Sales`

### Making Predictions
After fitting, you can use the `predict` method to make future predictions. The dataframe you pass should contain:
- `CustomerGroup`
- `Model`
- `Date`
The output will be a dataframe with forecasted sales and quantity.

## Structure
- `Forecaster` Class
  - `__init__`: Initializes the models.
  - `fit`: Fits the models based on grouped data.
  - `predict`: Makes forecast based on the fitted models.
