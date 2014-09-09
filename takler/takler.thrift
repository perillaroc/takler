namespace py takler_service

struct ServiceResponse{
1: i64 flag,
2: string str
}

service TaklerService{
    ServiceResponse queue(1:string node_path)
    ServiceResponse run(1:string node_path)
    ServiceResponse init(1:string node_path, 2:string task_id)
    ServiceResponse complete(1:string node_path)
    ServiceResponse abort(1:string node_path)
    ServiceResponse kill(1:string node_path)
    ServiceResponse bunch_tree()
}