# -*- coding: utf-8 -*-
"""Ручные оптимизаторы для части 2 лабораторной 8: Adam, AdamW, AMSGrad."""

import numpy as np


class _AdamBase:
    def __init__(self, lr=0.05, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.t = 0
        self.m = None
        self.v = None

    def _moments(self, grad):
        if self.m is None:
            self.m = np.zeros_like(grad)
            self.v = np.zeros_like(grad)
        self.t += 1
        self.m = self.beta1 * self.m + (1.0 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1.0 - self.beta2) * (grad ** 2)
        m_hat = self.m / (1.0 - self.beta1 ** self.t)
        v_hat = self.v / (1.0 - self.beta2 ** self.t)
        return m_hat, v_hat


class Adam(_AdamBase):
    """Adam: шаг делится на корень скользящего среднего квадратов градиента.

    m гасит дрожание направления, v не даёт большому градиенту сделать огромный шаг.
    Поправка (1 - beta^t) снимает смещение первых шагов, когда средние ещё около нуля.
    """

    def step(self, weights, grad):
        m_hat, v_hat = self._moments(grad)
        return weights - self.lr * m_hat / (np.sqrt(v_hat) + self.eps)


class AdamW(_AdamBase):
    """AdamW: затухание весов вычитается отдельно от адаптивного шага.

    В обычном Adam штраф weight decay попадает внутрь градиента и тоже делится
    на корень v. У AdamW штраф всегда равен lr * decay * w, без этого деления.
    """

    def __init__(self, lr=0.05, beta1=0.9, beta2=0.999, eps=1e-8, weight_decay=0.01):
        super().__init__(lr, beta1, beta2, eps)
        self.weight_decay = weight_decay

    def step(self, weights, grad):
        m_hat, v_hat = self._moments(grad)
        adapted = m_hat / (np.sqrt(v_hat) + self.eps)
        return weights - self.lr * (adapted + self.weight_decay * weights)


class AMSGrad(_AdamBase):
    """AMSGrad помнит наибольшую оценку второго момента и не даёт шагу снова вырасти.

    У Adam знаменатель sqrt(v_hat) иногда уменьшается, и шаг внезапно становится
    длиннее. AMSGrad держит v_max = max(v_max, v_hat) и делит только на него.
    """

    def __init__(self, lr=0.05, beta1=0.9, beta2=0.999, eps=1e-8):
        super().__init__(lr, beta1, beta2, eps)
        self.v_max = None

    def step(self, weights, grad):
        m_hat, v_hat = self._moments(grad)
        if self.v_max is None:
            self.v_max = v_hat.copy()
        else:
            self.v_max = np.maximum(self.v_max, v_hat)
        return weights - self.lr * m_hat / (np.sqrt(self.v_max) + self.eps)


def quadratic_loss_and_grad(weights, target):
    """Выпуклая функция 0.5 * ||w - target||^2. Минимум в точке target, градиент w - target."""
    diff = weights - target
    loss = 0.5 * float(np.sum(diff ** 2))
    return loss, diff


def run_optimizer(optimizer, steps=50, dimension=5, seed=0):
    """Пятьдесят шагов к известной точке. Возвращает потери и нормы весов."""
    rng = np.random.default_rng(seed)
    target = rng.normal(size=dimension)
    weights = np.zeros(dimension)
    losses = []
    norms = []
    for _ in range(steps):
        loss, grad = quadratic_loss_and_grad(weights, target)
        losses.append(loss)
        norms.append(float(np.linalg.norm(weights)))
        weights = optimizer.step(weights, grad)
    return np.asarray(losses), np.asarray(norms), weights, target
