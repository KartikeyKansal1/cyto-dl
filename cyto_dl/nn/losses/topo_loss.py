"""
Adapted from: https://github.com/search?q=repo%3Amarrlab%2FSHAPR_torch+torch_top&type=code
SHAPR
"""

import torch
import torch.nn as nn
from torch_topological.nn import CubicalComplex, VietorisRipsComplex
from torch_topological.nn import WassersteinDistance
from torch_topological.nn.data import batch_iter
from torch_topological.utils import total_persistence
from pointcloudutils.networks.modules import fps
from typing import Optional


class TopoLoss(nn.Module):
    def __init__(
        self,
        dim: int = 2,
        p: int = 2,
        topo_lambda: float = 1,
        farthest_point: bool = False,
        num_groups: Optional[int] = None,
        mean: Optional[bool] = True,
        **kwargs,
    ):
        super().__init__()
        self.topo_lambda = topo_lambda
        self.dim = dim
        self.p = p
        self.complex = VietorisRipsComplex(dim=self.dim, p=self.p)
        self.loss = WassersteinDistance()
        self.farthest_point = farthest_point
        self.num_groups = num_groups
        self.mean = mean

    def forward(self, gts, preds):

        if self.farthest_point:
            gts = fps(gts, self.num_groups)  # B G 3
            preds = fps(preds, self.num_groups) 

        pers_info_pred = self.complex(gts)
        pers_info_true = self.complex(preds)

        tl = torch.stack([
            self.loss(pred_batch, true_batch)
            for pred_batch, true_batch in zip(pers_info_pred, pers_info_true)
        ])
        if self.mean:
            tl = tl.mean()
        # tl
        return tl * self.topo_lambda
