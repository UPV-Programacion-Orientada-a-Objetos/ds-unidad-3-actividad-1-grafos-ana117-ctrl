#ifndef GRAFO_DISPERSO_H
#define GRAFO_DISPERSO_H

#include "GrafoBase.h"
#include <iostream>
#include <vector>
#include <map>
#include <queue>
#include <set>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <chrono>

// Implementación concreta usando formato CSR (Compressed Sparse Row)
class GrafoDisperso : public GrafoBase {
private:
    // Formato CSR: 3 vectores
    std::vector<int> valores;        // Valores (solo 1s para indicar conexión)
    std::vector<int> col_indices;    // Índices de columna
    std::vector<int> row_ptr;        // Punteros de inicio de cada fila
    
    int num_nodos;
    int num_aristas;
    
    // Mapa temporal para construir el grafo
    std::map<int, std::vector<int>> adj_temp;
    
    void construirCSR();
    
public:
    GrafoDisperso();
    ~GrafoDisperso();
    
    void cargarDatos(const std::string& archivo) override;
    int obtenerGrado(int nodo) override;
    std::vector<int> getVecinos(int nodo) override;
    std::vector<int> BFS(int nodoInicio, int profundidad) override;
    int getNumNodos() const override;
    int getNumAristas() const override;
    int getNodoMayorGrado() override;
};

#endif