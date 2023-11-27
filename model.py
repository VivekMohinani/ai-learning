from pymongo import MongoClient
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error

import numpy as np


def getData():
    # Mongo Setup
    client = MongoClient('localhost', 27017)  # Replace with your MongoDB server and port
    db = client['inoJam']  # Replace with your database name
    collection = db['modelingData2']  # Replace with your collection name

    # Data Setup
    data = []
    speeds = []
    for doc in collection.find():
        cpu = doc['cpu']
        gpu = doc['gpu']
        ram = doc['ram']
        mem = doc['mem']
        net_lag = doc['net_lag']
        speed = doc['speed']

        data.append([cpu, gpu, ram, mem, net_lag, speed])
        speeds.append(speed)
    client.close()

    return [data, speeds]


def createBaseline(x_train, x_test, y_train, y_test):
    # no hyperparameters for baseline
    dt_baseline = DecisionTreeRegressor(random_state=42)
    dt_baseline.fit(x_train, y_train)
    y_pred_baseline = dt_baseline.predict(x_test)
    return mean_squared_error(y_test, y_pred_baseline)


def getBestParams(x_train, y_train):
    dt_experiment = DecisionTreeRegressor(random_state=42)
    param_grid = {
        'max_depth': np.arange(8, 18),
        'min_samples_split': np.arange(2, 3),
        'min_samples_leaf': np.arange(2, 3)
    }

    # Perform grid search with cross-validation
    grid_search = GridSearchCV(dt_experiment, param_grid, cv=4, scoring='neg_mean_squared_error')
    grid_search.fit(x_train, y_train)
    # print("Best hyperparameters:", grid_search.best_params_)
    # print("Best score:", -grid_search.best_score_)
    return grid_search.best_params_


def createDtrWithBestParams(best_params):
    return DecisionTreeRegressor(
        random_state=42,
        max_depth=best_params['max_depth'],
        min_samples_split=best_params['min_samples_split'],
        min_samples_leaf=best_params['min_samples_leaf']
    )


def runModeler():
    data, speeds = getData()

    # x_train: training resources
    # x_test: testing resources
    # y_train: training target
    # y_test: testing target
    x_train, x_test, y_train, y_test = train_test_split(data, speeds, test_size=0.2, random_state=42)

    # Baseline mse
    mse_baseline = createBaseline(x_train, x_test, y_train, y_test)

    # Advanced mse
    dt_advanced = createDtrWithBestParams(getBestParams(x_train, y_train))
    dt_advanced.fit(x_train, y_train)
    y_pred_advanced = dt_advanced.predict(x_test)
    mse_advanced = mean_squared_error(y_test, y_pred_advanced)
    mse_difference = mse_advanced - mse_baseline

    if mse_advanced < mse_baseline:
        print('\033[32m' + "Advanced < Baseline:" + '\033[0m' + f"\n  {mse_advanced} < {mse_baseline}")
        print(f"    difference: \033[32m{mse_difference}\033[0m")
        return True
    else:
        print('\033[31m' + "Advanced > Baseline:" + '\033[0m' + f"\n  {mse_advanced} > {mse_baseline}")
        print(f"    difference: \033[31m{mse_difference}\033[0m")
        return False


# MAIN
def main():
    runModeler()


if __name__ == "__main__":
    main()
