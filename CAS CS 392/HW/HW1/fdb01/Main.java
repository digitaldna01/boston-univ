import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int t = scanner.nextInt();

        while (t-- > 0) {
            int n = scanner.nextInt();
            int a = scanner.nextInt();
            int b = scanner.nextInt();
            int c = scanner.nextInt();

            int d = n / (a + b + c);

            if (d * a + d * b + d * c >= n) {
                System.out.println(3 * d);
            } else if (d * a + d * b + d * c + a >= n) {
                System.out.println(3 * d + 1);
            } else {
                System.out.println(3 * d + 2);
            }
        }

        scanner.close();
    }
}
