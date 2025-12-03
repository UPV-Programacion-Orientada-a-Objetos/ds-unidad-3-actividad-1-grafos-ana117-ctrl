import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import grafo_wrapper
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

class NeuroNetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet - Análisis de Redes Masivas")
        self.root.geometry("1200x800")
        
        # Inicializar el grafo C++
        self.grafo = None
        
        # Crear interfaz
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame superior - Controles
        frame_controles = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        frame_controles.pack(side=tk.TOP, fill=tk.X)
        
        # Botón cargar archivo
        btn_cargar = tk.Button(
            frame_controles, 
            text="📁 Cargar Dataset", 
            command=self.cargar_dataset,
            bg="#3498db", 
            fg="white", 
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        btn_cargar.pack(side=tk.LEFT, padx=5)
        
        # Frame para métricas
        frame_metricas = tk.Frame(self.root, bg="#ecf0f1", padx=10, pady=10)
        frame_metricas.pack(side=tk.TOP, fill=tk.X)
        
        self.lbl_info = tk.Label(
            frame_metricas, 
            text="Sistema listo. Cargue un dataset para comenzar.",
            bg="#ecf0f1",
            font=("Arial", 10),
            justify=tk.LEFT
        )
        self.lbl_info.pack(anchor=tk.W)
        
        # Frame para análisis
        frame_analisis = tk.Frame(self.root, bg="#34495e", padx=10, pady=10)
        frame_analisis.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(
            frame_analisis, 
            text="Análisis BFS:", 
            bg="#34495e", 
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            frame_analisis, 
            text="Nodo Inicio:", 
            bg="#34495e", 
            fg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        self.entry_nodo = tk.Entry(frame_analisis, width=10)
        self.entry_nodo.insert(0, "0")
        self.entry_nodo.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            frame_analisis, 
            text="Profundidad:", 
            bg="#34495e", 
            fg="white"
        ).pack(side=tk.LEFT, padx=5)
        
        self.entry_profundidad = tk.Entry(frame_analisis, width=10)
        self.entry_profundidad.insert(0, "2")
        self.entry_profundidad.pack(side=tk.LEFT, padx=5)
        
        btn_bfs = tk.Button(
            frame_analisis, 
            text="🔍 Ejecutar BFS", 
            command=self.ejecutar_bfs,
            bg="#27ae60", 
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        )
        btn_bfs.pack(side=tk.LEFT, padx=10)
        
        btn_mayor_grado = tk.Button(
            frame_analisis, 
            text="⭐ Nodo Mayor Grado", 
            command=self.encontrar_nodo_critico,
            bg="#e74c3c", 
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        )
        btn_mayor_grado.pack(side=tk.LEFT, padx=5)
        
        # Frame para visualización
        frame_viz = tk.Frame(self.root, bg="white")
        frame_viz.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_viz)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Texto inicial
        self.ax.text(
            0.5, 0.5, 
            'Cargue un dataset para comenzar el análisis',
            horizontalalignment='center',
            verticalalignment='center',
            transform=self.ax.transAxes,
            fontsize=14,
            color='gray'
        )
        self.ax.axis('off')
        self.canvas.draw()
        
    def cargar_dataset(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar Dataset",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if not archivo:
            return
        
        # Cargar en un hilo separado para no bloquear la GUI
        def cargar():
            try:
                self.lbl_info.config(text="Cargando dataset... Por favor espere.")
                self.root.update()
                
                self.grafo = grafo_wrapper.PyGrafoDisperso()
                self.grafo.cargar_datos(archivo)
                
                # Obtener métricas
                num_nodos = self.grafo.get_num_nodos()
                num_aristas = self.grafo.get_num_aristas()
                
                info_text = f"""Dataset cargado exitosamente:
✓ Archivo: {archivo.split('/')[-1]}
✓ Nodos: {num_nodos:,}
✓ Aristas: {num_aristas:,}
✓ Motor: C++ con formato CSR"""
                
                self.lbl_info.config(text=info_text)
                messagebox.showinfo("Éxito", "Dataset cargado correctamente.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar dataset: {str(e)}")
                self.lbl_info.config(text="Error al cargar dataset.")
        
        thread = threading.Thread(target=cargar)
        thread.start()
        
    def ejecutar_bfs(self):
        if self.grafo is None:
            messagebox.showwarning("Advertencia", "Primero debe cargar un dataset.")
            return
        
        try:
            nodo_inicio = int(self.entry_nodo.get())
            profundidad = int(self.entry_profundidad.get())
            
            # Ejecutar BFS
            nodos_visitados = self.grafo.bfs(nodo_inicio, profundidad)
            
            if not nodos_visitados:
                messagebox.showinfo("Resultado", "No se encontraron nodos.")
                return
            
            # Construir subgrafo para visualizar
            G = nx.DiGraph()
            
            for nodo in nodos_visitados:
                vecinos = self.grafo.get_vecinos(nodo)
                for vecino in vecinos:
                    if vecino in nodos_visitados:
                        G.add_edge(nodo, vecino)
            
            # Visualizar
            self.visualizar_grafo(G, nodo_inicio, nodos_visitados)
            
            messagebox.showinfo(
                "BFS Completado", 
                f"Nodos alcanzados: {len(nodos_visitados)}\nProfundidad: {profundidad}"
            )
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar BFS: {str(e)}")
    
    def encontrar_nodo_critico(self):
        if self.grafo is None:
            messagebox.showwarning("Advertencia", "Primero debe cargar un dataset.")
            return
        
        try:
            nodo_max = self.grafo.get_nodo_mayor_grado()
            grado_max = self.grafo.obtener_grado(nodo_max)
            
            messagebox.showinfo(
                "Nodo Crítico",
                f"Nodo con mayor grado: {nodo_max}\nGrado (conexiones): {grado_max}"
            )
            
            # Visualizar el nodo y sus vecinos inmediatos
            self.entry_nodo.delete(0, tk.END)
            self.entry_nodo.insert(0, str(nodo_max))
            self.entry_profundidad.delete(0, tk.END)
            self.entry_profundidad.insert(0, "1")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al buscar nodo crítico: {str(e)}")
    
    def visualizar_grafo(self, G, nodo_central, nodos_visitados):
        self.ax.clear()
        
        if len(G.nodes()) == 0:
            self.ax.text(
                0.5, 0.5, 
                'No hay nodos para visualizar',
                horizontalalignment='center',
                verticalalignment='center',
                transform=self.ax.transAxes
            )
            self.ax.axis('off')
            self.canvas.draw()
            return
        
        # Layout del grafo
        if len(G.nodes()) < 100:
            pos = nx.spring_layout(G, k=0.5, iterations=50)
        else:
            pos = nx.spring_layout(G, k=0.3, iterations=20)
        
        # Dibujar nodos
        node_colors = ['red' if n == nodo_central else 'lightblue' for n in G.nodes()]
        nx.draw_networkx_nodes(
            G, pos, 
            node_color=node_colors, 
            node_size=300,
            ax=self.ax
        )
        
        # Dibujar aristas
        nx.draw_networkx_edges(
            G, pos, 
            edge_color='gray', 
            arrows=True,
            arrowsize=10,
            ax=self.ax
        )
        
        # Etiquetas (solo si hay pocos nodos)
        if len(G.nodes()) < 50:
            nx.draw_networkx_labels(G, pos, font_size=8, ax=self.ax)
        
        self.ax.set_title(
            f'Subgrafo BFS - Nodo Central: {nodo_central} - Nodos: {len(nodos_visitados)}',
            fontsize=12,
            fontweight='bold'
        )
        self.ax.axis('off')
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroNetGUI(root)
    root.mainloop()