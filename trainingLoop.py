import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import transforms
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, roc_curve, auc
import json
import os
import gc
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image


def train_model(
    combined_dataset,
    model_class,
    eventdataset_class,
    channels,
    num_epochs=10,
    batch_size=32,
    learning_rate=0.001,
    label_column=None,
    scale_factor=1.0,
    output_dir=".",
    train_ratio=0.7,
    val_ratio=0.15,
    test_ratio=0.15,
    random_state=42,
    experiment_name=None
):
    # Create experiment-specific output directory
    if experiment_name:
        output_dir = os.path.join(output_dir, experiment_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
   
    # Check for GPU availability
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name(0)}")

    # Split dataset into train, validation, and test
    print("Splitting dataset...")
    
    # First split: separate test set
    train_val_df, test_df = train_test_split(
        combined_dataset, 
        test_size=test_ratio, 
        random_state=random_state,
        stratify=combined_dataset[label_column] if label_column else None
    )
    
    # Second split: separate train and validation from remaining data
    val_size_adjusted = val_ratio / (train_ratio + val_ratio)
    train_df, val_df = train_test_split(
        train_val_df,
        test_size=val_size_adjusted,
        random_state=random_state,
        stratify=train_val_df[label_column] if label_column else None
    )
    
    print(f"Dataset split - Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")
    
    # Print class distribution for each split
    if label_column:
        print(f"Train class distribution: {train_df[label_column].value_counts().to_dict()}")
        print(f"Val class distribution: {val_df[label_column].value_counts().to_dict()}")
        print(f"Test class distribution: {test_df[label_column].value_counts().to_dict()}")

    # Compose transform with scaling
    transform_list = []
    if scale_factor != 1.0:
        def scale_size(img):
            w, h = img.size
            return (int(w * scale_factor), int(h * scale_factor))
        transform_list.append(transforms.Lambda(lambda img: img.resize(scale_size(img), Image.NEAREST)))
    transform_list.append(transforms.ToTensor())
    transform = transforms.Compose(transform_list)

    # Create datasets
    train_dataset = eventdataset_class(
        combined_dataset=train_df,
        transform=transform,
        label_column=label_column
    )
    val_dataset = eventdataset_class(
        combined_dataset=val_df,
        transform=transform,
        label_column=label_column
    )
    test_dataset = eventdataset_class(
        combined_dataset=test_df,
        transform=transform,
        label_column=label_column
    )

    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, pin_memory=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, pin_memory=True)

    # Infer input size from one sample
    sample_img, _ = train_dataset[0]
    input_height, input_width = sample_img.shape[1], sample_img.shape[2]
    model = model_class(input_height, input_width, channels)
    
    # Move model to GPU
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=0.9)

    # Initialize detailed history tracking
    detailed_history = {
        'iteration_losses': [],
        'iteration_epochs': [],
        'iteration_batches': [],
        'epoch_train_accuracies': [],
        'epoch_val_accuracies': [],
        'epoch_val_losses': [],
        'best_val_accuracy': 0.0,
        'test_accuracy': 0.0,
        'hyperparameters': {
            'num_epochs': num_epochs,
            'batch_size': batch_size,
            'learning_rate': learning_rate,
            'scale_factor': scale_factor,
            'model_class': model_class.__name__,
            'dataset_class': eventdataset_class.__name__
        }
    }

    # Training loop with validation
    best_val_accuracy = 0.0
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        train_correct = 0
        train_total = 0
        
        for i, (inputs, labels) in enumerate(train_loader):
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            # Save loss for every iteration
            detailed_history['iteration_losses'].append(loss.item())
            detailed_history['iteration_epochs'].append(epoch + 1)
            detailed_history['iteration_batches'].append(i + 1)
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            train_correct += (predicted == labels).sum().item()
            train_total += labels.size(0)

            if (i + 1) % 20 == 0:
                avg_loss = running_loss / 20
                print(f"[{epoch + 1}, {i + 1}] loss: {avg_loss:.3f}")
                running_loss = 0.0

        train_accuracy = train_correct / train_total if train_total > 0 else 0
        detailed_history['epoch_train_accuracies'].append(train_accuracy)
        
        # Validation phase
        model.eval()
        val_correct = 0
        val_total = 0
        val_loss = 0.0
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                
                _, predicted = torch.max(outputs.data, 1)
                val_correct += (predicted == labels).sum().item()
                val_total += labels.size(0)
        
        val_accuracy = val_correct / val_total if val_total > 0 else 0
        avg_val_loss = val_loss / len(val_loader)
        
        detailed_history['epoch_val_accuracies'].append(val_accuracy)
        detailed_history['epoch_val_losses'].append(avg_val_loss)
        
        print(f"Epoch {epoch + 1}: Train Acc: {train_accuracy:.4f}, Val Acc: {val_accuracy:.4f}, Val Loss: {avg_val_loss:.4f}")
        
        # Save best model
        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            detailed_history['best_val_accuracy'] = best_val_accuracy
            best_model_path = os.path.join(output_dir, "best_model.pth")
            torch.save(model.state_dict(), best_model_path)
            print(f"New best model saved with validation accuracy: {best_val_accuracy:.4f}")

    # Test phase with confusion matrix AND ROC curve
    print("\nEvaluating on test set...")
    model.load_state_dict(torch.load(best_model_path))
    model.eval()
    
    # Collect all predictions, probabilities, and true labels
    all_predictions = []
    all_probabilities = []
    all_labels = []
    test_correct = 0
    test_total = 0
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            
            # Get probabilities for ROC curve
            probabilities = torch.softmax(outputs, dim=1)
            all_probabilities.extend(probabilities[:, 1].cpu().numpy())
            
            _, predicted = torch.max(outputs.data, 1)
            
            # Collect predictions and labels for confusion matrix
            all_predictions.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            
            test_correct += (predicted == labels).sum().item()
            test_total += labels.size(0)
    
    test_accuracy = test_correct / test_total if test_total > 0 else 0
    detailed_history['test_accuracy'] = test_accuracy
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Calculate ROC curve
    fpr, tpr, thresholds = roc_curve(all_labels, all_probabilities)
    roc_auc = auc(fpr, tpr)
    
    # Generate confusion matrix
    cm = confusion_matrix(all_labels, all_predictions)
    
    # Calculate metrics
    tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)
    
    # Calculate additional metrics
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Add metrics to history
    detailed_history['confusion_matrix'] = cm.tolist()
    detailed_history['roc_curve'] = {
        'fpr': fpr.tolist(),
        'tpr': tpr.tolist(),
        'thresholds': thresholds.tolist(),
        'auc': roc_auc
    }
    detailed_history['test_metrics'] = {
        'accuracy': test_accuracy,
        'precision': precision,
        'recall': recall,
        'specificity': specificity,
        'f1_score': f1_score,
        'roc_auc': roc_auc,
        'true_positives': int(tp),
        'true_negatives': int(tn),
        'false_positives': int(fp),
        'false_negatives': int(fn)
    }
    
    # Print metrics
    print(f"\nDetailed Metrics:")
    print(f"True Positives: {tp}")
    print(f"True Negatives: {tn}")
    print(f"False Positives: {fp}")
    print(f"False Negatives: {fn}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall (Sensitivity): {recall:.4f}")
    print(f"Specificity: {specificity:.4f}")
    print(f"F1-Score: {f1_score:.4f}")
    print(f"ROC AUC: {roc_auc:.4f}")
    print("Finished Training")
    
    # Save final model
    final_model_path = os.path.join(output_dir, "final_model.pth")
    model = model.cpu()
    torch.save(model.state_dict(), final_model_path)
    
    # Save training history
    history_path = os.path.join(output_dir, f"training_history_{experiment_name}_{timestamp}.json")
    with open(history_path, 'w') as f:
        json.dump(detailed_history, f, indent=2)
    
    # Clean up GPU memory
    del model, optimizer, criterion
    del train_loader, val_loader, test_loader
    gc.collect()
    torch.cuda.empty_cache()
    
    return detailed_history, history_path