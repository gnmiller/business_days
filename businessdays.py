#!/usr/bin/python3.6

# init environment
import sys, os
env_name = "business_days"
path = os.path.dirname( os.path.realpath( __file__ ) )
sys.path.insert( 0, "{}/{}".format( path, env_name ) )

# actual imports
from datetime import date, timedelta as td
from dateutil.parser import parse as date_parse
from argparse import ArgumentParser as ap
import holidays

def is_empty( data ):
    try:
        data
        return False
    except:
        return True

# cli args
parser = ap( description="Prints the number of weekdays between two dates. Uses the dateutil library to parse the input. Should be able to accept most standard date formats." )
parser.add_argument( "start", action="store", help="the date to start counting from." )
parser.add_argument( "end", action="store", help="The date to count to." )
parser.add_argument( "-i", "--inverse", action="store_true", dest="i", help="Perform the inverse action and print the number of weekends" )
parser.add_argument( "-x", "--holidays", action="store_true", dest="x", help="Skip US holidays during calculation. Has no effect if specified with -i." )
parser.add_argument( "-a", "--all", action="store_true", dest="a", help="Count all days instead. Specifying -a causes -x and -i to have no effect." )
args = parser.parse_args()


# arg init and input error checks
try:
    s = date_parse( args.start )
    e = date_parse( args.end )
except ValueError:
    print( "[ERR] One of the provided dates was invalid." )
    sys.exit( -1 )
if e == s:
    print( "[ERR] Please select two dates that are not the same." )
    sys.exit( -1 )
if( s > e ):
    print( "invalid input" )
    sys.exit( -1 )
d = int(str(e-s).split(" ")[0])
if is_empty( args.x ):
    args.x = False
if is_empty( args.i ):
    args.i = False
if is_empty( args.a ):
    args.a = False
elif args.a:
    args.i = False
    args.x = False

wd = 0
# datetime.isoweekday() returns 1-7 sun-sat
if args.a:
    we = ()
else:
    we = (6,7)
debug = lambda x: print( "DATE: {}\nWeekday?: {}\nHoliday: {}\n{}".format( x, x.isoweekday(), x in holidays.US(), '*'*32 ) )
for i in range( 0, d+1 ):
    if not s.isoweekday() in we: # weekend?
        if not args.x:
            wd += 1
        elif not s in holidays.US(): # holiday?
            wd += 1
    s += td( days=1 )

# print
if args.i == True:
    print( "{} weekends (days)".format( d-wd ) )
elif args.a:
    print( "{} total days".format( wd ) )
else:
    print( "{} weekdays".format( wd ) )
