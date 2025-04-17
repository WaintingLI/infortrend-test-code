"""
用來獲取IP相關設定
"""
from argparse import ArgumentParser

def create_args():
    '''將CommandLine的參數帶入,如果設定參數則自動設定預設值'''
    parser = ArgumentParser(description="SQLserver Example")
    parser.add_argument(
        "--ip",
        type=str,
        default="172.24.128.214",
        metavar="N",
        help="input ipv4",
    )
    parser.add_argument(
        "--port",
        type=str,
        default="1433",
        metavar="N",
        help="input ip port",
    )
    parser_arguments = parser.parse_args()
    print("Arguments:")
    for arg in vars(parser_arguments):
        print(f"  {arg}: {getattr(parser_arguments, arg)}")
    return parser_arguments


if __name__ == "__main__":
        args = create_args()
        print(args.ip)
        print(args.port)
