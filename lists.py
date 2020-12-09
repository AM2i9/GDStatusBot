import gd

# This file is formatted so that each image corresponds to a difficulty
# The position in the difficulties list is the same as the link to its image

faces = [
    "https://cdn.discordapp.com/attachments/675532248493326359/785672432966828072/Auto.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785672432139894794/Unrated.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785672433948164116/Easy.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785970124657000448/Normal.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785672437227454474/Hard.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785672438948167680/Harder.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785672442789101588/Insane.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785672436708016148/EasyDemon.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785672442508476426/MediumDemon.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785973989495013416/Hard_Demon.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785672441879199764/InsaneDemon.png",
    "https://cdn.discordapp.com/attachments/675532248493326359/785672438746316840/ExtremeDemon.png"]

difficulties = [
    gd.LevelDifficulty.AUTO,
    gd.LevelDifficulty.NA,
    gd.LevelDifficulty.EASY,
    gd.LevelDifficulty.NORMAL,
    gd.LevelDifficulty.HARD,
    gd.LevelDifficulty.HARDER,
    gd.LevelDifficulty.INSANE,
    gd.DemonDifficulty.EASY_DEMON,
    gd.DemonDifficulty.MEDIUM_DEMON,
    gd.DemonDifficulty.HARD_DEMON,
    gd.DemonDifficulty.INSANE_DEMON,
    gd.DemonDifficulty.EXTREME_DEMON]

# A list of progress bar states

progress_bar = [
"░░░░░░░░░░░░░░░░░░░░",
"▓░░░░░░░░░░░░░░░░░░░",
"▓▓░░░░░░░░░░░░░░░░░░",
"▓▓▓░░░░░░░░░░░░░░░░░",
"▓▓▓▓░░░░░░░░░░░░░░░░",
"▓▓▓▓▓░░░░░░░░░░░░░░░",
"▓▓▓▓▓▓░░░░░░░░░░░░░░",
"▓▓▓▓▓▓▓░░░░░░░░░░░░░",
"▓▓▓▓▓▓▓▓░░░░░░░░░░░░",
"▓▓▓▓▓▓▓▓▓░░░░░░░░░░░",
"▓▓▓▓▓▓▓▓▓▓░░░░░░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓░",
"▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓"]