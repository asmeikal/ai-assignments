import it.uniroma1.di.tmancini.utils.*;
import it.uniroma1.di.tmancini.teaching.ai.SATCodec.*;
import java.util.*;

public class SATtoQueens {

	public static void main(String args[]) throws java.io.IOException, java.io.FileNotFoundException {
		
		SATModelDecoder md = new SATModelDecoder(args);
		md.run();
	
		int maxVar = md.getMaxVar();		
		int n = (int)Math.sqrt(maxVar);
	
		//System.out.println("MaxVar = " + maxVar + " --> N = " + n);
		char[][] board = new char[n][n];
		
		for (int i=0; i<n; i++) {
			for(int j=0; j<n; j++) {
				board[i][j] = '-';
			}
		}
		
		for (int i=1; i <= maxVar; i++) {
			Boolean v_i = md.getModelValue(i);
			if (v_i == null || !v_i) continue; // false or don't care literal
			
			SATModelDecoder.Var var = md.decodeVariable(i);
			int x = var.getIndices().get(0)-1;
			int y = var.getIndices().get(1)-1;
			assert 0 <= x && x < n;
			assert 0 <= y && y < n;
			board[x][y] = 'Q';
		}
		
		// Print-out chessboard
		
		printRow(3*n+2);
		
		for (int i=0; i<n; i++) {	
			System.out.print("|");
			for(int j=0; j<n; j++) {
				System.out.print(" " + board[i][j] + " ");
			}
			System.out.println("|");
			printRow(3*n+2);
		}
				
	}
	
	private static void printRow(int n) {
		for(int j=0; j<n; j++) {
			System.out.print("-");
		}
		System.out.println();
	}
	
} //:~