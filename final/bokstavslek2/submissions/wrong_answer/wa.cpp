#include <iostream>
#include <fstream>
#include <string>
 
const bool ANNA = 1, BOSSE = 0;
 
class node {
    protected:
    node* branch[28];
    int status;
    node(int n);
    public:
    friend class tree;
};
 
node::node(int n) {
    for (int i = 0; i < 28; ++i) {
        branch[i] = NULL;
    }
    status = n;
}
 
class tree {
    void insertMechanics(node*& place, std::string sTemp, int nDepth);
    node* root;
    bool Search(node*& curr, int player);
    public:
    tree();
    void insert(std::string sTemp);
    bool anna(int n);
};
 
tree::tree() {
    root = new node(1);
}
 
bool tree::Search(node*& curr, int player) {
    if (curr->status == ANNA)
        return ANNA;
    if (curr->status == BOSSE)
        return BOSSE;
 
    if (player == ANNA) {
        for (int i = 0 ; i < 28; ++i) {
            if (curr->branch[i] != NULL) {
                if (Search(curr->branch[i], BOSSE) == ANNA) {
                    return ANNA;
                }
            }
        }
        return BOSSE;
    }
    if (player == BOSSE) {
        for (int i = 0 ; i < 28; ++i) {
            if (curr->branch[i] != NULL) {
                if (Search(curr->branch[i], ANNA) == BOSSE) {
                    return BOSSE;
                }
            }
        }
        return ANNA;
    }
};
 
bool tree::anna(int n) {
    if (root->branch[n] == NULL)
        return BOSSE;
    return Search(root->branch[n], BOSSE);
}
 
void tree::insertMechanics(node*& place, std::string sTemp, int nDepth) {
    if (nDepth == sTemp.length()-1) {
        if (place->branch[sTemp[nDepth]-'A'] == NULL) {
            place->branch[sTemp[nDepth]-'A'] = new node(!(nDepth%2 == 0));
        } else {
            place->branch[sTemp[nDepth]-'A']->status = !(nDepth%2);
        }
    } else if (nDepth < sTemp.length()) {
        if (place->branch[sTemp[nDepth]-'A'] == NULL) {
            place->branch[sTemp[nDepth]-'A'] = new node(-1);
        }
        insertMechanics(place->branch[sTemp[nDepth]-'A'], sTemp, nDepth+1);
    }
    return;
}
 
void tree::insert(std::string sTemp) {
    insertMechanics(root, sTemp, 0);
}
 
int main() {
    std::ifstream fin("bokstav5.dat");
    tree tr;
    int nOrd;
	std::cin >> nOrd;
    for (int i = 0; i < nOrd; ++i) {
        std::string sTemp;
		std::cin >> sTemp;
        tr.insert(sTemp);
    }
    for (int i = 0; i < 28; ++i) {
        if (tr.anna(i)) {
            std::cout << char (i + 'A') << ' ';
        }
    }
    std::cout << "asd" << '\n';
    return 0;
}
