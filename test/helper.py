from takler.node_state import NodeState

def check_node_state(test_case, bunch, a_state_mapper):
    """Check node state given in a mapper.

    The mapper is like:
        state_mapper ={
            "/suite1", "queue",
            "/suite1/task1", "queue"
        }
    """
    for a_state_exp in a_state_mapper:
        a_state = bunch.find_node_by_absolute_path(a_state_exp).state
        required_state = NodeState.to_state(a_state_mapper[a_state_exp])
        test_case.assertEqual(a_state, required_state,
                              msg="{node_path}: {state} != {required_state}".format(
                                  node_path=a_state_exp,
                                  state=a_state,
                                  required_state=required_state
                              ))
