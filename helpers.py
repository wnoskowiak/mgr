import os
import numpy as np
import torch
import random
import matplotlib.pyplot as plt
import pickle
from datetime import datetime
from PIL import Image
import re


def average_png_size(directory):
    """
    Calculates the average size (in bytes) of all PNG files in the given directory.
    """
    png_files = [f for f in os.listdir(directory) if f.lower().endswith('.png')]
    if not png_files:
        return 0
    total_size = sum(os.path.getsize(os.path.join(directory, f)) for f in png_files)
    return total_size / len(png_files)


def getSize(imagePath):
    """
    Converts an image to a sparse tensor and calculates its memory usage.
    """
    image = Image.open(imagePath)
    image = image.convert('L')
    image_array = np.array(image)
    image_array = 255 - image_array
    
    dense_tensor = torch.tensor(image_array, dtype=torch.uint8)

    # Find the indices of non-zero elements
    non_zero_indices = torch.nonzero(dense_tensor, as_tuple=True)
    
    # Get the values of the non-zero elements
    non_zero_values = dense_tensor[non_zero_indices]

    # Create a sparse tensor
    sparse_tensor = torch.sparse_coo_tensor(
        indices=torch.stack(non_zero_indices),
        values=non_zero_values,
        size=dense_tensor.shape
    )

    sparse_tensor = sparse_tensor.coalesce()
    
    indices_memory = sparse_tensor.indices().numel() * sparse_tensor.indices().element_size()
    values_memory = sparse_tensor.values().numel() * sparse_tensor.values().element_size()
    sparse_tensor_memory_bytes = indices_memory + values_memory
    sparse_tensor_memory_mb = sparse_tensor_memory_bytes / (1024 ** 2)
    
    return sparse_tensor, sparse_tensor_memory_mb


def insert_fragment_randomly(ds, fragment, label_column='is_cc_nue', tensor_column='plane2_sparse_tensor'):
    """
    For each row in ds where label_column == 1, insert the given fragment at a random location
    in the image stored in tensor_column. Modifies ds in-place.
    """
    frag_h, frag_w = fragment.shape
    for idx, row in ds[ds[label_column] == 1].iterrows():
        img = row[tensor_column].to_dense().numpy()
        H, W = img.shape

        # Choose a random top-left corner where the fragment fits
        max_y = H - frag_h
        max_x = W - frag_w
        if max_y < 0 or max_x < 0:
            continue  # Skip if fragment doesn't fit

        rand_y = random.randint(0, max_y)
        rand_x = random.randint(0, max_x)

        # Insert the fragment
        img[rand_y:rand_y+frag_h, rand_x:rand_x+frag_w] = fragment

        # Convert back to sparse tensor and update the DataFrame
        dense_tensor = torch.tensor(img, dtype=torch.uint8)
        non_zero_indices = torch.nonzero(dense_tensor, as_tuple=True)
        non_zero_values = dense_tensor[non_zero_indices]
        sparse_tensor = torch.sparse_coo_tensor(
            indices=torch.stack(non_zero_indices),
            values=non_zero_values,
            size=dense_tensor.shape
        ).coalesce()
        ds.at[idx, tensor_column] = sparse_tensor


def get_fragment_from_event(ds, run, subrun, event):
    """
    Extracts a fragment from the plane2 image of the event specified by run, subrun, event.
    Returns the fragment and its coordinates (x_min, x_max, y_min, y_max).
    """
    row = ds[(ds['run'] == run) & (ds['subrun'] == subrun) & (ds['event'] == event)]
    if row.empty:
        raise ValueError("Event not found in dataset.")
    plane2_img = row.iloc[0]['plane2_sparse_tensor'].to_dense().numpy()

    # Define the vertical and horizontal lines
    x1 = int(plane2_img.shape[1] * 43 / 128)
    x2 = int(plane2_img.shape[1] * 11 / 16)
    y1 = int(plane2_img.shape[0] * 5 / 32)
    y2 = int(plane2_img.shape[0] * 3 / 8)

    # Ensure x1 < x2 and y1 < y2
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)

    # Extract the fragment from the reference image
    fragment = plane2_img[y_min:y_max, x_min:x_max]
    return fragment, (x_min, x_max, y_min, y_max)


def parse_losses(log_path):
    """
    Parses a log file with lines like '[1, 1] loss: 0.080' and returns a list of (epoch, batch, loss) tuples.
    """
    results = []
    pattern = re.compile(r"\[(\d+),\s*(\d+)\]\s+loss:\s+([0-9.]+)")

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                epoch = int(match.group(1))
                batch = int(match.group(2))
                loss = float(match.group(3))
                results.append((epoch, batch, loss))
    return results


def save_experiment_results(experiment_results, summary):
    """
    Saves experiment results and summary to pickle files with timestamps.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save experiment_results as pickle
    experiment_results_path = f"experiment_results_{timestamp}.pkl"
    with open(experiment_results_path, 'wb') as f:
        pickle.dump(experiment_results, f)

    # Save summary as pickle
    summary_path = f"experiment_summary_{timestamp}.pkl"
    with open(summary_path, 'wb') as f:
        pickle.dump(summary, f)

    print(f"Experiment results saved to: {experiment_results_path}")
    print(f"Summary saved to: {summary_path}")

    # Save both in a single pickle file
    combined_results = {
        'experiment_results': experiment_results,
        'summary': summary,
        'timestamp': timestamp
    }

    combined_path = f"all_experiments_{timestamp}.pkl"
    with open(combined_path, 'wb') as f:
        pickle.dump(combined_results, f)

    print(f"Combined results saved to: {combined_path}")
    return experiment_results_path, summary_path, combined_path