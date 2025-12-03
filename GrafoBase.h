#ifndef GRAFO_BASE_H
#define GRAFO_BASE_H

#include <string>
#include <vector>

// Clase abstracta que define la interfaz del grafo
class GrafoBase {
public:
    virtual ~GrafoBase() {}
    
    // Métodos virtuales puros
    virtual void cargarDatos(const std::string& archivo) = 0;
    virtual int obtenerGrado(int nodo) = 0;
    virtual std::vector<int> getVecinos(int nodo) = 0;
    virtual std::vector<int> BFS(int nodoInicio, int profundidad) = 0;
    virtual int getNumNodos() const = 0;
    virtual int getNumAristas() const = 0;
    virtual int getNodoMayorGrado() = 0;
};

#endif