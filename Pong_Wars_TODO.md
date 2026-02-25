# Pong Wars — What To Do

---

## STEP 1 — Wire ai.py into Paddle

In `Paddle.__init__`, based on the difficulty string, create an instance of EasyAI, MediumAI, or HardAI and store it as `self.ai`.

In `Paddle.ai_move()`, replace the current logic with a call to `self.ai.decide(paddle=self, ball=self.ball, dt=dt)` and assign the returned value to `self.direction.y`.

---

## STEP 2 — Implement EasyAI.decide()

- Accumulate `self.elapsed_time += dt`
- If it hasn't reached `self.reaction_time`, return 0
- Reset `self.elapsed_time`
- Add random noise to `ball.pos.y` to get a noisy target Y
- If the difference between target Y and paddle Y is tiny (< 5px), return 0
- Otherwise return −1 or +1 depending on which direction the paddle needs to move

Also fill in `reset()` so it sets `self.elapsed_time = 0`.

---

## STEP 3 — Implement MediumAI

Fill in `_predict_landing_y_no_bounces()`:
- If `ball.direction.x` is 0, return `ball.pos.y`
- Compute time for ball to reach `paddle_x` horizontally: `(paddle_x - ball.pos.x) / (ball.direction.x * ball.speed)`
- If that time is negative, return `ball.pos.y` (ball is moving away)
- Clamp the time to `self.prediction_horizon_limit`
- Return `ball.pos.y + (ball.direction.y * ball.speed * time)`

Then fill in `decide()` using the same reaction delay pattern as EasyAI, calling `_predict_landing_y_no_bounces()` and adding small noise before computing direction.

Also fill in `reset()`.

---

## STEP 4 — Implement HardAI

Fill in `_simulate_to_paddle_x()`:
- Copy the ball's current position and direction into local simulation variables
- Loop up to `max_simulation_steps`:
  - If horizontal direction is 0, return current simulated Y
  - Compute how long until ball reaches `paddle_x`
  - Compute where Y would be at that time
  - If that Y is within the window (0 to WINDOW_HEIGHT), return it — done
  - Otherwise, compute how long until the ball hits a wall (top or bottom)
  - Advance the simulated position to that wall
  - Flip the vertical direction (reflect)
  - Continue the loop
- If the loop ends without a result, return current simulated Y as fallback

Then fill in `decide()` using the same reaction delay pattern, calling `_simulate_to_paddle_x()` with minimal noise.

Also fill in `reset()`.

---

## STEP 5 — Call reset() Between Rounds

Wherever a new game starts (after a point is scored or a new Game is created), call `reset()` on the AI instance so the reaction timer doesn't carry over.

---

## STEP 6 — Test Each Difficulty

Play several games on each difficulty. Check:
- Easy loses to you most of the time
- Normal is competitive
- Hard is very hard to beat
- The AI never freezes or moves erratically
- Scoring, win condition (first to 10), and menus all still work

Adjust values in `DIFFICULTY_PRESETS` in `settings.py` if any difficulty feels wrong.

---

## STEP 7 — Fix the Scoreboard Redundancy (Optional but Worth Mentioning)

`Ball` tracks `playerScore` and `opponentScore` internally *and* updates `Scoreboard`. This is duplicate data. You don't need to fix it, but mention it in your evaluation as a design weakness you identified.

---

## STEP 8 — Write Up

- **Analysis:** Describe the problem, the three AI behaviours, and your architecture decisions
- **Design:** Explain each class, the data flow diagram, and the DIFFICULTY_PRESETS structure
- **Implementation:** Explain the prediction formulas in plain English with the maths shown
- **Testing:** Show score results across difficulties, and the edge cases you tested
- **Evaluation:** Honestly state what works, what doesn't, and what you'd improve

---

## Priority Order

1. Wire ai.py into Paddle ← do this first, everything else depends on it
2. EasyAI ← simplest, gets the pattern right
3. MediumAI ← builds on Easy
4. HardAI ← most complex, do last
5. Test and tune
6. Write up
