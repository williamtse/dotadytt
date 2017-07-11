#coding=utf-8
import enum

class Sex(enum.Enum):
    male=1
    female=2


#星座
class Horoscope(enum.Enum):
    Capricorn=1
    Aquarius=2
    Pisces=3
    Aries=4
    Taurus=5
    Gemini=6
    Leo=7
    Virgo=8
    Libra=9
    Scorpio=10
    Sagittarius=11


#影人类型
class CelebrityType(enum.Enum):
    director=1
    actor=2
    scriptwriter = 3
    
    
