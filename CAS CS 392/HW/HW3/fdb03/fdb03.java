import java.util.*;

public class fdb03{
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int t = scanner.nextInt();

        while(t-->0)
        {
            int n = scanner.nextInt(), m = scanner.nextInt();

            long[] a = new long[n];
            for(int i=0; i<n; i++) a[i] = scanner.nextLong();

            long[] b = new long[m];
            for(int i=0; i<m; i++) b[i] = scanner.nextLong();

            Arrays.sort(b);

            long prev = -(((long) 1) << 60);
            for(int i=0; i<n; i++)
            {
                // Using Binary Search to find b[j] such that b[j] >= a[i] + prev.
                // DO NOT EDIT THIS! IT IS CORRECT!
                int l = 0, r = m - 1;

                while(l < r)
                {
                    int mid = (l + r) / 2;

                    if(b[mid] >= a[i] + prev) r = mid;
                    else l = mid + 1;
                }
                    
                // Try to minimize a[i] by setting a[i] = b[j] - a[i] while making sure that a[i] >= a[i-1]
                if(b[l] >= a[i] + prev)
                {
                    if(i != 0 && a[i] >= a[i-1]) a[i] = Math.min(a[i], b[l] - a[i]);
                    else a[i] = b[l] - a[i];
                }
                    
                prev = a[i];
            }
                
            boolean ok = true;
            for(int i=0; i<n-1; i++) if(a[i] > a[i + 1]) ok = false;

            if(ok) System.out.println("Yes");
            else System.out.println("No");
        }

        scanner.close();
    }
}
