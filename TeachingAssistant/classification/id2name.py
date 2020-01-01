

def get_id2name_dict():
    id2name_path = r''
    id2name_dict = {}
    with open(id2name_path,'r',encoding='utf-8') as f:
        for line in f:
            sid,name = line.strip().split('\t')[0],line.strip().split('\t')[1]
            id2name_dict[name] = sid
            print(sid,name)
    print(id2name_dict)
    return id2name_dict
