"""
AI Strategy classes for Pong game.
Each AI class implements a decide() method that returns a vertical movement intent (-1, 0, +1).
Designed as separate strategies for educational clarity and NEA justification.
"""

import random
from settings import WINDOW_WIDTH, WINDOW_HEIGHT


class EasyAI:
    """
    Simple rule-based AI with reaction delay and noise.
    Suitable for beginner-level opponent.
    """

    def __init__(self, reaction_time=0.25, max_speed_factor=0.6, inaccuracy=0.2):
        """
        Args:
            reaction_time: Delay (seconds) before reacting to ball movement.
            max_speed_factor: Fraction of paddle's max speed to use (0.0 to 1.0).
                             Helps simulate slower, less capable opponent.
            inaccuracy: Noise magnitude applied to target Y position.
                       Larger values = more missed shots. Range: 0.0 (perfect) to ~0.5
        """
        self.reaction_time = reaction_time
        self.max_speed_factor = max_speed_factor
        self.inaccuracy = inaccuracy
        self.elapsed_time = 0.0

    def reset(self):
        """Reset internal state (e.g., reaction timer)."""
        # TODO: Reset elapsed_time to 0 so next frame AI reacts fresh
        pass

    def decide(self, paddle, ball, dt, game_state=None):
        """
        Return vertical movement intent: -1 (up), 0 (idle), +1 (down).

        PSEUDOCODE:
        1. Accumulate elapsed_time += dt
        2. If elapsed_time < reaction_time: return 0  # Simulate delayed reaction
        3. Reset elapsed_time to 0 (or small overshoot) for next cycle
        4. Compute noisy target Y:
           target_y = ball.pos.y + random.uniform(-inaccuracy, inaccuracy) * paddle.rect.height
        5. Compute delta = target_y - paddle.pos.y
        6. If abs(delta) < small deadzone (e.g., 5 pixels): return 0  # Stop jittering
        7. Determine direction based on sign(delta):
           if delta < 0: desired_direction = -1
           elif delta > 0: desired_direction = +1
           else: desired_direction = 0
        8. Return desired_direction

        Args:
            paddle: Paddle instance (has .pos.y, .rect.height, .speed)
            ball: Ball instance (has .pos.y)
            dt: Delta time (seconds) since last frame
            game_state: Optional dict with game context (unused in EasyAI)

        Returns:
            int: -1, 0, or +1
        """
        # TODO: Implement reaction delay accumulation
        # TODO: Apply noise to target position
        # TODO: Compute delta and return direction intent
        pass


class MediumAI:
    """
    Predictive AI that estimates ball landing Y without considering wall bounces.
    Includes human-like reaction delay and modest inaccuracy.
    Good balance for NEA: simple prediction logic but noticeably smarter than EasyAI.
    """

    def __init__(self, reaction_time=0.15, prediction_horizon_limit=5.0, inaccuracy=0.08):
        """
        Args:
            reaction_time: Delay before reacting (seconds).
            prediction_horizon_limit: Max time window (seconds) to look ahead.
                                     Prevents wild predictions if ball is slow/far away.
            inaccuracy: Small noise added to predicted Y to avoid perfect play.
        """
        self.reaction_time = reaction_time
        self.prediction_horizon_limit = prediction_horizon_limit
        self.inaccuracy = inaccuracy
        self.elapsed_time = 0.0

    def reset(self):
        """Reset internal state."""
        # TODO: Reset elapsed_time
        pass

    def _predict_landing_y_no_bounces(self, paddle_x, ball):
        """
        Estimate Y position of ball when it reaches paddle_x (horizontally).
        Does NOT account for top/bottom wall reflections (unlike HardAI).

        PSEUDOCODE:
        1. If ball.direction.x == 0: return ball.pos.y  # No horizontal movement; can't predict
        2. Compute time_to_reach = (paddle_x - ball.pos.x) / (ball.direction.x * ball.speed)
           - If time_to_reach < 0: ball is moving away; return current ball.pos.y or handle gracefully
        3. Clamp time_to_reach to [0, self.prediction_horizon_limit]
        4. Estimate: predicted_y = ball.pos.y + (ball.direction.y * ball.speed * time_to_reach)
        5. Return predicted_y (may be outside [0, WINDOW_HEIGHT]; that's OK for this simple version)

        Args:
            paddle_x: X coordinate of paddle (center)
            ball: Ball instance

        Returns:
            float: Predicted Y position
        """
        # TODO: Compute time until ball reaches paddle_x
        # TODO: Estimate landing Y using linear extrapolation (no bounces)
        pass

    def decide(self, paddle, ball, dt, game_state=None):
        """
        Return vertical movement intent based on predicted landing position.

        PSEUDOCODE:
        1. Accumulate elapsed_time += dt
        2. If elapsed_time < reaction_time: return 0
        3. Reset elapsed_time
        4. Call predicted_y = self._predict_landing_y_no_bounces(paddle.pos.x, ball)
        5. Add small noise: predicted_y += random.uniform(-inaccuracy, inaccuracy) * paddle.rect.height
        6. Compute delta = predicted_y - paddle.pos.y
        7. If abs(delta) < deadzone: return 0
        8. Return sign(delta) as direction

        Args:
            paddle: Paddle instance
            ball: Ball instance
            dt: Delta time (seconds)
            game_state: Optional context

        Returns:
            int: -1, 0, or +1
        """
        # TODO: Implement reaction delay
        # TODO: Predict landing Y (linear, no wall bounces)
        # TODO: Add noise and return direction
        pass


class HardAI:
    """
    Advanced predictive AI that includes top/bottom wall reflections.
    Simulates ball trajectory step-by-step, bouncing at walls, until ball reaches paddle X.
    Demonstrates geometric reflection logic suitable for advanced NEA.
    """

    def __init__(self, reaction_time=0.08, inaccuracy=0.02, max_simulation_steps=1000):
        """
        Args:
            reaction_time: Very small delay (AI is nearly instant).
            inaccuracy: Tiny noise (AI is nearly perfect).
            max_simulation_steps: Safety limit to prevent infinite loops during simulation.
        """
        self.reaction_time = reaction_time
        self.inaccuracy = inaccuracy
        self.max_simulation_steps = max_simulation_steps
        self.elapsed_time = 0.0

    def reset(self):
        """Reset internal state."""
        # TODO: Reset elapsed_time
        pass

    def _simulate_to_paddle_x(self, paddle_x, ball):
        """
        Simulate ball trajectory including top/bottom wall reflections.
        Returns the estimated Y position when ball reaches paddle_x.

        PSEUDOCODE (high level):
        1. Copy ball's current state: pos_x, pos_y, dir_x, dir_y; use ball.speed
        2. Loop (i = 0; i < max_simulation_steps; i++):
            a. If dir_x == 0: return pos_y  # Ball moving purely vertically; can't reach paddle_x
            b. Compute time_to_paddle_x = (paddle_x - pos_x) / (dir_x * ball.speed)
            c. If time_to_paddle_x >= 0:
               - Compute y_at_paddle = pos_y + (dir_y * ball.speed * time_to_paddle_x)
               - Check if y_at_paddle stays within [0, WINDOW_HEIGHT]:
                   * Yes: return y_at_paddle  # SUCCESS
                   * No: Ball will hit top/bottom before reaching paddle
            d. If ball will hit wall before paddle_x:
               - Compute time_to_wall = time until pos_y hits 0 or WINDOW_HEIGHT
               - Move ball forward: pos_x += dir_x * ball.speed * time_to_wall
               -                   pos_y += dir_y * ball.speed * time_to_wall
               - Clamp pos_y to [0, WINDOW_HEIGHT] (wall collision)
               - Reflect: dir_y = -dir_y
               - Continue loop (process next segment)
            e. Else (ball moving away from paddle_x):
               - return pos_y or handle bounce-back logic
        3. Fallback: return pos_y if loop exhausted without reaching paddle

        This logic requires careful handling of edge cases:
        - Ball speed may be 0 (avoid division by zero)
        - Multiple wall bounces may occur
        - time_to_wall calculation must account for current direction

        Args:
            paddle_x: X coordinate of target paddle
            ball: Ball instance

        Returns:
            float: Estimated Y position when ball reaches paddle_x (with bounces)
        """
        # TODO: Implement step-by-step ball trajectory simulation
        # TODO: Handle wall reflections (flip dir_y when hitting top/bottom)
        # TODO: Return predicted Y when ball reaches paddle_x
        pass

    def decide(self, paddle, ball, dt, game_state=None):
        """
        Return vertical movement intent using advanced ball trajectory prediction.

        PSEUDOCODE:
        1. Accumulate elapsed_time += dt
        2. If elapsed_time < reaction_time: return 0
        3. Reset elapsed_time
        4. Call predicted_y = self._simulate_to_paddle_x(paddle.pos.x, ball)
        5. Add tiny noise: predicted_y += random.uniform(-inaccuracy, inaccuracy) * 10
        6. Compute delta = predicted_y - paddle.pos.y
        7. If abs(delta) < small deadzone: return 0
        8. Return sign(delta)

        Args:
            paddle: Paddle instance
            ball: Ball instance
            dt: Delta time (seconds)
            game_state: Optional context

        Returns:
            int: -1, 0, or +1
        """
        # TODO: Implement reaction delay
        # TODO: Simulate ball path including wall bounces
        # TODO: Add minimal noise and return direction
        pass