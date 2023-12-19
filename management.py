# Imports.
# External imports.
import numpy as np

# Local imports.
from utils import export_dict_to_txt, get_hash


# Save function.
def save(user_stats: dict, user_equip: dict, user_map: np.array, inv: dict, npc: dict, ms: dict, x: int, y: int,
         path_usave: str = "cfg_save.txt", path_msave: str = "cfg_map.txt", path_hsave: str = "cfg_hash.txt") -> None:

    # Map drawing of user saving (export to txt).
    np.savetxt(path_msave, user_map.reshape(-1, user_map.shape[-1]), fmt='%d', delimiter='\t')

    # Inventory, user stats and map setting saving (export to txt).
    user_stats["x"], user_stats["y"] = x, y
    export_dict_to_txt({0: inv, 1: user_stats, 2: npc, 3: user_equip, 9: ms}, path_usave)

    # Hash saving (export to dict).
    export_dict_to_txt({"hash": get_hash(path_usave)}, path_hsave)
