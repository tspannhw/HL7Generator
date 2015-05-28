import argparse

parser = argparse.ArgumentParser(description="Test.")
parser.add_argument("messagetypes", nargs="+",
    help='A list of message types you want to include in your generation, ie. "SIU_S12 SIU_S13 Error SIU_S15"')

parser.add_argument("-t", "--total", default=False, type=int,
    help="The total number of messages that will be generated. Defaults to unlimited.")
parser.add_argument("-n", "--network", default=False, type=str,
    help='Send messages via MLLP at address:port, ex: localhost:2575, test.server.com, 192.168.0.1:10000.  If no port is specified, it will default to 2575.')
parser.add_argument("-v", "--version", default="2.3", type=str, 
    help='The version of HL7 messages to generate.  Defaults to 2.3')
parser.add_argument("-r", "--rate", default=False, type=int,
    help='The number of HL7 messages to generate per minute. Defaults to no rate limit.')
parser.add_argument("-f", "--files", default=False, type=str,
    help='Generate text files in directory. Use "default" for the messages subdirectory.')
args = parser.parse_args()

print args