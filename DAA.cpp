
#include <iostream>
using namespace std;

int main()
{
    int n;
    int a = 0, b = 1, c;
    int count = 0;

    cout << "Enter the number of terms: ";
    cin >> n;

    cout << "Fibonacci Series: ";

    for (int i = 0; i < n; i++)
    {
        cout << a << " ";
        count++;

        c = a + b;
        count++;

        a = b;
        count++;

        b = c;
        count++;
    }

    cout << "\nStep Count: " << count;

    return 0;
}
