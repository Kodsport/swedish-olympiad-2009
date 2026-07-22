#include <bits/stdc++.h>
using namespace std;

using ll = long long;
using vi = vector<ll>;
using vvi = vector<vi>;
using p2 = pair<ll, ll>;
const ll inf = 1e18;

#define rep(i,n) for (ll i = 0; i < (n); i++)
#define repp(i,a,n) for (ll i = (a); i < (n); i++)
#define repe(i, arr) for (auto& i : arr)
#define all(x) begin(x),end(x)
#define sz(x) ((ll)(x).size())

struct node
{
    char curr;
    map<char, node*> next;
    set<string> finished;
};

void addword(string& word, int index, node* n)
{
    if (index == sz(word)-1)
    {
        n->next[word[index]] = new node{ word[index],{}, {} };
        n->next[word[index]]->finished.insert(word);
        return;
    }

    char c = word[index];
    if (n->next.count(c))
    {
        addword(word, index + 1, n->next[c]);
    }
    else
    {
        n->next[word[index]] = new node{ word[index],{}, {} };
        addword(word, index + 1, n->next[word[index]]);
    }
}

int winning(node* n, string word, bool anna)
{
    int ret = (anna) ? -2 : 2;

    if (n->next.size() == 0 || n->finished.count(word))
    {
        return (anna) ? 1 : -1;
    }
    else
    {

        repe(n, n->next)
        {
            int r = winning(n.second, word + n.first, !anna);
            if (anna)
            {
                ret = max(ret, r);
            }
            else
            {
                ret = min(ret, r);
            }
        }
        
    }

    return ret;
}


int main() {
    cin.tie(0)->sync_with_stdio(0);

    int n;
    cin >> n;
    
    node* parent = new node{ '-', {} };

    set<char> upperCase;
    repp(c,'A','Z'+1) upperCase.insert(c);

    repe(c, upperCase)
    {
        parent->next[c] = new node{ c, {}, {} };
    }

    rep(i, n)
    {
        string word;
        cin >> word;
        transform(all(word), begin(word), ::toupper);
        if (word.size() == 1) parent->next[word[0]]->finished.insert(word);
        else addword(word, 1, parent->next[word[0]]);
    }

    vector<char> ans;
    repe(c, upperCase)
    {
        if (winning(parent->next[c], string(1,c), false) == 1)
        {
            ans.push_back(c);
        }
    }
    rep(i,sz(ans)) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    cout << endl;
    _Exit(0); // address sanitizer sidestep
}
