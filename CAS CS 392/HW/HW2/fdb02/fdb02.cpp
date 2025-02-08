#include<iostream>
#include<vector>

using namespace std;

#define ll long long

int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    ll n, m;
    cin >> n >> m;

    vector<ll> a(n);
    for(int i=0; i<n; i++) cin >> a[i];

    vector<ll> p(n+1, 0), q(n+1, 0);
    for(int i=1; i<n; i++) if(a[i] < a[i-1]) p[i] = a[i - 1] - a[i];
    for(int i=1; i<n; i++) if(a[i] > a[i-1]) q[i] = a[i] - a[i - 1];

    for(int i=1; i<n; i++) p[i] += p[i-1];
    for(int i=n-1; i>=1; i--) q[i-1] += q[i];

    while(m-->0)
    {
        ll l, r;
        cin >> l >> r;

        if(l < r) cout << p[r-1] - p[l-1] << "\n";
        else cout << q[r-1] - q[l-1] << "\n";
    }
}