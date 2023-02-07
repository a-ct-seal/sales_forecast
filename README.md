# sales_forecast
Research work: Sales forecast of a point of sale in the village of Pribrezhny, Yaroslavl region, Russia

A part of this research work is analysing data on sales of a retail outlet located in the Yaroslavl region, Russia. Superfluous information was removed, several signs were highlighted, graphs of the dependence of the target variable (number of sales) on these signs were constructed. Then several models were trained: kNN, linear regression, random forest, gradient boosting (the best hyperparameters were selected for each), after which they were compared. This part of the work can be seen in the files analytics.ipynb and model_fitting.ipynb.
|Model|MSE|MAE|
|-|-|-|
|Linear regression|21.918|2.678|
|Ridge regression|21.868|2.671|
|Lasso|22.562|2.694|
|ElasticNet|22.421|2.710|
|Gradient descent|33.108|3.483|
|kNN|20.283|2.292|
|Random forest|17.681|2.194|
|Boosting(CatBoostRegressor)|15.908|2.202|
|Boosting & random forest|15.669|2.117|
|Boosting & kNN|15.615|2.082|
The best model turned out to be the blending of boosting from the CatBoost library and knn from sklearn. Further, as an addition, a GUI was implemented for this model using the tkinter library. The GUI code is presented in the prediction_model.py and gui.py files.
