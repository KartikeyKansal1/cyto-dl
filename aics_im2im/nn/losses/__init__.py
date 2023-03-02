from .adversarial_loss import AdversarialLoss
from .chamfer_loss import ChamferLoss
from .continuous_bernoulli import CBLogLoss
from .cosine_loss import CosineLoss
from .gan_loss import GANLoss
from .gaussian_nll_loss import GaussianNLLLoss
from .weibull import WeibullLogLoss
from .weighted_mse_loss import WeightedMSELoss

try:
    from .spharm_loss import SpharmLoss
except ModuleNotFoundError:
    SpharmLoss = None
