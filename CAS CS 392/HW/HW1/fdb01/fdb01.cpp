#include <iostream>
using namespace std;

int main() {
    int t;
    cin >> t;

    while (t--) {
        int n, a, b, c;
        cin >> n >> a >> b >> c;

        int d = n / (a + b + c);

        if (d * a + d * b + d * c >= n) {
            cout << 3 * d << endl;
        } else if (d * a + d * b + d * c + a >= n) {
            cout << 3 * d + 1 << endl;
        } else {
            cout << 3 * d + 2 << endl;
        }
    }

    return 0;
}
