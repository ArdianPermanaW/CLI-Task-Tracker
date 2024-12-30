import argparse
import json
import os

parser = argparse.ArgumentParser() #main parser
subparsers = parser.add_subparsers(dest="command", help="the commands") #sub parser

add = subparsers.add_parser("add", help="add task to task tracker")
add.add_argument("task", type=str, help="task added")

update = subparsers.add_parser("update", help="update task at id in task tracker")
update.add_argument("id", type=int, help="id of the task")
update.add_argument("task", type=str, help="task updated to")

delete = subparsers.add_parser("delete", help="delete task at id in task tracker")
delete.add_argument("id", type=int, help="id of the task")

mark = subparsers.add_parser("mark", help="next put inprogress or done to mark that at id")
mark.add_argument("id", type=int, help="id of the task")
mark.add_argument("markType", type=str, help="change type of mark at id")

listData = subparsers.add_parser("list", help="lists data")
listData.add_argument("listType", help="all, todo, inprogress, done")


args = parser.parse_args()

file_path = 'data.json'

def save(data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

if args.command == "add":
    with open(file_path, 'r') as file:
        data = json.load(file)
        if os.path.getsize(file_path) == 0:
            data = []
            addId = 1
        else:
            existingId = {entry['id'] for entry in data}
            addId = 1
            while addId in existingId:
                addId += 1
                
        addData = {"id": addId, "task": args.task, "status": "todo"}
        data.append(addData)
        data.sort(key=lambda x: x['id'])
        save(data)
        print(f"Task added successfully (ID:{addId})")

elif args.command == "update":
    with open(file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            if item.get('id') == args.id:
                item['task'] = args.task
                print(f"Data at ID:{args.id} updated to {args.task}")
                break
        else:
            print(f"ID:{args.id} not found")

        save(data)

elif args.command == "delete":
    with open(file_path, 'r') as file:
        data = json.load(file)
        updateData = [item for item in data if item.get('id') != args.id]

        if len(updateData) != len(data):
            print(f"Data at ID:{args.id} deleted") 
        else:
            print(f"ID:{args.id} not found.")
        
        save(updateData)

elif args.command == "mark":
    if args.markType in ["inprogress", "done"]:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                if item.get('id') == args.id:
                    item['status'] = args.markType
                    print(f"Data at ID:{args.id} marked {args.markType}")
                    break
            else:
                print(f"ID:{args.id} not found")

            save(data)
        
    else:
        print("invalid mark type")

elif args.command == "list":
    with open(file_path, 'r') as file:
        data = json.load(file)
        if args.listType in ["todo", "inprogress", "done"]:
            filteredData = [entry for entry in data if str(entry.get("status", '')).lower() == str(args.listType).lower()]
            if filteredData:
                print(json.dumps(filteredData, indent=4))
            else:
                print("not found")
        elif args.listType == "all":
            print(json.dumps(data, indent=4))
        else:
            print("invalid list type")


    


