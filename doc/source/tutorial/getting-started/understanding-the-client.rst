理解客户端
============

与 Takler 服务的所有通讯都通过 takler_client 实现。
对于任意与服务器的通讯，客户端需要知道服务运行的主机和服务的端口号。
同一台主机上可能运行多个服务，每个服务有唯一的端口号。

下面展示通过 shell 命令行和 Python 脚本使用客户端的示例。

客户端 Shell 接口
-----------------

全部可用命令类型列表：

.. code-block:: bash

    takler_client --help

.. code-block::

    A CLI client for Takler.

    Usage:
      takler_client [flags]
      takler_client [command]

    Available Commands:
      abort       mark task to aborted
      complete    mark task to complete
      completion  Generate the autocompletion script for the specified shell
      event       change event
      help        Help about any command
      init        mark task to active
      meter       change meter
      ping        ping server
      requeue     requeue given nodes
      resume      resume given nodes
      run         run the tasks, ignore triggers
      show        print state of all flows in server
      suspend     suspend given nodes

    Flags:
      -h, --help   help for takler_client

    Use "takler_client [command] --help" for more information about a command.

takler_client 使用如下方法确定 ``host`` 和 ``port`` 值：

* 默认主机和端口号是 ``localhost:33083``
* 默认值可以被环境变量 ``TAKLER_HOST`` 和 ``TAKLER_PORT`` 覆盖
* 还可以使用 ``--host`` 和 ``--port`` 选项进一步覆盖。

使用命令行 ping  Takler 服务：

.. code-block:: bash

  takler_client ping --host=login_a06 --port=33083

输出信息类似：

.. code-block::

  login_a06:33083 ping
  ping server (login_a06:33083) succeeded in 3.292513ms


客户端 Python 接口
------------------

takler_client 提供的功能也可以通过 takler python 包的 client 模块实现。
Python 接口的 ``TaklerServiceClient`` 类提供默认的主机地址和端口号，用户也可以自行设置。


在 **${TAKLER_HOME}** 目录中创建 **client.py**

.. code-block:: py
    :linenos:

    from takler.client import TaklerServiceClient


    def main():
        client = TaklerServiceClient()
        client.ping()

        client.set_host_port("login_a06", "33083")
        client.ping()


    if __name__ == "__main__":
        main()

逐行解释代码：

- 1：导入 Takler 客户端类 ``TaklerServiceClient``
- 5：创建 Takler 客户端对象 ``TaklerServiceClient``，使用默认的主机和端口号 (``localhost::33083``)
- 6：执行 ``ping`` 操作
- 8：设置主机和端口号 (本教程为 ``login_a06:33083``，根据实际情况修改)

  .. warning::

      Takler 使用 gRPC Python 接口实现 RPC 功能。
      如果运行出错，提示如下信息：

      .. code-block::

          DNS resolution failed for login_a06:33083

      表示 gRPC 未识别 ``login_a06`` 域名。
      需要在运行前设置环境变量 ``GRPC_DNS_RESOLVER`` 为 ``native``，使用本地 DNS 解析服务。

      .. code-block:: bash

          export GRPC_DNS_RESOLVER=native

      使用 GOLANG 实现的 *takler_client* 无需设置环境变量。

- 9：再次执行 ``ping`` 操作

运行 **client.py**

.. code-block:: bash

    python client.py



输入结果类似：

.. code-block::

    ping server (localhost:33083) succeeded in 0:00:00.008180.
    ping server (login_a06:33083) succeeded in 0:00:00.004481.


练习
-----

1. 运行 ``takler_client ping`` 命令
2. 创建 **client.py** 脚本并运行