/*
 * Problem Set 1
 *
 * Practice with static methods, part I
 */

public class Methods {
    /*
     * printVertical - takes a string s and prints the characters of 
     * the string vertically -- with one character per line.
     */
    public static void printVertical(String s) {
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            System.out.println(c);
        }
    }
    /*
     * printWithSpace - takes a string s and prints the characrters of
     * the strinfg separated by spaces -- single space after the last character.
     */
    public static void printWithSpace(String s) {
    	for(int i = 0; i < s.length(); i++) {
    		char c = s.charAt(i);
    		System.out.print(c);
    	}
    }

    public static void main(String[] args) {
        /* Sample test call */
        printVertical("method");        
        printWithSpace("method");

    }
}
