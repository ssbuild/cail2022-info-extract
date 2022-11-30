# @Time    : 2022/4/10 20:07
# @Author  : tk
import json


def get_label_from_entity(text,pos,entities):
    for label in entities:
        o = entities[label]
        if text not in o:
            continue
        pt_list = o[text]
        for pt in pt_list:
            if pt[0] == pos[0] and pt[1] == pos[1]:
                return label
    return None

def get_pos(text: str,k: str):
    p = text.find(k)
    assert p != -1, k
    if p == -1:
        return None
    return [p,p+len(k) -1]

def convert2fastlabel(in_file,out_file):

    with open(in_file,mode='r',encoding='utf-8') as f:
        lines = f.readlines()
    with open(out_file,mode='w',encoding='utf-8',newline='\n') as f_out:
        for i,line in enumerate(lines):
            jd = json.loads(line)
            text = jd['text']

            entities = {}
            re_list = []

            spo_list = jd['spo_list']

            try:
                for spo in spo_list:
                    subject = spo['subject']
                    subject_type = spo['subject_type']
                    predicate = spo['predicate']
                    objects = spo['object']
                    object_types = spo['object_type']

                    if subject_type not in entities:
                        entities[subject_type] = {}
                    if subject not in entities[subject_type]:
                        entities[subject_type][subject] = []

                    s_pos = get_pos(text,subject)
                    entities[subject_type][subject].append(s_pos)

                    if s_pos is not None:
                        for k in objects.keys():
                            object = objects[k]
                            object_type = object_types[k]

                            if object_type not in entities:
                                entities[object_type] = {}
                            if object_type not in entities[object_type]:
                                entities[object_type][object] = []
                            o_pos = get_pos(text, object)
                            entities[object_type][object].append(o_pos)


                            re_list.append({
                                predicate:[
                                    {
                                        'entity': subject,
                                        'pos': s_pos,
                                        'label': subject_type
                                    },
                                    {
                                        'entity': object,
                                        'pos': o_pos,
                                        'label': object_type
                                    }
                                ]
                            })

                f_out.write(json.dumps({
                    "id": i,
                    "text": text,
                    "entities": entities,
                    're_list': re_list
                }, ensure_ascii=False) + '\n')
            except Exception as e:
                print(text,' error,',e)
                continue





def convert2labels(src,dst):
    with open(src, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(dst, mode='w', encoding='utf-8', newline='\n') as f_out:
        labels = set()
        for line in lines:
            jd = json.loads(line)
            if not jd:
                continue
            for o in list(jd['object_type'].values()):
                labels.add((jd['subject_type'],jd['predicate'],o))

        print(labels)
        print(len(labels))
        for l in labels:
            f_out.write(json.dumps(l,ensure_ascii=False) + '\n')



if __name__ == "__main__":
    in_file = r'F:\nlpdata_2022\比赛\百度关系\关系抽取\json\duie_train.json'
    out_file =r'F:\nlpdata_2022\比赛\百度关系\关系抽取\fastlabel_json\duie_train.json'
    convert2fastlabel(in_file,out_file)

    in_file = r'F:\nlpdata_2022\比赛\百度关系\关系抽取\json\duie_dev.json'
    out_file = r'F:\nlpdata_2022\比赛\百度关系\关系抽取\fastlabel_json\duie_dev.json'
    convert2fastlabel(in_file, out_file)

    in_file = r'F:\nlpdata_2022\比赛\百度关系\关系抽取\json\duie_schema.json'
    out_file = r'F:\nlpdata_2022\比赛\百度关系\关系抽取\fastlabel_json\duie_schema.json'
    convert2labels(in_file, out_file)


