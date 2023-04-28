from Levenshtein import distance
from db import local_db

def main():
    db = local_db()
    db.cur.execute("SELECT `game_id`, `game_name` FROM casino.games WHERE `game_type` in ('Video Slots', 'Classic Slots', 'Exclusive Slots')")    
    games = db.cur.fetchall()
    
    db.cur.execute("SELECT `id`, `name` FROM casino.cp_games WHERE `category` = 'SLOT'")    
    cp_games = db.cur.fetchall()

    for cp_game in cp_games:
        min_score = 10
        best_match = None
        
        for game in games:
            cur_score = distance(cp_game[1], game[1])
            if cur_score < min_score:
                min_score = cur_score
                best_match = game[0]
        
        if best_match:
            db.cur.execute("INSERT INTO casino.matches VALUES (%s, %s)", (best_match, cp_game[0]))
            db.conn.commit()

if __name__ == "__main__":
    main()
