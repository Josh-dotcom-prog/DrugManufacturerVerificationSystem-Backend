# Import all your models first
from .drugs import Drug
# from .verificationHistory import Verification  # If you have this model

# Optional: You can expose them for easier importing elsewhere
__all__ = ['Drug']