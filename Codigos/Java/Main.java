package Codigos.Java;

import java.util.*;
import java.io.*;

public class Main {

    public static void main(String[] args) {

        if (args.length < 1) {
            System.out.println("Uso: java Codigos.Main <arquivo_entrada>");
            return;
        }

        try (Scanner sc = new Scanner(new File(args[0]))) {

            int n = sc.nextInt();
            int m = sc.nextInt();

            Grafo grafo = new Grafo(n);

            for (int i = 0; i < m; i++) {

                int u = sc.nextInt();
                int v = sc.nextInt();
                int peso = sc.nextInt();

                grafo.adicionarAresta(u, v, peso);
            }

            int origem = sc.nextInt();
            int destino = sc.nextInt();

            Dijkstra dijkstra = new Dijkstra(grafo);

            long inicio = System.nanoTime();

            VerticeInfo[] info =
                dijkstra.encontrarCaminhoMinimo(origem);

            long fim = System.nanoTime();

            double tempoMs =
                (fim - inicio) / 1_000_000.0;

            if (info[destino].distancia == Integer.MAX_VALUE) {

                System.out.println(
                    "Nao ha caminho entre "
                    + origem + " e " + destino
                );

                return;
            }

            List<Integer> caminho =
                dijkstra.reconstruirCaminho(info, destino);

            System.out.println(
                "Distancia (comprimento): "
                + info[destino].distancia
            );

            System.out.println(
                "Numero de arestas: "
                + info[destino].numArestas
            );

            System.out.println(
                "Caminho: "
                + caminho
            );

            System.out.println(
                "Tempo: "
                + tempoMs + " ms"
            );

        } catch (FileNotFoundException e) {

            System.out.println(
                "Arquivo nao encontrado: "
                + args[0]
            );
        }
    }
}