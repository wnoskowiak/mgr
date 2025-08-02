import torch
from torch.utils.data import Dataset
from PIL import Image
import numpy as np


class EventDataset(Dataset):
    def __init__(self, combined_dataset, transform=None, label_column=None):
        self.data_frame = combined_dataset
        self.transform = transform
        self.label_column = label_column

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        # Convert sparse tensors back to dense
        image = self.data_frame.iloc[idx]["plane2_sparse_tensor"].to_dense().numpy()

        if self.transform:
            image = self.transform(Image.fromarray(image))

        label = self.data_frame.iloc[idx][self.label_column] if self.label_column else self.data_frame.iloc[idx, 3]
        return image, label


class EventDatasetThree(Dataset):
    def __init__(self, combined_dataset, transform=None, label_column=None):
        self.data_frame = combined_dataset
        self.transform = transform
        self.label_column = label_column

    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        # Get dense images from all three planes
        plane0 = self.data_frame.iloc[idx]["plane0_sparse_tensor"].to_dense().numpy()
        plane1 = self.data_frame.iloc[idx]["plane1_sparse_tensor"].to_dense().numpy()
        plane2 = self.data_frame.iloc[idx]["plane2_sparse_tensor"].to_dense().numpy()

        # Stretch plane0 and plane1 2x in x dimension (axis=1)
        def stretch_x(img, factor):
            pil_img = Image.fromarray(img)
            new_width = img.shape[1] * factor
            pil_img = pil_img.resize((new_width, img.shape[0]), resample=Image.NEAREST)
            return np.array(pil_img)

        plane0_stretched = stretch_x(plane0, 2)
        plane1_stretched = stretch_x(plane1, 2)

        target_width = plane0_stretched.shape[1]
        pad_total = target_width - plane2.shape[1]
        pad_left = pad_total // 2
        pad_right = pad_total - pad_left
        plane2_padded = np.pad(plane2, ((0, 0), (pad_left, pad_right)), mode='constant')

        stacked = np.stack([plane0_stretched, plane1_stretched, plane2_padded], axis=0)  # shape: (3, H, W)

        if self.transform:
            stacked_img = np.transpose(stacked, (1, 2, 0))  # (H, W, 3)
            stacked_img = Image.fromarray(stacked_img.astype(np.uint8))
            image = self.transform(stacked_img)
        else:
            image = torch.tensor(stacked, dtype=torch.float32)

        label = self.data_frame.iloc[idx][self.label_column] if self.label_column else self.data_frame.iloc[idx, 3]
        return image, label