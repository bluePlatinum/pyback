import argparse


def main():
    parser = argparse.ArgumentParser(prog="pybacked",
                                     description="A versatile backup utility, "
                                                 "which works across unix "
                                                 "based and windows systems."
                                                 "It even works under water!"
                                                 "(no it doesn't)",
                                     allow_abbrev=False)
    parser.add_argument("config_file", metavar="configuration", type=str,
                        help="The path to the configuration file")
    parser.add_argument("command", metavar="command", type=str,
                        help="The command for the operation which is to be"
                             "executed.")
    args = parser.parse_args()
    print(args.config_file)
    print(args.command)
    print("TEST")
