#include <cstdio>
#include <string>
#include <iostream>

using namespace std;

int main(int argc, char const *argv[])
{
	string time;
	int x0,y0,z0, x1,y1,z1, x2,y2,z2;

	while(cin >> time)
	{
		scanf("%d %d %d\n%d %d %d\n%d %d %d\n", &x0, &y0, &z0, &x1, &y1, &z1, &x2, &y2, &z2);
		cout << time << endl;
	}
	return 0;
}