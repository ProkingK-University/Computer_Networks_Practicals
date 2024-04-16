import java.io.*;
import java.net.*;
import java.util.*;

public class QuestionAnswer {
    private static final int PORT = 55555;
    private static String question = "";
    private static Random random = new Random();
    private static String display = "";

    public static void main(String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(PORT)) {
            System.out.println("Quiz Server is running on port " + PORT);
            while (true) {
                try (Socket clientSocket = serverSocket.accept()) {
                    System.out.println("Client connected: " + clientSocket.getInetAddress());
                    handleRequest(clientSocket);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void loadQuestionsFromFile(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String qna = "";
            String line;
            while ((line = reader.readLine()) != null) {
                qna += line + "\n";
            }
            String[] questionAndAnswers = qna.split("\\?");
            int index = getRandomQuestion(questionAndAnswers.length);
            while (questionAndAnswers[index].split("\n").length < 3) {
                index = getRandomQuestion(questionAndAnswers.length);
            }

            questionAndAnswers[index] += addQuestion(questionAndAnswers[index]);
            question = questionAndAnswers[index];

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static String addQuestion(String questionText) {
        String[] temp = questionText.split("\\n");
        for (int i = 0; i < temp.length; i++) {
            if (temp[i].startsWith("+")) {
                return "";
            }
        }
        return "+None of the above";
    }

    private static void handleRequest(Socket clientSocket) {
        try {
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            BufferedWriter out = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
            loadQuestionsFromFile("questions.txt");
            String[] temp = question.split("\\n");

            String requestLine = in.readLine();
            if (requestLine != null && requestLine.startsWith("GET")) {
                if (requestLine.contains("/next")) {
                    display = "<p>" + temp[0] + "</p>";
                    for (int i = 1; i < temp.length; i++) {
                        if (temp[i].startsWith("+")) {
                            display += "<a href=\"/correct\">" + (char) ('A' + (i - 1)) + ". " + temp[i].substring(1)
                                    + "</a></br>";
                        }
                        display += "<a href=\"/incorrect\">" + (char) ('A' + (i - 1)) + ". " + temp[i].substring(1)
                                + "</br></a>";
                    }
                    sendResponse(out);
                } else if (requestLine.contains("/correct")) {
                    display = "<h1>Correct Winner</h1><a href=\"/next\">Next</a>";
                    sendResponse(out);
                } else {
                    display = "<h1>Correct Winner SIKE YOUR A LOOOOSERRRRRRRRR</h1><a href=\"/next\">Try Again or you scared</a>";
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
        response.append("Server: QNA/1.0\r\n")
                .append("Date: ").append(new Date()).append("\r\n")
                .append("Content-Type: text/html\r\n");

        // Entity Headers
        response.append("Content-Length: ").append(calculateContentLength()).append("\r\n");

        response.append("\r\n")
                .append("<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 4.0//EN\">\r\n") // RFC1866 addition of HTMLDOCType
                .append("<html><head><title>Questions</title></head><body><h1>Questions</h1>")
                .append(display)
                .append("</body></html>");

        out.write(response.toString());
        out.flush();

    }

    // Method to calculate Content-Length based on the HTML body length
    private static int calculateContentLength() {
        String htmlBody = "<!DOCTYPE HTML PUBLIC \"-//IETF//DTD HTML 4.0//EN\">\r\n"
                + "<html><head><title>Questions</title></head><body><h1>Questions</h1>"
                + "<a href=\"/next\">Next</a></p>"
                + display
                + "</body></html>";
        return htmlBody.length();
    }

    private static int getRandomQuestion(int size) {
        int index = random.nextInt(size);
        return index;
    }
}