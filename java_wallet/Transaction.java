import com.google.gson.*;
import java.io.*;
import java.text.SimpleDateFormat;
import java.util.*;

public class Transaction {

    private static final String JSON_FILE = "../data/real_time_sentiment.json";
    private static double walletBalance = 5000.0;
    private static Map<String, Double> investments = new HashMap<>();

    public static void main(String[] args) {
        try {
            Gson gson = new GsonBuilder().setPrettyPrinting().create();
            JsonObject json;

            // 1. Load JSON
            File file = new File(JSON_FILE);
            if (!file.exists()) {
                System.out.println("JSON file not found: " + JSON_FILE);
                return;
            }
            try (Reader reader = new FileReader(JSON_FILE)) {
                json = JsonParser.parseReader(reader).getAsJsonObject();
            }

            // 2. Load previous wallet state if exists
            if (json.has("Wallet")) {
                JsonObject walletJson = json.getAsJsonObject("Wallet");
                walletBalance = walletJson.get("balance").getAsDouble();
                JsonObject invJson = walletJson.getAsJsonObject("investments");
                for (String key : invJson.keySet()) {
                    investments.put(key, invJson.get(key).getAsDouble());
                }
            }

            System.out.println("\n===== Simulating AI Actions in Real-Time =====");

            // 3. Simulate Buy/Sell/Hold actions with delay
            for (String company : json.keySet()) {
                if (company.equals("Wallet")) continue;

                JsonObject comp = json.getAsJsonObject(company);
                String action = comp.get("action").getAsString();

                // simulate AI "thinking"
                System.out.println("\nAI analyzing " + company + "...");
                Thread.sleep(1000); // 1-second pause

                double amount = 0;
                if (action.equalsIgnoreCase("Buy") && walletBalance > 0) {
                    amount = walletBalance / 3; // invest 1/3 of wallet
                    walletBalance -= amount;
                    investments.put(company, investments.getOrDefault(company, 0.0) + amount);
                    logTransaction("BUY", company, amount);
                } else if (action.equalsIgnoreCase("Sell") && investments.containsKey(company) && investments.get(company) > 0) {
                    amount = investments.get(company);
                    walletBalance += amount;
                    investments.put(company, 0.0);
                    logTransaction("SELL", company, amount);
                } else {
                    System.out.println("Holding investment for " + company);
                }

                // optional pause for realism
                Thread.sleep(500); // half-second
            }

            // 4. Update JSON with wallet state
            JsonObject walletJson = new JsonObject();
            walletJson.addProperty("balance", walletBalance);
            JsonObject invJson = new JsonObject();
            for (Map.Entry<String, Double> entry : investments.entrySet()) {
                invJson.addProperty(entry.getKey(), entry.getValue());
            }
            walletJson.add("investments", invJson);
            json.add("Wallet", walletJson);

            try (Writer writer = new FileWriter(JSON_FILE)) {
                gson.toJson(json, writer);
            }

            // 5. Display summary table
            displaySummary();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void logTransaction(String type, String company, double amount) throws InterruptedException {
        String timestamp = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss").format(new Date());
        System.out.printf("[%s] %s: ₹%.2f in %s\n", timestamp, type, amount, company);
        Thread.sleep(300); // small pause for effect
    }

    private static void displaySummary() {
        System.out.println("\n===== Wallet Summary =====");
        System.out.printf("%-15s %-15s %s\n", "Company", "Investment (₹)", "Graph");
        for (Map.Entry<String, Double> entry : investments.entrySet()) {
            System.out.printf("%-15s %-15.2f %s\n", entry.getKey(), entry.getValue(), generateGraph(entry.getValue()));
        }
        System.out.println("--------------------------------------------");
        System.out.printf("%-15s %-15.2f\n", "Wallet Balance", walletBalance);
    }

    // Optional: Simple ASCII graph
    private static String generateGraph(double value) {
        int maxLength = 30; // max number of bars
        int bars = (int) Math.round((value / 5000.0) * maxLength);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < bars; i++) sb.append("|");
        return sb.toString();
    }
}
