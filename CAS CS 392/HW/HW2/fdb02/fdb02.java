import java.util.Scanner;

public class fdb02{
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt(), m = scanner.nextInt();

        long[] a = new long[n];
        for(int i=0; i<n; i++) a[i] = scanner.nextLong();

        long[] p = new long[n+1], q = new long[n+1];
        for(int i=1; i<n; i++) if(a[i] < a[i-1]) p[i] = a[i - 1] - a[i];
        for(int i=1; i<n; i++) if(a[i] > a[i-1]) q[i] = a[i] - a[i - 1];

        for(int i=1; i<n; i++) p[i] += p[i-1];
        for(int i=n-1; i>=1; i--) q[i-1] += q[i];

        while (m-->0) 
        {
            int l = scanner.nextInt(), r = scanner.nextInt();

            if(l < r) System.out.println(p[r-1] - p[l-1]);
            else System.out.println(q[r-1] - q[l-1]);
        }

        scanner.close();
    }
}
