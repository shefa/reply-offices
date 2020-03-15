a=$(python3 score.py inputs/a_solar.txt outputs/a.out)
b=$(python3 score.py inputs/b_dream.txt outputs/b.out)
c=$(python3 score.py inputs/c_soup.txt outputs/c.out)
d=$(python3 score.py inputs/d_maelstrom.txt outputs/d.out)
e=$(python3 score.py inputs/e_igloos.txt outputs/e.out)
f=$(python3 score.py inputs/f_glitch.txt outputs/f.out)
echo "Before: $((a+b+c+d+e+f))"
a=$(python3 score.py inputs/a_solar.txt outputs/a.outx)
b=$(python3 score.py inputs/b_dream.txt outputs/b.outx)
c=$(python3 score.py inputs/c_soup.txt outputs/c.outx)
d=$(python3 score.py inputs/d_maelstrom.txt outputs/d.outx)
e=$(python3 score.py inputs/e_igloos.txt outputs/e.outx)
f=$(python3 score.py inputs/f_glitch.txt outputs/f.outx)
echo "After : $((a+b+c+d+e+f))"