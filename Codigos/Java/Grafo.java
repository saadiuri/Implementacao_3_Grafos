package Codigos.Java;

import java.util.*;

public class Grafo {

    int n;

    ArrayList<Aresta>[] adj;
    ArrayList<Aresta>[] adjReverso;

    @SuppressWarnings("unchecked")
    public Grafo(int n) {
        this.n = n;

        adj = new ArrayList[n + 1];
        adjReverso = new ArrayList[n + 1];

        for (int i = 1; i <= n; i++) {
            adj[i] = new ArrayList<>();
            adjReverso[i] = new ArrayList<>();
        }
    }

    public void adicionarAresta(int origem, int destino, int peso) {
        adj[origem].add(new Aresta(destino, peso));

        adjReverso[destino].add(new Aresta(origem, peso));
    }

    public int grauSaida(int v) {
        return adj[v].size();
    }

    public int grauEntrada(int v) {
        return adjReverso[v].size();
    }

    public ArrayList<Aresta> sucessores(int v) {
        return adj[v];
    }

    public ArrayList<Aresta> predecessores(int v) {
        return adjReverso[v];
    }
}
