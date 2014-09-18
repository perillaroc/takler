namespace py takler_service

# data structure

struct ServiceResponse{
    1: i64 flag,
    2: string str
}

exception InvalidRequestException{
    1:string why
}

# service api

service TaklerService{
    ServiceResponse queue(1:string node_path)
    ServiceResponse run(1:string node_path)
    ServiceResponse init(1:string node_path, 2:string task_id)
    ServiceResponse complete(1:string node_path)
    ServiceResponse abort(1:string node_path)
    ServiceResponse kill(1:string node_path)

    ServiceResponse bunch_tree()

    ServiceResponse add_suite(1:string suite_json_str)
        throws (1:InvalidRequestException ire)

    ServiceResponse update_suite(1:string suite_json_str)
        throws (1:InvalidRequestException ire)

    ServiceResponse update_node(1:string node_path, 2:string node_json_str)
        throws (1:InvalidRequestException ire)
}