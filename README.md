# Cut Finder

Meant to answer problems of the form "How should I cut boards a, b, and c into final boards x,
y,z to minimize waste"

cutfinder is available from [pypi](https://pypi.org/project/cutfinder/):
    
    pip install cutfinder


Basic use is meant to simply print the results:

    from cutfinder import CutFinder
    CutFinder(stocks=[100, 48], finals=[50,40, 36, 12, 12])
prints

    Unable to allocate final cuts: 12 
    Stock Board of length 48 is cut into final boards 40 with remainder 7.875 
    Stock Board of length 100 is cut into final boards 50, 36, 12 with remainder 1.625

Alternately, you can run cutfinder from the command line:

    python -m cutfinder 100 50,24 0.15

Note: the stock boards are listed first, final boards second, 
then kerf (optional). For listing multiple stock or final boards, 
separate by a comma, but no space 

However, you can find all the data in the actual CutFinder object if you want.
