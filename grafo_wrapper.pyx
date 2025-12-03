# distutils: language = c++
# distutils: extra_compile_args = -std=c++17

from libcpp.string cimport string
from libcpp.vector cimport vector

# Declaración de la clase C++
cdef extern from "GrafoDisperso.h":
    cdef cppclass GrafoDisperso:
        GrafoDisperso() except +
        void cargarDatos(const string& archivo)
        int obtenerGrado(int nodo)
        vector[int] getVecinos(int nodo)
        vector[int] BFS(int nodoInicio, int profundidad)
        int getNumNodos()
        int getNumAristas()
        int getNodoMayorGrado()

# Clase Python que envuelve la clase C++
cdef class PyGrafoDisperso:
    cdef GrafoDisperso* c_grafo
    
    def __cinit__(self):
        self.c_grafo = new GrafoDisperso()
        print("[Cython] Wrapper inicializado")
    
    def __dealloc__(self):
        if self.c_grafo != NULL:
            del self.c_grafo
    
    def cargar_datos(self, archivo):
        """Carga el dataset desde un archivo"""
        archivo_bytes = archivo.encode('utf-8')
        self.c_grafo.cargarDatos(archivo_bytes)
    
    def obtener_grado(self, nodo):
        """Obtiene el grado de un nodo"""
        return self.c_grafo.obtenerGrado(nodo)
    
    def get_vecinos(self, nodo):
        """Obtiene los vecinos de un nodo"""
        cdef vector[int] vecinos_cpp = self.c_grafo.getVecinos(nodo)
        return list(vecinos_cpp)
    
    def bfs(self, nodo_inicio, profundidad):
        """Ejecuta BFS desde un nodo con profundidad máxima"""
        print(f"[Cython] Solicitud recibida: BFS desde Nodo {nodo_inicio}, Profundidad {profundidad}.")
        cdef vector[int] resultado_cpp = self.c_grafo.BFS(nodo_inicio, profundidad)
        print("[Cython] Retornando lista de nodos visitados a Python.")
        return list(resultado_cpp)
    
    def get_num_nodos(self):
        """Retorna el número de nodos del grafo"""
        return self.c_grafo.getNumNodos()
    
    def get_num_aristas(self):
        """Retorna el número de aristas del grafo"""
        return self.c_grafo.getNumAristas()
    
    def get_nodo_mayor_grado(self):
        """Retorna el nodo con mayor grado"""
        return self.c_grafo.getNodoMayorGrado()