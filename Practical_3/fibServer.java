import java.io.*;
import java.net.*;

public class fibServer {
    private static final String INITIAL_NUMBERS_FILE = "initial_numbers.txt";
    private static int[] fibonacciNumbers = new int[3];

    public static void main(String[] args) {
        final int PORT = 55555;

        try {
            loadInitialNumbersFromFile(INITIAL_NUMBERS_FILE);
            @SuppressWarnings("resource")
            ServerSocket serverSocket = new ServerSocket(PORT);
            System.out.println("Fibonacci server is listening on port " + PORT + "...");

            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Connection from: " + clientSocket);
                handleRequest(clientSocket);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        
    }

    private static void loadInitialNumbersFromFile(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line = reader.readLine();
            if (line != null) {
                String[] numbers = line.trim().split("\\s+");
                for (int i =0; i <3;i++) {
                    fibonacciNumbers[i]= Integer.parseInt(numbers[i]);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void saveNumbersToFile(String filename) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            for (int i = 0; i <3; i++) {
                writer.write(Integer.toString(fibonacciNumbers[i]));
                if (i < 3) {
                    writer.write(" ");
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void handleRequest(Socket clientSocket) {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            BufferedWriter out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));

            String requestLine = in.readLine();
            if (requestLine != null && requestLine.startsWith("GET")) {
                if (requestLine.contains("/prev")) {
                    if(fibonacciNumbers[0] !=0 && fibonacciNumbers[1] != 0){
                        fibonacciNumbers[2] = fibonacciNumbers[1];
                        fibonacciNumbers[1] = fibonacciNumbers[0];
                        fibonacciNumbers[0] = fibonacciNumbers[2] - fibonacciNumbers[1];
                    }
                    sendResponse(out);
                } else if (requestLine.contains("/next")) {
                    fibonacciNumbers[0] = fibonacciNumbers[1]+ fibonacciNumbers[2];
                    fibonacciNumbers[1] = fibonacciNumbers[2]+ fibonacciNumbers[0];
                    fibonacciNumbers[2] = fibonacciNumbers[1]+ fibonacciNumbers[0];
                    sendResponse(out);
                } else {
                    sendResponse(out);
                }
            }

            in.close();
            out.close();
            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void sendResponse(BufferedWriter out) throws IOException {
        StringBuilder response = new StringBuilder();
        response.append("HTTP/1.1 200 OK\r\n")
                .append("Content-Type: text/html\r\n")
                .append("\r\n")
                .append("<html><head><title>Fibonacci Triples</title></head><body><h1>Fibonacci Triples</h1>")
                .append("<p>Current: (").append(fibonacciNumbers[0]).append(", ")
                .append(fibonacciNumbers[1]).append(", ")
                .append(fibonacciNumbers[2]).append(")</p>")
                .append("<p><a href=\"/prev\">Previous</a> | <a href=\"/next\">Next</a></p>")
                .append("</body></html>");

        out.write(response.toString());
        out.flush();

        saveNumbersToFile(INITIAL_NUMBERS_FILE);
    }
}