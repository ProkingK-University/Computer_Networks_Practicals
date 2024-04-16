import java.io.*;
import java.net.*;
import java.util.Date;

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
                for (int i = 0; i < 3; i++) {
                    fibonacciNumbers[i] = Integer.parseInt(numbers[i]);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void saveNumbersToFile(String filename) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            for (int i = 0; i < 3; i++) {
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
                    if (fibonacciNumbers[0] != 0 && fibonacciNumbers[1] != 0) {
                        fibonacciNumbers[2] = fibonacciNumbers[1];
                        fibonacciNumbers[1] = fibonacciNumbers[0];
                        fibonacciNumbers[0] = fibonacciNumbers[2] - fibonacciNumbers[1];
                    }
                    sendResponse(out);
                } else if (requestLine.contains("/next")) {
                    fibonacciNumbers[0] = fibonacciNumbers[1] + fibonacciNumbers[2];
                    fibonacciNumbers[1] = fibonacciNumbers[2] + fibonacciNumbers[0];
                    fibonacciNumbers[2] = fibonacciNumbers[1] + fibonacciNumbers[0];
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

        response.append("HTTP/1.1 200 OK\r\n");

        // Response Headers
        response.append("Server: fibServer/1.0\r\n")
                .append("Date: ").append(new Date()).append("\r\n")
                .append("Content-Type: text/html\r\n");

        // Entity Headers
        response.append("Content-Length: ").append(calculateContentLength()).append("\r\n");

        response.append("\r\n")
                .append("<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 4.0//EN\">\r\n") // RFC1866 addition of HTMLDOCType
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

    // Method to calculate Content-Length based on the HTML body length
    private static int calculateContentLength() {
        String htmlBody = "<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 4.0//EN\">\r\n"
                + "<html><head><title>Fibonacci Triples</title></head><body><h1>Fibonacci Triples</h1>"
                + "<p>Current: (" + fibonacciNumbers[0] + ", " + fibonacciNumbers[1] + ", " + fibonacciNumbers[2]
                + ")</p>"
                + "<p><a href=\"/prev\">Previous</a> | <a href=\"/next\">Next</a></p>"
                + "</body></html>";
        return htmlBody.length();
    }
}

/*
 * References:
 * RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1:
 * https://tools.ietf.org/html/rfc2616
 * RFC 7230 - Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and
 * Routing: https://tools.ietf.org/html/rfc7230
 * RFC 7231 - Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content:
 * https://tools.ietf.org/html/rfc7231
 * RFC 1866 - Hypertext Markup Language - 2.0:
 * https://tools.ietf.org/html/rfc1866
 * RFC 2854 - Hypertext Markup Language - 4.0:
 * https://tools.ietf.org/html/rfc2854
 * RFC 7650 - A Collection of Header Field Definitions:
 * https://tools.ietf.org/html/rfc7650
 * 
 * The structure and content of the HTTP response are influenced by RFC 7231.
 * The code follows the specifications outlined in RFC 2616.
 */