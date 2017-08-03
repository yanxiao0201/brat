#!/usr/bin/env python2.7

import sys, os, re, bisect, glob

'''
Convert brat annotations to graphs using graphviz.
Dependency: graphviz.
(installation on Ubuntu:
https://stackoverflow.com/questions/34228395/ubuntu-graphviz-sfdp-not-working)
All "<COLLECTION>/*.ann"s will be converted.
Graphs and intermediate results are saved in "graph/".
STARTS indicate the starting character positions of the sub-documents,
e.g. multiple case reports in one document.
If a document name is not in STARTS, assume one sub-document.
'''

COLLECTION = 'data/acrobat_yba'
STARTS = {'example': [0, 634, 2030]} # 3 sub-documents in example.txt


class Node:
    def __init__(self, id, label, type, start_pos):
        self.id = id
        self.label = label
        self.type = type
        self.start_pos = start_pos # starting position in the document
        self.next = [] # e.g. [(<Node>, 'BEFORE'), ...]
        self.attribs = [] # e.g. ['NEG', 'DECREASE_FROM']

    def get_id(self):
        return self.id

    def get_label(self):
        return self.label

    def get_type(self):
        return self.type

    def get_start(self):
        return self.start_pos

    def add_next(self, node, rel_type):
        self.next.append((node, rel_type))

    def get_next(self):
        return self.next

    def is_modifier(self):
        return self.type in ['Qualitative_concept', 'Quantitative_concept', \
        'Anatomical_structure']

    def add_attrib(self, attrib):
        self.attribs.append(attrib)

    def get_attribs(self):
        return self.attribs

    def __str__(self):
        return 'Node %s:\nlabel: %s\ntype: %s\ntype: %s\nattribute: %s\n' \
        'next: %s\n' % \
        (self.id, self.label, self.type, self.start_pos, self.attrib, self.next)


class Graph:
    def __init__(self):
        self.nodes = {}
        self.e_to_t = {} # e.g. {"E2": "T100", ...}
        # cluster == group of overlapping events
        self.clusters = [] # e.g. [["T1", "T2", "T3"], ["E5"], ...]

    def add_node(self, node):
        id = node.get_id()
        assert(id[0] == 'T')
        if id in self.nodes:
            raise RuntimeError('Duplicated nodes: %s and %s' % \
                (self.nodes[id], node))
        self.nodes[id] = node

    def add_duplicated_node(self, new_id, id):
        if not id in self.nodes:
            raise RuntimeError('Cannot find node: %s' % id)
        assert(new_id[0] == 'E' and id[0] == 'T')
        self.e_to_t[new_id] = id

    def get_node(self, id):
        node = self.nodes.get(id)
        if not node:
            node = self.nodes[self.e_to_t[id]]
        return node

    def group_into_new_cluster(self, node_id_list):
        cluster_id = len(self.clusters)
        self.clusters.append(node_id_list)

    def get_node_cluster_id(self, node):
        id = node.get_id()
        for i, node_id_list in enumerate(self.clusters):
            if id in node_id_list:
                return 'cluster_%s' % i
        return None

    def to_dot_language_and_image(self, doc):
        self.transform_e_to_t()
        # Create a list of dot language strings.
        if not doc in STARTS:
            STARTS[doc] = [0] # assuming one sub-document
        ss = ['digraph G {\n  graph [compound=true];\n  ' \
        'edge [fontname = "courier"];\n'] * len(STARTS[doc])
        for node in sort_nicely(self.nodes.values(), key=nodes_to_nums):
            s = '  %s [color=%s,\n     ' \
            'label=<<B><FONT POINT-SIZE="17">%s</FONT></B><br/>(%s)%s>,\n' \
            '     shape=%s];\n' % (node.get_id(), \
                'darkgoldenrod2' if node.is_modifier() else 'coral', 
                node.get_label(), \
                node.get_type(), self.get_attrib_str(node), \
                'ellipse' if node.is_modifier() else 'box')
            for next_node, rel_type in sort_nicely(node.get_next(), key=\
                nodes_with_rel_to_nums):
                s += '  %s -> %s %s;\n' % (node.get_id(), next_node.get_id(), \
                    self.get_arrow_str(node, next_node, rel_type))
            ss[self.get_doc_idx(node, doc)] += s # update one string in ss
        for i, node_id_list in enumerate(self.clusters):
            s = '  subgraph cluster_%s {\n' % i
            sample_node = None
            for node_id in sort_nicely(node_id_list):
                node = self.nodes[node_id]
                s += '    %s;\n' % (node_id)
                if not sample_node:
                    sample_node = node
            s += '    color=lightskyblue;\n  }\n'
            ss[self.get_doc_idx(node, doc)] += s # update one string in ss
        # Output the dot language strings to files.
        # Use them and graphviz to generate the final images.
        for i, s in enumerate(ss):
            s += '}'
            # print s
            fn = 'graph/%s/%s_%s' % (COLLECTION, doc, i)
            with open('%s.txt' % fn, "w") as f:
                f.write(s)
            os.system('dot -x -Goverlap=scale -Tpng %s.txt > %s.png' % (fn, fn))

    def get_attrib_str(self, node):
        attribs = node.get_attribs()
        if attribs:
            return '<br/>(%s)' % ', '.join(attribs)
        else:
            return ''

    def transform_e_to_t(self):
        for i, node_id_list in enumerate(self.clusters):
            self.clusters[i] = [self.e_to_t[id] if id in self.e_to_t else id \
            for id in node_id_list]

    def get_doc_idx(self, node, doc):
        char_index = node.get_start()
        doc_start_indices = STARTS[doc]
        # e.g. 
        # If char_index == 7, doc_start_indices == [0, 1, 5, 10],
        # should return 2.
        # If char_index == 5, doc_start_indices == [0, 1, 5, 10],
        # should return 2.
        i = bisect.bisect_right(doc_start_indices, char_index)
        return i - 1

    def get_arrow_str(self, node, next_node, rel_type):
        li = ['label=%s' % rel_type]
        if rel_type != 'BEFORE':
            li.append('color=gray')
        if not node.is_modifier():
            c1 = self.get_node_cluster_id(node)
            c2 = self.get_node_cluster_id(next_node)
            if c1:
                li.append('ltail=' + c1)
            if c2:
                li.append('lhead=' + c2)
        return str(li).replace("'", '')


def main():
    os.system('rm -rf graph/%s/* && mkdir -p graph/%s' % \
        (COLLECTION, COLLECTION))
    for file in glob.glob(os.path.join(COLLECTION, '*.ann')):
        doc = file.split('/')[-1].split('.')[0]
        graph = brat_to_graph(file)
        graph.to_dot_language_and_image(doc)

def brat_to_graph(file):
    g = Graph()
    with open(file) as f:
        for line in f:
            line = line.rstrip()
            # print line
            ls = line.split()
            c = ls[0][0]
            if c == 'T':
                # Entity or event.
                handle_entity_event(ls, g)
            elif c == 'E':
                # Event.
                handle_event(ls, g)
            elif c == 'R':
                # Relation.
                handle_relation(ls, g)
            elif c == '*':
                # Symmetric relation. In ACROBAT, it is "overlap".\
                handle_symmetric_relation(ls, g)
            elif c == 'A':
                # Attribute.
                handle_attribute(ls, g)
            elif c == '#':
                # Comment.
                continue
            else:
                raise RuntimeError('Unrecognized line: %s' % line)
    return g

def handle_entity_event(ls, g):
    assert(len(ls) >= 5)
    g.add_node(Node(ls[0], ' '.join(ls[4:]), ls[1], int(ls[2])))

def handle_event(ls, g):
    assert(len(ls) == 2)
    g.add_duplicated_node(ls[0], ls[1].split(':')[1])

def handle_relation(ls, g):
    assert(len(ls) == 4)
    t = ls[1]
    node_1 = get_node_from_ls(ls, 2, g)
    node_2 = get_node_from_ls(ls, 3, g)
    if t == 'BEFORE':
        node_1.add_next(node_2, 'BEFORE')
    elif t == 'AFTER':
        node_2.add_next(node_1, 'BEFORE')
    elif t == 'MODIFIER':
        if not node_1.is_modifier():
            raise RuntimeError('%s is actually not a modifier in %s' \
                % (node_1, ls))
        node_1.add_next(node_2, 'MODIFIER')
    elif t == 'DECREASE_TO':
        node_1.add_next(node_2, 'DECREASE_TO')
    elif t == 'DECREASE_FROM':
        node_1.add_next(node_2, 'DECREASE_FROM')
    elif t == 'INCREASE_TO':
        node_1.add_next(node_2, 'INCREASE_TO')
    elif t == 'INCREASE_FROM':
        node_1.add_next(node_2, 'INCREASE_FROM') 
    else:
        raise RuntimeError('Unrecognized relation type for line: %s' % ls)

def handle_symmetric_relation(ls, g):
    assert(len(ls) >= 3)
    assert(ls[1] == 'OVERLAP')
    g.group_into_new_cluster([id for id in ls[2:]])
    pass

def handle_attribute(ls, g):
    assert(len(ls) == 4)
    get_node_from_ls(ls, 2, g, False).add_attrib(ls[3])

def get_node_from_ls(ls, ls_index, g, split=True):
    w = ls[ls_index]
    if split:
        w = w.split(':')[1]
    return g.get_node(w)

'''
Code below is from 
https://stackoverflow.com/questions/4623446/how-do-you-sort-files-numerically.
'''
def tryint(s):
    try:
        return int(s)
    except:
        return s

def strings_to_nums(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def nodes_to_nums(s):
    """ Turn a string (from get_id()) into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s.get_id()) ]

def nodes_with_rel_to_nums(s):
    """ Turn a string (from s[0].get_id()) into a list of string and number 
    chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s[0].get_id()) ]

def sort_nicely(l, key=strings_to_nums):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=key)
    return l

'''
End of borrowing.
'''

if __name__ == '__main__':
    sys.exit(main())
