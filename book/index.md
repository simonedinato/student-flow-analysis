# Student Flow Analysis: A Data-Driven Approach

Welcome to the **Student Flow Analysis** project. This book documents the end-to-end process of analyzing international student mobility using a Gravity Model framework.

## Project Overview
The goal of this project is to understand the drivers of international student flows and to build a predictive model that can estimate the probability of a student choosing a specific destination based on their personal profile and economic factors.

## Structure of the Book

The book is organized into two main parts:

### Part 1: Data Preparation
We start by aggregating and cleaning data from various sources to build a comprehensive dataset.
- **01 Mobility Data**: Processing raw student flow data.
- **02 Economic Data**: Integrating earnings and cost of living data.
- **03 Employability Data**: Adding employability scores and university rankings.
- **04 Macro Data**: Incorporating macroeconomic indicators like GDP and distance.

### Part 2: Analysis & Results
We then use this dataset to estimate gravity models and visualize the results.
- **05 Regression Analysis**: Estimating four different gravity models (Base, Origin FE, ROI, Parsimonious) and generating personalized predictions.
- **06 Visualization**: An interactive 2D map visualizing the predicted student flows.

## Key Findings
- **Structural Forces Matter**: Economic size (GDP) and distance are robust predictors of student flows.
- **Cost as Quality Signal**: Higher tuition fees often correlate with higher student inflows, suggesting they act as a signal for quality or prestige in certain models.
- **Personalized Insights**: Our model can generate specific probability estimates for individual students based on their origin and field of study.
