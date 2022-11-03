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



def convert2fastlabel(src,dst):
    with open(src,mode='r',encoding='utf-8') as f:
        lines = f.readlines()
    with open(dst,mode='w',encoding='utf-8',newline='\n') as f_out:
        for i,line in enumerate(lines):
            jd = json.loads(line)
            text = jd['sentText']
            entity_list = jd['entityMentions']
            entities_new = {}
            for es in entity_list:
                s = es['start']
                e = es['end'] - 1
                l = es['label']
                if l not in entities_new:
                    entities_new[l] = {}
                l_o = entities_new[l]
                e_text = text[s:e + 1]
                if e_text not in l_o:
                    l_o[e_text] = []
                l_o[e_text].append([s,e])


            re_list = jd['relationMentions']

            re_list_new = []
            for relation in re_list:
                e1start = relation['e1start']
                em1Text = relation['em1Text']

                e21start = relation['e21start']
                em2Text = relation['em2Text']
                label =  relation['label']

                pos1 = [e1start,e1start + len(em1Text) -1]
                pos2 = [e21start,e21start + len(em2Text) -1]
                label1 = get_label_from_entity(em1Text, pos1, entities_new)
                label2 = get_label_from_entity(em2Text, pos2, entities_new)

                assert label1 is not None and label2 is not None
                entity1 = {
                    'entity': em1Text,
                    'pos': pos1,
                    'label': label1,
                }

                entity2 = {
                    'entity': em2Text,
                    'pos': pos2,
                    'label': label2,
                }

                re_list_new.append(
                    {
                        label: [
                            entity1,entity2
                        ]
                    }
                )


            f_out.write(json.dumps({
                "id":i,
                "text":text,
                "entities":entities_new,
                're_list': re_list_new
            },ensure_ascii=False) + '\n')




if __name__ == "__main__":
    convert2fastlabel(r'F:\nlpdata_2022\比赛\法研杯\cail2022_信息抽取_第一阶段\step1_train.json',
                      r'F:\nlpdata_2022\比赛\法研杯\cail2022_信息抽取_第一阶段\step1_train-fastlabel.json')