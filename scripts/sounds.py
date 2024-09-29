import pygame as pg

pg.mixer.init()

pg.mixer.music.load("data/Sounds/ambience.mp3")
pg.mixer.music.set_volume(0.05)
pg.mixer.music.play(loops=-1)