#include <bits/stdc++.h>
#define ll long long
#define pb push_back
 
using namespace std;
 
int main()
{
    ios_base::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
 
	int t = 1;
	cin >> t;
    while(t-->0)
    {
        ll n, m;
        cin >> n >> m;
 
        vector<ll> a(n);
        set<ll> B;
        for(int i=0; i<n; i++) cin >> a[i];
        for(int i=0; i<m; i++)
        {
            ll x;
            cin >> x;
 
            B.insert(x);
        }
 
        ll prev = -(1LL << 60);
        for(int i=0; i<n; i++)
        {
            // Using Binary Search to find b[j] such that b[j] >= a[i] + prev.
            // DO NOT EDIT THIS! IT IS CORRECT!
            auto it = B.lower_bound(a[i] + prev);
 
            // Try to minimize a[i] by setting a[i] = b[j] - a[i] while making sure that a[i] >= a[i-1]
            if(it != B.end())
            {
                if(i != 0 && a[i] >= a[i-1]) a[i] = min(a[i], *it - a[i]);
                else a[i] = *it - a[i];
            }
 
            prev = a[i];
        }
 
        bool ok = true;
        for(int i=0; i<n-1; i++) if(a[i] > a[i+1]) ok = false;
 
        if(ok) cout << "Yes\n";
        else cout << "No\n";
    }
}