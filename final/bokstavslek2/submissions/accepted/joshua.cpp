#include <bits/stdc++.h>

using namespace std;

#pragma GCC target ("avx2")
#pragma GCC optimization ("O3")
#pragma GCC optimization ("unroll-loops")

#define ll long long
#define vi vector<ll>
#define vvi vector<vi>
#define p2 pair<ll, ll>
#define p3 tuple<ll,ll,ll>
#define p4 vi
#define ip3 tuple<int,int,int>
#define ip4 tuple<int,int,int,int>
#define vp2 vector<p2>
#define vp3 vector<p3>
#define inf 2e9
#define linf 1e17

#define read(a) cin >> a
#define write(a) cout << (a) << "\n"
#define dread(type, a) type a; cin >> a
#define dread2(type, a, b) dread(type, a); dread(type, b)
#define dread3(type, a, b, c) dread2(type, a, b); dread(type, c)
#define dread4(type, a, b, c, d) dread3(type, a, b, c); dread(type, d)
#define dread5(type, a, b, c, d, e) dread4(type, a, b, c, d); dread(type, e)
#ifdef _DEBUG
#define deb __debugbreak();
#else
#define deb ;
#endif

#define rep(i, high) for (ll i = 0; i < high; i++)
#define repp(i, low, high) for (ll i = low; i < high; i++)
#define repe(i, container) for (auto& i : container)
#define per(i, high) for (ll i = high; i >= 0; i--)

#define readpush(type,vect) type temp; read(temp); vect.push_back(temp);
#define readvector(type, name, size) vector<type> name(size); rep(i,size) {dread(type,temp); name[i]=temp;}
#define readinsert(type,a) {type temp; read(temp); a.insert(temp);}
#define all(a) begin(a),end(a)
#define setcontains(set, x) (set.find(x) != set.end())
#define stringcontains(str, x) (str.find(x) != string::npos)
#define within(a, b, c, d) (a >= 0 && a < b && c >= 0 && c < d)

#define ceildiv(x,y) ((x + y - 1) / y)
#define fract(a) (a-floor(a))
#define sign(a) ((a>0) ? 1 : -1)

auto Start = chrono::high_resolution_clock::now();

inline void fast()
{
    ios::sync_with_stdio(false);
    cin.tie(NULL); cout.tie(NULL);
}

struct node
{
    char curr;
    map<char, node*> next;
    set<string> finished;
};

void addword(string& word, int index, node* n)
{
    if (index == word.size()-1)
    {
        n->next[word[index]] = new node{ word[index],{}, {} };
        n->next[word[index]]->finished.insert(word);
        return;
    }

    char c = word[index];
    if (setcontains(n->next, c))
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
    int ret = (anna) ? -inf : inf;

    if (n->next.size() == 0 || setcontains(n->finished, word))
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

int main()
{
    fast();

#if 0
    ifstream cin("C:\\Users\\Matis\\source\\repos\\Comp prog\\x64\\Debug\\in.txt");
#endif

    dread(int, n);
    
    node* parent = new node{ '-', {} };

    set<char> upperCase = { 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' };

    repe(c, upperCase)
    {
        parent->next[c] = new node{ c, {}, {} };
    }

    rep(i, n)
    {
        dread(string, word);
        transform(all(word), begin(word), ::toupper);
        if (word.size()==1)
        {
            continue;
        }
        addword(word, 1, parent->next[word[0]]);

    }

    repe(c, upperCase)
    {
        if (winning(parent->next[c], string(1,c), false) == 1)
        {
            cout << c << " ";
        }
    }

    cout << endl;
    _Exit(0);
}
