#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: construct_candidate.py
"""

from __future__ import print_function
import sys
import json
import random
import collections

def load_candidate_set(candidate_set_file):
    """
    load candidate set
    """
    candidate_set = []
    for line in open(candidate_set_file, encoding="utf-8"):
        candidate_set.append(json.loads(line.strip(), encoding="utf-8"))

    return candidate_set


def candidate_slection(candidate_set, knowledge_dict, slot_dict, candidate_num=10):
    """
    candidate slection
    """
    random.shuffle(candidate_set)
    candidate_legal = []
    for candidate in candidate_set:
        is_legal = True
        for slot in slot_dict:
            if slot in ["topic_a", "topic_b"]:
                continue
            if slot in candidate:
                if slot not in knowledge_dict:
                    is_legal = False
                    break
                w_ = random.choice(knowledge_dict[slot])
                candidate = candidate.replace(slot, w_)

        for slot in ["topic_a", "topic_b"]:
            if slot in candidate:
                if slot not in knowledge_dict:
                    is_legal = False
                    break
                w_ = random.choice(knowledge_dict[slot])
                candidate = candidate.replace(slot, w_)

        if is_legal and candidate not in candidate_legal:
            candidate_legal.append(candidate)

        if len(candidate_legal) >= candidate_num:
            break

    return candidate_legal


def get_candidate_for_conversation(conversation, candidate_set, candidate_num=10):
    """
    get candidate for conversation
    """
    candidate_set_gener, candidate_set_mater, candidate_set_list, slot_dict = candidate_set

    chat_path = conversation["goal"]
    knowledge = conversation["knowledge"]
    history = conversation["history"]

    topic_a = chat_path[0][1]
    topic_b = chat_path[0][2]
    domain_a = None
    domain_b = None
    knowledge_dict = {"topic_a":[topic_a], "topic_b":[topic_b]}
    for i, [s, p, o] in enumerate(knowledge):
        p_key = ""
        if topic_a.replace(' ', '') == s.replace(' ', ''):
            p_key = "topic_a_" + p.replace(' ', '')
            if u"??????" == p:
                domain_a = o
        elif topic_b.replace(' ', '') == s.replace(' ', ''):
            p_key = "topic_b_" + p.replace(' ', '')
            if u"??????" == p:
                domain_b = o

        if p_key == "":
            continue

        if p_key in knowledge_dict:
            knowledge_dict[p_key].append(o)
        else:
            knowledge_dict[p_key] = [o]

    assert domain_a is not None and domain_b is not None

    key = '_'.join([domain_a, domain_b, str(len(history))])

    candidate_legal = []
    if key in candidate_set_gener:
        candidate_legal.extend(candidate_slection(candidate_set_gener[key],
                                                  knowledge_dict, slot_dict,
                                                  candidate_num = candidate_num - len(candidate_legal)))

    if len(candidate_legal) < candidate_num and key in candidate_set_mater:
        candidate_legal.extend(candidate_slection(candidate_set_mater[key],
                                                  knowledge_dict, slot_dict,
                                                  candidate_num = candidate_num - len(candidate_legal)))

    if len(candidate_legal) < candidate_num:
        candidate_legal.extend(candidate_slection(candidate_set_list,
                                                  knowledge_dict, slot_dict,
                                                  candidate_num = candidate_num - len(candidate_legal)))

    return candidate_legal


def construct_candidate_for_corpus(corpus_file, candidate_set_file, candidate_file, candidate_num=10):
    """
    construct candidate for corpus

    case of data in corpus_file:
    {
        "goal": [["START", "??? ?? ??????", "????????? ?? ?????????"]],
        "knowledge": [["??? ?? ??????", "??????", "?????? ??? ??????"]],
        "history": ["??? ??? ?????? ????????? ??? ?????? ??? ?????? ??? ???",
                    "?????? ??? ??? ?????? ?????? ??? ??? ??? ??? ?????? ?????? ?????? ???"]
    }

    case of data in candidate_file:
    {
        "goal": [["START", "??? ?? ??????", "????????? ?? ?????????"]],
        "knowledge": [["??? ?? ??????", "??????", "?????? ??? ??????"]],
        "history": ["??? ??? ?????? ????????? ??? ?????? ??? ?????? ??? ???",
                    "?????? ??? ??? ?????? ?????? ??? ??? ??? ??? ?????? ?????? ?????? ???"],
        "candidate": ["??? ??? ??? ??? ??? ?? ?????? ???",
                      "??? ??? ??? ??? ??? ?? ?????? ???"]
    }
    """
    candidate_set = load_candidate_set(candidate_set_file)
    fout_text = open(candidate_file, 'w', encoding="utf-8")
    with open(corpus_file, 'r', encoding="utf-8") as f:
        for i, line in enumerate(f):
            conversation = json.loads(line.strip(), encoding="utf-8", \
                                 object_pairs_hook=collections.OrderedDict)
            candidates = get_candidate_for_conversation(conversation,
                                                        candidate_set,
                                                        candidate_num=candidate_num)
            conversation["candidate"] = candidates

            conversation = json.dumps(conversation, ensure_ascii=False)
            fout_text.write(conversation + "\n")

    fout_text.close()


def main():
    """
    main
    """
    construct_candidate_for_corpus(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nExited from the program ealier!")
