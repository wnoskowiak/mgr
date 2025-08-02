import os
import pickle
import pandas as pd
import numpy as np
import torch
from PIL import Image


def load_datasets(directory_path):
    """
    Loads pickled DataFrames from the given directory and concatenates them into a single DataFrame.
    Ignores files with 'nue' in the filename.
    Returns the combined DataFrame.
    """
    dataframes = pd.DataFrame()
    file_count = 0

    for filename in os.listdir(directory_path):
        if filename.endswith('.pkl') and 'nue' not in filename:
            print(f"Loading file: {filename}")
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'rb') as f:
                df = pickle.load(f)
                dataframes = pd.concat([dataframes, df], ignore_index=True)
            
            file_count += 1
            if file_count >= 100:
                break

    print(f"First {file_count} pickled datasets loaded and combined successfully!")
    return dataframes


def get_full_dataset(directory):
    """
    Loads, shuffles, and adds the 'is_cc_nue' column to the combined dataset.
    Returns the processed DataFrame.
    """
    combined_dataset = load_datasets(directory)
    
    csv_path = os.path.join(directory, 'parsed_data_from_dataset_bnb.csv')
    dataset = pd.read_csv(csv_path)
    
    csv_pathDos = os.path.join(directory, 'parsed_data_from_dataset_bnbdos.csv')
    dataset2 = pd.read_csv(csv_pathDos)
    
    dataset = pd.concat([dataset, dataset2], ignore_index=True)

    # Shuffle the combined_dataset randomly
    combined_dataset = combined_dataset.sample(frac=1).reset_index(drop=True)
    print("Dataset shuffled successfully!")
    
    merged = pd.merge(dataset, combined_dataset, on=['run', 'subrun', 'event'], suffixes=('_csv', '_combined'))

    # Add extra column: 1 if 'is_cc' == 1 and 'nu_pdg' == 12 or -12, else 0
    merged['is_cc_nue'] = (
        (merged['is_cc'] == 1) &
        (merged['nu_pdg'].isin([12, -12]))
    ).astype(int)

    return merged


def get_full_dataset_alt(directory):
    """
    Alternative dataset loader with additional filtering.
    """
    combined_dataset = load_datasets(directory)
    
    csv_path = os.path.join(directory, 'parsed_data_from_dataset_bnb.csv')
    dataset = pd.read_csv(csv_path)
    
    csv_pathDos = os.path.join(directory, 'parsed_data_from_dataset_bnbdos.csv')
    dataset2 = pd.read_csv(csv_pathDos)
    
    dataset = pd.concat([dataset, dataset2], ignore_index=True)

    combined_dataset = combined_dataset.sample(frac=1).reset_index(drop=True)
    print("Dataset shuffled successfully!")
    
    merged = pd.merge(dataset, combined_dataset, on=['run', 'subrun', 'event'], suffixes=('_csv', '_combined'))

    merged['is_cc_nue'] = (
        (merged['is_cc'] == 1) &
        (merged['nu_pdg'].isin([12, -12]))
    ).astype(int)
    
    merged['flag2'] = (
        ((merged['nu_pdg'] == 14) | (merged['nu_pdg'] == -14)) &
        (merged['is_cc'] == 0)
    ).astype(int)
    
    filtered = merged[(merged['is_cc_nue'] == 1) | (merged['flag2'] == 1)]

    return filtered


def get_top50_events_dataset(directory):
    """
    Returns the top 50% of events by lepton energy.
    """
    tmp = get_full_dataset(directory).copy()
    energy_threshold = tmp['lep_energy'].quantile(0.5)
    return tmp[tmp['lep_energy'] >= energy_threshold]


def get_balanced_dataset(df, label_column):
    """
    Creates a balanced dataset by sampling equal numbers from each class.
    """
    ones = df[df[label_column] == 1]
    zeros = df[df[label_column] == 0]
    min_len = min(len(ones), len(zeros))
    balanced = pd.concat([
        ones.sample(min_len, random_state=42),
        zeros.sample(min_len, random_state=42)
    ]).sample(frac=1, random_state=42).reset_index(drop=True)
    return balanced


def compare_sparse_dense_sizes(df, tensor_column='plane0_sparse_tensor'):
    """
    Calculates total memory usage (in MB) for sparse and dense tensors in the given column of the DataFrame.
    Returns (total_sparse_mb, total_dense_mb).
    """
    total_sparse_bytes = 0
    total_dense_bytes = 0

    for tensor in df[tensor_column]:
        if tensor is not None:
            # Sparse tensor memory
            tensor = tensor.coalesce()
            indices_mem = tensor.indices().numel() * tensor.indices().element_size()
            values_mem = tensor.values().numel() * tensor.values().element_size()
            total_sparse_bytes += indices_mem + values_mem

            # Dense tensor memory
            dense = tensor.to_dense()
            total_dense_bytes += dense.numel() * dense.element_size()

    total_sparse_mb = total_sparse_bytes / (1024 ** 2)
    total_dense_mb = total_dense_bytes / (1024 ** 2)
    print(f"Total sparse tensor memory: {total_sparse_mb:.2f} MB")
    print(f"Total dense tensor memory: {total_dense_mb:.2f} MB")
    return total_sparse_mb, total_dense_mb