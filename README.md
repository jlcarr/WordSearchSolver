# WordSearchSolver
A Jupyter notebook using Tesseract, PIL and numpy to automate solving word searches given as images.

I was inspired by [this Reddit post](https://www.reddit.com/r/puzzles/comments/1e5ml2e/my_wife_says_word_searches_are_too_easy_so_i_made/) to write an automated [word search](https://en.wikipedia.org/wiki/Word_search) solver. It's a great excuse to work with OCR and image processing tools.

I thought I'd need some image segmenting and clusering tools to determine the grid, but it turns out for nicely formatted grids given as a nice digital image we can actually do things much more easily with just numpy.
