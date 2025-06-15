public class Nombre extends Expression {
    private double valeurNombre;

    public Nombre(double valeurNombre) {
        this.valeurNombre = valeurNombre;
    }

    @Override
    public double valeur() {
        return valeurNombre;
    }

    @Override
    public String toString() {
        return Double.toString(valeurNombre);
    }
}
