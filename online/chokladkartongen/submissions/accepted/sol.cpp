#include <iostream>
using namespace std;
 
int main(){
	int antal_observationer;
	cin >> antal_observationer;
	int antal = 0;
	int last = 100;
	for (int i=0; i<antal_observationer; i++){
		int tmp;
		cin >> tmp;
		if (tmp > last)
			antal++;
		last = tmp;
	}
	cout << antal << endl;
	return 0;
}
