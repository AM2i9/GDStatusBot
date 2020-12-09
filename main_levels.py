import gd

# So gd.py dosen't get the difficulty of the main geometry dash lineup, so I have to do them manually by id
# Thankfully, each main level has a one digit id, and that id corresponds to its location in the following
# list

main_levels = [
    gd.LevelDifficulty.EASY,
    gd.LevelDifficulty.EASY,
    gd.LevelDifficulty.NORMAL,
    gd.LevelDifficulty.NORMAL,
    gd.LevelDifficulty.HARD,
    gd.LevelDifficulty.HARD,
    gd.LevelDifficulty.HARDER,
    gd.LevelDifficulty.HARDER,
    gd.LevelDifficulty.HARDER,
    gd.LevelDifficulty.INSANE,
    gd.LevelDifficulty.INSANE,
    gd.LevelDifficulty.INSANE,
    gd.LevelDifficulty.INSANE,
    gd.DemonDifficulty.HARD_DEMON,
    gd.LevelDifficulty.INSANE,
    gd.LevelDifficulty.INSANE,
    gd.LevelDifficulty.HARDER,
    gd.DemonDifficulty.HARD_DEMON,
    gd.LevelDifficulty.HARDER,
    gd.DemonDifficulty.HARD_DEMON,
    gd.LevelDifficulty.INSANE]
