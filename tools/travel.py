#!/usr/bin/env python3
"""Travel times in Seoul, late 1997, so in-game time stays honest.

Rough but consistent figures. Districts are the ones the game uses most.
Usage: python3 tools/travel.py Cheongnyangni Gangnam --mode subway
Modes: walk, bus, subway, taxi, van. Night (--night) slows buses and subway
(last trains near midnight; none until about 5:30), speeds taxis.
"""
import argparse, itertools, sys

# Approximate straight-line km between district centers, 1997 geography.
D = {
 ("Jongno","Jung"):2, ("Jongno","Yongsan"):5, ("Jongno","Mapo"):5, ("Jongno","Seongdong"):5,
 ("Jongno","Dongdaemun"):3, ("Jongno","Cheongnyangni"):5, ("Jongno","Gangnam"):9, ("Jongno","Seocho"):10,
 ("Jongno","Yeongdeungpo"):9, ("Jongno","Yeoksam"):10, ("Jongno","Dogok"):12, ("Jongno","Euljiro"):1,
 ("Jung","Yongsan"):3, ("Jung","Mapo"):5, ("Jung","Seongdong"):4, ("Jung","Dongdaemun"):2,
 ("Jung","Cheongnyangni"):5, ("Jung","Gangnam"):8, ("Jung","Seocho"):8, ("Jung","Yeongdeungpo"):8,
 ("Jung","Yeoksam"):9, ("Jung","Dogok"):11, ("Jung","Euljiro"):1,
 ("Yongsan","Mapo"):4, ("Yongsan","Seongdong"):6, ("Yongsan","Dongdaemun"):5, ("Yongsan","Cheongnyangni"):8,
 ("Yongsan","Gangnam"):6, ("Yongsan","Seocho"):6, ("Yongsan","Yeongdeungpo"):5, ("Yongsan","Yeoksam"):7,
 ("Yongsan","Dogok"):9, ("Yongsan","Euljiro"):3,
 ("Mapo","Seongdong"):9, ("Mapo","Dongdaemun"):7, ("Mapo","Cheongnyangni"):10, ("Mapo","Gangnam"):11,
 ("Mapo","Seocho"):10, ("Mapo","Yeongdeungpo"):4, ("Mapo","Yeoksam"):12, ("Mapo","Dogok"):14, ("Mapo","Euljiro"):5,
 ("Seongdong","Dongdaemun"):3, ("Seongdong","Cheongnyangni"):3, ("Seongdong","Gangnam"):6, ("Seongdong","Seocho"):8,
 ("Seongdong","Yeongdeungpo"):11, ("Seongdong","Yeoksam"):7, ("Seongdong","Dogok"):8, ("Seongdong","Euljiro"):4,
 ("Dongdaemun","Cheongnyangni"):2, ("Dongdaemun","Gangnam"):9, ("Dongdaemun","Seocho"):10, ("Dongdaemun","Yeongdeungpo"):11,
 ("Dongdaemun","Yeoksam"):10, ("Dongdaemun","Dogok"):11, ("Dongdaemun","Euljiro"):2,
 ("Cheongnyangni","Gangnam"):9, ("Cheongnyangni","Seocho"):11, ("Cheongnyangni","Yeongdeungpo"):13,
 ("Cheongnyangni","Yeoksam"):9, ("Cheongnyangni","Dogok"):10, ("Cheongnyangni","Euljiro"):4,
 ("Gangnam","Seocho"):3, ("Gangnam","Yeongdeungpo"):9, ("Gangnam","Yeoksam"):1, ("Gangnam","Dogok"):3, ("Gangnam","Euljiro"):8,
 ("Seocho","Yeongdeungpo"):8, ("Seocho","Yeoksam"):2, ("Seocho","Dogok"):4, ("Seocho","Euljiro"):8,
 ("Yeongdeungpo","Yeoksam"):10, ("Yeongdeungpo","Dogok"):12, ("Yeongdeungpo","Euljiro"):8,
 ("Yeoksam","Dogok"):3, ("Yeoksam","Euljiro"):9, ("Dogok","Euljiro"):11,
}
# minutes per km, day. Door to door overhead in minutes.
SPEED = {"walk": (13, 0), "bus": (4.5, 15), "subway": (3.0, 18), "taxi": (3.2, 5), "van": (3.5, 8)}

def km(a, b):
    if a == b:
        return 1
    return D.get((a, b)) or D.get((b, a))

def main():
    p = argparse.ArgumentParser()
    p.add_argument("origin"); p.add_argument("dest")
    p.add_argument("--mode", default="subway", choices=SPEED)
    p.add_argument("--night", action="store_true")
    a = p.parse_args()
    d = km(a.origin, a.dest)
    if d is None:
        print("Unknown district. Known:", ", ".join(sorted({x for k in D for x in k})))
        sys.exit(1)
    per, over = SPEED[a.mode]
    if a.night:
        if a.mode in ("bus", "subway"):
            per *= 1.4; over += 15
        if a.mode in ("taxi", "van"):
            per *= 0.7
    mins = round(d * per + over)
    print(f"{a.origin} to {a.dest} by {a.mode}{' at night' if a.night else ''}: about {mins} minutes ({d} km)")

if __name__ == "__main__":
    main()
