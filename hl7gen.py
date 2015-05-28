import argparse, os, sys
from classes import *
from randomdatasets import * 
from pprint import pprint

#Parse command line arguments
parser = argparse.ArgumentParser(description="Generate HL7 messages and save them in a directory and/or send via MLLP.")
parser.add_argument("messagetypes", nargs="+",
    help='A list of message types you want to include in your generation, ie. "SIU_S12 SIU_S13 Error SIU_S15"')
parser.add_argument("-m", "--mode", default="d", choices=["d","dn","nd","n"],
    help="Whether you want to generate messages in a (d)irectory and/or send them on the (n)etwork. Defaults to directory only.")
parser.add_argument("-n", "--number", default=1000, type=int,
    help="The total number of messages that will be generated. Defaults to 1000.")
parser.add_argument("-i", "--ipaddress", type=str,
    help='The hostname or IP address of the MLLP listening device. Required if mode includes network.')
parser.add_argument("-p", "--port", type=int,
    help='The port of the MLLP listening device. Required if mode includes network.')
parser.add_argument("-v", "--version", default="2.3", type=str, 
    help='The version of HL7 messages to generate.  Defaults to 2.3')
parser.add_argument("-r", "--rate", default=0, type=int,
    help='The number of HL7 messages to generate per minute. Defaults to 0 aka no rate limit.')
parser.add_argument("-o", "--outputdir", default="messages",
    help='The full directory path to where to place generated messages. Defaults to the "messages" subdirectory.')
args = parser.parse_args()

#Set constants based on args
MESSAGE_TYPES = args.messagetypes
if args.mode == "d":
    OUTPUT_FILE = True
    OUTPUT_NETWORK = False
    IPADDRESS = None
    PORT = None
elif args.mode == "n":
    OUTPUT_FILE = False
    OUTPUT_NETWORK = True
    IPADDRESS = args.ipaddress
    PORT = args.port
else:
    OUTPUT_FILE = True
    OUTPUT_NETWORK = True
    IPADDRESS = args.ipaddress
    PORT = args.port
MESSAGE_COUNT = args.number
HL7_VERSION = args.version
RATE = args.rate
if args.outputdir == 'messages':
    OUTPUT_DIR = os.path.join(os.path.realpath(__file__), 'messages')
else:
    OUTPUT_DIR = args.outputdir

# print MESSAGE_TYPES
# print OUTPUT_FILE
# print OUTPUT_NETWORK
# print IPADDRESS
# print PORT
# print MESSAGE_COUNT
# print HL7_VERSION
# print RATE
# print OUTPUT_DIR

#Validate inputs
if OUTPUT_NETWORK and IPADDRESS == None:
    print "Hostname or IP address required if utilizing MLLP."
    sys.exit()
if OUTPUT_NETWORK and PORT == None:
    print "Port required if utilizing MLLP."
    sys.exit()
try:
    for x in MESSAGE_TYPES:
        test = AbstractMessageFactory.factory(1,x,HL7_VERSION,DATASET)
except NotImplementedError:
    print "HL7 version '%s' not currently implemented." % HL7_VERSION
    sys.exit()
except Exception:
    print "Message type '%s' not currently implemented." % x
    sys.exit()

if __name__ == ('__main__'):
    id = 0
    while True:
        id += 1
        type = random.choice(MESSAGE_TYPES)
        out_message = AbstractMessageFactory.factory(id,type,HL7_VERSION,DATASET)
        out_message.assemble()
        
        pprint(out_message.message)
        print "\n"
        
        # sys.stdout.write(out_message.message)
        # pprint(vars(out_message))
        out_message.send(IPADDRESS,PORT)
