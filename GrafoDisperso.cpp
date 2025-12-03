#include "GrafoDisperso.h"

GrafoDisperso::GrafoDisperso() : num_nodos(0), num_aristas(0) {
    std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
}

GrafoDisperso::~GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const std::string& archivo) {
    std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..." << std::endl;
    
    std::ifstream file(archivo);
    if (!file.is_open()) {
        std::cerr << "[ERROR] No se pudo abrir el archivo: " << archivo << std::endl;
        return;
    }
    
    std::string linea;
    std::set<int> nodos_unicos;
    int aristas_count = 0;
    
    // Leer archivo línea por línea
    while (std::getline(file, linea)) {
        // Ignorar comentarios y líneas vacías
        if (linea.empty() || linea[0] == '#') continue;
        
        std::istringstream iss(linea);
        int origen, destino;
        
        if (iss >> origen >> destino) {
            adj_temp[origen].push_back(destino);
            nodos_unicos.insert(origen);
            nodos_unicos.insert(destino);
            aristas_count++;
        }
    }
    
    file.close();
    
    num_nodos = nodos_unicos.size();
    num_aristas = aristas_count;
    
    // Construir estructura CSR
    construirCSR();
    
    std::cout << "[C++ Core] Carga completa. Nodos: " << num_nodos 
              << " | Aristas: " << num_aristas << std::endl;
    
    // Estimar memoria (aproximado)
    int memoria_mb = (valores.size() + col_indices.size() + row_ptr.size()) * sizeof(int) / (1024 * 1024);
    if (memoria_mb == 0) memoria_mb = 1;
    std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: " 
              << memoria_mb << " MB." << std::endl;
}

void GrafoDisperso::construirCSR() {
    // Encontrar el nodo máximo para dimensionar
    int max_nodo = 0;
    for (const auto& par : adj_temp) {
        max_nodo = std::max(max_nodo, par.first);
        for (int vecino : par.second) {
            max_nodo = std::max(max_nodo, vecino);
        }
    }
    
    // Inicializar row_ptr
    row_ptr.resize(max_nodo + 2, 0);
    
    // Construir CSR
    for (int i = 0; i <= max_nodo; i++) {
        if (adj_temp.find(i) != adj_temp.end()) {
            for (int vecino : adj_temp[i]) {
                valores.push_back(1);
                col_indices.push_back(vecino);
            }
        }
        row_ptr[i + 1] = col_indices.size();
    }
}

int GrafoDisperso::obtenerGrado(int nodo) {
    if (nodo >= (int)row_ptr.size() - 1 || nodo < 0) return 0;
    return row_ptr[nodo + 1] - row_ptr[nodo];
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
    std::vector<int> vecinos;
    if (nodo >= (int)row_ptr.size() - 1 || nodo < 0) return vecinos;
    
    int inicio = row_ptr[nodo];
    int fin = row_ptr[nodo + 1];
    
    for (int i = inicio; i < fin; i++) {
        vecinos.push_back(col_indices[i]);
    }
    
    return vecinos;
}

std::vector<int> GrafoDisperso::BFS(int nodoInicio, int profundidad) {
    std::cout << "[C++ Core] Ejecutando BFS nativo..." << std::endl;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    
    std::vector<int> visitados;
    std::queue<std::pair<int, int>> cola; // (nodo, nivel)
    std::set<int> visitado_set;
    
    cola.push({nodoInicio, 0});
    visitado_set.insert(nodoInicio);
    
    while (!cola.empty()) {
        int nodo_actual = cola.front().first;
        int nivel = cola.front().second;
        cola.pop();
        
        if (nivel > profundidad) break;
        
        visitados.push_back(nodo_actual);
        
        // Obtener vecinos
        std::vector<int> vecinos = getVecinos(nodo_actual);
        for (int vecino : vecinos) {
            if (visitado_set.find(vecino) == visitado_set.end() && nivel < profundidad) {
                visitado_set.insert(vecino);
                cola.push({vecino, nivel + 1});
            }
        }
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end_time - start_time);
    
    std::cout << "[C++ Core] Nodos encontrados: " << visitados.size() 
              << ". Tiempo ejecución: " << duration.count() / 1000.0 << "ms." << std::endl;
    
    return visitados;
}

int GrafoDisperso::getNumNodos() const {
    return num_nodos;
}

int GrafoDisperso::getNumAristas() const {
    return num_aristas;
}

int GrafoDisperso::getNodoMayorGrado() {
    int max_grado = 0;
    int nodo_max = 0;
    
    for (int i = 0; i < (int)row_ptr.size() - 1; i++) {
        int grado = obtenerGrado(i);
        if (grado > max_grado) {
            max_grado = grado;
            nodo_max = i;
        }
    }
    
    return nodo_max;
}