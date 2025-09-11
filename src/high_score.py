import os

file = "highscore.txt"

def load_highscore():
    if os.path.exists(file):
        with open(file, "r") as f:
            try:
                return int(f.read().strip())  
            except ValueError:
                return 0
            
    return 0


def save_highscore(new_score):
    with open(file, "w") as f:  
        f.write(str(new_score))
        
        
def update_highscore(curr_score):
    old_score = load_highscore()
    if curr_score > old_score:    
        save_highscore(curr_score)
        return curr_score
    return old_score