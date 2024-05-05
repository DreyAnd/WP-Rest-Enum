import requests 
import sys 
import json 
import threading

def pull_namespaces(target):
    try:
        resp = requests.get(target + "/wp-json").json()
        namespaces = resp['namespaces']
        return namespaces 
    except:
        print(f"[-] {target} does not have an open WP Rest API.")
        return False

def enum_namespace(target, namespace):
    start = target + "/wp-json/" + namespace
    resp = requests.get(start).text

    routes_list = []
    if "routes" in resp:
        resp_json = json.loads(resp)
        routes = resp_json['routes']
        for obj in routes:
            routes_list.append(obj)
    
    enum_routes(target, routes_list)

def fill_id(route):
    route = route.split("/")
    c = 0
    for part in route:
        if "(?P" in part:    
            route[c] = "123"
        c += 1

    route = "/".join(route)
    return route
            
def enum_routes(target, routes_list):
    for route in routes_list:
        if "(?P" in route:
            route = fill_id(route)

        target_route = target + "/wp-json" + route
        r = requests.get(target_route)
        if r.status_code == 401:
            print(f"- {target_route} [401] [GET]")
        elif r.status_code == 404:
            r1 = requests.post(target_route)
            print(f"- {target_route} [{r1.status_code}] [POST]")
        else:
            print(f"- {target_route} [{r.status_code}] [GET]")

def enum_namespace_wrapper(target, namespace):
    threading.Thread(target=enum_namespace, args=(target, namespace)).start()

def main():
    target = sys.argv[1]
    namespaces = pull_namespaces(target)

    if namespaces:
        for namespace in namespaces:
            enum_namespace_wrapper(target, namespace)

if __name__ == "__main__":
    main()
