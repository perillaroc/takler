import json
import os
import takler


def main():
    client = takler.Client()
    #client.queue("/suite1")

    test_suite2 = takler.Suite("test_suite2")
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

    try:
        client.add_suite(test_suite2)
    except takler.InvalidRequestException, ire:
        print "[example_client]got InvalidRequestException: {why}".format(why=ire.why)

    family3.append_child("task5")
    family3.append_child("task6")
    client.update_suite(test_suite2)

    family3.append_child("task7")
    client.update_node("/test_suite2/family2/family3", family3)
    print client.get_bunch_tree_str()
    

if __name__ == "__main__":
    main()
