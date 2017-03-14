#!/usr/bin/env python
#******************************************************************************
# 
#  Project:  2017 WFS Benchmarking
#  Purpose:  Generate WFS BBOX/size requests randomly over a defined dataset.
#  Author:   Frank Warmerdam, warmerdam@pobox.com
# 
#******************************************************************************
#  Copyright (c) 2009, Frank Warmerdam
#  Copyright (c) 2017, Lorenzo Pini
# 
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
#******************************************************************************

import random
import math
import string
import sys

# =============================================================================
def Usage():
    print 'Usage: wfs_request.py [-count n] [-region minx miny maxx maxy]'
    print '                    [-size size] [-srs srs] '
    sys.exit(1)

# =============================================================================

if __name__ == '__main__':

    region = None
    srs = None
    count = 100000
    size = 10000 # 10km usually
    
    # Parse command line arguments.
    argv = sys.argv
    
    i = 1
    while i < len(argv):
        arg = argv[i]

        if arg == '-region' and i < len(argv)-4:
            region = (float(argv[i+1]),float(argv[i+2]),
                      float(argv[i+3]),float(argv[i+4]))
            i = i + 4

        elif arg == '-size' and i < len(argv)-1:
            size = int(argv[i+1])
            i = i + 1
            
        elif arg == '-srs' and i < len(argv)-1:
            srs = argv[i+1]
            i = i + 1

        elif arg == '-count' and i < len(argv)-1:
            count = int(argv[i+1])
            i = i + 1

        else:
            print 'Unable to process: %s' % arg
            Usage()

        i = i + 1

    if region is None:
        print '-region is required.'
        Usage()

    if size is None:
        print '-size is required.'
        Usage()
            
    if srs is None:
        print '-srs is required.'
        Usage()
            
    # -------------------------------------------------------------------------

    while count > 0:
        
        center_x = random.random() * (region[2] - region[0]) + region[0]
        center_y = random.random() * (region[3] - region[1]) + region[1]

        bbox = (center_x - size*0.5,
                center_y - size*0.5,
                center_x + size*0.5,
                center_y + size*0.5)

    # Disabled the check to trim the requests to the region
    #    if trim_to_region and bbox[0] >= region[0] \
    #       and bbox[1] >= region[1] \
    #       and bbox[2] <= region[2] \
    #       and bbox[3] <= region[3]:

        count = count-1
        print '%.8g,%.8g,%.8g,%.8g,%s;%s' \
              % (bbox[0],bbox[1],bbox[2],bbox[3],srs,srs)
