import it.uniroma1.di.tmancini.utils.*;
import it.uniroma1.di.tmancini.teaching.ai.SATCodec.*;
import java.util.*;

public class QueensToSAT {

	public static void main(String args[]) {
		
				
		// Defines the allowed/requested command-line options and flags
		CmdLineOptions clo = new CmdLineOptions("QueensToSAT", "2013-08-26", "Toni Mancini (http://tmancini.di.uniroma1.it)", 
			"A simple SAT encoder of the n-Queens problem: \n\nGiven integer n>0, we want to put n queens on a nxn chessboard in such a way that no queen is under attack.");
		
		// Second argument = true iff the option is mandatory. Default: false.
		clo.addOption("n", "The number of queens and the size of the chessboard (a positive integer)", true);
		clo.addOption("o", "The name of the output DIMACS file");
		clo.addFlag("debug", "Enable debug mode: output will NOT be in DIMACS format");
		
		// Parses the command-line arguments. It raises an error in case mandatory options are not given
		clo.parse(args);
		
		
		// Gets the value of an option
		int n = Integer.parseInt(clo.getOptionValue("n"));
		
		// Creates the encoder
		SATEncoder enc = new SATEncoder("nQueens (n=" + n + ")", clo.getOptionValue("o"));
		
		if (clo.isFlagSet("debug")) {
			enc.enableDebugMode(); // Enables debug mode: output is not in DIMACS format
		}
		
		// Defines an integer range: 1..n
		IntRange coordRange = new IntRange("coord", 1, n);
		
		RangeProduct twoCoordsRange = new RangeProduct("twoCoords", coordRange, 2);
		
		// Defines the family of variables Q_{i,j} with i and j ranging over 1..n
		enc.defineFamilyOfVariables("Q", coordRange, coordRange );	

	
		// Defines problem constraints:
		List<Integer> tuple = null;
		Iterator<List<Integer>> it = null;
		
		// 1. One queen per row
		for(int x : coordRange.values()) {
			enc.addComment("At least one queen in row " + x);
			for(int y : coordRange.values()) {
				enc.addToClause("Q", x, y);
			}
			enc.endClause();
			
			enc.addComment("At most one queen in row " + x);
			it = twoCoordsRange.iterator(RangeProduct.FILTER.ALLDIFF_ORDERED);
			while (it.hasNext()) {
				tuple = it.next();
				// -Q[x,y1] or -Q[x,y2]
				enc.addNegToClause("Q", x, tuple.get(0));
				enc.addNegToClause("Q", x, tuple.get(1));
				enc.endClause();
			}
		}
		
		// 2. One queen per column
		for(int y : coordRange.values()) {
			enc.addComment("At least one queen in column " + y);		
			for(int x : coordRange.values()) {
				enc.addToClause("Q", x, y);
			}
			enc.endClause();
			
			enc.addComment("At most one queen in column " + y);
			it = twoCoordsRange.iterator(RangeProduct.FILTER.ALLDIFF_ORDERED);
			while (it.hasNext()) {
				tuple = it.next();
				// -Q[x1,y] or -Q[x2,y]
				enc.addNegToClause("Q", tuple.get(0), y);
				enc.addNegToClause("Q", tuple.get(1), y);					
				enc.endClause();
			}
		}		
		
		// 3. At most one queen for each NE-SW diagonal 
		for(int x1 : coordRange.values()) {
			for(int y1 : coordRange.values()) {
				// Going SW
				int x2 = x1+1;
				int y2 = y1-1;

				enc.addComment("No two queens on the diagonal starting from ("+x1 + "," + y1+") and going SW");
				while (coordRange.inBounds(x2) && coordRange.inBounds(y2)) {
					// -Q[x1, y1] or -Q[x2,y2]
					enc.addNegToClause("Q", x1, y1);
					enc.addNegToClause("Q", x2, y2);
					enc.endClause();
					x2++;
					y2--;
				}
			}
		}
		
		// 4. At most one queen for each NW-SE diagonal 
		for(int x1 : coordRange.values()) {
			for(int y1 : coordRange.values()) {
				// Going SE
				int x2 = x1+1;
				int y2 = y1+1;

				enc.addComment("No two queens on the diagonal starting from ("+x1 + "," + y1+") and going SE");
				while (coordRange.inBounds(x2) && coordRange.inBounds(y2)) {
					// -Q[x1, y1] or -Q[x2,y2]
					enc.addNegToClause("Q", x1, y1);
					enc.addNegToClause("Q", x2, y2);
					enc.endClause();
					x2++;
					y2++;
				}
			}
		}
		
		// Finalizes everything, frees-up temp memory and closes the output file.
		enc.end();
	}


} //:~