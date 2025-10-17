import java.util.HashMap;
import java.util.Map;

public class Wallet {
    private double balance;
    private Map<String, Double> investments;

    public Wallet(double initialBalance) {
        this.balance = initialBalance;
        this.investments = new HashMap<>();
    }

    public double getBalance() {
        return balance;
    }

    public Map<String, Double> getInvestments() {
        return investments;
    }

    // Allocate money to a company
    public void invest(String company, double amount) {
        if (amount > balance) {
            System.out.println("Not enough balance to invest in " + company);
            return;
        }
        balance -= amount;
        investments.put(company, investments.getOrDefault(company, 0.0) + amount);
        System.out.println("Invested ₹" + amount + " in " + company);
    }

    // Sell money from a company
    public void sell(String company, double amount) {
        double invested = investments.getOrDefault(company, 0.0);
        if (amount > invested) {
            System.out.println("Not enough investment to sell in " + company);
            return;
        }
        balance += amount;
        investments.put(company, invested - amount);
        System.out.println("Sold ₹" + amount + " from " + company);
    }

    // Display wallet status
    public void displayStatus() {
        System.out.println("\nWallet Balance: ₹" + balance);
        System.out.println("Investments:");
        for (String company : investments.keySet()) {
            System.out.println(company + ": ₹" + investments.get(company));
        }
    }
}
