from argparse import ArgumentParser


def create_args():
    parser = ArgumentParser(description="Auto Install App Example")
    parser.add_argument(
        "--app_name",
        type=str,
        default="MySQL",
        metavar="XXX",
        help="input App Name (default: MySQL)",
    )
    parser.add_argument(
        "--service_type",
        type=str,
        default="LoadBalancer",
        metavar="LoadBalancer",
        help="input app service type (default: LoadBalancer)",
    )
    parser.add_argument(
        "--name_space", 
        type=str, 
        default="test-for-long-1", 
        metavar="NNNNNNN", 
        help="input name space (default: test-for-long-1)"
    )
    parser.add_argument(
        "--ip",
        type=str,
        default="172.24.128.170",
        metavar="XXX.XXX.XXX.XXX",
        help="Input app ip (default: 172.24.128.170)"
    )
    parser.add_argument(
        "--momentum", type=float, default=0.5, metavar="M", help="SGD momentum (default: 0.5)"
    )
    parser.add_argument("--register", dest="register", default=False, help="register model in mlflow(default: False)")
    parser.add_argument("--register-name", dest="register_name", help="register model name (default: mnist)", default="mnist")
    parser.add_argument("--seed", type=int, default=1, metavar="S", help="random seed (default: 1)")
    parser.add_argument(
        "--log-interval",
        type=int,
        default=100,
        metavar="N",
        help="how many batches to wait before logging training status",
    )
    parser.add_argument("--experiment-name", dest="experiment_name", help="Experiment name", default='default_2')
    args = parser.parse_args()
    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")
    return args








if __name__ == "__main__":
    print("pass")
    args = create_args()
    print(args.ip,type(args.ip))
