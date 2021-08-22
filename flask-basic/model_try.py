"""
Code has been adapted from:
https://gitlab.doc.ic.ac.uk/lab2021_autumn/neural_networks_72
"""

from flask import Blueprint, jsonify, request
import numpy as np
import pandas as pd
import torch
import pickle
import os
from sklearn import preprocessing
import matplotlib.pyplot as plt
import sys
import json

pd.set_option('mode.chained_assignment', None)

class Network(torch.nn.Module):
    
    def __init__(self, input_dimension, output_dimension, hidden_units=32, dropout_rate=0.3):
        super(Network, self).__init__()
        self.layer_1 = torch.nn.Linear(in_features=input_dimension, out_features=hidden_units)
        self.layer_2 = torch.nn.Linear(in_features=hidden_units, out_features=hidden_units)
        self.layer_3 = torch.nn.Linear(in_features=hidden_units, out_features=hidden_units)

        self.batch_norm1 = torch.nn.BatchNorm1d(input_dimension)
        self.batch_norm2 = torch.nn.BatchNorm1d(hidden_units)
        self.batch_norm3 = torch.nn.BatchNorm1d(hidden_units)
        self.batch_norm4 = torch.nn.BatchNorm1d(hidden_units)

        self.drops = torch.nn.Dropout(dropout_rate)
        self.output_layer = torch.nn.Linear(in_features=hidden_units, out_features=output_dimension)

    def forward(self, input_data):
        """
        Make a forward pass through the neural network
        """
        self.eval()

        # define the activation function for the layers
        x = self.batch_norm1(input_data)
        x = torch.sigmoid(self.layer_1(x))
        x = self.drops(x)
        x = self.batch_norm2(x)
        x = torch.sigmoid(self.layer_2(x))
        x = self.drops(x)
        x = self.batch_norm3(x)
        x = torch.sigmoid(self.layer_3(x))
        x = self.drops(x)
        x = self.batch_norm4(x)

        output = torch.sigmoid(self.output_layer(x))
        return output

class Regressor():

    def __init__(self, x, nb_epoch=10, learning_rate=0.0002, hidden_units=32, dropout_rate=0.3):
        """ 
        Initialise the model
        Requires pandas dataframe as input
        """
        self.max_values = None
        self.min_values = None
        self.y_max_values = None
        self.y_min_values = None

        self.binarizers = []

        # store values from training to be used in practice
        self.input_size = None
        self.output_size = 1
        self.nb_epoch = nb_epoch
        self.learning_rate = learning_rate
        self.hidden_units = hidden_units
        self.dropout_rate = dropout_rate

        self.model = None
        self.optimizer = None

    def _preprocessor(self, x, y = None, training = False):
        """ 
        Preprocess input of the network
        Takes pandas data frame as input and returns tensors in PyTorch
        """

        categorical_cols = ['PROPERTY_TYPE', 'GLAZED_TYPE', 'HOTWATER_DESCRIPTION', 'FLOOR_DESCRIPTION', 'WALLS_DESCRIPTION', 'ROOF_DESCRIPTION', 'MAINHEAT_DESCRIPTION', 'MAINHEATCONT_DESCRIPTION', 'MAIN_FUEL', 'CONSTRUCTION_AGE_BAND']
        
        # map the True/False columns to 1 and 0
        x['MAINS_GAS_FLAG'] = x['MAINS_GAS_FLAG'].map({'True': 1, 'False': 0})
        x['SOLAR_WATER_HEATING_FLAG'] = x['SOLAR_WATER_HEATING_FLAG'].map({'True': 1, 'False': 0})

        if not training:
            # binarize each categorical column
            for col in range(len(self.binarizers)):
                current = self.binarizers[col].transform(x[categorical_cols[col]])
                new_cols = list(self.binarizers[col].classes_)
                new_df = pd.DataFrame(current)
                new_df.columns = new_cols
                new_df.index = x.index
                x = pd.concat([x, new_df], axis=1)
                x = x.drop([categorical_cols[col]], axis=1)

            # normalize values and convert to tensor 
            normalized_x = (x - self.min_values) / (self.max_values - self.min_values)
            normalized_x = normalized_x.astype('float32')
            x = torch.tensor(normalized_x.values, dtype=torch.float32)
            if isinstance(y, pd.DataFrame):
                normalized_y = (y - self.y_min_values) / (self.y_max_values - self.y_min_values)
                y_tensor = torch.tensor(normalized_y.values, dtype=torch.float32)
            return x, (y_tensor if isinstance(y, pd.DataFrame) else None)

        self.binarizers = []

        # use binarizers from training to binarize current input
        for col in categorical_cols:
            lb = preprocessing.LabelBinarizer()
            current_binarizer = lb.fit_transform(x[col])
            self.binarizers.append(lb)
            new_cols = list(lb.classes_)
            new_df = pd.DataFrame(current_binarizer)
            new_df.columns = new_cols
            new_df.index = x.index
            x = pd.concat([x, new_df], axis=1)
            x = x.drop([col], axis=1)
        
        # store the max and min values of each column
        self.max_values = x.max()
        self.min_values = x.min()

        # normalize dataset with min-max scaling
        normalized_x = (x - x.min()) / (x.max() - x.min())

        # convert to tensors
        x = torch.tensor(normalized_x.values, dtype=torch.float32)

        if isinstance(y, pd.DataFrame):
            self.y_max_values = y.max()
            self.y_min_values = y.min()
            normalized_y = (y - y.min()) / (y.max() - y.min())
            y_tensor = torch.tensor(normalized_y.values, dtype=torch.float32)

        return x, (y_tensor if isinstance(y, pd.DataFrame) else None)
        
    def fit(self, x, y, x_val=None, y_val=None):
        """
        Train a regressor model given the input and expected output
        Returns a trained model
        """

        X, Y = self._preprocessor(x, y = y, training = True)

        # create neural network with Adam optimizer and MSE loss
        self.input_size = X.shape[1]
        self.model = Network(self.input_size, self.output_size, self.hidden_units, self.dropout_rate)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)
        data_size, input_size = X.shape
        minibatch_size = 128
        loss_fn = torch.nn.MSELoss()

        losses = []

        # run model for epochs provided
        for epoch in range(self.nb_epoch):

            permutation = torch.randperm(data_size)
            epoch_losses = []

            # at each epoch run the batch through the network and collect the loss
            for i in range(0, data_size, minibatch_size):
                
                self.optimizer.zero_grad()

                indices = permutation[i:i + minibatch_size]
                X_batch, Y_batch = X[indices], Y[indices]

                Y_pred = self.model.forward(X_batch.float())

                loss = loss_fn(Y_pred, Y_batch.float())
                epoch_losses.append(loss.item())

                # back propagate the gradient
                loss.backward()
                self.optimizer.step()

            losses.append(np.mean(epoch_losses))

        return losses
            
    def predict(self, x):
        """
        Use a trained model to predict the output for a dataframe provided
        """

        # preprocess data and propagate through network
        X, _ = self._preprocessor(x, training = False)
        predicted_y = self.model.forward(X.float())

        # scale the data back to original value after normalization to get the energy efficiency score 
        predicted_y = predicted_y.detach().numpy()
        predicted_y = pd.DataFrame(predicted_y, columns=['CURRENT_ENERGY_EFFICIENCY'])
        multiplication_constant = self.y_max_values - self.y_min_values
        mult_result = pd.DataFrame(predicted_y.values * multiplication_constant.values, columns=predicted_y.columns, index=predicted_y.index)
        scaled_predicted_y = mult_result + self.y_min_values
        scaled_predicted_y = scaled_predicted_y.values

        return scaled_predicted_y

    def score(self, x, y):
        """
        Evaluates the neural network by taking an input, running it through the neural network and comparing with expected output
        Returns loss values
        """

        # predict output based on input given 
        loss_fn = torch.nn.MSELoss()
        Y_pred = self.predict(x)
        Y_pred = torch.tensor(Y_pred)

        Y = torch.tensor(y.values, dtype=torch.float32)

        loss = loss_fn(Y_pred, Y).item()

        return loss, loss**(1/2)

def save_regressor(trained_model, path=None): 
    """
    Utility function to save the trained regressor model as a pickle model
    """
    with open(path, 'wb') as target:
        pickle.dump(trained_model, target)

def load_regressor(path=None): 
    """ 
    Utility function to load the trained regressor model as a pickle model
    """
    with open(path, 'rb') as target:
        trained_model = pickle.load(target)
    return trained_model

def RegressorHyperParameterSearch(dataset, output_label, k=5, seed=10): 
    """
    Run a hyperparameter search to find the best hyperparameter values
    """

    HYPER_PARAMS_SPACE = []
    for nb_epoch in [10]:
        for lr in [0.002, 0.001]:
            for hidden_units in [48, 64, 80]:
                for dropout_rate in [0.3, 0.4, 0.5]:
                    HYPER_PARAMS_SPACE += [[nb_epoch, lr, hidden_units, dropout_rate]]

    # save original dataset and randomize
    data = dataset.copy()
    data.sample(frac=1)

    avg_RMSE_s = np.zeros((len(HYPER_PARAMS_SPACE), 1))

    N, _ = data.shape
    a = N // k

    # create a neural network for each set of hyperparameters and evaluate
    for i, hyper_params in enumerate(HYPER_PARAMS_SPACE):

        for j in range(0, k):

            validate = data[a*j:a*(j+1)]
            train = pd.concat((data[:a*j], data[a*(j+1):]), axis=0)
        
            x_train = train.loc[:, train.columns != output_label]
            y_train = train.loc[:, [output_label]]

            x_val = validate.loc[:, validate.columns != output_label]
            y_val = validate.loc[:, [output_label]]

            regressor = Regressor(x_train, nb_epoch = hyper_params[0], learning_rate=hyper_params[1])
            losses = regressor.fit(x_train, y_train)

            _, RMSE = regressor.score(x_val, y_val)

            # collect average RMSE for each batch
            if j == 0:
                avg_RMSE_s[i] = RMSE
            else:
                avg_RMSE_s[i] = (j / (j + 1)) * (avg_RMSE_s[i] + (RMSE / j))

    opt_params_indice = np.argmin(avg_RMSE_s)

    return HYPER_PARAMS_SPACE[opt_params_indice], avg_RMSE_s[opt_params_indice]

def train_model(file=None):
    """
    Train a model given a CSV file as input
    Returns the trained model
    """

    if not file:
        return

    # read CSV file and convert to pandas dataframe
    output_label = 'CURRENT_ENERGY_EFFICIENCY'
    used_cols = ['CURRENT_ENERGY_EFFICIENCY', 'PROPERTY_TYPE', 'MAINS_GAS_FLAG', 'GLAZED_TYPE', 'NUMBER_HABITABLE_ROOMS', 'LOW_ENERGY_LIGHTING', 'HOTWATER_DESCRIPTION', 'FLOOR_DESCRIPTION', 'WALLS_DESCRIPTION', 'ROOF_DESCRIPTION', 'MAINHEAT_DESCRIPTION', 'MAINHEATCONT_DESCRIPTION', 'MAIN_FUEL', 'SOLAR_WATER_HEATING_FLAG', 'CONSTRUCTION_AGE_BAND']
    data_types = {'CURRENT_ENERGY_EFFICIENCY': 'int', 'PROPERTY_TYPE': 'string', 'MAINS_GAS_FLAG': 'string', 'GLAZED_TYPE': 'string', 'NUMBER_HABITABLE_ROOMS': 'int', 'LOW_ENERGY_LIGHTING': 'int', 'HOTWATER_DESCRIPTION': 'string', 'FLOOR_DESCRIPTION': 'string', 'WALLS_DESCRIPTION': 'string', 'ROOF_DESCRIPTION': 'string', 'MAINHEAT_DESCRIPTION': 'string', 'MAINHEATCONT_DESCRIPTION': 'string', 'MAIN_FUEL': 'string', 'SOLAR_WATER_HEATING_FLAG': 'string', 'CONSTRUCTION_AGE_BAND': 'string'}
    data = pd.read_csv(file, usecols=used_cols, dtype=data_types)

    # use 80-20 split for train and test
    data = data.sample(frac=1)
    msk = np.random.rand(len(data)) < 0.8
    train = data[msk]
    test = data[~msk]

    x_train = train.loc[:, train.columns != output_label]
    y_train = train.loc[:, [output_label]]

    x_test = test.loc[:, test.columns != output_label]
    y_test = test.loc[:, [output_label]]

    # create the neural network
    regressor = Regressor(x_train, nb_epoch=10, learning_rate=0.002, hidden_units=64, dropout_rate=0.3)
    losses = regressor.fit(x_train, y_train)

    return regressor, RMSE

def create_all_models():
    """
    Creates a neural network model for each post town and saves it as a pickle file
    """

    directory = "DB Outputs"
    df = pd.DataFrame(columns = ['Name', 'Test RMSE'])

    # create pickle model for each CSV file in directory
    for file in os.listdir(directory):
        print("Working on file: " + file)

        # if model exists then skip it
        if ".csv" not in file or (file.replace(".csv", "") + ".pickle") in os.listdir("Pickle Models"):
            print("Model already exists, skipping file: " + file)
            continue

        # create model
        regressor, error = train_model(directory + '/' + file)

        # save model as pickle file
        name = "Pickle Models/" + file.replace(".csv", "") + ".pickle"
        save_regressor(regressor, name)

        # save the error in another file
        df = df.append({'Name': file.replace(".csv", ""), 'Test RMSE': error}, ignore_index=True)
        print(file + "\t" +  str(error) + "\n")

    df.to_csv("Pickle Model Errors.csv", index=False)

def make_one_prediction(filename=None, inputs={}):
    """
    Load a pickle model and use it to make one prediction based on the inputs given
    Returns the predicted energy efficiency score on a scale of 0 to 100
    """

    # load the model
    regressor = load_regressor(filename)

    # prepare the input 
    used_cols = ['PROPERTY_TYPE', 'MAINS_GAS_FLAG', 'GLAZED_TYPE', 'NUMBER_HABITABLE_ROOMS', 'LOW_ENERGY_LIGHTING', 'HOTWATER_DESCRIPTION', 'FLOOR_DESCRIPTION', 'WALLS_DESCRIPTION', 'ROOF_DESCRIPTION', 'MAINHEAT_DESCRIPTION', 'MAINHEATCONT_DESCRIPTION', 'MAIN_FUEL', 'SOLAR_WATER_HEATING_FLAG', 'CONSTRUCTION_AGE_BAND']
    df = pd.DataFrame(columns=used_cols)
    df = df.append(new_row, ignore_index=True)

    # run the model and return the result
    result = regressor.predict(df)
    print(result[0][0])
    return result[0][0]

if __name__ == "__main__":
    """
    Takes a filename and property data as json input and loads the model from the to make one prediction
    """
    file = sys.argv[1]
    new_row = json.loads(sys.argv[2])
    to_return = make_one_prediction(file, new_row)
