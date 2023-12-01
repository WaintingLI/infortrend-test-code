'''
這是一份用來測試ML Flow的是自動測試文件
'''
import os
import sys
import logging
import configparser
from argparse import ArgumentParser
import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
from torchvision import datasets, transforms

#切換命令提示字元到Python檔案所在的目錄
os.chdir(os.path.dirname(sys.argv[0]))

#讀取檔案參數與全域變數
cf=configparser.ConfigParser()
cf.read_file(open('config.ini', 'r', encoding='UTF-8'))
MLFLOW_IP=cf.get("APP_Info","Mlflow_ip")
DEBUG_MODE = cf.getboolean("APP_Info","Debug_mode")
RUN_ID = "run_id"

#設定是否要開啟Debug Mode
if DEBUG_MODE:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.ERROR)


print("MLflow Version:", mlflow.__version__)
print("Torch Version:", torch.__version__)


def init(init_args):
    '''初始化torch模型'''
    torch.manual_seed(init_args.seed)

def create_args():
    '''將CommandLine的參數帶入,如果設定參數則自動設定預設值'''
    parser = ArgumentParser(description="PyTorch MNIST Example")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        metavar="N",
        help="input batch size for training (default: 64)",
    )
    parser.add_argument(
        "--test-batch-size",
        type=int,
        default=1000,
        metavar="N",
        help="input batch size for testing (default: 1000)",
    )
    parser.add_argument(
        "--epochs", 
        type=int,
        default=10,
        metavar="N",
        help="number of epochs to train (default: 10)"
    )
    parser.add_argument(
        "--lr", type=float, default=0.5, metavar="LR", help="learning rate (default: 0.01)"
    )
    parser.add_argument(
        "--momentum", type=float, default=0.5, metavar="M", help="SGD momentum (default: 0.5)"
    )
    parser.add_argument("--register",
                        dest="register",
                        default=False,
                        help="register model in mlflow(default: False)")
    parser.add_argument("--register-name",
                        dest="register_name",
                        help="register model name (default: mnist)", default="mnist")
    parser.add_argument("--seed",
                        type=int,
                        default=1,
                        metavar="S",
                        help="random seed (default: 1)")
    parser.add_argument(
        "--log-interval",
        type=int,
        default=100,
        metavar="N",
        help="how many batches to wait before logging training status",
    )
    parser.add_argument("--experiment-name",
                        dest="experiment_name",
                        help="Experiment name",
                        default='default_test')
    parser_arguments = parser.parse_args()
    print("Arguments:")
    for arg in vars(parser_arguments):
        print(f"  {arg}: {getattr(parser_arguments, arg)}")
    return parser_arguments


class Net(nn.Module):
    '''應該是訓練用的東西吧'''
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d(p=0.1)
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, i):
        '''應該是訓練用的東西吧'''
        i = F.relu(F.max_pool2d(self.conv1(i), 2))
        i = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(i)), 2))
        i = i.view(-1, 320)
        i = F.relu(self.fc1(i))
        i = F.dropout(i, p=0.1, training=self.training)
        i = self.fc2(i)
        return F.log_softmax(i, dim=0)




def train(model, optimizer, epoch, train_args, train_loader):
    '''訓練用的模型'''
    model.train()
    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = Variable(data), Variable(target)
        optimizer.zero_grad()
        output = model(data)
        loss = F.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        if batch_idx % train_args.log_interval == 0:
            print(
                "Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}".format(
                    epoch,
                    batch_idx * len(data),
                    len(train_loader.dataset),
                    100.0 * batch_idx / len(train_loader),
                    loss.data.item(),
                )
            )
            step = epoch * len(train_loader) + batch_idx
            log_scalar("train_loss", loss.data.item(), step)


def test(model, epoch, train_loader, test_loader):
    '''模型測試'''
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in test_loader:
            data, target = Variable(data), Variable(target)
            output = model(data)
            test_loss += F.nll_loss(
                output, target, reduction="sum"
            ).data.item()  # sum up batch loss
            pred = output.data.max(1)[1]  # get the index of the max log-probability
            correct += pred.eq(target.data).cpu().sum().item()

    test_loss /= len(test_loader.dataset)
    test_accuracy = 100.0 * correct / len(test_loader.dataset)
    print(
        "\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n".format(
            test_loss, correct, len(test_loader.dataset), test_accuracy
        )
    )
    step = (epoch + 1) * len(train_loader)
    log_scalar("test_loss", test_loss, step)
    log_scalar("test_accuracy", test_accuracy, step)


def log_scalar(name, value, step):
    """Log a scalar value to both MLflow and TensorBoard"""

    mlflow.log_metric(name, value,step=step)


def do_train(args_parameter):
    '''開始訓練模型'''
    model = Net()
    optimizer = optim.SGD(model.parameters(),
                          lr=args_parameter.lr,
                          momentum=args_parameter.momentum)

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    dataset1 = datasets.MNIST('../data', train=True, download=True,
                            transform=transform)
    dataset2 = datasets.MNIST('../data', train=False,
                            transform=transform)
    train_loader = torch.utils.data.DataLoader(dataset1,
                                               batch_size=args_parameter.batch_size,
                                               shuffle=True)
    test_loader = torch.utils.data.DataLoader(dataset2,
                                              batch_size=args_parameter.batch_size,
                                              shuffle=True)
    with mlflow.start_run() as run:
        global RUN_ID
        print("run_id:",run.info.run_id)
        RUN_ID = run.info.run_id
        mlflow.set_tag("mlflow_version",mlflow.__version__)
        mlflow.set_tag("torch_version",torch.__version__)

        # Perform the training
        for epoch in range(1, args_parameter.epochs + 1):
            train(model, optimizer, epoch, args_parameter, train_loader)
            test(model, epoch, train_loader, test_loader)


        for key, value in vars(args_parameter).items():
            mlflow.log_param(key, value)
        print('start log model...')
        mlflow.pytorch.log_model(model, "pytorch-model")
        if args_parameter.register:
            print('register model...')
            model_uri = f"runs:/{run.info.run_id}/model"
            model_details = mlflow.register_model(model_uri, args_parameter.register_name)
            print(model_details)




if __name__ == "__main__":
    args = create_args()
    mlflow.set_tracking_uri(f"{MLFLOW_IP}")
    init(args)
    #檢查ML flow上，被刪除的experiment中是否有相同命名的Experiments名稱,如果有，則改變Experiment名稱
    experiments = mlflow.get_experiment_by_name(f"{args.experiment_name}")
    COUNTER = 0
    HOLD_EXPERIMENT_NAME = args.experiment_name
    while experiments and experiments.lifecycle_stage=="deleted":
        lifecycle_stage_string=experiments.lifecycle_stage
        logging.debug("lifecycle_stage_string = %s",lifecycle_stage_string)
        if  lifecycle_stage_string=="deleted":
            logging.debug(
                        "The ML flow has already been same experiment name which is %s, \
                        and lifecycle_stage is %s",
                        args.experiment_name,
                        lifecycle_stage_string
                        )
            COUNTER = COUNTER + 1
            args.experiment_name = HOLD_EXPERIMENT_NAME + f"{COUNTER}"
            logging.debug("Modify args.experiment_name = %s",args.experiment_name)
            experiments = mlflow.get_experiment_by_name(f"{args.experiment_name}")

    if args.experiment_name:
        print("args.experiment_name = ",args.experiment_name)
        mlflow.set_experiment(args.experiment_name)

    do_train(args)

    #檢查Experiment中的資料是否上傳完成
    if mlflow.get_run(RUN_ID).info.status == "FINISHED":
        print("ML flow test is Pass")
    else:
        print("Error,")
        info = mlflow.get_run(RUN_ID).info
        experiment_name = mlflow.get_experiment(mlflow.get_run(RUN_ID).info.experiment_id).name
        print(f"The Run Name, {info.run_name}, is {info.lifecycle_stage} in the Experiment {experiment_name}")

    logging.debug(" run id status %s",mlflow.get_run(RUN_ID).info.status)
    experiment_id = mlflow.get_run(RUN_ID).info.experiment_id

    """
    #刪除測試用的experiment
    mlflow.delete_experiment(experiment_id)

    # Examine the deleted experiment details.
    experiment_deleted_data = mlflow.get_experiment(experiment_id)
    logging.info("Deleted Experiment: %s",experiment_deleted_data.name)
    logging.debug("Artifact Location: %s", experiment_deleted_data.artifact_location)
    logging.debug("Lifecycle_stage: %s",experiment_deleted_data.lifecycle_stage)
    logging.debug("Last Updated timestamp: %s", experiment_deleted_data.last_update_time)
    """
