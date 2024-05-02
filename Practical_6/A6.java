import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Base64;
import java.util.Random;

import javax.net.ssl.SSLSocket;
import javax.net.ssl.SSLSocketFactory;

public class A6 {
    private static final int PORT = 55555;
    private static String question = "";
    private static Random random = new Random();

    public static void main(String[] args) {
        int correct = 0;
        int total = 0;

        try {
            @SuppressWarnings("resource")
            ServerSocket serverSocket = new ServerSocket(PORT);
            System.out.println("Waiting for a Telnet connection on port 55555...");
            readQuestions("questions.txt");
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("Connection from: " + clientSocket.getInetAddress().getHostAddress());

                BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
                PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);

                while (true) {
                    if (total != 0) {
                        out.println("\n\rAny key for question or q to Quit and view results\n\r");
                        String response = in.readLine();
                        if (response.trim().equalsIgnoreCase("q")) {
                            out.print("Enter email addess :");
                            String recpt = in.readLine();
                            System.out.println("here " + recpt);
                            SendMail(recpt, correct, total);
                            break;
                        }
                    }
                    String[] temp = question.split("\\n");
                    out.println(temp[0].substring(0));
                    String cor = "";
                    for (int i = 1; i < temp.length; i++) {
                        if (temp[i].startsWith("+")) {
                            out.println((char) ('A' + (i - 1)) + ". " + temp[i].substring(1));
                            cor = "" + (char) ('A' + (i - 1));
                        } else {
                            out.println((char) ('A' + (i - 1)) + ". " + temp[i].substring(1));
                        }
                    }
                    total++;

                    String response = in.readLine();
                    if (response.trim().equalsIgnoreCase(cor)) {
                        correct++;
                        out.println("Correct answer");
                    }
                }

                clientSocket.close();
                System.out.println("Connection closed.");
                total = 0;
                correct = 0;

            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void SendMail(String recpt, int correct, int total) throws UnknownHostException, IOException {
        String username = "u18003193@tuks.co.za";
        final String password = "wbdh yqyu ekwe ndjk";// lbhs tybh ztue // aqye kshd cmqe idui
        String subject = "Test Results";
        String body = "You got " + correct + " out of " + total + "LOL";

        String host = "smtp.gmail.com";
        int port = 465;

        SSLSocketFactory factory = (SSLSocketFactory) SSLSocketFactory.getDefault();
        SSLSocket socket = (SSLSocket) factory.createSocket(host, port);
        BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));

        String line = reader.readLine();
        System.out.println(line);

        writer.write("EHLO " + host + "\r\n");
        writer.flush();
        line = reader.readLine();
        System.out.println(line);

        writer.write("AUTH LOGIN\r\n");
        writer.flush();
        line = reader.readLine();
        System.out.println(line);

        String encodedUsername = Base64.getEncoder().encodeToString(username.getBytes());
        writer.write(encodedUsername + "\r\n");
        writer.flush();
        line = reader.readLine();
        System.out.println(line);

        String encodedPassword = Base64.getEncoder().encodeToString(password.getBytes());
        writer.write(encodedPassword + "\r\n");
        writer.flush();
        line = reader.readLine();
        System.out.println(line);

        writer.write("MAIL FROM:<" + username + ">\r\n");
        writer.flush();
        line = reader.readLine();
        System.out.println(line);

        writer.write("RCPT TO:<" + recpt + ">\r\n");
        writer.flush();
        line = reader.readLine();
        System.out.println(line);

        writer.write("DATA\r\n");
        writer.flush();
        line = reader.readLine();
        System.out.println(line);

        writer.write("Subject: " + subject + "\r\n\r\n" + body + "\r\n.\r\n");
        writer.flush();
        line = reader.readLine();
        System.out.println(line);

        writer.write("QUIT\r\n");
        writer.flush();
        line = reader.readLine();
        System.out.println(line);
        // System.out.println("test");

        writer.close();
        reader.close();
        socket.close();

        System.out.println("email sent successfully");
    }

    private static void readQuestions(String filename) {
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

    private static int getRandomQuestion(int size) {
        int index = random.nextInt(size);
        return index;
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
}
