# Baboon Crossing Problem

## Problem description:

Baboons can cross the canyon by swinging hand-over-hand on the rope, but if two baboons going in opposite directions meet in the middle, they will fight and drop to their deaths. Furthermore, the rope is only strong enough to hold 5 baboons. If there are more baboons on the rope at the same time, it will break.

The following properties are ensured:

1. Once a baboon has begun to cross, it is guaranteed to get to the other side without running into a baboon going the other way.
2. There are never more than 5 baboons on the rope.
3. A continuing stream of baboons crossing in one direction should not bar baboons going the other way indefinitely (no starvation).

## Running the gui for ubuntu:

1. Install vpython
```python2
sudo apt-get install python-visual
sudo apt-get install libgtkglextmm-x11-1.2-dev
```

2. Install pygame
```python2
sudo apt-get install python-pygame
```

3. Run gui.py file
```python2
python2 gui.py
```

## User options:
### These options can be set by the user by editing the source gui.py file.
```python2
# default values
max_on_rope = 5 
left_baboon_count = 15
right_baboon_count = 15

# uncomment to select music
#mixer.music.load('songs/five-little-mokeys.mp3')
mixer.music.load('songs/mowgli-sahara-theme.mp3')
#mixer.music.load('songs/monkey.mp3')
```
