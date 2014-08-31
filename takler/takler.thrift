namespace py takler_service

struct ServiceResponse{
1: i64 flag,
2: string str
}

service TaklerService{
    ServiceResponse init(1:string node_path, 2:string node_rid)
    ServiceResponse complete(1:string node_path)
    ServiceResponse abort(1:string node_path)
}