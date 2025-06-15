public class Calculatrice {
    public static void main(String[] args) {
        try {
            Expression zero = new Nombre(0);
            Expression deux = new Nombre(2) ;
            Expression trois = new Nombre(3) ;
            Expression dixSept = new Nombre(17) ;
            Expression s = new Soustraction(dixSept, deux) ;
            Expression a = new Addition(deux, trois) ;
            Expression d = new Division(s, a) ;
            Expression m = new Multiplication(s,a);
            Expression dzero = new Division(deux, zero);
            System.out.println(d + " = " + d.valeur()) ; // affiche "((17 - 2) / (2 + 3)) = 3"
            System.out.println(m + " = " + m.valeur()) ; // affiche "((17 - 2) * (2 + 3)) = 75"
            System.out.println(dzero.valeur()) ; // affiche "Division par 0 interdite"

            
            
    
            
        
            }
            catch (ArithmeticException erreurdivzero) { // On teste l'exception du dénominateur nul
            System.out.println(erreurdivzero.getMessage());
        }
    }
}

