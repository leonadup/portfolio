public class Multiplication extends Operation {
    public Multiplication(Expression operande1, Expression operande2) {
        super(operande1, operande2);
    }

    @Override
    public double valeur() {
        return operande1.valeur() * operande2.valeur();
    }

    @Override
    public String toString() {
        String res = "(" + operande1 + "*" + operande2 + ")";
        return res;
    }
}