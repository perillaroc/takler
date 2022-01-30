#测试数据

suite1结构如下：

<pre>
|- suite1 [Unknown] Trigger: True
    |- family1 [Unknown] Trigger: True
        |- task1 [Unknown] Trigger: True
        |- task2 [Unknown] Trigger: [task1 == complete] False
    |- family2 [Unknown] Trigger: [family1 == complete] False
        |- task3 [Unknown] Trigger: True
        |- family3 [Unknown] Trigger: [task3 == complete] False
            |- task4 [Unknown] Trigger: True
</pre>