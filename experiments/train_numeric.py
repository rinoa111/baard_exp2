import argparse
import datetime
import os
import sys
import time

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision as tv
import torchvision.datasets as datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset

sys.path.append(os.getcwd())
# # Adding the parent directory.
from models.numeric import NumericModel
from experiments.train_pt import train, validate

DATA_NAMES = ['banknote', 'htru2', 'segment', 'texture']
DATA = {
    'banknote': {'file_name': 'banknote_preprocessed.csv', 'n_features': 4, 'n_test': 400, 'n_classes': 2},
    'htru2': {'file_name': 'htru2_preprocessed.csv', 'n_features': 8, 'n_test': 4000, 'n_classes': 2},
    'segment': {'file_name': 'segment_preprocessed.csv', 'n_features': 18, 'n_test': 400, 'n_classes': 7},
    'texture': {'file_name': 'texture_preprocessed.csv', 'n_features': 40, 'n_test': 600, 'n_classes': 11},
}
RANDOM_STATE = int(2**12)


def load_csv(file_path):
    """Load a pre-processed CSV file."""
    df = pd.read_csv(file_path, sep=',')
    y = df['Class'].to_numpy().astype(np.long)
    X = df.drop(['Class'], axis=1).to_numpy().astype(np.float32)
    return X, y


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, required=True, choices=DATA_NAMES)
    parser.add_argument('--data_path', type=str, default='data')
    parser.add_argument('--output_path', type=str, default='results')
    parser.add_argument('--batch_size', type=int, default=128)
    parser.add_argument('--epochs', type=int, default=5)
    args = parser.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print('Device: {}'.format(device))

    # Prepare data
    data_path = os.path.join(args.data_path, DATA[args.data]['file_name'])
    print('Read file: {}'.format(data_path))
    X, y = load_csv(data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=DATA[args.data]['n_test'], random_state=RANDOM_STATE)
    scaler = MinMaxScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    dataset_train = TensorDataset(
        torch.from_numpy(X_train).type(torch.float32),
        torch.from_numpy(y_train).type(torch.long))
    dataset_test = TensorDataset(
        torch.from_numpy(X_test).type(torch.float32),
        torch.from_numpy(y_test).type(torch.long))
    dataloader_train = DataLoader(dataset_train, args.batch_size, shuffle=True)
    dataloader_test = DataLoader(dataset_test, args.batch_size, shuffle=True)
    print('Train set: {}, Test set: {}'.format(X_train.shape, X_test.shape))

    # Prepare model
    n_features = DATA[args.data]['n_features']
    n_classes = DATA[args.data]['n_classes']
    print('n_features: {}, n_classes: {}'.format(n_features, n_classes))
    model = NumericModel(n_features,
                         n_hidden=n_features * 4,
                         n_classes=n_classes).to(device)
    optimizer = optim.SGD(model.parameters(), lr=0.01,
                          momentum=0.9, weight_decay=5e-4)
    loss = nn.CrossEntropyLoss()
    scheduler = optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=args.epochs, eta_min=1e-7)

    # Train model
    since = time.time()
    for epoch in range(args.epochs):
        start = time.time()
        tr_loss, tr_acc = train(model, dataloader_train,
                                loss, optimizer, device)
        va_loss, va_acc = validate(model, dataloader_test, loss, device)
        scheduler.step()

        time_elapsed = time.time() - start
        print(('{:2d}/{:d}[{:s}] Train Loss: {:.4f} Acc: {:.4f}%, ' +
               'Test Loss: {:.4f} Acc: {:.4f}%').format(
            epoch + 1, args.epochs,
            str(datetime.timedelta(seconds=time_elapsed)),
            tr_loss, tr_acc*100.,
            va_loss, va_acc*100.))

    time_elapsed = time.time() - since
    print('Total run time: {:.0f}m {:.1f}s'.format(
        time_elapsed // 60,
        time_elapsed % 60))

    # Save model
    file_name = os.path.join(
        args.output_path, '{}_{}.pt'.format(args.data, args.epochs))
    print('Output file name: {}'.format(file_name))
    torch.save(model.state_dict(), file_name)


if __name__ == '__main__':
    main()
