"""
Unit superclass, each combat unit should inherit from this, see `reapers.py` for example
We can also add reusable methods here that multiple unit types could use
"""
import math
from abc import ABC, abstractmethod

import numpy as np
from bot.combat.turn_rate import TURN_RATE
from bot.pathing import Pathing
from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units


class BaseUnit(ABC):
    def __init__(self, ai: BotAI, pathing: Pathing):
        self.ai: BotAI = ai
        self.pathing: Pathing = pathing

    @abstractmethod
    def handle_attackers(self, units: Units, attack_target: Point2) -> None:
        # implement in subclass
        pass

    def attack_ready(self, unit: Unit, target: Unit) -> bool:
        """
        Determine whether the unit can attack the target by the time the unit faces the target.
        Thanks Sasha for her original example code.
        """
        # Time elapsed per game step
        step_time = self.ai.client.game_step / 22.4

        # Time it will take for unit to turn to face target
        angle = self._angle_diff(
            unit.facing, self._angle_to(unit.position, target.position)
        )
        turn_time = angle / self._get_turn_speed(unit)

        # Time it will take for unit to move in range of target
        distance = (
            unit.position.distance_to(target)
            - unit.radius
            - target.radius
            - self._range_vs_target(unit, target)
        )
        distance = max(0, distance)
        move_time = distance / (unit.real_speed * 1.4)

        return step_time + turn_time + move_time >= unit.weapon_cooldown / 22.4

    def move_to_safety(self, unit: Unit, grid: np.ndarray):
        """
        Find a close safe spot on our grid
        Then path to it
        """
        safe_spot: Point2 = self.pathing.find_closest_safe_spot(unit.position, grid)
        move_to: Point2 = self.pathing.find_path_next_point(
            unit.position, safe_spot, grid
        )
        unit.move(move_to)

    @staticmethod
    def pick_enemy_target(enemies: Units) -> Unit:
        """For best enemy target from the provided enemies
        TODO: If there are multiple units that can be killed in one shot, pick the highest value one
        """
        return min(
            enemies,
            key=lambda e: (e.health + e.shield, e.tag),
        )

    @staticmethod
    def _angle_to(from_pos: Point2, to_pos: Point2) -> float:
        """Angle from point to other point in radians"""
        return math.atan2(to_pos.y - from_pos.y, to_pos.x - to_pos.x)

    @staticmethod
    def _angle_diff(a, b) -> float:
        """Absolute angle difference between 2 angles"""
        if a < 0:
            a += math.pi * 2
        if b < 0:
            b += math.pi * 2
        return math.fabs(a - b)

    @staticmethod
    def _get_turn_speed(unit: Unit) -> float:
        """Returns turn speed of unit in radians"""
        if unit.type_id in TURN_RATE:
            return TURN_RATE[unit.type_id] * 1.4 * math.pi / 180

    @staticmethod
    def _range_vs_target(unit, target) -> float:
        """Get the range of a unit to a target."""
        if unit.can_attack_air and target.is_flying:
            return unit.air_range
        else:
            return unit.ground_range
