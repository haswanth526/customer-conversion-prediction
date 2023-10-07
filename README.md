# Prediction of Customer Conversion ## Features
age (a number)
2. occupation: category
3. marital: status of the union
4. educational_qual: status of education
A contact's communication type is call_type.
6. day: the month's final contact day (numerical)
7. Mon: The year's final contact month
8. dur: the time since the last contact, in numeric form
9. num_calls: the total number of contacts made for this client and during this campaign.
10. prev_outcome: the results of the prior marketing effort (categories: "unknown," "other," "failure," or "success").

## Output Variable (Sought-after Goal)

Has the customer purchased the insurance?

## Minimum Conditions

It is not enough to just fit a model; the model must be examined to identify the crucial elements that affect the conversion rate. The measure AUROC must be utilised to assess the performance


## Preprocessing Data

The data was loaded and preprocessed, with missing value management and categorical feature encoding included.

Analysing Exploratory Data

To glean useful insights from the dataset, exploratory data analysis and data visualisation were carried out.

## Model Construction

Logistic regression was the first model utilised, and it had a favourable AUROC score. However, a respectable F1 score was necessary to construct a more accurate model taking into account the domain context.

## Model Assessment

Pycaret was utilised to compare and fine-tune the models, and feature importances were examined.

## Summary

An artificial intelligence (AI) algorithm was created to forecast whether a customer will purchase insurance. AUROC and F1 scores were used to assess the model's performance and dependability.

## Usage

The Python script can be run locally or you can deploy the model using the Streamlit app.





