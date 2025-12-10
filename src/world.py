# Imports.
# Local imports.
from .biome import Biome, Entry
from .entities.entitie import Fish, Tree
from .enums import *
from .item import Item
from .mob import Mob
from .npc import Npc
from .region import Region
from .skill import Skill
from .quest import QuestObjective, Quest
from .status import Buff, Status

# External imports.
from enum import Enum

BUFFS = {
    "little_strength_potion": Buff(
        name="Little Strength Potion",
        stat=StatType.STRENGTH.value,
        amount=3,
        duration=10,
        description="Little strength Potion.",
        source="little_strength_potion",
    ),

    "strength_potion": Buff(
        name="Strength Potion",
        stat=StatType.STRENGTH.value,
        amount=5,
        duration=20,
        description="Increases strength temporarily.",
        source="strength_potion",
    ),

    "great_strength_potion": Buff(
        name="Great Strength Potion",
        stat=StatType.STRENGTH.value,
        amount=10,
        duration=30,
        description="Greatly increases strength for a while.",
        source="great_strength_potion",
    ),

    "little_agility_potion": Buff(
        name="Little Agility Potion",
        stat=StatType.AGILITY.value,
        amount=2,
        duration=10,
        description="Slightly increases agility for a short time.",
        source="little_agility_potion",
    ),

    "agility_potion": Buff(
        name="Agility Potion",
        stat=StatType.AGILITY.value,
        amount=5,
        duration=20,
        description="Increases agility temporarily.",
        source="agility_potion",
    ),

    "great_agility_potion": Buff(
        name="Great Agility Potion",
        stat=StatType.AGILITY.value,
        amount=10,
        duration=30,
        description="Greatly increases agility for a while.",
        source="great_agility_potion",
    ),

    "little_vitality_potion": Buff(
        name="Little Vitality Potion",
        stat=StatType.VITALITY.value,
        amount=3,
        duration=10,
        description="Slightly increases vitality for a short time.",
        source="little_vitality_potion",
    ),

    "vitality_potion": Buff(
        name="Vitality Potion",
        stat=StatType.VITALITY.value,
        amount=6,
        duration=20,
        description="Increases vitality temporarily.",
        source="vitality_potion",
    ),

    "great_vitality_potion": Buff(
        name="Great Vitality Potion",
        stat=StatType.VITALITY.value,
        amount=12,
        duration=30,
        description="Greatly increases vitality for a while.",
        source="great_vitality_potion",
    ),

    "little_resistance_potion": Buff(
        name="Little Resistance Potion",
        stat=StatType.RESISTANCE.value,
        amount=2,
        duration=10,
        description="Slightly increases resistance for a short time.",
        source="little_resistance_potion",
    ),

    "resistance_potion": Buff(
        name="Resistance Potion",
        stat=StatType.RESISTANCE.value,
        amount=4,
        duration=20,
        description="Increases resistance temporarily.",
        source="resistance_potion",
    ),

    "great_resistance_potion": Buff(
        name="Great Resistance Potion",
        stat=StatType.RESISTANCE.value,
        amount=8,
        duration=30,
        description="Greatly increases resistance for a while.",
        source="great_resistance_potion",
    ),
}

SKILLS = {
    # Normal attack.
    "attack": Skill(
        id="attack",
        name="Attack",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=0,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        accuracy=1,
        desviation=1,
        critical_factor=1.05,
        critical_chance=0.1,
        cooldown=0,
        scaling={
            "attack": 1,
        },
        scaling_critical={
            "agility": 0.01,
        },
        requirements_equip={},
        tags=["attack"]
    ),

    # Attacks with weapons.
    "lunge": Skill(
        id="lunge",
        name="Lunge",
        description="A swift thrust that pierces the enemy’s defense.",
        element=SkillElements.NEUTRAL.value,
        power=5,
        cost=2,
        skill_type=SkillType.ATTACK.value,
        accuracy=0.6,
        desviation=2,
        critical_chance=0.5,
        cooldown=0,
        scaling={
            "strength": 0.1,
            "agility": 0.1,
            "attack": 1,
        },
        scaling_critical={
            "agility": 0.005,
        },
        requirements_equip={
            "short_sword": EquipCondition.NOT_NECESSARY.value,
            "sword": EquipCondition.NOT_NECESSARY.value,
        },
        tags=["lunge"]
    ),

    "hammer_crush": Skill(
        id="hammer_crush",
        name="Hammer Crush",
        description="",
        element=SkillElements.NEUTRAL.value,
        power=4,
        cost=3,
        skill_type=SkillType.ATTACK.value,
        accuracy=0.7,
        desviation=3,
        critical_chance=0.2,
        cooldown=0,
        status_effects=[
            Status.gen_stun(duration=2, stacks=1, max_stacks=1, source="Hammer Crush"),
        ],
        status_accuracy=[0.7],
        scaling={
            "strength": 0.1,
            "attack": 1,
        },
        scaling_critical={
            "strength": 0.005,
        },
        requirements_equip={
            "hammer": 1,
        },
        tags=["hammer_crush"],
    ),

    # Magic attacks.
    "fire_ground": Skill(
        id="fire_ground",
        name="Fire Ground",
        description="",
        element=SkillElements.FIRE.value,
        power=1,
        cost=6,
        skill_type=SkillType.ATTACK.value,
        accuracy=1,
        desviation=0,
        critical_chance=0,
        cooldown=0,
        status_effects=[
            Status.gen_burn(duration=10, stacks=1, max_stacks=1, source="Fire Ground"),
        ],
        status_accuracy=[1],
        scaling={
            "vit": 0.2,
        },
        tags=["fire_ground"],
    ),
}

SKILLS_MOB = {
    "attack_bandit": Skill(
        id="mob_attack",
        name="Attack Bandit",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=3,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_bandit"]
    ),

    "attack_basilisk": Skill(
        id="mob_attack",
        name="Attack Basilisk",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=19,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_basilisk"]
    ),

    "attack_climbing_goblin": Skill(
        id="mob_attack",
        name="Attack Climbing Goblin",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=14,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_climbing_goblin"]
    ),

    "attack_dragon": Skill(
        id="mob_attack",
        name="Attack Dragon FireFrost",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=36,  # attack 30 * 1.2
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_dragon_firefrost"]
    ),

    "attack_dryad": Skill(
        id="mob_attack",
        name="Attack Dryad",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=12,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=0,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_dryad"]
    ),

    "attack_giant_blind_spider": Skill(
        id="mob_attack",
        name="Attack Giant Blind Spider",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=20,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        status_effects=[
            Status.gen_poison(duration=20, stacks=1, max_stacks=2, source="Giant Blind Spider"),
            Status.gen_paralyze(duration=1, stacks=1, max_stacks=1, source="Giant Blind Spider"),
        ],
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_giant_blind_spider"]
    ),

    "attack_giant_slime": Skill(
        id="mob_attack",
        name="Attack Giant Slime",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=3,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=0,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_giant_slime"]
    ),

    "attack_giant_spider": Skill(
        id="mob_attack",
        name="Attack Giant Spider",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=14,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=5,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_giant_spider"]
    ),

    "attack_goblin": Skill(
        id="mob_attack",
        name="Attack Goblin",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=3,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={
            "attack": 1,
        },
        requirements_equip={},
        tags=["attack_goblin"]
    ),

    "attack_goblin_chief": Skill(
        id="mob_attack",
        name="Attack Goblin Chief",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=12,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=3,
        accuracy=1,
        critical_factor=1.3,
        critical_chance=0.3,
        cooldown=0,
        scaling={
            "attack": 1,
        },
        requirements_equip={},
        tags=["attack_goblin_chief"]
    ),

    "attack_little_slime": Skill(
        id="mob_attack",
        name="Attack Little Slime",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=1,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=0,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={
            "attack": 1,
        },
        requirements_equip={},
        tags=["attack_little_slime"]
    ),

    "attack_slime": Skill(
        id="mob_attack",
        name="Attack Slime",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=2,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=0,
        critical_chance=0,
        cooldown=0,
        scaling={
            "attack": 1,
        },
        requirements_equip={},
        tags=["attack_slime"]
    ),

    "attack_training_dummy": Skill(
        id="mob_attack",
        name="Attack Training Dummy",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=1,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=0,
        accuracy=1,
        critical_factor=0,
        critical_chance=0,
        cooldown=0,
        scaling={
            "attack": 1,
        },
        requirements_equip={},
        tags=["attack_training_dummy"]
    ),

    "attack_goblin_hunter": Skill(
        id="mob_attack",
        name="Attack Goblin Hunter",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=7,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_goblin_hunter"]
    ),

    "attack_goblin_war_chief": Skill(
        id="mob_attack",
        name="Attack Goblin War Chief",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=15,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_goblin_war_chief"]
    ),

    "attack_goblin_war": Skill(
        id="mob_attack",
        name="Attack War Goblin",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=6,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_goblin_war"]
    ),

    "attack_poison_slime": Skill(
        id="mob_attack",
        name="Attack Poison Slime",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=3,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=2,
        accuracy=1,
        critical_factor=1.5,
        critical_chance=0.2,
        cooldown=0,
        status_effects=[Status.gen_poison(duration=20, stacks=1, max_stacks=1, source="Poison Slime")],
        status_accuracy=[0.2],
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_poison_slime"]
    ),

    "attack_poison_spider": Skill(
        id="mob_attack",
        name="Attack Poison Spider",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=5,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.25,
        critical_chance=0.2,
        cooldown=0,
        status_effects=[Status.gen_poison(duration=20, stacks=1, max_stacks=2, source="Poison Slime")],
        status_accuracy=[0.2],
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_poison_spider"]
    ),

    "attack_shadow_wolf": Skill(
        id="mob_attack",
        name="Attack Shadow Wolf",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=10,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_shadow_wolf"]
    ),

    "attack_skeleton_warrior": Skill(
        id="mob_attack",
        name="Attack Skeleton Warrior",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=20,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_skeleton_warrior"]
    ),

    "attack_orc": Skill(
        id="mob_attack",
        name="Attack Orc",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=6,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_orc"]
    ),

    "attack_spectral_foxshade": Skill(
        id="mob_attack",
        name="Attack Spectral Foxshade",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=10,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_spectral_foxshade"]
    ),

    "attack_spectrum": Skill(
        id="mob_attack",
        name="Attack Spectrum",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=17,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_spectrum"]
    ),

    "attack_troll": Skill(
        id="mob_attack",
        name="Attack Troll",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=14,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=3,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        status_effects=[
            Status.gen_stun(duration=1, stacks=1, max_stacks=1, source="Troll")
        ],
        status_accuracy=[0.2],
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_troll"]
    ),

    "attack_undead_warrior": Skill(
        id="mob_attack",
        name="Attack Undead Warrior",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=16,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_undead_warrior"]
    ),

    "attack_watchful_goblin": Skill(
        id="mob_attack",
        name="Attack Watchful Goblin",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=3,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_watchful_goblin"]
    ),

    "attack_wild_boar": Skill(
        id="mob_attack",
        name="Attack Wild Boar",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=4,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_wild_boar"]
    ),

    "attack_young_dragon": Skill(
        id="mob_attack",
        name="Attack Young Dragon",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=20,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_young_dragon"]
    ),

    "attack_zombie": Skill(
        id="mob_attack",
        name="Attack Zombie",
        description="A basic physical strike.",
        element=SkillElements.NEUTRAL.value,
        power=5,
        cost=0,
        skill_type=SkillType.ATTACK.value,
        desviation=1,
        accuracy=1,
        critical_factor=1.2,
        critical_chance=0.2,
        cooldown=0,
        scaling={"attack": 1},
        requirements_equip={},
        tags=["attack_zombie"]
    ),
}

# Fishs.
FISHES = {
    # Coast, sea and ocean fishes.
    "fish_flounder": Fish(
        name="Fish Flounder",
        description="A flat fish that camouflages on sandy ocean floors to hunt.",
        depth=10,
        spawn_months=[0, 1, 2, 3],
        catch_chance=0.3,
        growth_rate=0.0015,
        max_weight=3,
        movable=True,
        movable_biomes=["bay", "coast", "estuary"],
        move_chance=0.15
    ),

    "fish_grouper": Fish(
        name="Fish Grouper",
        description="A sturdy fish inhabiting reefs and rocky ocean floors.",
        depth=20,
        spawn_months=[2, 3, 4, 5],
        catch_chance=0.25,
        growth_rate=0.0012,
        max_weight=20,
        movable=True,
        movable_biomes=["coast", "reef"],
        move_chance=0.1
    ),

    "fish_hammerhead_shark": Fish(
        name="Fish Hammerhead Shark",
        description="A unique predator with a distinctive hammer-shaped head.",
        depth=30,
        spawn_months=[2, 3, 4, 5],
        catch_chance=0.05,
        growth_rate=0.0008,
        max_weight=300,
        movable=True,
        movable_biomes=["coast", "sea"],
        move_chance=0.05
    ),

    "fish_mackerel": Fish(
        name="Fish Mackerel",
        description="A swift, striped fish, commonly found in coastal schools.",
        depth=10,
        spawn_months=[1, 2, 3, 4],
        catch_chance=0.4,
        growth_rate=0.002,
        max_weight=2,
        movable=True,
        movable_biomes=["coast", "sea"],
        move_chance=0.25
    ),

    "fish_mahi_mahi": Fish(
        name="Fish Mahi-Mahi",
        description="A vibrant-colored fish, known for its strength and leaping ability.",
        depth=20,
        spawn_months=[2, 3, 4, 5],
        catch_chance=0.25,
        growth_rate=0.002,
        max_weight=30,
        movable=True,
        movable_biomes=["sea"],
        move_chance=0.2
    ),

    "fish_ray": Fish(
        name="Fish Ray",
        description="A flattened fish with wide fins and a venomous sting in its tail.",
        depth=10,
        spawn_months=[0, 1, 2, 3, 4, 5],
        catch_chance=0.15,
        growth_rate=0.001,
        max_weight=10,
        movable=True,
        movable_biomes=["coast", "estuary", "reef"],
        move_chance=0.1
    ),

    "fish_sardine": Fish(
        name="Fish Sardine",
        description="A small silvery fish, popular among anglers and vital to the marine ecosystem.",
        depth=10,
        spawn_months=[0, 1, 2, 3, 4, 5, 6, 7],
        catch_chance=0.5,
        growth_rate=0.002,
        max_weight=0.3,
        movable=True,
        movable_biomes=["coast", "sea"],
        move_chance=0.4
    ),

    "fish_snapper": Fish(
        name="Fish Snapper",
        description="A white-fleshed fish, common in tropical and subtropical waters.",
        depth=10,
        spawn_months=[2, 3, 4, 5],
        catch_chance=0.3,
        growth_rate=0.0013,
        max_weight=8,
        movable=True,
        movable_biomes=["coast", "reef"],
        move_chance=0.15
    ),

    "fish_swordfish": Fish(
        name="Fish Swordfish",
        description="A large predator with a characteristic elongated sword-like snout.",
        depth=40,
        spawn_months=[3, 4, 5],
        catch_chance=0.1,
        growth_rate=0.001,
        max_weight=400,
        movable=True,
        movable_biomes=["sea"],
        move_chance=0.05
    ),

    "fish_tuna": Fish(
        name="Fish Tuna",
        description="A fast ocean fish, highly valued for its delicious and versatile meat.",
        depth=40,
        spawn_months=[2, 3, 4, 5],
        catch_chance=0.2,
        growth_rate=0.0015,
        max_weight=250,
        movable=True,
        movable_biomes=["sea"],
        move_chance=0.1
    ),

    # River fishes.
    "fish_sabalo": Fish(
        name="Fish Sabalo",
        description="A plump, silvery catch, prized for its rich flavor and hearty nourishment.",
        depth=5,
        spawn_months=[0, 1, 2, 3],
        catch_chance=0.35,
        growth_rate=0.0015,
        max_weight=5,
        movable=True,
        movable_biomes=["river", "estuary"],
        move_chance=0.3
    ),

    "fish_trout": Fish(
        name="Fish Trout",
        description="A lively river fish with shimmering scales and delicate, savory flesh.",
        depth=2,
        spawn_months=[0, 1, 2, 3],
        catch_chance=0.35,
        growth_rate=0.0018,
        max_weight=2.5,
        movable=True,
        movable_biomes=["river", "lake"],
        move_chance=0.25
    ),

    "fish_salmon": Fish(
        name="Fish Salmon",
        description="A strong swimmer known for its migration and rich, nourishing meat.",
        depth=5,
        spawn_months=[0, 1, 4, 5],
        catch_chance=0.25,
        growth_rate=0.002,
        max_weight=6,
        movable=True,
        movable_biomes=["river", "estuary", "sea"],
        move_chance=0.2
    ),

    "fish_catfish": Fish(
        name="Fish Catfish",
        description="A bottom-dwelling fish with whiskers and thick skin, common in muddy waters.",
        depth=5,
        spawn_months=[2, 3, 4, 5],
        catch_chance=0.3,
        growth_rate=0.0014,
        max_weight=12,
        movable=True,
        movable_biomes=["river", "lake", "estuary"],
        move_chance=0.15
    ),

    "fish_piranha": Fish(
        name="Fish Piranha",
        description="A fierce river predator with sharp teeth and a taste for blood.",
        depth=2,
        spawn_months=[2, 3, 4, 5],
        catch_chance=0.4,
        growth_rate=0.0016,
        max_weight=1.2,
        movable=True,
        movable_biomes=["river"],
        move_chance=0.3
    ),

    "fish_carp": Fish(
        name="Fish Carp",
        description="A common river fish, adaptable and resilient, often seen near calm waters.",
        depth=2,
        spawn_months=[0, 1, 2, 3, 4, 5],
        catch_chance=0.45,
        growth_rate=0.0017,
        max_weight=4,
        movable=True,
        movable_biomes=["river", "lake", "estuary"],
        move_chance=0.25
    ),

    "fish_eel": Fish(
        name="Fish Eel",
        description="A slippery, nocturnal fish that hides in the mud and emerges after dusk.",
        depth=5,
        spawn_months=[4, 5, 6, 7],
        catch_chance=0.2,
        growth_rate=0.0013,
        max_weight=3,
        movable=True,
        movable_biomes=["river", "estuary", "coast"],
        move_chance=0.15
    ),
}

# Trees.
TREES = {
    "coconut_palm": Tree(
        name="Coconut Palm",
        description="A tall palm with sweet coconuts swaying in warm winds.",
        height=20,
        leaf_color=LeafColors.GREEN,
        fruit_bearing=True,
        bearing_months=[0, 1, 2, 3],
        bearing_frencuency=32,
        bearing_quantity=2,
        fruit="coconut"
    )
}

# Items.
ITEMS = {
    # Equippable items.
    "axe": Item(name="Axe",
                description="A rugged Axe: perfect for chopping wood or cleaving enemies with powerful, heavy strikes.",
                attack=4,
                defense=0,
                precision=0,
                evasion=0,
                weight=5,
                body_part=BodyPart.RIGHT_HAND,
                pickable=True,
                consumable=False,
                equippable=True,
                expiration=None,
                buy_price=200,
                sell_price=150),

    "bludgeon": Item(name="Bludgeon",
                     description="Hefty Bludgeon blunt and brutal, ideal for stunning foes with a single, "
                                 "powerful blow.",
                     attack=2,
                     defense=0,
                     precision=0,
                     evasion=0,
                     weight=5,
                     body_part=BodyPart.RIGHT_HAND,
                     pickable=True,
                     consumable=False,
                     equippable=True,
                     expiration=None,
                     buy_price=200,
                     sell_price=40),

    "bone_shield": Item(name="Bone Shield",
                        description="Basic defense with sharp edges, deals damage but lacks durability in "
                                    "tough battles.",
                        attack=1,
                        defense=1,
                        precision=0,
                        evasion=0,
                        weight=3,
                        body_part=BodyPart.LEFT_HAND,
                        pickable=True,
                        consumable=False,
                        equippable=True,
                        expiration=None,
                        buy_price=130,
                        sell_price=50),

    "bone_sword": Item(name="Bone Sword",
                       description="Lightweight and sharp, crafted from bone, it strikes swiftly but lacks durability.",
                       attack=2,
                       defense=0,
                       precision=-0.1,
                       evasion=0,
                       weight=3,
                       body_part=BodyPart.RIGHT_HAND,
                       pickable=True,
                       consumable=False,
                       equippable=True,
                       expiration=None,
                       buy_price=100,
                       sell_price=50),

    "chainmail_armor": Item(name="Chainmail Armor",
                            description=("Sturdy armor made of interlocked rings. Offers great protection for the "
                                         "chest."),
                            attack=0,
                            defense=3,
                            precision=0,
                            evasion=0,
                            weight=10,
                            body_part=BodyPart.CHEST,
                            pickable=True,
                            consumable=False,
                            equippable=True,
                            expiration=None,
                            buy_price=500,
                            sell_price=150),

    "hammer": Item(name="Hammer",
                   description="Heavy and crushing, capable of stunning foes with a well-placed, thunderous strike.",
                   attack=3,
                   defense=0,
                   precision=0,
                   evasion=0,
                   weight=4,
                   body_part=BodyPart.RIGHT_HAND,
                   pickable=True,
                   consumable=False,
                   equippable=True,
                   expiration=None,
                   buy_price=100,
                   sell_price=50),

    "hardened_leather_armor": Item(name="Hardened Leather Armor",
                                   description=("Thick, reinforced leather armor. Flexible and offers decent "
                                                "protection."),
                                   attack=0,
                                   defense=2,
                                   precision=0,
                                   evasion=0,
                                   weight=8,
                                   body_part=BodyPart.CHEST,
                                   pickable=True,
                                   consumable=False,
                                   equippable=True,
                                   expiration=None,
                                   buy_price=300,
                                   sell_price=60),

    "harpoon": Item(name="Harpoon",
                    description="A sharp harpoon for striking enemies from a distance. Balanced and quick.",
                    attack=2,
                    defense=0,
                    precision=0,
                    evasion=0.1,
                    weight=4,
                    body_part=BodyPart.RIGHT_HAND,
                    pickable=True,
                    consumable=False,
                    equippable=True,
                    expiration=None,
                    buy_price=150,
                    sell_price=40),

    "iron_shield": Item(name="Iron Shield",
                        description="Solid iron shield. Blocks incoming attacks with ease.",
                        attack=0,
                        defense=3,
                        weight=10,
                        precision=0,
                        evasion=0,
                        body_part=BodyPart.LEFT_HAND,
                        pickable=True,
                        consumable=False,
                        equippable=True,
                        expiration=None,
                        buy_price=400,
                        sell_price=75),

    "large_belt": Item(name="Large Belt",
                       description="",
                       id="large_belt",
                       weight=1,
                       body_part=BodyPart.WAIST,
                       pickable=True,
                       consumable=False,
                       equippable=True,
                       expiration=None,
                       buy_price=400,
                       sell_price=200,
                       slots=3),

    "large_bow": Item(name="Large Bow",
                      description="A hefty bow designed for long-range attacks. Great precision and speed.",
                      attack=2,
                      defense=0,
                      precision=0.15,
                      evasion=0.30,
                      weight=3,
                      body_part=BodyPart.RIGHT_HAND,
                      pickable=True,
                      consumable=False,
                      equippable=True,
                      expiration=None,
                      buy_price=350,
                      sell_price=110),

    "leather_armor": Item(name="Leather Armor",
                          description="Basic leather armor. Provides light protection to the chest.",
                          attack=0,
                          defense=1,
                          precision=0,
                          evasion=0,
                          weight=5,
                          body_part=BodyPart.CHEST,
                          pickable=True,
                          consumable=False,
                          equippable=True,
                          expiration=None,
                          buy_price=200,
                          sell_price=35),

    "leather_boots": Item(name="Leather Boots",
                          description="Sturdy boots made of leather. Offers some defense for your legs.",
                          attack=0,
                          defense=1,
                          precision=0,
                          evasion=0,
                          weight=2,
                          body_part=BodyPart.LEGS,
                          pickable=True,
                          consumable=False,
                          equippable=True,
                          expiration=None,
                          buy_price=150,
                          sell_price=25),

    "linen_shirt": Item(name="Linen Shirt",
                        description="Light and breathable, offering simple comfort for travels under sun or shade.",
                        attack=0,
                        defense=0,
                        precision=0,
                        evasion=0,
                        weight=0,
                        body_part=BodyPart.CHEST,
                        pickable=True,
                        consumable=False,
                        equippable=True,
                        expiration=None,
                        buy_price=25,
                        sell_price=15,
                        warmness=8),

    "linen_trousers": Item(name="Linen Trousers",
                           description="Durable and soft, ideal for wandering through forests, fields, or "
                                       "bustling towns.",
                           attack=0,
                           defense=0,
                           precision=0,
                           evasion=0,
                           weight=0,
                           body_part=BodyPart.LEGS,
                           pickable=True,
                           consumable=False,
                           equippable=True,
                           expiration=None,
                           buy_price=25,
                           sell_price=15,
                           warmness=5),

    "longsword": Item(name="Longsword",
                      description="A finely crafted longsword. Perfect for dealing heavy, precise strikes.",
                      attack=4,
                      defense=0,
                      precision=0.05,
                      evasion=0,
                      weight=9,
                      body_part=BodyPart.RIGHT_HAND,
                      pickable=True,
                      consumable=False,
                      equippable=True,
                      expiration=None,
                      buy_price=500,
                      sell_price=175),

    "mesh_boots": Item(name="Mesh Boots",
                       description="Flexible boots with added defense. Protects legs while maintaining mobility.",
                       attack=0,
                       defense=2,
                       precision=0,
                       evasion=0,
                       weight=6,
                       body_part=BodyPart.LEGS,
                       pickable=True,
                       consumable=False,
                       equippable=True,
                       expiration=None,
                       buy_price=250,
                       sell_price=50),

    "plate_armor": Item(name="Plate Armor",
                        description="Heavy plate armor that offers superior protection to the chest.",
                        attack=0,
                        defense=4,
                        precision=0,
                        evasion=0,
                        weight=15,
                        body_part=BodyPart.CHEST,
                        pickable=True,
                        consumable=False,
                        equippable=True,
                        expiration=None,
                        buy_price=700,
                        sell_price=200),

    "rusty_shield": Item(name="Rusty Shield",
                         description="Dented and weak, offers minimal protection but tells tales of bygone battles.",
                         attack=0,
                         defense=2,
                         precision=0,
                         evasion=0,
                         weight=6,
                         body_part=BodyPart.LEFT_HAND,
                         pickable=True,
                         consumable=False,
                         equippable=True,
                         expiration=None,
                         buy_price=150,
                         sell_price=50),

    "rusty_sword": Item(name="Rusty Sword",
                        description="Worn and brittle, unreliable in battle but holds echoes of a warrior's past.",
                        attack=2,
                        defense=0,
                        precision=0.00,
                        evasion=0,
                        weight=6,
                        body_part=BodyPart.RIGHT_HAND,
                        pickable=True,
                        consumable=False,
                        equippable=True,
                        expiration=None,
                        buy_price=100,
                        sell_price=50),

    "short_sword": Item(name="Short Sword",
                        description=("A trusty Short Sword, swift and precise, ideal for close-quarter battles against "
                                     "foes in the wild."),
                        attack=1,
                        defense=0,
                        precision=0.05,
                        evasion=0,
                        weight=3,
                        body_part=BodyPart.RIGHT_HAND,
                        pickable=True,
                        consumable=False,
                        equippable=True,
                        expiration=None,
                        buy_price=150,
                        sell_price=50),

    "spear": Item(name="Spear",
                  description="A long spear for thrusting attacks. Great reach and balance.",
                  attack=3,
                  defense=0,
                  precision=0.05,
                  evasion=0.15,
                  weight=6,
                  body_part=BodyPart.RIGHT_HAND,
                  pickable=True,
                  consumable=False,
                  equippable=True,
                  expiration=None,
                  buy_price=300,
                  sell_price=125),

    "spike_shield": Item(name="Spike Shield",
                         description="A sturdy shield with deadly spikes. Can block and deal damage.",
                         attack=1,
                         defense=3,
                         precision=0,
                         evasion=0,
                         weight=9,
                         body_part=BodyPart.LEFT_HAND,
                         pickable=True,
                         consumable=False,
                         equippable=True,
                         expiration=None,
                         buy_price=500,
                         sell_price=150),

    "sword": Item(name="Sword",
                  description="A balanced sword. Reliable for close combat with decent attack power.",
                  attack=3,
                  defense=0,
                  precision=0.1,
                  evasion=0,
                  weight=6,
                  body_part=BodyPart.RIGHT_HAND,
                  pickable=True,
                  consumable=False,
                  equippable=True,
                  expiration=None,
                  buy_price=400,
                  sell_price=150),

    "tower_shield": Item(name="Tower Shield",
                         description="A massive shield offering unparalleled defense. Best for tanking heavy attacks.",
                         attack=0,
                         defense=4,
                         precision=0,
                         evasion=0,
                         weight=11,
                         body_part=BodyPart.LEFT_HAND,
                         pickable=True,
                         consumable=False,
                         equippable=True,
                         expiration=None,
                         buy_price=600,
                         sell_price=150),

    "travelers_belt": Item(name="Traveler's Belt",
                           description="Sturdy and practical belt, grants quick access to essential items during "
                                       "any journey.",
                           id="travelers_belt",
                           attack=0,
                           defense=0,
                           precision=0,
                           evasion=0,
                           weight=0.5,
                           body_part=BodyPart.WAIST,
                           pickable=True,
                           consumable=False,
                           equippable=True,
                           expiration=None,
                           buy_price=200,
                           sell_price=100,
                           slots=2),

    "wood_shield": Item(name="Wood Shield",
                        description="A simple wooden shield. Provides basic defense.",
                        attack=0,
                        defense=1,
                        precision=0,
                        evasion=0,
                        weight=5,
                        body_part=BodyPart.LEFT_HAND,
                        pickable=True,
                        consumable=False,
                        equippable=True,
                        expiration=None,
                        buy_price=100,
                        sell_price=20),

    "worn_boots": Item(name="Worn Boots",
                       description="Sturdy and dependable, giving steady footing across rugged paths and "
                                   "quiet roads.",
                       attack=0,
                       defense=0,
                       precision=0,
                       evasion=0,
                       weight=0,
                       body_part=BodyPart.FEET,
                       pickable=True,
                       consumable=False,
                       equippable=True,
                       expiration=None,
                       buy_price=25,
                       sell_price=15,
                       warmness=5),

    # Consumable items.
    "antinas_beer": Item(name="Antinas's Beer",
                         description="Renowned city brew, rich and frothy, celebrated for its unmatched flavor "
                                     "and heritage.",
                         id="antinas_beer",
                         weight=0.1,
                         pickable=True,
                         consumable=True,
                         equippable=False,
                         expiration=None,
                         edible=True,
                         buy_price=2,
                         sell_price=1,
                         hungry_refill=15,
                         thirsty_refill=40),

    "apple": Item(name="Apple",
                  description="A fresh, red apple. Satisfies hunger but offers no special effects.",
                  attack=0,
                  defense=0,
                  precision=0,
                  evasion=0,
                  weight=0.1,
                  pickable=True,
                  consumable=True,
                  equippable=False,
                  expiration=None,
                  edible=True,
                  buy_price=1,
                  sell_price=1,
                  hungry_refill=20,
                  thirsty_refill=2),

    "antidote": Item(name="Antidote",
                     description="A small vial that cures poison. Essential for survival in venomous areas.",
                     attack=0,
                     defense=0,
                     precision=0,
                     evasion=0,
                     weight=0.1,
                     pickable=True,
                     consumable=True,
                     equippable=False,
                     expiration=None,
                     buy_price=5,
                     sell_price=3),

    "basilisk_fangs": Item(name="Basilisk Fangs",
                           description="Deadly fangs of a basilisk. Handle with care, might still be venomous.",
                           attack=0,
                           defense=0,
                           precision=0,
                           evasion=0,
                           weight=0.05,
                           pickable=True,
                           consumable=False,
                           equippable=False,
                           expiration=None,
                           buy_price=15,
                           sell_price=15),

    "bier": Item(name="Bier",
                 description="A simple bier. Helps recover energy after a long day's journey.",
                 attack=0,
                 defense=0,
                 precision=0,
                 evasion=0,
                 weight=0.1,
                 pickable=True,
                 consumable=True,
                 equippable=False,
                 expiration=None,
                 edible=True,
                 buy_price=1,
                 sell_price=1,
                 hungry_refill=5,
                 thirsty_refill=35),

    "boar_tusk": Item(name="Boar Tusk",
                      description="Curved and sturdy, used for crafting or as a symbol of primal strength.",
                      weight=0.2,
                      pickable=True,
                      buy_price=15,
                      sell_price=10,
                      hungry_refill=30),

    "bones": Item(name="Bones",
                  description="Brittle remains of the fallen, useful for crafting or as a grim reminder of mortality.",
                  weight=0.5,
                  pickable=True,
                  buy_price=15,
                  sell_price=10),

    "bread": Item(name="Bread",
                  description="A crusty loaf of bread, filling and freshly baked for hungry travelers.",
                  attack=0,
                  defense=0,
                  precision=0,
                  evasion=0,
                  weight=0.3,
                  pickable=True,
                  consumable=True,
                  equippable=False,
                  expiration=None,
                  edible=True,
                  buy_price=1,
                  sell_price=1,
                  hungry_refill=25),

    "cheese": Item(name="Cheese",
                   description="A wedge of cheese. Restores energy but offers no additional effects.",
                   attack=0,
                   defense=0,
                   precision=0,
                   evasion=0,
                   weight=0.3,
                   pickable=True,
                   consumable=True,
                   equippable=False,
                   expiration=None,
                   edible=True,
                   buy_price=2,
                   sell_price=2,
                   hungry_refill=40,
                   thirsty_refill=1),

    "coconut": Item(name="Coconut",
                    description="Hard-shelled fruit, offers sweet water and nourishing flesh, a tropical traveler’s "
                                "delight.",
                    attack=0,
                    defense=0,
                    precision=0,
                    evasion=0,
                    weight=0.2,
                    pickable=True,
                    consumable=True,
                    equippable=False,
                    expiration=None,
                    edible=True,
                    buy_price=1,
                    sell_price=1,
                    hungry_refill=20,
                    thirsty_refill=20),

    "fish_flounder": Item(name="Fish Flounder",
                          description="A flat fish that camouflages on sandy ocean floors to hunt.",
                          weight=0.5,
                          pickable=True,
                          consumable=True,
                          edible=True,
                          buy_price=48,
                          sell_price=40,
                          hungry_refill=50,
                          thirsty_refill=5),

    "fish_grouper": Item(name="Fish Grouper",
                         description="A sturdy fish inhabiting reefs and rocky ocean floors.",
                         weight=0.5,
                         pickable=True,
                         consumable=True,
                         edible=True,
                         buy_price=35,
                         sell_price=25,
                         hungry_refill=50,
                         thirsty_refill=5),

    "fish_hammerhead_shark": Item(name="Fish Hammerhead Shark",
                                  description="A unique predator with a distinctive hammer-shaped head.",
                                  weight=1,
                                  pickable=True,
                                  consumable=True,
                                  edible=True,
                                  buy_price=80,
                                  sell_price=70,
                                  hungry_refill=100,
                                  thirsty_refill=20),

    "fish_mackerel": Item(name="Fish Mackerel",
                          description="A swift, striped fish, commonly found in coastal schools.",
                          weight=1,
                          pickable=True,
                          consumable=True,
                          edible=True,
                          buy_price=30,
                          sell_price=23,
                          hungry_refill=50,
                          thirsty_refill=5),

    "fish_mahi-mahi": Item(name="Fish Mahi-Mahi",
                           description="A vibrant-colored fish, known for its strength and leaping ability.",
                           weight=1,
                           pickable=True,
                           consumable=True,
                           edible=True,
                           buy_price=25,
                           sell_price=18,
                           hungry_refill=40,
                           thirsty_refill=10),

    "fish_ray": Item(name="Fish Ray",
                     description="A flattened fish with wide fins and a venomous sting in its tail.",
                     weight=1,
                     pickable=True,
                     consumable=True,
                     edible=True,
                     buy_price=60,
                     sell_price=50,
                     hungry_refill=50,
                     thirsty_refill=10),

    "fish_sabalo": Item(name="Fish Sabalo",
                        description="A plump, silvery catch, prized for its rich flavor and hearty nourishment.",
                        weight=0.5,
                        pickable=True,
                        consumable=True,
                        edible=True,
                        buy_price=20,
                        sell_price=15,
                        hungry_refill=20,
                        thirsty_refill=3),

    "fish_sardine": Item(name="Fish Sardine",
                         description="A small silvery fish, popular among anglers and vital to the marine ecosystem.",
                         weight=1,
                         pickable=True,
                         consumable=True,
                         edible=True,
                         buy_price=46,
                         sell_price=39,
                         hungry_refill=35,
                         thirsty_refill=5),

    "fish_snapper": Item(name="Fish Snapper",
                         description="A white-fleshed fish, common in tropical and subtropical waters.",
                         weight=1,
                         pickable=True,
                         consumable=True,
                         edible=True,
                         buy_price=36,
                         sell_price=29,
                         hungry_refill=35,
                         thirsty_refill=5),

    "fish_swordfish": Item(name="Fish Swordfish",
                           description="A large predator with a characteristic elongated sword-like snout.",
                           weight=2,
                           pickable=True,
                           consumable=True,
                           edible=True,
                           buy_price=100,
                           sell_price=60,
                           hungry_refill=90,
                           thirsty_refill=20),

    "fish_tuna": Item(name="Fish Tuna",
                      description="A fast ocean fish, highly valued for its delicious and versatile meat.",
                      weight=1,
                      pickable=True,
                      consumable=True,
                      edible=True,
                      buy_price=80,
                      sell_price=60,
                      hungry_refill=70,
                      thirsty_refill=10),

    "fish_soup": Item(name="Soup",
                      description="Warm and savory, a comforting dish that nourishes the body and soothes the soul.",
                      weight=0.5,
                      pickable=True,
                      consumable=True,
                      equippable=False,
                      expiration=None,
                      edible=True,
                      buy_price=3,
                      sell_price=2,
                      hungry_refill=30,
                      thirsty_refill=15),

    "giant_silk": Item(name="Giant Silk",
                       description="Silk from a giant spider. Valuable for crafting or trading.",
                       weight=0.5,
                       attack=0,
                       defense=0,
                       precision=0,
                       evasion=0,
                       pickable=True,
                       consumable=False,
                       equippable=False,
                       expiration=None,
                       buy_price=30,
                       sell_price=30),

    "poison_gland": Item(name="Poison Gland",
                         description="A toxic organ, harvested to craft potent poisons or deadly alchemical "
                                     "concoctions.",
                         weight=0.3,
                         pickable=True,
                         buy_price=20,
                         sell_price=15),

    "rotten_flesh": Item(name="Boar Tusk",
                         description="Decayed and foul, a remnant of the cursed, unsuitable for consumption but "
                                     "oddly useful.",
                         weight=0.5,
                         pickable=True,
                         buy_price=15,
                         sell_price=10),

    "slime_balls": Item(name="Slime Balls",
                        description="Gooey remnants of a defeated slime. Maybe useful, but hard to tell.",
                        weight=0.2,
                        attack=0,
                        defense=0,
                        precision=0,
                        evasion=0,
                        pickable=True,
                        consumable=False,
                        equippable=False,
                        expiration=None,
                        buy_price=1,
                        sell_price=1),

    "soup": Item(name="Soup",
                 description="A warm bowl of hearty soup, perfect for cold, weary adventurers.",
                 weight=0.4,

                 pickable=True,
                 consumable=False,
                 equippable=False,
                 expiration=None,
                 edible=True,
                 buy_price=1,
                 sell_price=1,
                 hungry_refill=20,
                 thirsty_refill=20),

    "water": Item(name="Water",
                  description="A bottle of clean water. Refreshing and essential for survival.",
                  weight=1,
                  pickable=True,
                  consumable=True,
                  equippable=False,
                  expiration=None,
                  edible=True,
                  buy_price=1,
                  sell_price=1,
                  hungry_refill=0,
                  thirsty_refill=40),

    "wolf_claw": Item(name="Boar Tusk",
                      description="Sharp and deadly, a prized material for weapons or a trophy of a fierce hunt.",
                      weight=0.2,
                      pickable=True,
                      buy_price=15,
                      sell_price=10),

    "wolf_fur": Item(name="Boar Tusk",
                     description="Thick and warm, ideal for crafting durable garments or insulating against"
                                 " harsh cold.",
                     weight=5,
                     pickable=True,
                     buy_price=30,
                     sell_price=25),

    "wood": Item(name="Wood",
                 description="A piece of sturdy wood, useful for crafting tools, fires, or simple repairs.",
                 weight=1,
                 pickable=True,
                 buy_price=15,
                 sell_price=10),

    # Usable items
    "explorer_telescope": Item(name="Explorer Telescope",
                               description="Enhanced vision, revealing distant lands with greater clarity and detail "
                                           "than a regular telescope.",
                               vision=1,
                               weight=1,
                               pickable=True,
                               consumable=False,
                               equippable=False,
                               expiration=None,
                               buy_price=250,
                               sell_price=85),

    "powder_keg": Item(name="Powder Keg",
                       description="Volatile and dangerous, capable of causing great destruction with a "
                                   "single spark.",
                       weight=5,
                       pickable=True,
                       consumable=False,
                       equippable=False,
                       droppable=False,
                       expiration=None,
                       buy_price=125,
                       sell_price=125),

    "rope": Item(name="Rope",
                 description="Sturdy and versatile, perfect for climbing, tying, or creating pathways in "
                             "rugged terrains.",
                 weight=2,
                 pickable=True,
                 consumable=False,
                 equippable=False,
                 expiration=None,
                 buy_price=30,
                 sell_price=20,
                 crafting_materials={"giant_silk": 10, "slime_balls": 15}),

    "telescope": Item(name="Telescope",
                      description="A long-range viewing device.",
                      vision=0.5,
                      weight=1,
                      pickable=True,
                      consumable=False,
                      equippable=False,
                      expiration=None,
                      buy_price=125,
                      sell_price=100),

    "torch": Item(name="Torch",
                  description="A burning torch to light the way. Useful in dark places.",
                  weight=1,
                  pickable=True,
                  consumable=False,
                  equippable=False,
                  expiration=None,
                  buy_price=10,
                  sell_price=10,
                  crafting_materials={"stick": 1, "giant_silk": 1, "slime_balls": 1}),

    # Fishing poles.
    "river_fishing_pole": Item(
        name="River Fishing Pole",
        description="A simple pole for catching small river fish. Light and easy to use.",
        weight=1,
        pickable=True,
        consumable=False,
        equippable=False,
        expiration=None,
        buy_price=100,
        sell_price=70,
        fishing=True,
        depth_range=2
    ),

    "deep_river_fishing_pole": Item(
        name="Deep River Fishing Pole",
        description="A stronger river pole for larger freshwater fish.",
        weight=1.5,
        pickable=True,
        consumable=False,
        equippable=False,
        expiration=None,
        buy_price=150,
        sell_price=80,
        fishing=True,
        depth_range=5
    ),

    "sturdy_fishing_pole": Item(name="Sturdy Fishing Pole",
                                description="A sturdy pole for fishing. A useful tool for catching food.",
                                weight=1,
                                pickable=True,
                                consumable=False,
                                equippable=False,
                                expiration=None,
                                buy_price=150,
                                sell_price=100,
                                fishing=True,
                                depth_range=10),

    "shore_fishing_pole": Item(
        name="Shore Fishing Pole",
        description="A pole designed for fishing near the shore. Great for medium-sized fish.",
        weight=1.5,
        pickable=True,
        consumable=False,
        equippable=False,
        expiration=None,
        buy_price=200,
        sell_price=130,
        fishing=True,
        depth_range=20
    ),

    "sea_fishing_pole": Item(
        name="Sea Fishing Pole",
        description="A durable fishing pole for open sea fishing. Can handle larger catches.",
        weight=2,
        pickable=True,
        consumable=False,
        equippable=False,
        expiration=None,
        buy_price=300,
        sell_price=200,
        fishing=True,
        depth_range=30
    ),

    "ocean_fishing_pole": Item(
        name="Ocean Fishing Pole",
        description="A reinforced pole built for deep ocean fishing and massive fish.",
        weight=2,
        pickable=True,
        consumable=False,
        equippable=False,
        expiration=None,
        buy_price=400,
        sell_price=270,
        fishing=True,
        depth_range=40
    ),

    # Quest items.
    "marlins_fish_tuna": Item(name="Marlin's Fish Tuna",
                              description="A fast ocean fish, highly valued for its delicious and versatile meat."
                                          " Marlin gave it to you for a delivery.",
                              id="marlins_fish_tuna",
                              weight=1,
                              droppable=False,
                              buy_price=80,
                              sell_price=60,
                              hungry_refill=70,
                              thirsty_refill=10,
                              ),

    # Places items.
    "bed": Item(name="Bed",
                description="Simple yet soft, promising warmth and restful sleep in humble surroundings",
                weight=75,
                attack=0,
                defense=0,
                precision=0,
                evasion=0,
                pickable=False,
                consumable=False,
                equippable=False,
                expiration=None,
                buy_price=300,
                sell_price=150),

    "boat": Item(name="Boat",
                 description="A sturdy sooden ship crafted to brave the seas, steady against waves and fierce winds.",
                 weight=500,
                 buy_price=1000,
                 sell_price=700),

    "broken_boat": Item(
        name="Broken Boat",
        description="A damaged wooden vessel, its hull cracked and barely afloat after harsh storms.",
        weight=650,
        buy_price=200,
        sell_price=80
    ),

    "giant_telescope": Item(name="Giant Telescope",
                            description="Giant Telescope, towering and precise, reveals distant lands and secrets "
                                        "hidden among the stars.",
                            weight=700),

    "origame_flowers": Item(name="Origame Flowers",
                            description="Paper flowers, seem to have something inside the stem, but you can't get it "
                                        "out with your fingers, you need a long stick.",
                            weight=0.05),

    "old_book": Item(name="Old Book",
                     description="A weathered tome with brittle pages, faint ink, and a lingering scent of forgotten "
                                 "stories.",
                     pickable=True,
                     readable=True,
                     weight=0.35,
                     title="Illegible Title",
                     readings=["Gravity",
                               "You pull me in",
                               "Neutro star",
                               "My head spins",
                               "Pulsar",
                               "My pulse speed up.",
                               "In your arms, the cosmos feels right",
                               "pulling me closer like a black hole's might.",
                               "Through the lens of this gift, we'll",
                               "discover the secrets of the sky.",
                               "Comets, planets and stars,",
                               "galaxies spinning in infinite dance.",
                               "Our love is celestial, cosmical & astronomical.",
                               "Woven in stardust, born of chance.",
                               "Let's take the ... illegible...,",
                               "go somewhere far,",
                               "Past... illegible... lights and... illegible...,",
                               "And lie beneath the quiet stars."]),

    "rockfall": Item(
        name="Rockfall",
        description="",
        weight=80000,
        droppable=False,
        blocker=True,
    ),

    # Innkeeper room keys.
    "aliras_first_room_key": Item(name="Lyssia's First Room Key",
                                  description="Polished and ornate, grants access to a refined room in a bustling"
                                              " metropolis.",
                                  id="aliras_first_room_key",
                                  weight=0.05,
                                  expiration=30,
                                  buy_price=15),

    "aliras_second_room_key": Item(name="Lyssia's Second Room Key",
                                   description="Polished and ornate, grants access to a refined room in a bustling"
                                               " metropolis.",
                                   id="aliras_second_room_key",
                                   weight=0.05,
                                   expiration=30,
                                   buy_price=10),

    "aliras_third_room_key": Item(name="Lyssia's Third Room Key",
                                  description="Polished and ornate, grants access to a refined room in a bustling"
                                              " metropolis.",
                                  id="aliras_third_room_key",
                                  weight=0.05,
                                  expiration=30,
                                  buy_price=8),

    "aliras_fourth_room_key": Item(name="Lyssia's Fourth Room Key",
                                   description="Polished and ornate, grants access to a refined room in a bustling"
                                               " metropolis.",
                                   id="aliras_fourth_room_key",
                                   weight=0.05,
                                   expiration=30,
                                   buy_price=8),

    "lyssias_first_room_key": Item(name="Lyssia's First Room Key",
                                   description="Weathered and salty, unlocks a cozy room overlooking the tranquil"
                                               " ocean waves.",
                                   id="lyssias_first_room_key",
                                   weight=0.05,
                                   expiration=30,
                                   buy_price=12),

    "lyssias_second_room_key": Item(name="Lyssia's Second Room Key",
                                    description="Weathered and salty, unlocks a cozy room overlooking the tranquil"
                                                " ocean waves.",
                                    id="lyssias_second_room_key",
                                    weight=0.05,
                                    expiration=30,
                                    buy_price=8),

    "lyssias_third_room_key": Item(name="Lyssia's Third Room Key",
                                   description="Weathered and salty, unlocks a cozy room overlooking the tranquil"
                                               " ocean waves.",
                                   id="lyssias_third_room_key",
                                   weight=0.05,
                                   expiration=30,
                                   buy_price=5),

    "mirabelles_small_room_key": Item(name="Mirabelle's Small Room Key",
                                      description="Small room key, worn and simple, granting access to a modest inn"
                                                  " chamber.",
                                      id="mirabelles_small_room_key",
                                      weight=0.05,
                                      expiration=30,
                                      buy_price=3),

    "mirabelles_main_room_key": Item(name="Mirabelle's Small Room Key",
                                     description="Small room key, worn and simple, granting access to a modest inn"
                                                 " chamber.",
                                     id="mirabelles_main_room_key",
                                     weight=0.05,
                                     expiration=30,
                                     buy_price=5),

    # Potion items.
    "little_red_potion": Item(name="Little Red Potion",
                              description="A small potion that restores a minor amount of health.",
                              weight=0.2,
                              pickable=True,
                              consumable=True,
                              equippable=False,
                              expiration=None,
                              buy_price=2,
                              sell_price=2),

    "red_potion": Item(name="Red Potion",
                       description="A standard red potion to restore health during battle.",
                       weight=0.3,
                       pickable=True,
                       consumable=True,
                       equippable=False,
                       expiration=None,
                       buy_price=5,
                       sell_price=5),

    "giant_red_potion": Item(name="Giant Red Potion",
                             description="A large red potion that restores a significant amount of health.",
                             weight=0.5,
                             pickable=True,
                             consumable=True,
                             buy_price=10,
                             sell_price=10),

    "little_strength_potion": Item(
        name="Slightly increases strength for a short time.",
        description="",
        weight=0.5,
        pickable=True,
        consumable=True,
        buy_price=10,
        sell_price=5,
        droppable=True),

    "strength_potion": Item(
        name="Strength Potion",
        description="Increases strength temporarily.",
        weight=0.7,
        pickable=True,
        consumable=True,
        buy_price=25,
        sell_price=12,
        droppable=True,
    ),

    "great_strength_potion": Item(
        name="Great Strength Potion",
        description="Greatly increases strength for a while.",
        weight=1.0,
        pickable=True,
        consumable=True,
        buy_price=50,
        sell_price=25,
        droppable=True,
    ),

    "little_agility_potion": Item(
        name="Little Agility Potion",
        description="Slightly increases agility for a short time.",
        weight=0.5,
        pickable=True,
        consumable=True,
        buy_price=10,
        sell_price=5,
        droppable=True,
    ),

    "agility_potion": Item(
        name="Agility Potion",
        description="Increases agility temporarily.",
        weight=0.7,
        pickable=True,
        consumable=True,
        buy_price=25,
        sell_price=12,
        droppable=True,
    ),

    "great_agility_potion": Item(
        name="Great Agility Potion",
        description="Greatly increases agility for a while.",
        weight=1.0,
        pickable=True,
        consumable=True,
        buy_price=50,
        sell_price=25,
        droppable=True,
    ),

    "little_vitality_potion": Item(
        name="Little Vitality Potion",
        description="Slightly increases vitality for a short time.",
        weight=0.5,
        pickable=True,
        consumable=True,
        buy_price=10,
        sell_price=5,
        droppable=True,
    ),

    "vitality_potion": Item(
        name="Vitality Potion",
        description="Increases vitality temporarily.",
        weight=0.7,
        pickable=True,
        consumable=True,
        buy_price=25,
        sell_price=12,
        droppable=True,
    ),

    "great_vitality_potion": Item(
        name="Great Vitality Potion",
        description="Greatly increases vitality for a while.",
        weight=1.0,
        pickable=True,
        consumable=True,
        buy_price=50,
        sell_price=25,
        droppable=True,
    ),

    "little_resistance_potion": Item(
        name="Little Resistance Potion",
        description="Slightly increases resistance for a short time.",
        weight=0.5,
        pickable=True,
        consumable=True,
        buy_price=10,
        sell_price=5,
        droppable=True,
    ),
    "resistance_potion": Item(
        name="Resistance Potion",
        description="Increases resistance temporarily.",
        weight=0.7,
        pickable=True,
        consumable=True,
        buy_price=25,
        sell_price=12,
        droppable=True,
    ),

    "great_resistance_potion": Item(
        name="Great Resistance Potion",
        description="Greatly increases resistance for a while.",
        weight=1.0,
        pickable=True,
        consumable=True,
        buy_price=50,
        sell_price=25,
        droppable=True,
    ),

    # Others.
    "gold": Item(name="gold",
                 description="Gleaming and precious, essential currency for trade, treasure, and unlocking hidden"
                             " opportunities.",
                 pickable=True,
                 droppable=True),

    "dragon_scales": Item(name="Dragon Scales",
                          description="A fast ocean fish, highly valued for its delicious and versatile meat."
                                      " Marlin gave it to you for his friend Brann.",
                          droppable=False),
}

# Quests.
QUEST_OBJETIVES = {
    # Talk quest objectives.
    "meet_ant_nynaeve": QuestObjective(
        type=ObjectiveType.TALK,
        target="islander_nynaeve"
    ),

    # Collect quest objectives.
    "coco_collect_I": QuestObjective(
        type=ObjectiveType.COLLECT,
        target="coconut",
        amount=5
    ),

    # Delivery quest objectives.
    "water_for_nynaeve": QuestObjective(
        type=ObjectiveType.DELIVER,
        target="islander_nynaeve",
        deliver_item="water",
        deliver_amount=1),

    # Reputation quest objectives.
    "reputation_test": QuestObjective(
        type=ObjectiveType.REPUTATION,
        target="epiiat",
        amount=10),
}

QUESTS = {
    # Starter quests.
    "quest_exit_the_hut": Quest(
        id="quest_exit_the_hut",
        title="Step Into the Light",
        description="You awaken inside a dim hut. A faint breeze calls you outside.",
        objectives=[
            QuestObjective(
                type=ObjectiveType.EXPLORE,
                target="(12, 24)",
                amount=1
            )
        ],
    ),

    "quest_eat_soup": Quest(
        id="quest_eat_soup",
        title="Warmth in a Bowl",
        description="A fragrant aroma fills the hut. Maybe you should EAT the soup.",
        objectives=[
            QuestObjective(
                type=ObjectiveType.EAT,
                target="soup",
                amount=1
            )
        ],
    ),

    "quest_find_loial": Quest(
        id="quest_find_loial",
        title="Where Is Loial?",
        description=(
            "Nynaeve seems worried. Loial hasn't returned from the Isla lumberyard. "
            "She asks you to find him and make sure he is safe or need some help."
        ),
        objectives=[
            QuestObjective(
                type=ObjectiveType.TALK,
                target="islander_loial",
                amount=1
            )
        ],
        rewards={"soup": 1, "apple": 1, "water": 1},
        messages_start={
            0: [
                "Have you seen Loial?",
                "He went to the lumberyard earlier on Isla… but he hasn’t returned.",
                "Could you check on him?"
            ],
        },
        messages_in_progress={
            0: [
                "Please, check the Isla lumberyard. Loial might need help."
            ],
        },
        messages_reward={
            0: [
                "Oh, good… you found him. He must have just lost track of time."
            ]
        },
    ),

    "quest_deliver_wood": Quest(
        id="quest_deliver_wood",
        title="Deliver the Wood",
        description=(
            "Loial has finished cutting a bundle of wood but cannot leave the lumberyard. "
            "He asks you to carry it to the Hut and deliver it to Nynaeve."
        ),
        objectives=[
            QuestObjective(
                type=ObjectiveType.DELIVER,
                target="islander_nynaeve",
                amount=1,
                deliver_item="wood",
                deliver_amount=1,
            )
        ],
        rewards={"water": 1, "bread": 1},
        messages_start={
            0: [
                "Ah it's you..., could you lend me a hand?",
                "I’ve chopped this wood, but I can’t leave the lumberyard right now.",
                "Please take it to Nynaeve at the Hut—she’ll know what to do with it."
            ],
        },
        answers_start={
            1: "Yes I can help"
        },
        messages_in_progress={
            0: [
                "Please, deliver that wood to Nynaeve at the Hut."
            ],
        },
        messages_reward={
            0: [
                "Ah, wonderful. Nynaeve received the wood safely?",
                "Thank you. You’ve helped more than you know."
            ]
        },
    ),

    "slime_slayer_I": Quest(
        id="slime_slayer_I",
        title="The Slimy Slayer",
        description=(
            "Loial is troubled by a group of little slimes lingering near his cabin. "
            "He asks you to get rid of them before they cause trouble."
        ),
        objectives=[
            QuestObjective(
                type=ObjectiveType.KILL,
                target="little_slime",
                amount=5
            ),
        ],
        rewards={"little_red_potion": 2},

        messages_start={
            0: [
                "Ah, you're here. Good.",
                "I’m having a small problem… little slimes have appeared around the hut.",
                "You can use LOOK AROUND to spot them, then ATTACK to deal with them.",
                "There should be five of them lurking nearby.",
                "Could you handle this for me?"
            ],
            1: [
                "Perfect. When you're done, come back to me."
            ]
        },
        answers_start={
            1: "Yes, I can help",
        },

        messages_in_progress={
            0: [
                "The little slimes should still be nearby.",
                "Remember: LOOK AROUND to find them, ATTACK to fight them."
            ],
        },

        messages_reward={
            0: [
                "You did it! The area finally feels safe again.",
                "Thank you, truly. These creatures can be more annoying than they look."
            ]
        }
    ),

    "slime_slayer_II": Quest(
        id="slime_slayer_II",
        title="The Slime Slayer II",
        description=(
            "Loial asks you to deal with stronger slimes nearby. "
            "He mentions a sword stored in the small room that might help, "
            "and that he needs the area safe to repair a small boat on the coast."
        ),
        objectives=[
            QuestObjective(
                type=ObjectiveType.KILL,
                target="slime",
                amount=2
            )
        ],
        rewards={"red_potion": 1},

        messages_start={
            0: [
                "Those little slimes weren’t the only ones… stronger ones have appeared.",
                "I need the area cleared soon—there’s a small boat on the coast that I must repair.",
                "In the small room beside the hut, you can find a sword.",
                "Once you pick it up, remember to EQUIP it before fighting.",
                "It should help you deal with these tougher slimes."
            ],
            1: [
                "Good. Grab the sword and EQUIP it if you haven't already.",
                "And watch yourself—these slimes are far stronger.",
                "Once the area is safe, I can finally work on that broken boat."
            ],
        },

        answers_start={
            1: "Yes"
        },

        messages_in_progress={
            0: [
                "Make sure your sword is equipped.",
                "Use LOOK AROUND to find the stronger slimes, then ATTACK as usual.",
                "I can't repair the boat until the area is secure."
            ],
        },

        messages_reward={
            0: [
                "Excellent work! Those slimes were much tougher.",
                "Now that the area is clear, I can start repairing the boat on the coast.",
                "Once it's fixed, you’ll be able to use it. It may take me 3 days..."
            ],
        }
    ),

    # Epiiat quests.
    "quest_goblin_chief": Quest(
        id="quest_goblin_chief",
        title="The Goblin Chief Of Epiiat",
        description="The mayor of Epiiat fears for his missing daughter, Maisie, who vanished near the "
                    "goblin-infested woods. Rumors speak of a ruthless Goblin Chief leading the creatures. Finding "
                    "him may be the only way to uncover what happened and bring Maisie home safely.",
        objectives=[
            QuestObjective(
                type=ObjectiveType.KILL,
                target="goblin_chief",
                amount=1
            )
        ],
        rewards={"hardened_leather_armor": 1, "gold": 50},

        messages_start={
            0: [
                "Welcome to Epiiat, traveler.",
                "Though I greet you as I would any of our own, my heart is heavy with concern. My"
                " daughter, Maisie, has gone missing.",
                "She wandered off days ago, and no trace of her remains. If your path allows it, "
                "please keep an eye out for her.",
                "The villagers and I are desperate for her safe return."
            ],
        },

        messages_in_progress={
            0: [
                "Every passing hour weighs on me… I try to stay strong for the village, but a father’s worry "
                "is hard to hide.",
                "Maisie has always been brave, wandering farther than she should… I should have been stricter.",
                "If the goblins truly have her, Light help them if I ever lay my hands on their chief."
            ],
        },

        messages_reward={
            0: [
                "I’ve heard the tale from my daughter, Maisie. You rescued her from the clutches of those "
                "vile goblins.",
                "I thank you, not as a mayor, but as a father. Our village owes you a debt we cannot repay.",
                "Please, accept this reward—a small token of our gratitude. Epiiat's doors are always open to you,"
                " brave soul."
            ],
        }
    ),

    # Aquiri quests.
    "quest_marlin_fish_for_brann": Quest(
        id="quest_marlin_fish_for_brann",
        title="Marlin want to deliver fish to Brann",
        description="Marlin needs help delivering a batch of fresh tuna to his friend Brann, who "
                    "lives in the southern region. Busy with constant fishing, he hasn’t been able "
                    "to make the trip himself. He has entrusted you with bringing the fish safely "
                    "to Brann before it loses its freshness.",
        objectives=[
            QuestObjective(
                type=ObjectiveType.DELIVER,
                target="fisherman_brann",
                amount=1,
                deliver_item="marlins_fish_tuna",
                deliver_amount=3,
            )
        ],
        rewards={"gold": 20},

        messages_start={
            0: ["Ahoy, traveler!",
                "I’ve got a delivery of fish for my friend down south. The waters there have been"
                " tricky lately, so I’ve had to catch extra here in town.",
                "Problem is, I’ve been so busy fishing, I haven’t found the time to make the"
                " trip!"],
            1: ["Thank you for offering to help! I need you to deliver two tuna to my friend Brann "
                "in the south. He’ll be waiting—it’s a special request."],
        },

        answers_start={
            1: "I can help you with the delivery",
        },

        messages_in_progress={
            0: [
                "Ah, it’s you! Tell me, have you managed to deliver that fish to my friend in the south? I’ve been "
                "wondering if it arrived fresh!"
            ],
        },

        messages_reward={
            0: [
                "Thank you for delivering the tuna to Brann! You’ve been a great help.",
                "But now I’m worried about another shipment I sent with a caravan to Epiiat.",
                "I haven’t heard back from them."
            ],
        }
    ),

    "quest_find_caravan_leader_darek": Quest(
        id="quest_find_caravan_leader_darek",
        title="What happen with the Caravan?",
        description=(
            "Marlin is concerned about a caravan he sent toward Epiiat. "
            "He hasn't received any news from them and fears something may have happened "
            "on the road. He asked you to investigate their whereabouts."
        ),
        objectives=[
            QuestObjective(
                type=ObjectiveType.TALK,
                target="caravan_leader_darek",
                amount=1
            )
        ],
        rewards={"gold": 25},
        messages_start={
            0: [
                "Thanks again for delivering that order to Brann! Now, there’s something else...",
                "I’m worried about a shipment I sent with a caravan to Epiiat. I haven’t heard from them.",
                "Could you check on them for me? I’d really appreciate it."
            ],
        },
        messages_in_progress={
            0: [
                "The caravan still hasn't checked in... Please, let me know the moment you find something."
            ],
        },
        messages_reward={
            0: [
                "A derrumbe in the valley? That explains the delay. Thank you for letting me know!"
            ]
        },
    ),

    "quest_destroy_rocks_on_valley": Quest(
        id="quest_destroy_rocks_on_valley",
        title="What happen with the Caravan?",
        description=(
            "Marlin discovered that a massive rockfall is blocking the valley road. "
            "The caravan cannot proceed until the path is cleared. He believes explosives "
            "might be necessary to break through and hints that Captain Thorne may have some."
        ),
        objectives=[
            QuestObjective(
                type=ObjectiveType.DESTROY,
                target="rockfall",
                amount=1
            )
        ],
        rewards={"gold": 30},
        messages_start={
            0: [
                "So the caravan was stopped by a rockfall in the valley? That explains everything...",
                "If that path stays blocked, no one will be able to travel to or from Epiiat safely.",
                "..., I think I saw Captain Thorne loading some onto his ship recently...",
                "Could you clear out those rocks? Something tells me you might just be able to handle it."
            ],
        },
        messages_in_progress={
            0: [
                "The caravan’s still stuck behind that rockfall.",
                "I saw Captain Thorne might have explosives aboard his ship.",
                "If you can get your hands on them, you should be able to clear the valley."
            ],
        },
        messages_reward={
            0: [
                "Ah, you've done it! The valley is clear at last. I can’t thank you enough for your help.",
                "Here, take this as a token of my gratitude."
            ]
        },
    ),

    "quest_gareth_deliver": Quest(
        id="quest_gareth_deliver",
        title="A Delivery for Gareth",
        description=(
            "Marlin has entrusted you with delivering a package of fresh tunas to Gareth, "
            "a villager in Antina. With the travel permit he gave you, you can reach the town "
            "without trouble. Gareth has been waiting on this delivery for days."
        ),
        objectives=[
            QuestObjective(
                type=ObjectiveType.DELIVER,
                target="marlins_fish_tuna",
                amount=3
            )
        ],
        rewards={"fishingpole": 1},
        remove=True,
        messages_start={
            0: ["Ahoy, traveler! It's you again!",
                "I have one last favor to ask. Could you deliver this package to Antina for me?"
                ],
        },
        messages_in_progress={
            0: [
                "Ah, have you managed to deliver those tunas to Gareth yet?",
                "I hope he’s gotten them by now. He's been waiting on those for quite some time. Let me know if you"
                "ran into any trouble!"
            ],
        },
        messages_reward={
            0: [
                "You made the delivery? Wonderful! Gareth must be relieved.",
                "Thank you for handling that for me. I knew I could count on you.",
                "Here—take this fishing pole. You’ve earned it, and I’m sure it’ll serve you well on the road."
            ]
        },
    ),

    "quest_firefrost_first_encounter": Quest(
        id="quest_firefrost_first_encounter",
        title="The First Clash with FireFrost",
        description="A mysterious force calls to you from deep within Naiwat. Following the whispers of the wind, "
                    "you encounter FireFrost—a majestic dragon whose presence feels strangely familiar. "
                    "Though its intentions are unclear, the creature challenges you, testing your strength.",
        objectives=[
            QuestObjective(
                type=ObjectiveType.KILL,
                target="dragon",
                amount=1
            )
        ],
        messages_start={
            0: [

            ],
        },

        messages_in_progress={
            0: [

            ],
        },

        messages_reward={
            0: [

            ],
        }
    ),
}

# NPCs.
NPCS = {
    "islander_loial": Npc(
        name="Islander Loial",
        npc_type=NpcTypes.VETERAN,
        id="islander_loial",
        place_morning=[(13, 23)],
        messages_morning={
            0: ["Ah, you look in good shape today.",
                "I’m already at work—these trees won’t fell themselves."]
        },
        messages_afternoon={
            0: ["This is taking longer than I thought…",
                "My stomach’s growling too. A bowl of Nynaeve’s soup would do wonders right now."]
        },
        messages_evening={
            0: ["Still not done… Seems I’ll need to sharpen this axe if I want any chance of finishing."]
        },
        messages_night={
            0: ["I’m exhausted… but I must keep going.",
                "Once I finish here, I still need to look at the boat—its hull won’t mend itself."]
        },
    ),

    "islander_nynaeve": Npc(
        name="Islander Nynaeve",
        npc_type=NpcTypes.VETERAN,
        messages={
            0: [
                "Oh! You’re already up? I didn’t expect you out of bed so soon. Come here and TALK with me for "
                "a moment.",
            ],
        },
        id="islander_nynaeve",
        place=[(12, 24)]
    ),

    "artisan_brenwick": Npc(name="artisan brenwick",
                            npc_type=NpcTypes.ARTISAN,
                            messages={
                                0: ["Ah, greetings, wanderer! Need something crafted? I’ve got the tools and the "
                                    "talent!"],
                                1: ["Excellent! So, what’ll it be, traveler?"]},
                            answers={
                                1: "I need craft something"},
                            place=[(13, 37), "artisan_shop"],
                            quantity_message="How many #item do you need to craft?",
                            crafting_items={
                                "rope": {"gold": 25},
                                "torch": {"gold": 15}}),

    "astronomer_aldric": Npc(name="astronomer aldric",
                             npc_type=NpcTypes.ASTRONOMER,
                             messages_afternoon={
                                 0: ["Oh, a visitor? I didn’t expect anyone up here... You must be curious "
                                     "about Karûn."],
                                 1: ["Ah, the Red Moon, Karûn? It has a cycle of 32 days and graces the night skies.",
                                     "Many say it governs war, passion, and swift changes.",
                                     "Quite the fiery companion, wouldn't you agree?"],
                                 2: ["Ah, you wish to know about the year?,"
                                     "It spans 512 days, divided into 8 months of 64 days each. Each month holds 8 "
                                     "weeks, with 8 days in every week. A fascinating rhythm, don’t you think?"],
                                 3: ["Ah, an excellent question! Our calendar ties deeply to the moons' cycles and "
                                     "nature's rhythms",
                                     "Aurenar, the Month of Beginnings, marks nature's rebirth as Karûn waxes and "
                                     "Eldra starts anew.",
                                     "Sylvanna, the Month of the Forest, celebrates flourishing life under Eldra's "
                                     "full, wise glow.",
                                     "Ignaris, the Month of Flame, aligns with Karûn’s fullness, bringing long days "
                                     "and summer’s heat.",
                                     "Tempora, the Month of Storms, comes with Karûn waning, bringing rains and "
                                     "untamed forces of nature.",
                                     "Ouskara, the Month of Twilight, sees Eldra waning too, a time for introspection.",
                                     "Valora, the Month of Harvest, is when both moons align, rewarding the "
                                     "year's labors.",
                                     "Nerith, the Month of Darkness, has Karûn new, with long nights and eerie "
                                     "myths of shadowed creatures.",
                                     "Reveris, the Month of Rest, ends the cycle with Eldra's renewal, a time of "
                                     "peace before the year's rebirth."]},
                             answers_afternoon={
                                 1: "Can you tell me about Karûn?",
                                 2: "How long is a year in this land?",
                                 3: "Can you explain the meaning of the months?"},
                             place_afternoon=[(14, 36), "tower", "second_floor"],
                             messages_morning={
                                 0: ["Zzz... the stars... always moving... Zzz... Karûn's light... so bright..."]},
                             answers_morning={},
                             place_morning=[(14, 36), "tower"],
                             leave_message=["Farewell, traveler! May the stars guide your path, and perhaps we’ll "
                                            "meet again under Karûn’s glow."]),

    "astronomer_quillon": Npc(name="astronomer quillon",
                              npc_type=NpcTypes.ASTRONOMER,
                              messages_afternoon={
                                  0: ["Oh my, a visitor? It’s rare for anyone to make it up here. Welcome to the Tower"
                                      " of Eldra—a name of my own choosing.",
                                      "I built it to study the movements of our great moon, Eldra.",
                                      "Fascinating, isn’t it? If you’re curious, I’d be glad to share what I’ve "
                                      "learned about its mysterious dance across the night sky."],
                                  1: ["Marvelous, isn’t it? I built this grand telescope with my own hands. It lets"
                                      " me study the stars and the mysteries of the heavens.",
                                      "But it’s not just for the sky—I can peer into distant lands as well. The "
                                      "world looks so small from up here, yet so full of wonder."],
                                  2: ["Ah, Eldra—the moon of wisdom and magic. Its cycle spans 64 days, visible both "
                                      "day and night, tied to nature’s rhythms.",
                                      "Many believe it grants mystical power, but I suspect its effects stem from its"
                                      " geological makeup.",
                                      "Imagine the secrets its surface holds! Wouldn’t you agree the truth is just"
                                      " as fascinating as legend?"],
                                  3: ["Karûn, the Red Moon—a younger sister to Eldra.",
                                      "Its cycle is shorter, just 32 days, and it graces the night skies. I haven’t "
                                      "studied it much myself, but I know someone who has.",
                                      "A colleague of mine in the west is dedicated to uncovering its secrets. You "
                                      "might seek them out if Karûn intrigues you."]},
                              answers_afternoon={
                                  1: "What can you tell me about the large telescope that is here?",
                                  2: "What do you know about the moon Eldra?",
                                  3: "There is another moon, right?"},
                              place_afternoon=[(34, 42), "tower_of_eldra", "tower_of_eldra_second_floor"],
                              leave_message=["Farewell, traveler! May the stars guide your path, and perhaps we’ll "
                                             "meet again under Eldran’s glow."],
                              messages_morning={
                                  0: ["Zzz... the stars... always moving... Zzz... Eldra's light... so bright..."]
                              },
                              answers_morning={},
                              place_morning=[(34, 42), "tower_of_eldra"]),

    "bard_caelan": Npc(name="bard caelan",
                       npc_type=NpcTypes.BARD,
                       place=[(22, 42), "tavern"],
                       messages_morning={
                           0: ["Ah, greetings, traveler! I am Caelan, a humble bard. Do you seek a tale or a tune?"]},
                       tracks={
                           0: "./rsc/media/Echoes_of_the_Undead.mp3",
                           1: "./rsc/media/Echoes_of_Ancient_Desire.mp3",
                           2: "./rsc/media/Echoes_of_the_Undead.mp3",
                           3: "./rsc/media/Echoes_of_Ancient_Desire.mp3",
                           4: "./rsc/media/Echoes_of_the_Undead.mp3",
                           5: "./rsc/media/Echoes_of_Ancient_Desire.mp3",
                           6: "./rsc/media/Echoes_of_the_Undead.mp3",
                           7: "./rsc/media/Echoes_of_Ancient_Desire.mp3",
                       }),

    "bard_lyricus": Npc(name="bard lyricus",
                        npc_type=NpcTypes.BARD,
                        place=[(21, 29), "inn"],
                        messages_morning={
                            0: ["Ah, greetings, traveler! Come by the inn tonight—I’ll be performing songs to lift "
                                "weary spirits.",
                                "Don’t miss it!"]},
                        messages_evening={
                            0: ["Greetings, traveler! Tonight, I shall sing of heroes and their grand deeds.",
                                "Perhaps, if you achieve great fame one day, I’ll compose songs about you too.",
                                "What tales might you bring to inspire the bards?"]},
                        tracks={
                            0: "./rsc/media/The_Blue_Foxs_Fortune.mp3",
                            1: "./rsc/media/Under_Two_Moons.mp3",
                            2: "./rsc/media/The_Blue_Foxs_Fortune.mp3",
                            3: "./rsc/media/The_Blue_Foxs_Fortune.mp3",
                            4: "./rsc/media/Whispers_of_the_Moons.mp3",
                            5: "./rsc/media/The_Blue_Foxs_Fortune.mp3",
                            6: "./rsc/media/Whispers_of_the_Moons.mp3",
                            7: "./rsc/media/Under_Two_Moons.mp3",
                        }),

    "captain_thorne": Npc(name="captain thorne",
                          npc_type=NpcTypes.CAPTAIN,
                          messages_morning={
                              0: ["Ahoy, traveler. I'm Captain Thorne.",
                                  "You see my ship there? We won't be setting sail today. A dragon's presence spells "
                                  "danger on the open seas. Until the skies are clear, we remain anchored. Better "
                                  "to be safe in port than to risk the wrath of such a fearsome creature.",
                                  "But fear not, when the danger has passed, I'll gladly offer you passage to the "
                                  "next port."]},
                          place_morning=[(39, 39)],
                          messages_night={
                              0: ["What business would a dragon have in these lands, traveler? Curious... and"
                                  " troubling, isn’t it?"]},
                          place_night=[(39, 39), "inn", "first_room"]),

    "captain_zelian": Npc(name="captain zelian",
                          npc_type=NpcTypes.CAPTAIN,
                          messages={
                              0: ["Ah, the sea, a fickle friend and fierce foe.",
                                  "Many a ship I've sailed, battling monsters and discovering uncharted isles. "
                                  "The ocean whispers secrets to those who listen.",
                                  "One day, perhaps, the tides will reveal its mysteries to a brave soul like "
                                  "yourself, adventurer."]},
                          place=[(17, 27)]),

    "caravan_leader_darek": Npc(name="caravan leader darek",
                                npc_type=NpcTypes.CARAVAN_LEADER,
                                messages={
                                    0: ["We’re stuck here, traveler. The path through the valley to Epiiat is "
                                        "blocked by a landslide. Until the rubble is cleared, there’s no way forward.",
                                        "It’s put quite the halt to our journey."]}),

    "caravenner_lorien": Npc(name="caravanner lorien",
                             npc_type=NpcTypes.CARAVANNER,
                             messages={
                                 0: ["Epiiat... It’s been years since I last visited. A quiet little place, if I "
                                     "recall.",
                                     "I was looking forward to seeing it again, but with this landslide, who knows "
                                     "when we’ll get through."]}),

    "dragon_firefrost": Npc(name="dragon firefrost",
                            npc_type=NpcTypes.DRAGON,
                            messages={
                                0: ["Hero...",
                                    "You finally come to me...",
                                    "Destiny calls for a dance of fire and frost between us...",
                                    "Ready your blade..."]},
                            place=[(56, 92)]),

    "elder_lirian": Npc(name="elder lirian",
                        npc_type=NpcTypes.ELDER,
                        messages={
                            0: ["Welcome, traveler, to the humble temple of Epiiat. These walls whisper of ancient "
                                "prayers. May you find solace here."]},
                        place_morning=[(22, 28), "temple"]),

    "fisherman_brann": Npc(name="fisherman brann",
                           npc_type=NpcTypes.FISHERMAN,
                           messages={
                               0: ["You there, traveler... Have you come from the port?",
                                   "I’ve been waiting for days now. Marlin, the fisherman, promised to send "
                                   "supplies, but nothing has arrived yet. My stores are running low, and the "
                                   "sea hasn’t been kind lately.",
                                   "If you see him, could you ask what’s causing the delay?"]},
                           place_morning=[(34, 51)],
                           place_evening=[(34, 51), "coast_hut"]),

    "fisherman_marlin": Npc(name="fisherman marlin",
                            npc_type=NpcTypes.FISHERMAN,
                            messages={
                                0: ["Ah, it's a quiet day today. The sea's calm, but the fish are being stubborn.",
                                    "Still, there's always something peaceful about being near the water.",
                                    "If you’re ever in need of some good fish, you know where to find me."],
                            },
                            leave_message=["Safe travels, friend! May the waters guide you to calm shores."],
                            place_morning=[(39, 38)],
                            place_night=[(39, 38), "marlins_hut"]),

    "goblin_griznuk": Npc(name="chief goblin griznuk",
                          npc_type=NpcTypes.MONSTER,
                          messages={
                              0: ["Grraaak... hssssk!", "Zilgruk!", "Fwaahh!"]}),

    "guard_lorian": Npc(name="guard lorian",
                        npc_type=NpcTypes.GUARD,
                        messages={
                            0: ["Halt, traveler! Antina City permits only those with proper credentials to pass "
                                "these gates.",
                                "State your business and present your identification, or you shall not venture beyond.",
                                "The safety of our citizens is paramount, and we cannot afford to be lax in these "
                                "trying times."]},
                        place_morning=[(25, 41)]),

    "jester_ralzo": Npc(name="jester ralzo",
                        npc_type=NpcTypes.JESTER,
                        messages={
                            0: ["Traveling solo, but tagging along with this fine caravan! Life’s a journey, after"
                                " all, and laughter is my trade. Stuck here or not, the road’s more fun with a bit "
                                "of mischief, wouldn’t you say?"]}),

    "innkeeper_alira": Npc(name="innkeeper alira",
                           npc_type=NpcTypes.INNKEEPER,
                           messages={
                               0: ["Welcome, traveler! I’m Alira, keeper of this fine inn. Do you need a room to "
                                   "rest or perhaps a meal to fill your belly?"],
                               1: ["Our rooms are cozy and warm, perfect for a weary traveler. Would you like to "
                                   "stay the night?"],
                               2: ["Feeling hungry? We've got hearty meals to fill you up. What will it be?"]},
                           answers={
                               1: "I need to sleep",
                               2: "Buy food"},
                           buy_items={"bread": {"gold": 1},
                                      "cheese": {"gold": 2},
                                      "soup": {"gold": 2},
                                      "water": {"gold": 1},
                                      "bier": {"gold": 2},
                                      "wine": {"gold": 3},
                                      "fish_sardine": {"gold": 3}},
                           buy_beds={"aliras_first_room_key": {"gold": 15},
                                     "aliras_second_room_key": {"gold": 10},
                                     "aliras_third_room_key": {"gold": 8},
                                     "aliras_fourth_room_key": {"gold": 8}},
                           bed_key_message="Perfect. Keep this key, until 30 days.",
                           bed_low_message="Mmmmmmm... you don't have enough.",
                           quantity_message="How many #item do you want to #action?",
                           place=[(22, 42), "inn"]),

    "innkeeper_lyssia": Npc(name="innkeeper lyssia",
                            npc_type=NpcTypes.INNKEEPER,
                            messages={
                                0: ["Welcome to the Aquiri Harbor Inn, traveler! Need a place to rest or a hot meal?"
                                    " Let me know how I can help."],
                                1: ["Our rooms are quiet and cozy, perfect for a weary traveler. Just let me know if"
                                    " you'd like to stay the night."],
                                2: ["Are you looking to purchase some nourishment? What do you want?"]},
                            answers={
                                1: "I need to sleep",
                                2: "Buy food"},
                            buy_items={"bread": {"gold": 1},
                                       "cheese": {"gold": 2},
                                       "soup": {"gold": 2},
                                       "water": {"gold": 1},
                                       "bier": {"gold": 2},
                                       "fish_sardine": {"gold": 3}},
                            buy_beds={"lyssias_first_room_key": {"gold": 12},
                                      "lyssias_second_room_key": {"gold": 8},
                                      "lyssias_third_room_key": {"gold": 5}},
                            bed_key_message="Perfect. Keep this key, until 30 days.",
                            bed_low_message="Mmmmmmm... you don't have enough.",
                            quantity_message="How many #item do you want to #action?",
                            place=[(39, 39), "inn"]),

    "innkeeper_mirabelle": Npc(name="innkeeper mirabelle",
                               npc_type=NpcTypes.INNKEEPER,
                               messages={
                                   0: ["Step into Mirabelle's Inn, weary wanderer. Here, amidst the tranquility of "
                                       "Epiiat, find shelter from the trials of the road. With hearty meals and "
                                       "soft beds, let your worries melt away."],
                                   1: ["Interested in accommodations? Take your pick of rooms tailored to your needs."],
                                   2: ["Are you looking to purchase some nourishment? What do you want?"]},
                               answers={
                                   1: "I need to sleep",
                                   2: "Buy food"},
                               buy_items={"bread": {"gold": 1},
                                          "cheese": {"gold": 2},
                                          "soup": {"gold": 2},
                                          "water": {"gold": 1},
                                          "bier": {"gold": 2}},
                               buy_beds={"mirabelles_main_room_key": {"gold": 5},
                                         "mirabelles_small_room_key": {"gold": 3}},
                               bed_key_message="Perfect. Keep this key, until 30 days.",
                               bed_low_message="Mmmmmmm... you don't have enough.",
                               quantity_message="How many #item do you want to #action?",
                               place=[(21, 29), "inn"]),

    "lord_aric": Npc(name="lord aric",
                     npc_type=NpcTypes.LORD,
                     messages_morning={
                         0: ["Greetings, traveler. Alas, these are troubled times for our fair city.",
                             "Just days past, a dragon's shadow darkened our skies. Fear lingers in the hearts of our "
                             "citizens. The safety of Antina is at stake, and our once-stalwart walls now seem "
                             "fragile.",
                             "May the goddesses watch over us and protect us."]},
                     place_morning=[(23, 40)],
                     place_night=[(24, 40), "arics_house"]),

    "marquis_edrion": Npc(name="marquis edrion",
                          npc_type=NpcTypes.MARQUIS,
                          messages_morning={
                              0: ["A dragon... now of all times? As if these endless skirmishes weren’t burden enough.",
                                  "What cruel twist of fate is this?"]},
                          messages_night={
                              0: ["Zzzzz... zzzz... uhgzz..."]},
                          place=[(24, 40), "edrions_house"]),

    "mayor_thorian": Npc(
        name="mayor thorian",
        npc_type=NpcTypes.MAYOR,
        messages={
            0: ["Welcome to Epiiat, traveler.",
                "Though I greet you as I would any of our own, my heart is heavy with concern. My"
                " daughter, Maisie, has gone missing.",
                "She wandered off days ago, and no trace of her remains. If your path allows it, "
                "please keep an eye out for her.",
                "The villagers and I are desperate for her safe return."]},
        place_morning=[(22, 28), "mayors_house"],
        place_night=[(22, 28), "temple"]
    ),

    "mayors_daughter_maisie": Npc(name="mayor's daughter maisie",
                                  npc_type=NpcTypes.MAYORS_DAUGHTER,
                                  messages={0: ["You... you saved me! I feared I'd never escape Griznuk's clutches.",
                                                "My father, the mayor, will want to thank you properly. Please, come"
                                                " back with me to the village.",
                                                "Words cannot express my gratitude, but I hope our people can repay"
                                                " your bravery."]},
                                  place=[(25, 24), "cave_entrance", "cave_pit", "cave_basin", "cave_gallery",
                                         "chiefs_cave", "goblin_chief_bedroom"]),

    "merchant_bryson": Npc(name="merchant bryson",
                           npc_type=NpcTypes.MERCHANT,
                           messages={
                               0: ["Ah, welcome, welcome! Peruse my wares, brave one. From enchanted potions to sturdy"
                                   " shields",
                                   "Bryson's Emporium has all you need for your journey.",
                                   "Each item tells a tale, and every purchase brings you one step closer to becoming "
                                   "a legend. Don't hesitate to ask if you seek something specific, for in this square,"
                                   " dreams and adventures await!"],
                               1: ["What do you want to buy?"],
                               2: ["What do you want to sell?"]},
                           answers={
                               1: "Buy",
                               2: "Sell"},
                           buy_items={"antidote": {"gold": 5},
                                      "leather_armor": {"gold": 75},
                                      "leather_boots": {"gold": 60},
                                      "little_red_potion": {"gold": 5},
                                      "red_potion": {"gold": 10},
                                      "short_sword": {"gold": 100},
                                      "wood_shield": {"gold": 50},
                                      "torch": {"gold": 20}},
                           quantity_message="How many #item do you want to #action?",
                           place=[(21, 29)]),

    "merchant_elden": Npc(name="merchant elden",
                          npc_type=NpcTypes.MERCHANT,
                          messages={0: ["Hail, warrior! Seek the finest blades and armor in Antina? Forge Master Elden "
                                        "crafts each piece with skill and care. From gleaming swords to resilient "
                                        "shields, my forge yields the tools to shape your destiny.",
                                        "Arm yourself, adventurer, and may the battles you face be victorious!"],
                                    1: ["What do you want to buy?"],
                                    2: ["What do you want to sell?"]},
                          answers={
                              1: "Buy",
                              2: "Sell"},
                          buy_items={"axe": {"gold": 280},
                                     "chainmail_armor": {"gold": 300},
                                     "large_bow": {"gold": 220},
                                     "longsword": {"gold": 350},
                                     "iron_shield": {"gold": 130},
                                     "mesh_boots": {"gold": 100},
                                     "plate_armor": {"gold": 400},
                                     "spear": {"gold": 250},
                                     "spike_shield": {"gold": 150},
                                     "tower_shield": {"gold": 150}},
                          place=[(24, 42)]),

    "merchant_roland": Npc(name="merchant roland",
                           npc_type=NpcTypes.MERCHANT,
                           messages={0: ["Greetings, noble traveler! Step into Roland's Emporium, where treasures and "
                                         "trinkets await your discerning eye. From potions to weapons, my wares are "
                                         "the finest in Antina.",
                                         "Peruse at your leisure, and may your coffers overflow with the spoils of a "
                                         "grand adventure!"],
                                     1: ["What do you want to buy?"],
                                     2: ["What do you want to sell?"]},
                           answers={
                               1: "Buy",
                               2: "Sell"},
                           buy_items={"antidote": {"gold": 7},
                                      "giant_red_potion": {"gold": 15},
                                      "red_potion": {"gold": 10},
                                      "sword": {"gold": 300},
                                      "iron_shield": {"gold": 150},
                                      "torch": {"gold": 20}},
                           place_morning=[(23, 41)]),

    "merchant_selena": Npc(name="merchant selena",
                           npc_type=NpcTypes.MERCHANT,
                           messages={
                               0: ["Ahoy, brave one! Step right up and behold the treasures of Aqiri's Market!",
                                   "From the finest catches of the sea to enchanted trinkets, Selena's Wares has all "
                                   "you desire. A purchase to aid your journey, perhaps?",
                                   "Sail through our goods, and may your pouch grow lighter with satisfaction!"],
                               1: ["What do you want to buy?"],
                               2: ["What do you want to sell?"]},
                           answers={
                               1: "Buy",
                               2: "Sell"},
                           buy_items={"antidote": {"gold": 5},
                                      "harpoon": {"gold": 150},
                                      "hardened_leather_armor": {"gold": 120},
                                      "red_potion": {"gold": 10},
                                      "coast_fishing_pole": {"gold": 200},
                                      "wood_shield": {"gold": 50},
                                      "telescope": {"gold": 200}},
                           place=[(39, 39)]),

    "sailor_kael": Npc(name="sailor kael",
                       npc_type=NpcTypes.SAILOR,
                       messages_morning={
                           0: ["Hold it right there, traveler! This ship isn’t open to passengers. Captain’s orders—no "
                               "exceptions!"]},
                       place_morning=[(39, 39), "thornes_ship"],
                       messages_night={
                           0: ["Zzz... Zzz... Hngh..."]},
                       place_night=[(39, 39), "inn", "third_room"]),

    "sailor_rolan": Npc(name="sailor rolan",
                        npc_type=NpcTypes.SAILOR,
                        messages={
                            0: ["We arrived in Aquiri not long ago, but who knows when we’ll leave. We spotted a "
                                "dragon not far from here... it’s keeping us on edge.",
                                "Better safe than sorry, eh?"]}),

    "tavern_keeper_rudrik": Npc(name="Tavern Keeper Rudrik",
                                npc_type=NpcTypes.TAVERN_KEEPER,
                                messages={
                                    0: ["Welcome to The Golden Tankard, traveler! Take a seat and warm yourself by"
                                        " the fire. We've got hearty stew and the finest ale in town."
                                        " What'll it be—food, drink, or both?"],
                                    1: ["What do you want to buy?"]},
                                answers={
                                    1: "Buy"},
                                buy_items={"bread": {"gold": 2},
                                           "cheese": {"gold": 4},
                                           "soup": {"gold": 2},
                                           "water": {"gold": 1},
                                           "antinas_beer": {"gold": 2}}),

    "traveler_clara": Npc(name="traveler clara",
                          npc_type=NpcTypes.TRAVELER,
                          messages={
                              0: ["Hello there, traveler. It's always good to LISTEN, you know.",
                                  "There's wisdom in hearing others' stories. I'm Clara, by the way."]},
                          place=[(21, 29), "inn"]),

    "traveler_elara": Npc(
        name="traveler elara",
        npc_type=NpcTypes.TRAVELER,
        messages={
            0: ["Greetings, seeker of paths! If you yearn to traverse the mighty mountain range that veils our"
                " land, head eastward.",
                "Beyond the emerald canopy and whispering trees lies a hidden valley. It weaves through the ancient "
                "peaks, offering passage to those who dare to journey.",
                "Take heed, for the woods conceal both mystery and peril, but the call of adventure echoes through "
                "the leaves. May the spirits guide your way, brave traveler."],
            1: ["Northward, the land ascends into highlands infested with goblins and other vile creatures. A "
                "challenge for even the most seasoned adventurer."],
            2: ["To the south, dense woodlands stretch as far as the eye can see.",
                "An enchanting realm, but one must tread cautiously, for shadows dance amidst the trees."],
            3: ["Nay, brave one. The west remains a mystery to me. My journey has yet to unveil the secrets concealed "
                "in those unexplored lands.", "Perhaps one day, the winds of fate will carry me in that direction."]},
        leave_message=["May the spirits guide your way, brave traveler."],
        answers={
            1: "What lies to the north?",
            2: "And what of the southern lands?",
            3: "What about the western reaches? Have you ventured there?"},
        place_morning=[(22, 29)]),

    "traveler_elinor": Npc(name="traveler elinor",
                           npc_type=NpcTypes.TRAVELER,
                           messages={
                               0: ["Alas, the city gates remain closed to me. But fear not, fellow wanderer!",
                                   "To the east lies the charming fishing village of Aquiri. A quaint haven where the"
                                   " sea breeze dances with the scent of salt and adventure.",
                                   "Seek refuge there, share tales with the fishermen, and who knows, perhaps your "
                                   "path will intertwine with the whims of destiny. May the winds guide your steps, "
                                   "for there is always another path to tread."]},
                           place=[(25, 41)]),

    "traveler_kaelen": Npc(name="traveler kaelen",
                           npc_type=NpcTypes.TRAVELER,
                           messages={
                               0: ["You know, if we had some explosives, those rocks would be gone in no time.",
                                   "Do you, by chance, carry any? It’d make clearing this path a lot easier."]},
                           place=[(21, 41)]),

    "traveler_kaelin": Npc(name="traveler kaelin",
                           npc_type=NpcTypes.TRAVELER,
                           messages={
                               0: ["Hail, fellow wanderer. I've treaded the southern realms, through the treacherous "
                                   "Dark Forest.",
                                   "A word of caution, brave soul – the woods conceal more than beauty. Dark whispers "
                                   "and lurking dangers await. I'd advise against venturing there unless your courage "
                                   "knows no bounds.",
                                   "May your travels be safer than mine, and the path you choose be bathed in the "
                                   "light of wisdom."]}),

    "traveler renan": Npc(name="traveler renan",
                          npc_type=NpcTypes.TRAVELER,
                          messages={
                              0: ["You look like you’ve seen your share of the road, friend. If you need rest, "
                                  "look for an inn—there’s no better place to regain your strength.",
                                  "A warm bed and a hearty meal can make all the difference before facing "
                                  "whatever lies ahead."]},
                          place=[(21, 29)]),

    "traveler seraph": Npc(name="traveler seraph",
                           npc_type=NpcTypes.TRAVELER,
                           messages={
                               0: ["Ah, greetings, fellow wayfarer! Stuck, just like me, eh? Gorrick here "
                                   "mentioned some caves to the north that might lead us across.",
                                   "Aye, those caves are an option, but beware! Lately, they've become a haven "
                                   "for Goblins and other foul creatures.",
                                   "A perilous journey awaits, my friend. Tread "
                                   "carefully if you choose that path."]},
                           place=[(26, 29)]),

    "traveler_sylas": Npc(name="traveler sylas",
                          npc_type=NpcTypes.TRAVELER,
                          messages={
                              0: ["Greetings, wanderer. A word of wisdom for your journey: always embrace exploration.",
                                  "Hidden wonders and untold tales await those who venture beyond the familiar. May "
                                  "your steps be guided by curiosity, and may the world unveil its mysteries before "
                                  "you."]},
                          place=[(21, 29)]),

    "traveler_thaldir": Npc(name="traveler thaldir",
                            npc_type=NpcTypes.TRAVELER,
                            messages={
                                0: ["Greetings, seeker of fortune. Remember, in every step, 'tis wise to look around "
                                    "and check. Secrets often hide where the eye does not linger.",
                                    "May the journey unveil the unseen, brave one."]},
                            place=[(21, 28)]),

    # Villager from Epiiat.
    "villager_doran": Npc(name="villager_doran",
                          npc_type=NpcTypes.VILLAGER,
                          messages_morning={
                              0: ["Zzzz... zzz... Zzzz...",
                                  "Ugh... uphg...",
                                  "Zzzz... zzz..."]},
                          messages_night={
                              0: ["Ah, nothing like a good drink and a hot meal after a long day. The bard's song"
                                  " tonight is a fine one—fills the air with tales of heroes and lost treasures.",
                                  "Sit and listen a while, friend. The road can wait a moment longer, can’t it?"]},
                          place=[(21, 29), "inn"]),

    "villager_fira": Npc(name="villager fira",
                         npc_type=NpcTypes.VILLAGER,
                         messages={
                             0: ["Oh, traveler, have you heard? The mayor’s daughter, Maisie, hasn’t been seen "
                                 "for days."
                                 " I’m so worried—she’s always been kind to us all.",
                                 "If she’s in danger, we must do something. Please, if you find any trace of her, "
                                 "let the mayor know."]},
                         place_morning=[(22, 28)],
                         place_evening=[(22, 28), "wooden_house"]),

    "villager_merrin": Npc(name="villager merrin",
                           npc_type=NpcTypes.VILLAGER,
                           messages={
                               0: ["Oh, traveler, have you heard? The mayor’s daughter, Elara, has gone missing.",
                                   "Some say she wandered too far, but I fear the worst... The goblins have been"
                                   " lurking near the forest caves lately. It’s possible they’ve taken her.",
                                   "I hope I’m wrong, but we need help before it’s too late."]},
                           place_morning=[(21, 29)]),

    # Villager from Aquiri.

    # Villager from Antina.
    "villager_gareth": Npc(name="villager gareth",
                           npc_type=NpcTypes.VILLAGER,
                           messages={
                               0: ["Ah, these must be from Marlin! He always sends the best catch. Thank you for"
                                   " bringing them all the way here. It couldn’t have been an easy journey."]},
                           place_morning=[(22, 40)],
                           place_night=[(23, 42), "mid_house"]),

    "villager_fenna": Npc(name="villager fenna",
                          npc_type=NpcTypes.VILLAGER,
                          messages_morning={
                              0: ["Dragons are majestic creatures, aren’t they? I wish I could see one with "
                                  "my own eyes... from afar, of course!"]},
                          messages_evening={
                              0: ["The stars look so bright tonight. If the dragon is out there, I hope it’s "
                                  "somewhere far away.",
                                  "I can’t help but dream of seeing one up close, though."]},
                          place_morning=[(23, 42), "white_house"]),

    "villager_garrek": Npc(name="villager garrek",
                           npc_type=NpcTypes.VILLAGER,
                           messages_morning={
                               0: ["A dragon could spell disaster for our crops and livestock... I can’t sleep "
                                   "thinking about it."]},
                           messages_evening={
                               0: ["They say a dragon was spotted near the hills... Do you think it will come here?"]},
                           place_morning=[(23, 41)],
                           place_evening=[(23, 42), "white_house"]),

    "villager_halden": Npc(name="villager halden",
                           npc_type=NpcTypes.VILLAGER,
                           messages_morning={
                               0: ["A dragon, eh? Curious sight indeed. Haven’t seen one since the old tales of "
                                   "my youth."]},
                           messages_night={
                               0: ["Strange, isn't it? The night feels heavier... Maybe the dragon's watching over "
                                   "us, or maybe it's the calm before the storm."]},
                           place_morning=[(22, 41)],
                           place_night=[(22, 42), "tavern"]),

    "villager_lyria": Npc(name="villager lyria",
                          npc_type=NpcTypes.VILLAGER,
                          messages_morning={
                              0: ["They say a dragon was spotted near the hills... Do you think it will come here?"]},
                          messages_evening={
                              0: ["I can't shake off the thought of that dragon... It's so quiet tonight, almost "
                                  "eerie. Do you think it could be out there, watching us?"]},
                          place_morning=[(23, 42)],
                          place_evening=[(23, 42), "family_house"]),

    "villager_mirrel": Npc(name="villager mirrel",
                           npc_type=NpcTypes.VILLAGER,
                           messages_morning={
                               0: ["If the rumors are true, the kingdom’s knights better step up. We need protection "
                                   "now more than ever."]},
                           messages_evening={
                               0: ["I can barely sleep, thinking of the danger we might be in. I hope the soldiers "
                                   "are preparing... They better be, or we'll all be in trouble."]},
                           place_morning=[(23, 41)],
                           place_evening=[(24, 41)]),

    "villager_orik": Npc(name="villager orik",
                         npc_type=NpcTypes.VILLAGER,
                         messages_morning={
                             0: ["Bah! Dragons or not, life goes on. Let the royals deal with it. I’ve got fields "
                                 "to tend."]},
                         messages_evening={
                             0: ["I can't shake off the thought of that dragon... It's so quiet tonight, almost "
                                 "eerie. Do you think it could be out there, watching us?"]},
                         place_morning=[(23, 41)],
                         place_evening=[(23, 42), "family_house"]),

    "worker_gorrick": Npc(name="worker gorrick",
                          npc_type=NpcTypes.WORKER,
                          messages={
                              0: ["Oh, traveler, have you heard? The mayor’s daughter, Maisie, has gone missing.",
                                  "Some say she wandered too far, but I fear the worst... The goblins have been "
                                  "lurking near the forest caves lately. It’s possible they’ve taken her. ",
                                  "I hope I’m wrong, but we need help before it’s too late."]},
                          place=[(26, 29)]),

    "whispers": Npc(name="whispers",
                    npc_type=NpcTypes.WHISPERS,
                    messages={0: ["Elina...", "Elina...", "...your destiny awaits.", "Follow the whispers of the wind,"
                                                                                     " and come to me.",
                                  "Secrets untold and challenges unknown lie ahead.",
                                  "Trust in the unseen path...", "... come to me."]}),

    # Others.
    "animal_wild_cat": Npc(name="animal wild cat",
                           npc_type=NpcTypes.ANIMAL,
                           place=[(12, 24)],
                           messages_morning={
                               0: ["Purr... purr... purr... purr..."]},
                           place_morning=[(12, 24)],
                           messages_night={
                               0: ["Meow!"]},
                           place_night=[(13, 25)])
}

# MOBS.
MOBS = {
    "bandit": Mob(
        name="Bandit",
        hp=30,
        hpmax=30,
        description="A ruthless rogue lurking in the shadows, ready to ambush travelers for gold and loot.",
        attack=3,
        defense=2,
        evasion=0.4,
        precision=0.8,
        critical_coeficient=1.5,
        critical_chance=20,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=0.4,
        items={"gold": 15, "red_potion": 1, "antidote": 1},
        items_drop_chances=[0.5, 0.2, 0.1],
        experience=4,
        skills=[SKILLS_MOB["attack_bandit"]],
    ),
    "basilisk": Mob(
        name="Basilisk",
        hp=80,
        hpmax=80,
        description="A fearsome serpent with petrifying eyes. One glance can turn the bravest warrior to stone.",
        attack=19,
        defense=8,
        evasion=0.6,
        precision=0.7,
        critical_coeficient=1.7,
        critical_chance=20,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=20,
        items={"basilisk_fangs": 2},
        items_drop_chances=[0.7],
        experience=14,
        skills=[SKILLS_MOB["attack_basilisk"]],
    ),
    "climbing_goblin": Mob(
        name="Climbing Goblin",
        hp=35,
        hpmax=35,
        description="A nimble goblin adept at scaling walls, striking from above with cunning and speed.",
        attack=14,
        defense=4,
        evasion=0.3,
        precision=0.8,
        critical_coeficient=1.5,
        critical_chance=20,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=40,
        items={"gold": 20, "red_potion": 1, "wood_shield": 1, "antidote": 1},
        items_drop_chances=[0.5, 0.1, 0.05, 0.05],
        experience=10,
        skills=[SKILLS_MOB["attack_climbing_goblin"]],
    ),

    "dragon": Mob(
        name="Dragon FireFrost",
        hp=150,
        hpmax=150,
        description="A legendary beast of fire and ice, guarding ancient treasures with unyielding might.",
        id_key="dragon",
        attack=30,
        defense=10,
        evasion=0.5,
        precision=0.9,
        critical_coeficient=1.5,
        critical_chance=30,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=0,
        items={},
        items_drop_chances=[1],
        experience=888,
        skills=[SKILLS_MOB["attack_dragon"]],
    ),

    "dryad": Mob(
        name="Dryad",
        hp=20,
        hpmax=20,
        description="A mystical forest guardian, blending with trees to protect nature from intruders.",
        attack=12,
        defense=10,
        evasion=0.6,
        precision=0.9,
        critical_coeficient=1.7,
        critical_chance=20,
        poison_stacks=3,
        poison_chance=0.33,
        escape_chance=50,
        items={},
        items_drop_chances=[],
        experience=12,
        skills=[SKILLS_MOB["attack_dryad"]],
    ),

    "giant_blind_spider": Mob(
        name="Giant Blind Spider",
        hp=70,
        hpmax=70,
        description="A massive arachnid relying on sharp senses to hunt prey in total darkness.",
        attack=20,
        defense=5,
        evasion=0.6,
        precision=0.8,
        critical_coeficient=1.5,
        critical_chance=20,
        poison_stacks=5,
        poison_chance=0.5,
        escape_chance=5,
        items={"giant_silk": 1},
        items_drop_chances=[0.5],
        experience=15,
        skills=[SKILLS_MOB["attack_giant_blind_spider"]],
    ),

    "giant_slime": Mob(
        name="Giant Slime",
        hp=40,
        hpmax=40,
        description="A massive, gelatinous creature that engulfs anything in its path, splitting when struck.",
        attack=3,
        defense=0,
        evasion=0,
        precision=0.65,
        critical_coeficient=1.5,
        critical_chance=20,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=50,
        items={"slime_balls": 2, "red_potion": 1},
        items_drop_chances=[0.5, 0.2],
        experience=3,
        skills=[SKILLS_MOB["attack_giant_slime"]],
    ),

    "giant_spider": Mob(
        name="Giant Spider",
        hp=70,
        hpmax=70,
        description="A monstrous predator weaving deadly webs to ensnare its unsuspecting prey.",
        attack=14,
        defense=5,
        evasion=0.3,
        precision=0.65,
        critical_coeficient=1.6,
        critical_chance=15,
        poison_stacks=1,
        poison_chance=0.15,
        escape_chance=30,
        items={"giant_silk": 1, "red_potion": 1},
        items_drop_chances=[0.6, 0.2],
        experience=11,
        skills=[SKILLS_MOB["attack_giant_spider"]],
    ),

    "goblin": Mob(
        name="Goblin",
        hp=15,
        hpmax=15,
        description="A mischievous, cunning creature that thrives in chaos and ambushes the unwary.",
        attack=3,
        defense=1,
        evasion=0.3,
        precision=0.7,
        critical_coeficient=1.7,
        critical_chance=60,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=45,
        items={"gold": 5, "little_red_potion": 1, "red_potion": 1, "antidote": 1},
        items_drop_chances=[0.5, 0.4, 0.2, 0.4],
        experience=3,
        skills=[SKILLS_MOB["attack_goblin"]],
    ),

    "goblin_chief": Mob(
        name="Goblin Chief",
        hp=75,
        hpmax=75,
        description="A ruthless leader commanding goblin hordes with brute strength and wicked intelligence.",
        attack=12,
        defense=6,
        evasion=0.4,
        precision=0.6,
        critical_coeficient=1.3,
        critical_chance=30,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=0,
        items={"gold": 60, "red_potion": 5},
        items_drop_chances=[0.5, 0.7],
        experience=30,
        skills=[SKILLS_MOB["attack_goblin_chief"]],
    ),

    "goblin_hunter": Mob(
        name="Goblin Hunter",
        hp=35,
        hpmax=35,
        description="A stealthy goblin skilled with bows, striking enemies from the shadows.",
        attack=7,
        defense=2,
        evasion=0.5,
        precision=0.7,
        critical_coeficient=1.5,
        critical_chance=60,
        poison_stacks=2,
        poison_chance=0.15,
        escape_chance=50,
        items={"gold": 10, "little_red_potion": 1, "bone_sword": 1, "bone_shield": 1, "antidote": 1},
        items_drop_chances=[0.5, 0.1, 0.1, 0.05, 0.05],
        experience=4,
        skills=[SKILLS_MOB["attack_goblin_hunter"]],
    ),

    "goblin_war_chief": Mob(
        name="Goblin War Chief",
        hp=60,
        hpmax=60,
        description="A battle-hardened goblin, wielding brutal weapons and rallying troops into bloodthirsty frenzies.",
        attack=15,
        defense=6,
        evasion=0.5,
        precision=0.7,
        critical_coeficient=1.2,
        critical_chance=30,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=35,
        items={"gold": 30, "red_potion": 1, "iron_shield": 1, "axe": 1},
        items_drop_chances=[0.8, 0.05, 0.05, 0.05],
        experience=12,
        skills=[SKILLS_MOB["attack_goblin_war_chief"]],
    ),

    "goblin_war": Mob(
        name="War Goblin",
        hp=35,
        hpmax=35,
        description="A vicious goblin berserker, charging into battle with reckless abandon.",
        attack=6,
        defense=3,
        evasion=0.4,
        precision=0.7,
        critical_coeficient=1.7,
        critical_chance=40,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=40,
        items={"gold": 10, "bone_sword": 1, "bone_shield": 1},
        items_drop_chances=[0.5, 0.1, 0.1],
        experience=4,
        skills=[SKILLS_MOB["attack_goblin_war"]],
    ),

    "little_slime": Mob(
        name="Little Slime",
        hp=10,
        hpmax=10,
        description="A tiny, bouncing blob that seems harmless but multiplies rapidly.",
        movable=True,
        movable_biomes=[23],
        move_chance=0.2,
        attack=2,
        defense=0,
        evasion=0,
        precision=0.6,
        critical_coeficient=1.5,
        critical_chance=10,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=70,
        items={"slime_balls": 1},
        items_drop_chances=[0.5],
        experience=1,
        skills=[SKILLS_MOB["attack_little_slime"]]
    ),

    "poison_slime": Mob(
        name="Poison Slime",
        hp=20,
        hpmax=20,
        description="A toxic, pulsing mass that leaves a deadly trail of venom.",
        attack=3,
        defense=1,
        evasion=0.3,
        precision=0.6,
        critical_coeficient=1.2,
        critical_chance=30,
        poison_stacks=1,
        poison_chance=0.15,
        escape_chance=50,
        items={"slime_balls": 2},
        items_drop_chances=[0.4],
        experience=2,
        skills=[SKILLS_MOB["attack_poison_slime"]],
    ),

    "poison_spider": Mob(
        name="Poison Spider",
        hp=30,
        hpmax=30,
        description="A venomous spider lurking in the dark, its bite bringing slow and painful death.",
        attack=5,
        defense=3,
        evasion=0.4,
        precision=0.8,
        critical_coeficient=1.4,
        critical_chance=15,
        poison_stacks=2,
        poison_chance=0.25,
        escape_chance=50,
        items={"giant_silk": 1, "poison_gland": 1},
        items_drop_chances=[0.4, 0.2],
        experience=5,
        skills=[SKILLS_MOB["attack_poison_spider"]],
    ),

    "rabbit": Mob(
        name="Rabbit",
        hp=5,
        description="A swift, timid creature that dashes away at the slightest noise. Its soft fur hides surprising "
                    "agility.",
        escape_chance=100,
        escape_mob_probability=0.7,
        hostile=False,
        items={"rabbit_meat": 1},
        items_drop_chances=[0.5],
        experience=1
    ),

    "shadow_wolf": Mob(
        name="Shadow Wolf",
        hp=50,
        hpmax=50,
        description="A spectral beast emerging from darkness, striking unseen before vanishing.",
        attack=10,
        defense=5,
        evasion=0.5,
        precision=0.85,
        critical_coeficient=1.6,
        critical_chance=20,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=20,
        items={"wolf_fur": 1, "wolf_claw": 2},
        items_drop_chances=[0.3, 0.2],
        experience=15,
        skills=[SKILLS_MOB["attack_shadow_wolf"]],
    ),

    "skeleton_warrior": Mob(
        name="Skeleton Warrior",
        hp=40,
        hpmax=40,
        description="An undead knight bound by ancient magic, wielding rusted weapons with eerie precision.",
        attack=20,
        defense=12,
        evasion=0.3,
        precision=0.7,
        critical_coeficient=1.3,
        critical_chance=10,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=10,
        items={"bone_sword": 1, "bone_shield": 1},
        items_drop_chances=[0.4, 0.4],
        experience=13,
        skills=[SKILLS_MOB["attack_skeleton_warrior"]],
    ),

    "slime": Mob(
        name="Slime",
        hp=20,
        hpmax=20,
        description="A shapeless, gooey creature absorbing anything foolish enough to get close.",
        attack=3,
        defense=1,
        evasion=0.3,
        precision=0.5,
        critical_coeficient=1.5,
        critical_chance=40,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=60,
        items={"slime_balls": 2},
        items_drop_chances=[0.6],
        experience=2,
        skills=[SKILLS_MOB["attack_slime"]]
    ),

    "training_dummy": Mob(
        name="Training Dummy",
        hp=999,
        hpmax=999,
        description="A wooden target that strikes back unexpectedly, teaching adventurers the pain of careless blows.",
        attack=1,
        defense=1,
        evasion=0.2,
        precision=0.8,
        critical_coeficient=1,
        critical_chance=40,
        poison_stacks=1,
        poison_duration=2,
        poison_source="training_dummy",
        poison_max_stacks=30,
        poison_chance=80,
        escape_chance=99,
        experience=0,
        skills=[SKILLS_MOB["attack_training_dummy"]]
    ),

    "orc": Mob(
        name="Orc",
        hp=35,
        hpmax=35,
        description="A savage brute with immense strength, thriving in battle and chaos.",
        attack=6,
        defense=5,
        evasion=0.3,
        precision=0.7,
        critical_coeficient=1.5,
        critical_chance=20,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=0,
        items={"gold": 20, "red_potion": 1, "antidote": 1},
        items_drop_chances=[0.5, 0.2, 0.1],
        experience=5,
        skills=[SKILLS_MOB["attack_orc"]],
    ),

    "spectral_foxshade": Mob(
        name="Spectral Foxshade",
        hp=1,
        hpmax=1,
        description="A ghostly fox flickering through dimensions, impossible to catch.",
        attack=10,
        defense=0,
        evasion=0,
        precision=1,
        critical_coeficient=1.7,
        critical_chance=20,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=100,
        items={"gold": 100},
        items_drop_chances=[0.9],
        experience=25,
        escape_mob_probability=0.5,
        skills=[SKILLS_MOB["attack_spectral_foxshade"]],
    ),
    "spectrum": Mob(
        name="Spectrum",
        hp=40,
        hpmax=40,
        description="A shifting, ethereal being of pure energy, bending light to evade attacks.",
        attack=17,
        defense=0,
        evasion=0.8,
        precision=0.8,
        critical_coeficient=1.7,
        critical_chance=20,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=20,
        items={},
        items_drop_chances=[],
        experience=16,
        skills=[SKILLS_MOB["attack_spectrum"]],
    ),
    "troll": Mob(
        name="Troll",
        hp=50,
        hpmax=50,
        description="A hulking monster with relentless regeneration, crushing foes with sheer brute force.",
        attack=15,
        defense=8,
        evasion=0.2,
        precision=0.75,
        critical_coeficient=1.4,
        critical_chance=20,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=50,
        items={"gold": 15, "red_potion": 1, "bludgeon": 1},
        items_drop_chances=[0.5, 0.2, 0.1],
        experience=12,
        skills=[SKILLS_MOB["attack_troll"]],
    ),

    "undead_warrior": Mob(
        name="Undead Warrior",
        hp=50,
        hpmax=50,
        description="A cursed knight refusing to rest, forever seeking battle.",
        attack=16,
        defense=12,
        evasion=0.2,
        precision=0.7,
        critical_coeficient=1.6,
        critical_chance=15,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=10,
        items={"gold": 20, "rusty_sword": 1, "rusty_shield": 1},
        items_drop_chances=[0.4, 0.2, 0.2],
        experience=16,
        skills=[SKILLS_MOB["attack_undead_warrior"]],
    ),

    "watchful_goblin": Mob(
        name="Watchful Goblin",
        hp=25,
        hpmax=25,
        description="A keen-eyed goblin acting as a scout, alerting allies to approaching danger.",
        attack=3,
        defense=1,
        evasion=0.4,
        precision=0.7,
        critical_coeficient=1.5,
        critical_chance=30,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=40,
        items={"gold": 5, "bones": 1},
        items_drop_chances=[0.5, 0.05],
        experience=3,
        skills=[SKILLS_MOB["attack_watchful_goblin"]],
    ),

    "wild_boar": Mob(
        name="Wild Boar",
        hp=25,
        hpmax=25,
        description="A fierce, territorial beast that charges with unstoppable force.",
        attack=4,
        defense=2,
        evasion=0.3,
        precision=0.8,
        critical_coeficient=1.4,
        critical_chance=10,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=30,
        items={"boar_tusk": 2},
        items_drop_chances=[0.4],
        experience=3,
        skills=[SKILLS_MOB["attack_wild_boar"]],
        escape_mob_probability=0.4
    ),

    "young_dragon": Mob(
        name="Young Dragon",
        hp=150,
        hpmax=150,
        description="A growing drake still mastering its flames, yet already a formidable threat.",
        attack=20,
        defense=15,
        evasion=0.4,
        precision=0.9,
        critical_coeficient=1.7,
        critical_chance=25,
        poison_stacks=0,
        poison_chance=0,
        escape_chance=5,
        items={"dragon_scales": 2},
        items_drop_chances=[0.7],
        experience=30,
        skills=[SKILLS_MOB["attack_young_dragon"]],
    ),

    "zombie": Mob(
        name="Zombie",
        hp=60,
        hpmax=60,
        description="A mindless corpse driven by hunger, endlessly shambling forward.",
        attack=5,
        defense=2,
        evasion=0.2,
        precision=0.6,
        critical_coeficient=1.2,
        critical_chance=5,
        poison_stacks=3,
        poison_chance=0.05,
        escape_chance=5,
        items={"rotten_flesh": 3},
        items_drop_chances=[0.5],
        experience=7,
        skills=[SKILLS_MOB["attack_zombie"]],
    ),
}

# Regions.
REGIONS = {
    "aerthos": Region(
        name="AERTHOS",
        description="The rugged continent of storms, stone plains, and ancient winds.",
        color_label=Colors.YELLOW.value,
    ),
    "aerthos_dune_sea": Region(
        name="DUNE SEA OF AERTHOS",
        description="A vast desert of shifting dunes where the sun scorches unbroken horizons.",
        color_label=Colors.CYAN.value,
    ),
    "boreal": Region(
        name="BOREAL",
        description="A frigid southern continent shaped by forests, glaciers, and eternal frost.",
        color_label=Colors.BLUE.value,
    ),
    "great_steppe_of_aerthos": Region(
        name="GREAT STEPPE OF AERTHOS",
        description="Endless grasslands swept by fierce winds and roaming nomadic clans.",
        color_label=Colors.VIOLET.value,
    ),
    "isle_of_the_burning_crest": Region(
        name="ISLE OF THE BURNING CREST",
        description="A volcanic island crowned by fiery peaks and ever-glowing embers.",
        color_label=Colors.BLACK.value,
    ),
    "isle_of_everice": Region(
        name="ISLE OF EVERICE",
        description="A frozen island locked in perpetual winter, untouched by the sun’s warmth.",
        color_label=Colors.WHITE.value,
    ),
    "naiwat": Region(
        name="NAIWAT",
        description="The ancient continent where you have awakened, land of two moons and old whispers.",
        color_label=Colors.ORANGE.value,
    ),
    "solara": Region(
        name="SOLARA",
        description="A bright and fertile continent blessed with long days and radiant skies.",
        color_label=Colors.GREN.value,
    ),
    "the_silent_north": Region(
        name="THE SILENT NORTH",
        description="A remote frozen frontier near Everice, where silence rules the winds.",
        color_label=Colors.DARK_GREY.value,
    ),
    "the_unknown_expanse": Region(
        name="THE UNKNOWN EXPANSE",
        description="A mysterious region unmapped by any traveler, shrouded in doubt and rumor.",
        color_label=Colors.DARK_BLUE.value,
    ),

    "none": Region(),
}

# Bioms of map.
BIOMES = {
    "arctic_tundra": Biome(
        color=(150, 200, 200, 255),
        description="Frozen ground stretches endlessly, dotted with hardy moss and lichen. Icy winds sweep across "
                    "the barren, snow-covered plains beneath a pale, silent sky.",
        color_label=(150, 200, 200, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="ARCTIC TUNDRA",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 0,
            Months.IGNARIS.value: 5,
            Months.OUSKARA.value: -10,
            Months.NERITH.value: -40,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "ash_covered_rocky": Biome(
        color=(120, 110, 100, 255),
        description="Charred stones lie buried beneath layers of gray ash. The air is dry and still, carrying the "
                    "scent of cooled volcanic fire.",
        color_label=(120, 110, 100, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="ASH-COVERED ROCKY",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 25,
            Months.IGNARIS.value: 45,
            Months.OUSKARA.value: 20,
            Months.NERITH.value: 15,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "bai": Biome(),

    "building": Biome(
        color=(180, 110, 60, 255),
        description="...",
        color_label=(180, 110, 60, 255),
        fight=True,
        mobs_base=MOBS,
        name="...",
        pace=4,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "canyon": Biome(
        color=(54, 54, 54, 255),
        description="Shadowy canyon inhabited by fearsome creatures, dark depths, echoing roars, and lurking horrors",
        color_label=(54, 54, 54, 255),
        fight=True,
        mobs_names=["basilisk", "giant_blind_spider", "orc", "spectrum"],
        mobs_chances=[30, 50, 10, 30],
        mobs_base=MOBS,
        name="CANYON",
        req=["torch", "rope"],
        pace=12,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 25,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 4,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "cave": Biome(
        color=(1, 1, 1, 255),
        description="...",
        color_label=(1, 1, 1, 255),
        fight=True,
        mobs_names=["goblin", "orc"],
        mobs_chances=[80, 50],
        mobs_base=MOBS,
        name="CAVE",
        req=["torch"],
        pace=10,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 25,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 4,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "coast": Biome(
        color=(239, 228, 176, 255),
        description="Seaside with swaying palm trees, echoing waves, and vibrant life.",
        color_label=(239, 228, 176, 255),
        fight=True,
        mobs_names=["little_slime", "slime"],
        mobs_chances=[5, 30],
        mobs_base=MOBS,
        name="COAST",
        req=[],
        pace=4,
        water=True,
        status=[PlayerStatus.WALK.value, PlayerStatus.SURF.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees=["coconut_palm"],
        trees_base=TREES,
        trees_ratio={"coconut_palm": 0.33},
        fishes=["fish_sabalo", "fish_tuna", "fish_snapper", "fish_sardine", "fish_ray", "fish_mahi-mahi"],
        fishes_base=FISHES,

    ),

    "cold_island_steppe": Biome(
        color=(145, 145, 120, 255),
        description="Flat, treeless plains stretch beneath gray skies, covered in frost-kissed grasses and swept by"
                    " relentless coastal winds from the surrounding sea.",
        color_label=(145, 145, 120, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="COLD ISLAND STEPPE",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 16,
            Months.IGNARIS.value: 20,
            Months.OUSKARA.value: 13,
            Months.NERITH.value: 5,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "dark_forest": Biome(
        color=(22, 118, 51, 255),
        description="Shadowy forest of peril, twisted trees loom overhead, their gnarled branches casting eerie "
                    "shadows. ",
        color_label=(22, 118, 51, 255),
        fight=True,
        mobs_names=["spectral_foxshade", "giant_spider", "poison_spider"],
        mobs_chances=[1, 30, 10],
        mobs_base=MOBS,
        name="DARK FOREST",
        req=[],
        pace=7,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 25,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "death_valley": Biome(
        color=(152, 176, 159, 255),
        description="Dreadful dead valley, a chilling abyss where every step deepens the terror within. The air grows "
                    "heavy, and eerie whispers intensify, inducing an unsettling unease as you delve further.",
        color_label=(152, 176, 159, 255),
        fight=True,
        mobs_names=["skeleton_warrior"],
        mobs_chances=[40],
        mobs_base=MOBS,
        name="DEATH VALLEY",
        req=[],
        pace=7,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "deep_ocean": Biome(
        color=(40, 49, 151, 255),
        description="Dark, cold waters stretch endlessly, illuminated only by bioluminescent creatures. Pressure "
                    "crushes all but the hardiest life in this mysterious abyss.",
        color_label=(40, 49, 151, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="DEEP OCEAN",
        pace=18,
        water=True,
        fishes=["fish_sabalo", "fish_tuna", "fish_swordfish", "fish_snapper", "fish_sardine", "fish_sabalo", "fish_ray",
                "fish_mahi-mahi", "fish_mackerel", "fish_hammerhead_shark", "fish_grouper", "fish_flounder"],
        status=[PlayerStatus.SURF.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "desert": Biome(
        color=(210, 180, 100, 255),
        description="Vast, sun-scorched land with cracked earth, scattered cacti, and distant mirages. Wind sweeps "
                    "through dunes, whispering across the barren, unforgiving landscape.",
        color_label=(210, 180, 100, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="DESERT",
        req=[],
        pace=10,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 25,
            Months.IGNARIS.value: 35,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 2,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "desert_coast": Biome(
        color=(190, 150, 100, 255),
        description="Narrow strip of life along shimmering waters, with sparse reeds, cracked soil, and golden sands"
                    " stretching beyond the fragile, flowing boundary.",
        color_label=(190, 150, 100, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="DESERT RIVER COAST",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value, PlayerStatus.SURF.value],
        month_temperatures={
            Months.AURENAR.value: 25,
            Months.IGNARIS.value: 35,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 2,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "desert_mountains": Biome(
        color=(140, 100, 60, 255),
        description="Rugged, sunbaked peaks rise from dry valleys, their rocky faces carved by wind. Sparse vegetation "
                    "clings to life in the harsh, arid terrain.",
        color_label=(140, 100, 60, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="DESERT MOUNTAINS",
        req=[],
        pace=10,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 25,
            Months.IGNARIS.value: 35,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 2,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "desert_river": Biome(
        color=(50, 100, 255, 255),
        description="A rare lifeline winding through arid sands, its banks lined with hardy vegetation and scattered "
                    "stones, bringing fleeting freshness to the sunbaked land.",
        color_label=(50, 100, 255, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="RIVER",
        req=[],
        pace=6,
        water=True,
        fishes=[],
        status=[PlayerStatus.SURF.value],
        month_temperatures={
            Months.AURENAR.value: 25,
            Months.IGNARIS.value: 35,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 2,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "dunes": Biome(
        color=(210, 180, 140, 255),
        description="Endless waves of golden sand rise and fall under scorching sun, shaped by wind into ever-changing "
                    "ridges in a silent, arid expanse.",
        color_label=(210, 180, 140, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="DUNES",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 25,
            Months.IGNARIS.value: 35,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 2,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "estuary": Biome(),

    "fields": Biome(
        color=(115, 231, 29, 255),
        description="Verdant fields, rolling emerald expanses dotted with wildflowers, where gentle breezes carry the "
                    "sweet scent of blooming herbs and distant melodies from hidden creatures in the tall grass.",
        color_label=(115, 231, 29, 255),
        fight=True,
        mobs_names=["dryad", "slime", "poison_slime"],
        mobs_chances=[15, 30, 15],
        mobs_base=MOBS,
        name="FIELDS",
        req=[],
        pace=5,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "forest": Biome(
        color=(34, 177, 76, 255),
        description="Thick trees, vibrant flora, wildlife, hidden trails, and lurking danger in this treacherous "
                    "forest realm.",
        color_label=(34, 177, 76, 255),
        fight=True,
        mobs_names=["bandit", "spectral_foxshade", "poison_spider", "wild_boar"],
        mobs_chances=[20, 1, 5, 5],
        mobs_base=MOBS,
        name="FOREST",
        req=[],
        pace=6,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "frostvale": Biome(
        color=(120, 186, 252, 255),
        description="A pristine, snow-covered expanse where frost-kissed silence reigns. Glistening ice formations "
                    "adorn the landscape, creating an ethereal and serene winter tableau in nature's icy embrace.",
        color_label=(120, 186, 252, 255),
        fight=False,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="FROSTVALE",
        req=[],
        pace=6,
        water=True,
        fishes=["fish_sabalo"],
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "frozen_coast": Biome(
        color=(230, 240, 240, 255),
        description="Snow-covered beaches meet icy waves, where frost clings to driftwood and sea spray freezes "
                    "mid-air under a pale, wintry sky.",
        color_label=(230, 240, 240, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="FROZEN COAST",
        req=[],
        pace=9,
        water=True,
        fishes=[],
        status=[PlayerStatus.WALK.value, PlayerStatus.SURF.value],
        month_temperatures={
            Months.AURENAR.value: 16,
            Months.IGNARIS.value: 20,
            Months.OUSKARA.value: 13,
            Months.NERITH.value: 5,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "frozen_sea": Biome(
        color={Months.AURENAR.value: (63, 72, 204, 255),
               Months.NERITH.value: (120, 180, 250, 255)},
        description={Months.AURENAR.value: "Nothing important.",
                     Months.NERITH.value: "Vast, cracked ice sheets stretch to the horizon, with jagged floes and "
                                          "silent, frigid waters trapped beneath a pale, icy expanse."},
        color_label=(120, 180, 250, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name={Months.AURENAR.value: "SEA",
              Months.NERITH.value: "FROZEN SEA"},
        req=[],
        pace={Months.AURENAR.value: 9,
              Months.NERITH.value: 11},
        water=True,
        fishes=[],
        status={Months.AURENAR.value: [PlayerStatus.SURF.value],
                Months.NERITH.value: [PlayerStatus.WALK.value]},
        month_temperatures={
            Months.AURENAR.value: 14,
            Months.IGNARIS.value: 18,
            Months.OUSKARA.value: 11,
            Months.NERITH.value: 3,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "gates": Biome(
        color=(200, 191, 231, 255),
        description="Nothing important.",
        color_label=(200, 191, 231, 255),
        fight=False,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="GATES",
        req=[],
        pace=2,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "highlands": Biome(
        color=(195, 195, 195, 255),
        description="Rugged terrain, sinister caves, and sneaky goblin tribes dominate these perilous elevated lands.",
        color_label=(195, 195, 195, 255),
        fight=True,
        mobs_names=["goblin"],
        mobs_chances=[40],
        mobs_base=MOBS,
        name="HIGHLANDS",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "hills": Biome(
        color=(78, 185, 32, 255),
        description="Undulating landscapes concealing lurking dangers. Treacherous creatures, hidden in the shadows, "
                    "make these hills a realm of risk for those who dare to traverse their slopes.",
        color_label=(78, 185, 32, 255),
        fight=True,
        mobs_names=["climbing_goblin", "troll", "goblin_war_chief"],
        mobs_chances=[30, 30, 5],
        mobs_base=MOBS,
        name="HILLS",
        req=[],
        pace=6,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "hut": Biome(
        color=(185, 122, 87, 255),
        description="Nothing important.",
        entries={"hut": Biome(description="Island hut, a cozy retreat adorned with a bed, a table, two "
                                          "chairs, and a window, invites serenity amid nature's whispers.",
                              items=["bed"])},
        color_label=(185, 122, 87, 255),
        fight=False,
        items=[],
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="HUT",
        pace=2,
        req=[],
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "incandescent_lava": Biome(
        color=(255, 100, 40, 255),
        description="Blazing currents flow between blackened crags, casting an intense red glow. The air trembles "
                    "with heat, and the ground hisses beneath every step.",
        color_label=(255, 100, 40, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="INCANDESCENT LAVA",
        req=[],
        pace=7,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 30,
            Months.IGNARIS.value: 55,
            Months.OUSKARA.value: 25,
            Months.NERITH.value: 20,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "island": Biome(
        color=(201, 237, 92, 255),
        description="Island rainforest, dense foliage, vibrant biodiversity, and cascading waterfalls characterize "
                    "this tropical haven of life and greenery.",
        color_label=(201, 237, 92, 255),
        fight=True,
        mobs_names=["little_slime"],
        mobs_chances=[30],
        mobs_base=MOBS,
        name="ISLAND",
        req=[],
        pace=4,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "magic_zone": Biome(
        color=(160, 75, 165, 255),
        description="Magic zone.",
        color_label=(160, 75, 165, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="MISTERIOUS MAGIC ZONE",
        req=[],
        pace=5,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "molten_surface": Biome(
        color=(210, 70, 25, 255),
        description="Rivers of glowing lava snake through scorched ground, heat distorting the air as fiery cracks "
                    "pulse with dangerous, untamed energy.",
        color_label=(210, 70, 25, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="MOLTEN SURFACE",
        req=[],
        pace=7,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 30,
            Months.IGNARIS.value: 55,
            Months.OUSKARA.value: 25,
            Months.NERITH.value: 20,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "mountains": Biome(
        color=(127, 127, 127, 255),
        description="Nothing important.",
        color_label=(127, 127, 127, 255),
        fight=False,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="MOUNTAINS",
        req=["climbing tools"],
        pace=10,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 18,
            Months.IGNARIS.value: 28,
            Months.OUSKARA.value: 12,
            Months.NERITH.value: 6,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "oasis": Biome(
        color=(0, 255, 245, 255),
        description="A tranquil haven in the desert, with cool, clear water.",
        color_label=(0, 255, 245, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="OASIS",
        pace=18,
        water=True,
        fishes=[],
        status=[PlayerStatus.SURF.value],
        month_temperatures={
            Months.AURENAR.value: 23,
            Months.IGNARIS.value: 33,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 5,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "oasis_vegetation": Biome(
        color=(47, 56, 176, 255),
        description="Lush palms and vibrant greenery surround a clear water pool, offering life and shade amid the "
                    "surrounding arid desert sands.",
        color_label=(47, 56, 176, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="OASIS",
        pace=18,
        water=False,
        fishes=[],
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 23,
            Months.IGNARIS.value: 33,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 5,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "ocean": Biome(
        color=(45, 140, 90, 255),
        description="Endless waves shimmer beneath the sun, teeming with life below the surface, where deep currents "
                    "carry secrets of the mysterious blue expanse.",
        color_label=(45, 140, 90, 255),
        fight=False,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="OCEAN",
        pace=18,
        water=True,
        fishes=["fish_sabalo", "fish_tuna", "fish_swordfish", "fish_snapper", "fish_sardine", "fish_sabalo", "fish_ray",
                "fish_mahi-mahi", "fish_mackerel", "fish_hammerhead_shark", "fish_grouper", "fish_flounder"],
        status=[PlayerStatus.SURF.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 26,
            Months.OUSKARA.value: 17,
            Months.NERITH.value: 12,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "plains": Biome(
        color=(181, 230, 29, 255),
        description="Gentle terrain, waving grasslands, and minimal elevation define this vast, open expanse of natural"
                    " simplicity and beauty.",
        color_label=(181, 230, 29, 255),
        fight=True,
        mobs_names=["giant_slime", "goblin", "slime"],
        mobs_chances=[20, 30, 30],
        mobs_base=MOBS,
        name="PLAINS",
        req=[],
        pace=6,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "plateau": Biome(
        color=(82, 249, 11, 255),
        description="Elevated plateau, expansive views, flat summits, and resilient flora characterize this "
                    "high-altitude, majestic landscape.",
        color_label=(82, 249, 11, 255),
        fight=True,
        mobs_names=["slime"],
        mobs_chances=[30],
        mobs_base=MOBS,
        name="PLATEAU",
        req=[],
        pace=6,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "reef": Biome(),

    "river": Biome(
        color=(0, 162, 232, 255),
        description="Nothing important.",
        color_label=(0, 162, 232, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="RIVER",
        req=[],
        pace=6,
        water=True,
        fishes=["fish_sabalo"],
        status=[PlayerStatus.SURF.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "rocks": Biome(
        color=(85, 80, 85, 255),
        description="Nothing important.",
        color_label=(85, 80, 85, 255),
        fight=False,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="ROCKS",
        req=["wings"],
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "rocky_desert": Biome(
        color=(175, 130, 80, 255),
        description="Jagged stones and scattered boulders dominate the harsh terrain, with dry winds sweeping through "
                    "canyons under a blazing, unforgiving sun.",
        color_label=(175, 130, 80, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="ROCKY DESERT",
        req=[],
        pace=10,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 25,
            Months.IGNARIS.value: 35,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 2,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "ruins": Biome(
        color=(202, 154, 128, 255),
        description="Crumbled towers and scorched stone lie beneath tangled vines. The land is silent, scarred by "
                    "blackened earth and warped ruins that still radiate a faint, unnatural heat.",
        color_label=(202, 154, 128, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="RUINS",
        req=[],
        pace=7,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "ruins_desert": Biome(
        color=(200, 150, 130, 255),
        description="Sand-buried walls and crumbling arches rise from the dunes, silent witnesses to a once-thriving "
                    "realm lost to time and shifting winds.",
        color_label=(200, 150, 130, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="RUINS",
        req=[],
        pace=7,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 25,
            Months.IGNARIS.value: 35,
            Months.OUSKARA.value: 10,
            Months.NERITH.value: 2,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "shrubland": Biome(
        color=(145, 140, 80, 255),
        description="Thorny bushes and hardy plants sprawl across dry, uneven ground, alive with rustling leaves, "
                    "darting creatures, and the scent of sun-warmed earth.",
        color_label=(145, 140, 80, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="SHRUBLAND",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 18,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 14,
            Months.NERITH.value: 6,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "sea": Biome(
        color=(63, 72, 204, 255),
        description="Nothing important.",
        color_label=(63, 72, 204, 255),
        fight=False,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="SEA",
        pace=10,
        water=True,
        fishes=["fish_sabalo", "fish_tuna", "fish_swordfish", "fish_snapper", "fish_sardine", "fish_sabalo", "fish_ray",
                "fish_mahi-mahi", "fish_mackerel", "fish_hammerhead_shark", "fish_grouper", "fish_flounder"],
        status=[PlayerStatus.SURF.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "seleran_forest": Biome(
        color=(15, 180, 10, 255),
        description="Time drifts slowly here—leaves hang mid-fall, whispers echo endlessly, and the air shimmers with "
                    "ancient, motionless magic frozen between moments.",
        color_label=(15, 180, 10, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="SELERAN FOREST",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "snow": Biome(
        color=(250, 250, 250, 255),
        description="Nothing important.",
        color_label=(250, 250, 250, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="SNOW",
        req=["snow clothing"],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 10,
            Months.IGNARIS.value: 15,
            Months.OUSKARA.value: 8,
            Months.NERITH.value: 2,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "snowy_forest": Biome(
        color=(220, 230, 230, 255),
        description="Tall, frost-covered pines stand silent under heavy snow. Footsteps crunch softly, and mist drifts "
                    "between the trunks in the frozen stillness.",
        color_label=(220, 230, 230, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="SNOWY FOREST",
        req=["snow clothing"],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 14,
            Months.IGNARIS.value: 18,
            Months.OUSKARA.value: 11,
            Months.NERITH.value: 3,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "snowy_mountains": Biome(
        color=(240, 250, 250, 255),
        description="Jagged peaks cloaked in white, icy winds howl through pine-covered slopes under a pale,"
                    " sunlit sky.",
        color_label=(240, 250, 250, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="SNOWY MOUNTAINS",
        req=["snow clothing"],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 16,
            Months.IGNARIS.value: 20,
            Months.OUSKARA.value: 13,
            Months.NERITH.value: 5,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "snowy_covered_steppe": Biome(
        color=(220, 220, 220, 255),
        description="Frozen grasslands stretch endlessly, blanketed in snow and silence, where only the wind and"
                    " occasional tracks hint at life enduring the cold.",
        color_label=(220, 220, 220, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="SNOW-COVERED STEPPE",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 16,
            Months.IGNARIS.value: 20,
            Months.OUSKARA.value: 13,
            Months.NERITH.value: 5,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "steppe": Biome(
        color=(165, 165, 80, 255),
        description="Endless grasslands ripple in the wind, dotted with hardy shrubs and scattered stones beneath a"
                    " wide, ever-changing sky.",
        color_label=(165, 165, 80, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="STEPPE",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 18,
            Months.IGNARIS.value: 24,
            Months.OUSKARA.value: 14,
            Months.NERITH.value: 7,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "town": Biome(
        color=(170, 105, 70, 255),
        description="Nothing important.",
        color_label=(170, 105, 70, 255),
        fight=False,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="TOWN",
        req=[],
        accessible_from=["gates", "town"],
        accessible_to=["gates", "town"],
        pace=2,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "valley": Biome(
        color=(148, 148, 148, 255),
        description="Desolate, silent valley, cracked earth stretches between imposing cliffs, where an eerie stillness"
                    " envelops the barren landscape, untouched by the whispers of wind or the rustle of life.",
        color_label=(148, 148, 148, 255),
        fight=False,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="VALLEY",
        req=[],
        pace=5,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "volcanic_mountain": Biome(
        color=(53, 53, 53, 255),
        description="Towering peak crowned with smoke and ash, its slopes scarred by ancient lava flows and"
                    " trembling with the rumble of fiery power below.",
        color_label=(53, 53, 53, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="VOLCANIC MOUNTAIN",
        req=[],
        pace=8,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 22,
            Months.IGNARIS.value: 42,
            Months.OUSKARA.value: 17,
            Months.NERITH.value: 12,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "volcanic_rock": Biome(
        color=(90, 75, 65, 255),
        description="Charred, blackened terrain of jagged lava stone and steaming fissures, where heat radiates from "
                    "the ground and few dare to tread.",
        color_label=(90, 75, 65, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="VOLCANIC ROCK",
        req=[],
        pace=5,
        status=[PlayerStatus.WALK.value],
        month_temperatures={
            Months.AURENAR.value: 25,
            Months.IGNARIS.value: 45,
            Months.OUSKARA.value: 20,
            Months.NERITH.value: 15,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "water": Biome(
        color=(128, 255, 255, 255),
        description="Quiet water.",
        color_label=(128, 255, 255, 255),
        fight=False,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="WATER",
        req=[],
        pace=6,
        water=True,
        fishes=["fish_sabalo"],
        status=[PlayerStatus.SURF.value],
        month_temperatures={
            Months.AURENAR.value: 20,
            Months.IGNARIS.value: 30,
            Months.OUSKARA.value: 15,
            Months.NERITH.value: 8,
        },
        trees_base=TREES,
        fishes_base=FISHES
    ),

    "none": Biome(
        color=(255, 0, 0, 255),
        description="Nothing important.",
        color_label=(255, 0, 0, 255),
        fight=True,
        mobs_names=[],
        mobs_chances=[],
        mobs_base=MOBS,
        name="none",
        req=[],
        status=[PlayerStatus.WALK.value],
        trees_base=TREES,
        fishes_base=FISHES
    ),
}

# Biome types.
BiomeTypes = Enum(value="BiomeType", names=list(BIOMES.keys()))
for k, v in BIOMES.items():
    v.id = BiomeTypes[k].name

# Entries.
ENTRIES = {
    "test_hut": Entry(
        description="A simple testing hut where mechanics and events are safely evaluated.",
        name="Test Hut",
        entry_type=EntryType.HUT,
        mobs_base=MOBS,
        month_temperatures={0: 0},
        items=["large_belt", "little_strength_potion"],
    ),

    "arena_antina": Entry(
        description="Arena interior, grand stands circle a sandy pit, with torches lining the walls. Echoes "
                    "of cheers and clashes fill the air.",
        name="ANTINA'S ARENA",
        entry_type=EntryType.CASTLE,
        mobs_base=MOBS,
    ),

    "artisan_shop": Entry(
        description="A workshop filled with the clanging of metal, tools neatly arranged on wooden racks, "
                    "and half-finished crafts displayed under flickering lantern light.",
        name="HAMMER & HEARTH",
        entry_type=EntryType.MARKET,
        mobs_base=MOBS,
    ),

    "castle": Entry(
        description="Majestic castle with towering spires and sturdy stone walls, adorned with banners. Its grand "
                    "gates lead to vast halls echoing with Antina’s storied history.",
        name="CASTLE SALOON",
        entry_type=EntryType.CASTLE,
        mobs_base=MOBS,
    ),

    "cave_25_24": Entry(
        description="Echoing cave, shadows stretch across damp walls, while unsettling sounds resonate from unseen"
                    " depths, hinting at hidden creatures lurking within the dark.",
        name="CAVE ENTRANCE",
        hide={"visibility": False, "finding_chance": 0.80},
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True,
        mobs_names=["goblin"],
        mobs_chances=[40],
        req=["torch"]),

    "cave_39_43": Entry(
        description="...",
        name="CAVE ENTRANCE",
        hide={"visibility": False, "finding_chance": 0.60},
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True,
        mobs_names=["slime"],
        mobs_chances=[80],
        req=["torch"]),

    "sub_cave_1_0": Entry(
        description="Cave pit, jagged walls descend into darkness, littered with bones and crude markings. The air is"
                    " thick with the stench of decay and faint goblin whispers.",
        name="CAVE PIT",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True,
        mobs_names=["goblin"],
        mobs_chances=[40]),

    "sub_cave_1_1": Entry(
        description="Goblin lookout hole, roughly dug with narrow slits for spying, scattered with makeshift weapons."
                    " Flickering torchlight reveals grimy walls and vigilant goblin eyes peering into the shadows.",
        name="GOBLIN LOOKOUT HOLE",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True,
        mobs_names=["watchful_goblin", "goblin_war"],
        mobs_chances=[90, 30]),

    "sub_cave_1_2": Entry(
        description="Crude racks hold jagged weapons, rusted blades, and splintered shields. The walls bear scratch "
                    "marks, and a foul smell lingers amid the chaotic stash.",
        name="GOBLIN'S ARMORY CAVE",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True,
        mobs_names=["goblin", "goblin_war"],
        mobs_chances=[30, 60]),

    "sub_cave_2_0": Entry(
        description="Basin, murky, foul-smelling pool at the pit's depths, filled with discarded scraps, broken bones,"
                    " and refuse. A grimy layer coats the stagnant surface, emitting a nauseating stench.",
        name="CAVE BASIN",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=False),

    "sub_cave_2_1": Entry(
        description="Goblin chief's cave, dark and cluttered, adorned with stolen trinkets and crude trophies. A "
                    "makeshift throne sits in the center, surrounded by flickering torches.",
        name="CHIEF'S CAVE",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True),

    "sub_cave_2_2": Entry(
        description="Goblin chief's bedroom, dimly lit by flickering torches, the room is strewn with riches and "
                    "treasures. Shackled prisoners lie in the shadows, while the chief’s bed, made of rough furs, "
                    "dominates the chaotic space.",
        name="GOBLIN CHIEF'S BEDROOM",
        id="goblin_chief_bedroom",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=False),

    "sub_cave_2_3": Entry(
        description="Cave passage, narrow and winding, with jagged walls and low ceilings. The air is damp, filled "
                    "with the faint sound of scurrying feet and the occasional echo of distant growls.",
        name="CAVE PASSAGEWAY ENTRANCE",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True,
        mobs_names=["goblin", "goblin_war"],
        mobs_chances=[60, 20]),

    "sub_cave_2_4": Entry(
        description="Goblin cave cage chamber, rows of rusted iron cages line the damp stone walls, holding captives "
                    "in grim silence. The air is thick with tension, and the faint clinking of chains echoes "
                    "throughout.",
        name="CAGE CHAMBER",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True,
        mobs_names=["goblin", "goblin_war"],
        mobs_chances=[60, 20]),

    "sub_cave_3_0": Entry(
        description="Towering stalactites hang from the ceiling, casting eerie shadows in the dim light. The damp air"
                    " drips steadily, creating a haunting, rhythmic echo throughout the chamber.",
        name="CAVE GALLERY",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True,
        mobs_names=["goblin", "goblin_war"],
        mobs_chances=[60, 20]),

    "sub_cave_3_1": Entry(
        description="Cave passage, narrow and winding, with jagged walls and low ceilings. The air is damp, filled "
                    "with the faint sound of scurrying feet and the occasional echo of distant growls.",
        name="CAVE PASSAGEWAY EXIT",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True,
        mobs_names=["goblin", "goblin_war"],
        mobs_chances=[50, 50]),

    "sub_cave_3_2": Entry(
        description="Crude stone tables scattered with scraps of half-eaten food and cracked bones. The air is "
                    "thick with the smell of rancid meat, and discarded remnants litter the grimy floor.",
        name="GOBLIN DINING GALLERY",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        fight=True,
        mobs_names=["goblin", "goblin_war"],
        mobs_chances=[70, 70]),

    "sub_cave_4_0": Entry(
        description="Unused goblin cave chimney. A narrow, soot-stained shaft reaching upward, clogged with debris "
                    "and cobwebs. Cold drafts whistle through, hinting at an abandoned escape route to the surface.",
        name="CHIMNEY CAVE",
        entry_type=EntryType.CAVE,
        mobs_base=MOBS,
        hide={"visibility": False, "finding_chance": 0.9}),

    "house_antina_gareth": Entry(
        description="Warm and inviting, the house features wooden beams, a stone hearth, neatly arranged furniture, "
                    "and shelves lined with books and trinkets from city markets.",
        name="GARETH'S MID HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_antina_aric": Entry(
        description="Spacious home with elegant furniture, a grand chandelier, and shelves filled with books and "
                    "ornaments reflecting wealth and sophistication.",
        name="LORD ARIC'S HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_antina_edrion": Entry(
        description="Luxurious house with velvet drapes, polished floors, and a cabinet displaying rare artifacts "
                    "collected from distant lands.",
        name="LORD EDRION'S HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_antina_edrion_room": Entry(
        description="Luxurious house with velvet drapes, polished floors, and a cabinet displaying rare artifacts "
                    "collected from distant lands.",
        name="LORD EDRION'S HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_antina_white": Entry(
        description="Modest dwelling with neatly arranged furniture, a small hearth, and colorful tapestries adding "
                    "a touch of warmth to the stone walls.",
        name="WHITE HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_antina_family": Entry(
        description="Bustling household with a large dining table, scattered toys, and a lively, lived-in "
                    "atmosphere beneath high wooden beams.",
        name="FAMILY HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_antina_small": Entry(
        description="Quiet home with a simple bed, a writing desk, and potted plants by the window overlooking "
                    "the bustling city streets.",
        name="SMALL HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_aquiri_marlin": Entry(
        description="Weathered wooden hut with fishing nets hanging by the door, a small table inside, and the scent "
                    "of fresh-caught fish lingering.",
        name="MARLIN'S HUT",
        entry_type=EntryType.HUT,
        mobs_base=MOBS
    ),

    "house_aquiri_normal": Entry(
        description="Cozy seaside home with a thatched roof, seashell wind chimes on the porch, and a hammock "
                    "swaying gently in the ocean breeze.",
        name="COAST HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_aquiri_stone": Entry(
        description="Simple stone cottage with a driftwood door, a warm hearth, and sand-dusted floors, reflecting "
                    "the close bond between life and the sea.",
        name="STONE COAST HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_epiiat_mayor": Entry(
        description="A spacious room with a sturdy oak desk, shelves of documents, and an ornate rug covering the "
                    "polished wooden floor.",
        name="MAYOR'S HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_epiiat_small": Entry(
        description="Small house with a modest hearth, a wooden bench, and handmade decorations adorning the walls, "
                    "reflecting the owner's humble but creative spirit.",
        name="SMALL HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_epiiat_normal": Entry(
        description="Cozy home with a simple table, a woven rug, and dried herbs hanging from the ceiling beams, "
                    "filling the air with an earthy scent.",
        name="HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "house_epiiat_wooden": Entry(
        description="Compact dwelling with a single bed, a chest for belongings, and a faint aroma of baked goods "
                    "lingering from the small corner kitchen.",
        name="WOODEN HOUSE",
        entry_type=EntryType.HOUSE,
        mobs_base=MOBS
    ),

    "hut_12_24_lobby": Entry(
        name="NYNAEVE'S HUT",
        description="A humble living and dining space where a wooden table, scattered utensils, and soft lantern "
                    "light create a warm island welcome.",
        entry_type=EntryType.HUT,
        mobs_base=MOBS
    ),

    "hut_12_24_nynaeve_room": Entry(
        name="NYNAEVE'S ROOM",
        description="A warm, tidy chamber filled with herbal scents; shelves brim with vials,"
                    " cloths, and worn journals.",
        items=["bed"],
        entry_type=EntryType.HUT,
        mobs_base=MOBS
    ),

    "hut_12_24_son_room": Entry(
        name="LITTLE ROOM",
        description="A cozy room adorned with a bed, a table, two chairs, and a window, "
                    "invites serenity amid nature's whispers.",
        items=["old_book", "short_sword", "travelers_belt", "bed"],
        entry_type=EntryType.HUT,
        mobs_base=MOBS
    ),

    "hut_13_47": Entry(
        description="Interior of isolated refuge, dimly lit, flickering candles cast dancing shadows "
                    "on weathered walls. Tattered maps and makeshift barricades hint at cautious attempts"
                    " to secure the uncertain safety within.",
        items=["bed"],
        entry_type=EntryType.HUT,
        mobs_base=MOBS
    ),

    "hut_34_25": Entry(
        description="Abandoned woodland hut, dilapidated and forgotten, this rustic abode near the "
                    "forest stands as a silent witness to nature's reclamation.",
        items=["bed", "rusty_sword"],
        name="ABANDONED HUT",
        entry_type=EntryType.HUT,
        mobs_base=MOBS
    ),

    "hut_34_51": Entry(
        description="Seaside hut, weathered wood and a thatched roof, filled with fishing gear and seashells."
                    " The salty breeze drifts through, mingling with the scent of dried fish.",
        items=["bed", "harpoon"],
        name="BRANN'S SEASIDE HUT",
        entry_type=EntryType.HUT,
        mobs_base=MOBS
    ),

    "hut_39_38_1": Entry(
        description="Seaside hut, weathered wood and a thatched roof, filled with fishing gear and seashells."
                    " The salty breeze drifts through, mingling with the scent of dried fish.",
        items=["bed", "harpoon", "fish_tuna", "fish_tuna", "bread"],
        name="MARLIN'S HUT",
        entry_type=EntryType.HUT,
        mobs_base=MOBS
    ),

    "hut_39_38_2": Entry(
        description="Seaside hut, weathered wood and a thatched roof, filled with fishing gear and seashells."
                    " The salty breeze drifts through, mingling with the scent of dried fish.",
        items=["bed", "fish_tuna", "fish_sardine", "fish_ray"],
        name="HUT",
        entry_type=EntryType.HUT,
        mobs_base=MOBS
    ),

    "aliras_inn": Entry(
        description="Warm and inviting, the inn’s interior features polished wooden beams, a roaring hearth, and "
                    "a bustling common room filled with travelers sharing tales over hearty meals.",
        name="ALIRA'S INN",
        entry_type=EntryType.INN,
        mobs_base=MOBS
    ),

    "aliras_first_room": Entry(
        description="A luxurious suite with velvet curtains, a canopy bed, and a private fireplace, exuding comfort "
                    "and refinement.",
        items=["bed"],
        name="ALIRA'S FIRST ROOM",
        req=["aliras_first_room_key"],
        entry_type=EntryType.ROOM,
        mobs_base=MOBS
    ),

    "aliras_second_room": Entry(
        description="A cozy room with a soft feather bed, a small writing desk, and a balcony overlooking the "
                    "bustling streets.",
        items=["bed"],
        name="ALIRA'S SECOND ROOM",
        req=["aliras_second_room_key"],
        entry_type=EntryType.ROOM,
        mobs_base=MOBS
    ),

    "aliras_third_room": Entry(
        description="A modest room with twin beds, a faded rug, and an old map of the city pinned to the wall.",
        items=["bed", "bed"],
        name="ALIRA'S THIRD ROOM",
        req=["aliras_third_room_key"],
        entry_type=EntryType.ROOM,
        mobs_base=MOBS
    ),

    "aliras_fourth_room": Entry(
        description="A basic but clean room with a single bed, a sturdy chest for belongings, and a small window "
                    "letting in morning light.",
        items=["bed", "bed"],
        name="ALIRA'S FOURTH ROOM",
        req=["aliras_fourth_room_key"],
        entry_type=EntryType.ROOM,
        mobs_base=MOBS
    ),

    "lyssias_inn": Entry(
        description="Coastal inn with weathered stone walls and a thatched roof, offering warm meals, cozy rooms, "
                    "and ocean views through salt-crusted windows.",
        name="LYSSIA'S INN",
        entry_type=EntryType.INN,
        mobs_base=MOBS
    ),

    "lyssias_first_room": Entry(
        description="A cozy room with a worn armchair by the fireplace, seashells arranged on the windowsill, "
                    "and soft candlelight flickering across the walls.",
        items=["bed"],
        name="LYSSIA'S FIRST ROOM",
        req=["lyssias_first_room_key"],
        entry_type=EntryType.ROOM,
        mobs_base=MOBS
    ),

    "lyssias_second_room": Entry(
        description="Simple room with a sturdy wooden bed, a small desk, and an open window letting in the scent"
                    " of the sea.",
        items=["bed"],
        name="LYSSIA'S SECOND ROOM",
        req=["lyssias_second_room_key"],
        entry_type=EntryType.ROOM,
        mobs_base=MOBS
    ),

    "lyssias_third_room": Entry(
        description="A spacious room with twin beds, a nautical map pinned to the wall, and a large chest at the "
                    "foot of each bed.",
        items=["bed", "bed"],
        name="LYSSIA'S THIRD ROOM",
        req=["lyssias_third_room_key"],
        entry_type=EntryType.ROOM,
        mobs_base=MOBS
    ),

    "mirabelles_inn": Entry(
        description="Warm hearth, wooden beams, and cozy furnishings create a welcoming "
                    "atmosphere. Aromas of home-cooked meals linger, inviting weary travelers to "
                    "find respite.",
        name="MIRABELLE'S INN",
        npcs=["innkeeper_mirabelle"],
        entry_type=EntryType.INN,
        mobs_base=MOBS
    ),

    "mirabelles_main_room": Entry(
        description="In the main chamber of the inn, a comfortable bed awaits amidst the charming ambiance of "
                    "a warm hearth, rustic wooden beams, and snug furnishings.",
        items=["bed"],
        name="MIRABELLE'S INN MAIN ROOM",
        req=["mirabelles_main_room_key"],
        entry_type=EntryType.ROOM,
        mobs_base=MOBS
    ),

    "mirabelles_small_room": Entry(
        description="In the main chamber of the inn, a comfortable bed awaits amidst the charming ambiance of "
                    "a warm hearth, rustic wooden beams, and snug furnishings.",
        items=["bed"],
        name="MIRABELLE'S INN SMALL ROOM",
        req=["mirabelles_small_room_key"],
        entry_type=EntryType.ROOM,
        mobs_base=MOBS
    ),

    "potion_shop_antina": Entry(
        description="Shelves brimming with glowing bottles, dried herbs hanging from beams, and a bubbling cauldron "
                    "in the corner adding to the mystical ambiance.",
        name="MYSTIC VIALS",
        entry_type=EntryType.POTION_SHOP,
        mobs_base=MOBS
    ),

    "temple_antina": Entry(
        description="Sunlit through stained glass, the temple's marble floors glisten. Golden icons and flickering "
                    "candles evoke a serene, divine atmosphere.",
        name="SANTUARY OF THE RADIANT FLAME",
        mobs_base=MOBS
    ),

    "temple_epiiat": Entry(
        description="Simple stone temple with wooden pews, a central altar adorned with fresh flowers, and sunlight "
                    "streaming through plain but graceful stained-glass windows.",
        name="TEMPLE",
        mobs_base=MOBS
    ),

    "the_golden_tankard_tavern": Entry(
        description="Bustling with laughter and music, this lively tavern features polished oak tables, a "
                    "roaring hearth, and the finest ale in Antina.",
        name="THE GOLDEN TANKARD TAVERN",
        npcs=["tavern_keeper_rudrik"],
        entry_type=EntryType.TAVERN,
        mobs_base=MOBS
    ),

    "thornes_ship": Entry(
        description="Weathered wood glistens with sea spray, ropes coil neatly, and seagulls circle overhead as the "
                    "harbor hums with maritime activity.",
        name="CAPTAIN THORNE'S SHIP",
        items=["powder_keg"],
        entry_type=EntryType.SHIP,
        mobs_base=MOBS
    ),

    "tower_of_eldra_floor_1": Entry(
        description="Simple bed beside a small desk, lit by a dim lantern. Personal belongings and handwritten"
                    "notes lie scattered across a worn rug.",
        items=["bed", "telescope", "notes"],
        name="TOWER OF ELDRA FIRST FLOOR",
        entry_type=EntryType.TOWER,
        mobs_base=MOBS
    ),

    "tower_of_eldra_floor_2": Entry(
        description="Shelves packed with star charts and ancient tomes. A brass telescope points skyward, surrounded"
                    " by scattered scrolls and glowing crystal orbs.",
        items=["giant_telescope"],
        name="TOWER OF ELDRA SECOND FLOOR",
        entry_type=EntryType.TOWER,
        mobs_base=MOBS,
        draw_map=True
    ),

    "tower_of_karun_floor_1": Entry(
        description="Simple ground floor, with a modest bed, scattered maps, and a warm hearth where the astronomer "
                    "rests after long nights.",
        name="TOWER OF KARUN FIRST FLOOR",
        entry_type=EntryType.TOWER,
        mobs_base=MOBS
    ),

    "tower_of_karun_floor_2": Entry(
        description="Upper floor filled with star charts and celestial books, a large telescope pointing toward "
                    "the heavens, and intricate brass instruments for stargazing.",
        name="TOWER OF KARUN SECOND FLOOR",
        entry_type=EntryType.TOWER,
        mobs_base=MOBS,
        draw_map=True
    )
}

# Mob types.
MobTypes = Enum(value="MobType", names=list(MOBS.keys()))
for k, v in MOBS.items():
    v.id = MobTypes[k].value
