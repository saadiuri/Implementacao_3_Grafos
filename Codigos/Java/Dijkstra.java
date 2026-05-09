package Codigos.Java;
import java.util.*;

public class Dijkstra {

    private Grafo grafo;

    public Dijkstra(Grafo grafo) {
        this.grafo = grafo;
    }

    public VerticeInfo[] encontrarCaminhoMinimo(int origem) {
        int n = grafo.n;
        VerticeInfo[] info = new VerticeInfo[n + 1];

        for (int i = 1; i <= n; i++) {
            info[i] = new VerticeInfo(Integer.MAX_VALUE, Integer.MAX_VALUE, -1);
        }
        info[origem] = new VerticeInfo(0, 0, -1);

        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.offer(new int[]{origem, 0, 0});

        while (!pq.isEmpty()) {
            int[] current = pq.poll();
            int u = current[0];
            int distU = current[1];
            int arestasU = current[2];

            if (distU > info[u].distancia ||
                (distU == info[u].distancia && arestasU > info[u].numArestas)) {
                continue;
            }

            for (Aresta aresta : grafo.sucessores(u)) {
                int v = aresta.destino;
                int peso = aresta.peso;
                int novaDist = distU + peso;
                int novasArestas = arestasU + 1;

                if (novaDist < info[v].distancia ||
                    (novaDist == info[v].distancia && novasArestas < info[v].numArestas)) {
                    info[v].distancia = novaDist;
                    info[v].numArestas = novasArestas;
                    info[v].anterior = u;
                    pq.offer(new int[]{v, novaDist, novasArestas});
                }
            }
        }

        return info;
    }

    public List<Integer> reconstruirCaminho(VerticeInfo[] info, int destino) {
        List<Integer> caminho = new ArrayList<>();
        if (info[destino].distancia == Integer.MAX_VALUE) return caminho;

        for (int v = destino; v != -1; v = info[v].anterior) {
            caminho.add(v);
        }
        Collections.reverse(caminho);
        return caminho;
    }
}
