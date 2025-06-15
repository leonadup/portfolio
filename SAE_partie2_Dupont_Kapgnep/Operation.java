public abstract class Operation extends Expression {
    protected Expression operande1;  // On utilise protected pour ne pas avoir à utiliser de getter et setter.
    protected Expression operande2; 

    public Operation(Expression operande1, Expression operande2) {
        this.operande1 = operande1;
        this.operande2 = operande2;
    }

    @Override
    public abstract double valeur();

    public Expression getOperande1() {
        return operande1;
    }

    public Expression getOperande2() {
        return operande2;
    }

}
