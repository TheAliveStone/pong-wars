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
        self.elapsed_time = 0.0

    def decide(self, paddle, ball, dt, game_state=None):
        """AI algorithm that decides which direction to travel in based on ball position."""
        # Starts a timer. Paddle doesn't move until reaction time
        self.elapsed_time += dt
        if self.elapsed_time < self.reaction_time:
            return 0
        self.elapsed_time = 0
        
        # Calculate ball position and distance
        target_y = ball.pos.y + random.uniform(-self.inaccuracy, self.inaccuracy) * paddle.rect.height
        delta = target_y - paddle.pos.y
        # If too close, don't move to reduce jittering
        if abs(delta) < 5:
            return 0
        
        # Returns the paddles direction
        if delta < 0:
            return -1
        elif delta > 0:
            return 1



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
        self.elapsed_time = 0.0

    def _predict_landing_y_no_bounces(self, paddle_x, ball):
        """
        Calculates the time for the ball to reach the paddle and returns the y position of the ball when it reaches it
        """
        if ball.direction.x == 0:
            return ball.pos.y
        time_to_reach = (paddle_x - ball.pos.x) / (ball.direction.x * ball.speed)
        if time_to_reach < 0:
            # Ball is moving away from paddle; return current Y or handle gracefully
            return ball.pos.y
        time_to_reach = min(time_to_reach, self.prediction_horizon_limit)
        predicted_y = ball.pos.y + (ball.direction.y * ball.speed * time_to_reach)
        return predicted_y


    def decide(self, paddle, ball, dt, game_state=None):
        """
        AI algorithm that decides which direction to travel in based on ball position.
        """
        # Starts a timer. Paddle doesn't move until reaction time
        self.elapsed_time += dt
        if self.elapsed_time < self.reaction_time:
            return 0
        self.elapsed_time = 0
        
        # Calculate ball position and distance
        predicted_y = self._predict_landing_y_no_bounces(paddle.pos.x, ball)
        predicted_y += random.uniform(-self.inaccuracy, self.inaccuracy) * paddle.rect.height
        delta = predicted_y - paddle.pos.y
        # If too close, don't move to reduce jittering
        if abs(delta) < 5:
            return 0
        
        # Returns the paddles direction
        if delta < 0:
            return -1
        elif delta > 0:
            return 1


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
        self.elapsed_time = 0.0

    def _simulate_to_paddle_x(self, paddle_x, ball):
        """
        Simulate ball trajectory including top/bottom wall reflections.
        Returns the estimated Y position when ball reaches paddle_x.
        """
        pos_x = ball.pos.x
        pos_y = ball.pos.y
        dir_x = ball.direction.x
        dir_y = ball.direction.y
        
        for i in range(self.max_simulation_steps):
            if dir_x == 0:
                return pos_y # Ball moving vertically only, can't reach paddle_x
            time_to_paddle_x = (paddle_x - pos_x) / (dir_x * ball.speed) 
            if time_to_paddle_x >= 0: 
                # Compute where the ball would be in Y when it reaches paddle_x
                y_at_paddle = pos_y + (dir_y * ball.speed * time_to_paddle_x)
                if 0 <= y_at_paddle <= WINDOW_HEIGHT:
                    return y_at_paddle # Ball reaches paddle_x without hitting wall
                else:
                    # Ball will hit wall before reaching paddle_x
                    time_to_wall = None
                    if dir_y > 0:
                        # Time until hitting bottom wall
                        time_to_wall = (WINDOW_HEIGHT - pos_y) / (dir_y * ball.speed)
                    elif dir_y < 0:
                        # Time until hitting top wall
                        time_to_wall = -pos_y / (dir_y * ball.speed)
                    else:
                        # dir_y == 0 means ball is moving horizontally, so it won't hit walls
                        return pos_y  # No vertical movement 
                    pos_x += dir_x * ball.speed * time_to_wall # Move to wall collision point
                    pos_y += dir_y * ball.speed * time_to_wall # Move to wall collision point
                    pos_y = max(0, min(WINDOW_HEIGHT, pos_y))  # Clamp
                    dir_y = -dir_y  # Reflect
            else:
                # Ball is moving away from paddle_x; we can either return current pos_y or handle bounce-back logic
                 return pos_y
        return pos_y  # Fallback if max_simulation_steps exhausted

    def decide(self, paddle, ball, dt, game_state=None):
        """
        Return vertical movement intent using advanced ball trajectory prediction.
        AI algorithm that decides which direction to travel in based on ball position.
        """
        # Starts a timer. Paddle doesn't move until reaction time
        self.elapsed_time += dt
        if self.elapsed_time < self.reaction_time:
            return 0
        self.elapsed_time = 0
        
        # Calculate ball position and distance
        predicted_y = self._simulate_to_paddle_x(paddle.pos.x, ball)
        predicted_y += random.uniform(-self.inaccuracy, self.inaccuracy) * paddle.rect.height
        delta = predicted_y - paddle.pos.y
        # If too close, don't move to reduce jittering
        if abs(delta) < 5:
            return 0
        
        # Returns the paddles direction
        if delta < 0:
            return -1
        elif delta > 0:
            return 1