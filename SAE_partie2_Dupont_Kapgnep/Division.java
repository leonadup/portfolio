public class Division extends Operation {
    public Division(Expression operande1, Expression operande2) {
        super(operande1, operande2);
    }

    @Override
    public double valeur() {
        if (operande2.valeur() == 0) {
            throw new ArithmeticException("Division par 0 interdite"); 
        } // On envoie une exception qui stoppe le code si le dénominateur est égal à zéro.
        else{
        return operande1.valeur() / operande2.valeur();}
        
    }

    @Override
    public String toString() {
        String res = "(" + operande1 + "/" + operande2 + ")";
        return res;
    }
}