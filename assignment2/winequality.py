from __future__ import print_function
import sys
import math

class Node:
    def __init__(self, leaf=False):
        self.attr = None
        self.splitval = None
        self.leaf = leaf

        self.left = None
        self.right = None

        if leaf == True:
            self.label = None

def get_labels(data):
    # all the label here
    labels = [num[1] for num in data]
    # Create a list named lable.
    label = []
    # create a list of value.
    value = []
    # traverse for all elements
    for x in labels:
        # check if exists in unique_list or not
        if x not in label:
            label.append(x)
    for x in label:
        count = 0
        for y in labels:
            if x == y:
                count = count + 1
            else:
                continue
        value.append(count)
    # Merge to form a dictionary 
    return dict( zip ( label , value) )

def check_length_attr(data):
    check_len = [num[0] for num in data]
    if len(check_len) == 1:
        return True
    else:
        return False

# entrophy to find the root (what attr has the highest score)
def entropy(data):
    length = len(data)
    counter = get_labels(data)

    entropy = 0.0

    for label, value  in counter.items():
        a = float(value) / length
        entropy += - (a * math.log(a, 2))

    return entropy

# split data
def split_data(data, attr, splitval):
    left_tree = []
    right_tree = []
    for entry in data:
        x = entry[0]
        if x[attr] <= splitval:
            left_tree.append(entry)
        else:
            right_tree.append(entry)
    return (left_tree, right_tree)

#function choose split data
def choose_split(data):
    n = len(data)
    max_gain = 0
    best_attr = None
    label_entropy = entropy(data)
    for attr in range(len(data[0][0])):
        data.sort(key= lambda x: x[0][attr])
        for i in range(len(data) - 1):
            splitval = 0.5 * (data[i][0][attr] + data[i+1][0][attr])
            px1 = float(i+1)/n
            px2 = float(n - i - 1) / n
            left, right = split_data(data, attr, splitval)
            if len(left) == 0 or len(right) == 0:
                continue
            left_entropy = entropy(left)
            right_entropy = entropy(right)
            gain = label_entropy - (px1 * left_entropy + px2 * right_entropy)
            if gain > max_gain:
                best_attr = attr
                best_split = splitval
                max_gain = gain
    
    return (best_attr, best_split)

def DTL(data, minleaf):
    N = len(data)
    labels_count = get_labels(data)
    if N <= minleaf or len(labels_count) == 1 or check_length_attr(data):
        leaf_node = Node(leaf=True)
        max_freq = 0
        label = ""
        tie = False
        for l, val in labels_count.items():
            if val > max_freq:
                max_freq = val
                label = l
                tie = False
            elif val == max_freq:
                tie = True
        if not tie:
            leaf_node.label = label
        return leaf_node
    
    attr, splitval = choose_split(data)
    node = Node()
    node.attr = attr
    node.splitval = splitval
    left_data, right_data = split_data(data, attr, splitval)
    node.left = DTL(left_data, minleaf)
    node.right = DTL(right_data, minleaf)
    return node

def predict(node, data):
    while not node.leaf:
        if data[node.attr] <= node.splitval:
            node  = node.left
        else:
            node = node.right
    return node.label

def main():
    train_path = sys.argv[1]
    test_path = sys.argv[2]
    minleaf = int(sys.argv[3])

    train_file = open(train_path)
    test_file = open(test_path)
    
    # get rid off the attribute header later
    string_header = train_file.readline().strip().split()
    
    # Modify train data 
    train_array = []
    for line in train_file.readlines():
        X = [float(val) for val in line.strip().split()]
        Y = X[11]
        # get rid the label off of the X sample
        X.pop()
        # push to train
        train_array.append([X, Y])
    
    # Modify Test Data
    test_array = []
    test_file.readline() # Skip headers
    for line in test_file.readlines():
        X = [float(val) for val in line.strip().split()]
        # Push to test array
        test_array.append(X)

    #print(get_unique_labels(train_array))
    #print(check_length_attr(train_array))
    #print(entropy(train_array))
    print(choose_split(train_array))
    
    '''
    # the Decision tree learning model here
    best_value = DTL(train_array, minleaf) # find best attribute, best split value

    for test_data in test_array:
        # run model against testing data
        print(predict(best_value, test_data))
    '''
if __name__ == '__main__':
    main()
   