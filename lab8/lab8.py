# -*- coding: utf-8 -*-
"""
Лабораторная работа 8 — свёрточная сеть на CIFAR-10 и сравнение оптимизаторов.

Запуск: python lab8/lab8.py
Графики: lab8/figures/
Данные CIFAR-10 скачиваются в lab8/data.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from optimizers import AMSGrad, Adam, AdamW, run_optimizer

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

CLASSES = [
    "самолёт",
    "автомобиль",
    "птица",
    "кошка",
    "олень",
    "собака",
    "лягушка",
    "лошадь",
    "корабль",
    "грузовик",
]
CLASS_EN = [
    "airplane",
    "automobile",
    "bird",
    "cat",
    "deer",
    "dog",
    "frog",
    "horse",
    "ship",
    "truck",
]


def categorical_crossentropy(probabilities, one_hot):
    """Среднее -sum y log p. Вероятности уже после softmax."""
    clipped = probabilities.clamp(min=1e-8)
    return -(one_hot * clipped.log()).sum(dim=1).mean()


class SmallCNN(nn.Module):
    """Два свёрточных блока, полносвязный слой, Dropout и softmax на 10 классов."""

    def __init__(self, channels=(32, 64), dropout=0.3, batch_norm=False):
        super().__init__()
        blocks = []
        in_channels = 3
        for out_channels in channels:
            blocks.append(nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1))
            if batch_norm:
                blocks.append(nn.BatchNorm2d(out_channels))
            blocks.append(nn.ReLU())
            blocks.append(nn.MaxPool2d(2))
            in_channels = out_channels
        self.features = nn.Sequential(*blocks)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(channels[-1] * 8 * 8, 128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, 10),
        )

    def forward(self, images):
        logits = self.classifier(self.features(images))
        return torch.softmax(logits, dim=1)

    def first_conv(self):
        return self.features[0]


def load_cifar(batch_size=128):
    transform = transforms.ToTensor()
    train = datasets.CIFAR10(DATA, train=True, download=True, transform=transform)
    test = datasets.CIFAR10(DATA, train=False, download=True, transform=transform)
    train_loader = DataLoader(train, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test, batch_size=batch_size, shuffle=False)
    return train_loader, test_loader


def epoch_pass(model, loader, optimizer=None):
    training = optimizer is not None
    model.train(training)
    total_loss = 0.0
    total_correct = 0
    total = 0
    grad_mode = torch.enable_grad() if training else torch.no_grad()
    with grad_mode:
        for images, labels in loader:
            one_hot = torch.nn.functional.one_hot(labels, num_classes=10).float()
            probabilities = model(images)
            loss = categorical_crossentropy(probabilities, one_hot)
            if training:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            predicted = probabilities.argmax(dim=1)
            total_loss += float(loss.detach()) * len(labels)
            total_correct += int((predicted == labels).sum())
            total += len(labels)
    return total_loss / total, total_correct / total


def train_model(model, train_loader, test_loader, epochs=10, lr=1e-3):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    history = []
    for epoch in range(1, epochs + 1):
        train_loss, train_acc = epoch_pass(model, train_loader, optimizer)
        test_loss, test_acc = epoch_pass(model, test_loader)
        history.append(
            {
                "epoch": epoch,
                "train_loss": train_loss,
                "train_acc": train_acc,
                "test_loss": test_loss,
                "test_acc": test_acc,
            }
        )
        print(
            f"  эпоха {epoch:02d}  train acc={train_acc:.3f}  test acc={test_acc:.3f}  "
            f"test loss={test_loss:.3f}"
        )
    return history


def predict_all(model, loader):
    model.eval()
    true_labels = []
    pred_labels = []
    images_kept = []
    kept = 0
    with torch.no_grad():
        for images, labels in loader:
            probabilities = model(images)
            true_labels.append(labels.numpy())
            pred_labels.append(probabilities.argmax(dim=1).numpy())
            if kept < 12:
                piece = images[: 12 - kept]
                images_kept.append(piece)
                kept += len(piece)
    return (
        np.concatenate(true_labels),
        np.concatenate(pred_labels),
        torch.cat(images_kept, dim=0),
    )


def plot_history(histories, path):
    fig, ax = plt.subplots(figsize=(7, 4))
    for name, history in histories.items():
        epochs = [row["epoch"] for row in history]
        ax.plot(epochs, [row["test_acc"] for row in history], marker="o", label=name)
    ax.set_xlabel("Эпоха")
    ax.set_ylabel("Accuracy на тесте")
    ax.set_title("Базовая и улучшенная сети")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def plot_confusion(y_true, y_pred, path):
    fig, ax = plt.subplots(figsize=(8, 7))
    ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        display_labels=CLASS_EN,
        xticks_rotation=45,
        ax=ax,
        colorbar=False,
    )
    ax.set_title("Матрица ошибок улучшенной сети")
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def plot_examples(images, y_true, y_pred, path):
    fig, axes = plt.subplots(3, 4, figsize=(10, 7))
    for ax, image, true_i, pred_i in zip(axes.ravel(), images, y_true, y_pred):
        picture = image.permute(1, 2, 0).numpy()
        ax.imshow(picture)
        mark = "верно" if true_i == pred_i else "ошибка"
        ax.set_title(f"{CLASS_EN[true_i]} → {CLASS_EN[pred_i]}\n{mark}", fontsize=8)
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def plot_filters(model, path):
    weight = model.first_conv().weight.detach().cpu()
    count = min(16, weight.shape[0])
    fig, axes = plt.subplots(4, 4, figsize=(6, 6))
    for ax, filt in zip(axes.ravel(), weight[:count]):
        image = filt.permute(1, 2, 0).numpy()
        image = image - image.min()
        image = image / max(image.max(), 1e-8)
        ax.imshow(image)
        ax.axis("off")
    fig.suptitle("Фильтры первого свёрточного слоя")
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def compare_optimizers(path):
    runs = {
        "Adam": Adam(lr=0.1),
        "AdamW": AdamW(lr=0.1, weight_decay=0.01),
        "AMSGrad": AMSGrad(lr=0.1),
    }
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for name, optimizer in runs.items():
        losses, norms, _weights, _target = run_optimizer(optimizer, steps=50, seed=0)
        axes[0].plot(losses, label=name)
        axes[1].plot(norms, label=name)
        print(f"  {name:8s} потеря 0→{losses[0]:.3f}, 49→{losses[-1]:.4f}")
    axes[0].set_title("Потеря за 50 шагов")
    axes[0].set_xlabel("Шаг")
    axes[0].set_ylabel("0.5 ||w - цель||²")
    axes[0].legend()
    axes[1].set_title("Норма весов")
    axes[1].set_xlabel("Шаг")
    axes[1].legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def main():
    torch.manual_seed(42)
    np.random.seed(42)
    print("=" * 60)
    print("1. CIFAR-10")
    print("=" * 60)
    train_loader, test_loader = load_cifar(batch_size=128)
    images, labels = next(iter(train_loader))
    print("Батч:", tuple(images.shape), "пиксели", float(images.min()), float(images.max()))
    print("Классы:", CLASS_EN)

    print("\n" + "=" * 60)
    print("2. Базовая сеть, 10 эпох, Adam")
    print("=" * 60)
    base = SmallCNN(channels=(32, 64), dropout=0.3, batch_norm=False)
    base_history = train_model(base, train_loader, test_loader, epochs=10, lr=1e-3)

    print("\n" + "=" * 60)
    print("3. Улучшенная сеть: BatchNorm, больше фильтров, Dropout 0.5")
    print("=" * 60)
    better = SmallCNN(channels=(64, 128), dropout=0.5, batch_norm=True)
    better_history = train_model(better, train_loader, test_loader, epochs=10, lr=1e-3)
    plot_history(
        {"базовая": base_history, "улучшенная": better_history},
        FIG / "01_accuracy.png",
    )

    y_true, y_pred, preview = predict_all(better, test_loader)
    print(f"\nТест улучшенной сети: accuracy={accuracy_score(y_true, y_pred):.4f}")
    plot_confusion(y_true, y_pred, FIG / "02_confusion.png")
    plot_examples(preview, y_true[:12], y_pred[:12], FIG / "03_examples.png")
    plot_filters(better, FIG / "04_filters.png")

    print("\n" + "=" * 60)
    print("4. Adam, AdamW и AMSGrad, 50 шагов")
    print("=" * 60)
    compare_optimizers(FIG / "05_optimizers.png")
    print(f"\nГрафики: {FIG}")


if __name__ == "__main__":
    main()
