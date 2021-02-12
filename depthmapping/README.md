# Guide to the python
Sorry, readability was not my primary concern when I was writing it. Hopefully the comments will help. Here is an overview of the structure of the code:

## External dependencies
### PIL
Lets me open and convert images.
### numpy
I need it for this one awkward conversion issue you can ignore it.

## My code
### main.py
This is the starting point. All of this is just wrapper code to load in the data and pass it into the actual algorithm, which is in
### pixim.py
The actual algorithm. It takes in two images and returns one.
### util.py
Some important utility functions and classes.

**Please refer to Writeup/Design.md for a better explanation of how it works, complete with nicely commented pseudocode and some suggestions for improvements.**