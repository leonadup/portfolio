public class Addition extends Operation { // Addition hérite de Operation.
    public Addition(Expression operande1, Expression operande2) {
        super(operande1, operande2); // "super" accède à la classe mère.
    }

    @Override
    public double valeur() {
        return operande1.valeur() + operande2.valeur();
    }

    @Override
    public String toString() {
        String res = "(" + operande1 + "+" + operande2 + ")";
        return res;
    }
}
