import time


class Score:
    def __init__(self):
        self.reset()
        
        
    def reset(self):
        self.start_time = time.time()
        self.score = 0
        
    def update(self):
        self.score = int(time.time() - self.start_time)
        
    def get_score(self):
        return self.score
    
    