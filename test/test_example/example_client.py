import json
import os
import takler
from takler.suite import Suite


def main():
    client = takler.Client()
    client.queue("/suite1")

    test_suite2 = Suite("test_suite2")
    test_suite2.var_map["suite_home"] = os.path.join(os.path.dirname(__file__), '../test_data/py')
    family1 = test_suite2.append_child("family1")
    task1 = family1.append_child("task1")
    task2 = family1.append_child("task2")
    task2.add_trigger("task1 == complete")

    family2 = test_suite2.append_child("family2")
    family2.add_trigger("family1 == complete")

    task3 = family2.append_child("task3")

    family3 = family2.append_child("family3")
    family3.add_trigger("task3 == complete")
    task4 = family3.append_child("task4")

    client.add_suite(test_suite2)

    server_response = client.bunch_tree()
    bunch_tree = json.loads(server_response.str)
    print json.dumps(bunch_tree, indent=4, separators=(',', ':'))
    

if __name__ == "__main__":
    main()
