import gymnasium as gym

class CarRacingPenaltiesWrapper(gym.Wrapper):
    def __init__(
        self,
        env,
        min_speed=0.1,
        penalty_contramao=1,
        penalty_offroad=1,
        penalty_devagar=1
    ):
        super().__init__(env)
        self.prev_x = None
        self.prev_y = None
        self.min_speed = min_speed
        self.penalty_contramao = penalty_contramao
        self.penalty_offroad = penalty_offroad
        self.penalty_devagar = penalty_devagar

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self.prev_x = None
        self.prev_y = None
        return obs, info

    def step(self, action):
        obs, reward, done, truncated, info = self.env.step(action)

        if self.prev_y is not None:
            dy = info.get("y_position", 0) - self.prev_y
            if dy < 0:
                reward -= self.penalty_contramao

        if reward < -1:
            reward -= self.penalty_offroad
            truncated = False

        speed = info.get("speed", None)
        if speed is not None:
            if speed < self.min_speed:
                reward -= self.penalty_devagar
            else:
                reward += 100  
        else:
            if self.prev_x is not None and self.prev_y is not None:
                dx = info.get("x_position", 0) - self.prev_x
                dy = info.get("y_position", 0) - self.prev_y
                dist = (dx**2 + dy**2) ** 0.5
                if dist < self.min_speed:
                    reward -= self.penalty_devagar
                else:
                    reward += 100  
                  
        self.prev_x = info.get("x_position", 0)
        self.prev_y = info.get("y_position", 0)

        return obs, reward, done, truncated, info
