import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import math

from grilla_torrente_sanguineo import GrillaTorrenteSanguineo
from estado_celular import EstadoCelular


class Simulador:
    """
    SIMULADOR DE INFECCIÓN ZOMBIE A NIVEL SANGUÍNEO

    Visualiza el torrente sanguíneo humano durante una infección zombie
    con dashboard médico en tiempo real.
    """

    ANCHO_SANGRE = 120
    ALTO_SANGRE = 80
    TAMANO_CELULA = 7

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🩸 Simulador de Infección Zombie")
        self.root.configure(bg="#f8f9fa")

        #Dimensiones ventana
        self.root.geometry("1350x750")

        self.torrente_sanguineo = GrillaTorrenteSanguineo(self.ANCHO_SANGRE, self.ALTO_SANGRE)
        self.ejecutando = False
        self.hilo_simulacion = None

        #Crear contenedor scrollable y dentro él la interfaz.
        self._crear_contenedor_scrollable()

        #Construcción de la interfaz dentro del contenedor scrollable.
        self.configurar_interfaz()

        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)

    def _crear_contenedor_scrollable(self):
        #Interfaz principal que tendrá el contenido y tiene scrollbar.
        self.main_canvas = tk.Canvas(self.root, bg="#f8f9fa", highlightthickness=0)
        self.main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #Scrollbar vertical.
        self.v_scroll = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.main_canvas.yview)
        self.v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.main_canvas.configure(yscrollcommand=self.v_scroll.set)

        #Frame que continue la UI.
        self.contenedor_principal = tk.Frame(self.main_canvas, bg="#f8f9fa")
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.contenedor_principal, anchor="nw")

        #Cuando el tamaño del frame cambie, actualizar scrollregion.
        def _on_frame_configure(event):
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

        self.contenedor_principal.bind("<Configure>", _on_frame_configure)

        def _on_canvas_resize(event):
            canvas_width = event.width
            self.main_canvas.itemconfigure(self.canvas_window, width=canvas_width)

        self.main_canvas.bind("<Configure>", _on_canvas_resize)

        def _on_mousewheel(event):
            if hasattr(event, 'delta') and event.delta:
                self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                if event.num == 4:
                    self.main_canvas.yview_scroll(-3, "units")
                elif event.num == 5:
                    self.main_canvas.yview_scroll(3, "units")

        self.root.bind_all("<MouseWheel>", _on_mousewheel)
        self.root.bind_all("<Button-4>", _on_mousewheel)
        self.root.bind_all("<Button-5>", _on_mousewheel)

    def configurar_interfaz(self):

        #Configuración de toda la interface dentro del contenedor principal.
        parent = self.contenedor_principal

        self.crear_encabezado(parent)
        # Panel de controles
        self.crear_panel_controles(parent)

        #Contenedor horizontal para simulación + dashboard.
        contenedor_horizontal = tk.Frame(parent, bg="#f8f9fa")
        contenedor_horizontal.pack(fill=tk.BOTH, expand=True, pady=8, padx=10)

        #Panel de simulación (a la izquierda).
        self.crear_panel_simulacion(contenedor_horizontal)

        #Dashboard médico (a la derecha).
        self.crear_dashboard_medico(contenedor_horizontal)

        self.actualizar_visualizacion()

    def crear_encabezado(self, parent):
        header = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT, bd=0)
        header.pack(fill=tk.X, pady=(0, 10))

        linea_top = tk.Frame(header, bg="#e74c3c", height=3)
        linea_top.pack(fill=tk.X)

        #Contenido del header.
        contenido = tk.Frame(header, bg="#ffffff")
        contenido.pack(fill=tk.X, pady=12, padx=25)

        #Título.
        titulo = tk.Label(
            contenido,
            text="🧬 Simulador de Infección Zombie",
            font=("Helvetica", 20, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        titulo.pack(side=tk.LEFT)

        #Subtítulo.
        subtitulo = tk.Label(
            contenido,
            text="Visualización de Autómata Celular en Torrente Sanguíneo",
            font=("Helvetica", 10),
            bg="#ffffff",
            fg="#7f8c8d"
        )
        subtitulo.pack(side=tk.LEFT, padx=15)

    def crear_panel_controles(self, parent):
        
        panel = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT)
        panel.pack(fill=tk.X, pady=(0, 10))

        sombra = tk.Frame(panel, bg="#e0e0e0", height=1)
        sombra.pack(fill=tk.X, side=tk.BOTTOM)

        contenido = tk.Frame(panel, bg="#ffffff")
        contenido.pack(fill=tk.X, pady=10, padx=20)

        #Botones.
        botones = [
            ("▶ Iniciar", "#27ae60", self.iniciar),
            ("⏸ Pausar", "#f39c12", self.pausar),
            ("⏭ Paso", "#95a5a6", self.paso),
            ("🔄 Reiniciar", "#3498db", self.reiniciar),
            ("💉 Inyectar Virus", "#e74c3c", self.inyectar_virus),
        ]

        for texto, color, comando in botones:
            btn = tk.Button(
                contenido,
                text=texto,
                font=("Helvetica", 10, "bold"),
                bg=color,
                fg="white",
                activebackground=self.oscurecer_color(color),
                activeforeground="white",
                relief=tk.FLAT,
                padx=20,
                pady=8,
                cursor="hand2",
                command=comando
            )
            btn.pack(side=tk.LEFT, padx=4)

            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.oscurecer_color(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

    #Intento de efecto hover.
    def oscurecer_color(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = max(0, r-30), max(0, g-30), max(0, b-30)
        return f'#{r:02x}{g:02x}{b:02x}'

    def crear_panel_simulacion(self, parent):
       
        panel = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT)
        panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        #Panel.
        titulo = tk.Label(
            panel,
            text="🔬 Vista del Torrente Sanguíneo",
            font=("Helvetica", 13, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        titulo.pack(pady=(10, 8), padx=15, anchor="w")

        canvas_container = tk.Frame(panel, bg="#ecf0f1", relief=tk.FLAT, bd=1)
        canvas_container.pack(padx=15, pady=(0, 10))

        self.canvas = tk.Canvas(
            canvas_container,
            width=self.ANCHO_SANGRE * self.TAMANO_CELULA,
            height=self.ALTO_SANGRE * self.TAMANO_CELULA,
            bg="#1a1a1a",
            highlightthickness=0
        )
        self.canvas.pack(padx=2, pady=2)

        #Leyenda.
        leyenda_frame = tk.Frame(panel, bg="#ffffff")
        leyenda_frame.pack(pady=(0, 10), padx=15, fill=tk.X)

        leyendas = [
            ("●", "#dc143c", "Eritrocitos"),
            ("●", "#6495ed", "Leucocitos"),
            ("●", "#ffeb3b", "Virus"),
            ("●", "#ff8c00", "Infectadas"),
            ("●", "#8b0000", "Zombie"),
            ("●", "#ffe0e0", "Plasma"),
        ]

        for simbolo, color, texto in leyendas:
            item_frame = tk.Frame(leyenda_frame, bg="#ffffff")
            item_frame.pack(side=tk.LEFT, padx=8)

            circulo = tk.Label(
                item_frame,
                text=simbolo,
                font=("Helvetica", 14),
                fg=color,
                bg="#ffffff"
            )
            circulo.pack(side=tk.LEFT, padx=(0, 4))

            label = tk.Label(
                item_frame,
                text=texto,
                font=("Helvetica", 9),
                fg="#34495e",
                bg="#ffffff"
            )
            label.pack(side=tk.LEFT)

    def crear_dashboard_medico(self, parent):
        """Crea el dashboard médico."""
        dashboard = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT, width=330)
        dashboard.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(8, 0))
        dashboard.pack_propagate(False)

        #Título.
        titulo = tk.Label(
            dashboard,
            text="📊 Monitoreo Vital",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#2c3e50"
        )
        titulo.pack(pady=(12, 10), padx=15, anchor="w")

        #Barra de temperatura.
        self.crear_metrica_temperatura(dashboard)

        #Barra nivel  
        self.crear_metrica_infeccion(dashboard)

        #Barra de Zombificación.
        self.crear_metrica_zombificacion(dashboard)

        #Sistema Inmune.
        self.crear_metrica_inmune(dashboard)

        #Conteo Celular.
        self.crear_metrica_conteo(dashboard)

    def crear_metrica_temperatura(self, parent):
        panel = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT)
        panel.pack(fill=tk.X, padx=15, pady=5)

        tk.Frame(panel, bg="#ecf0f1", height=1).pack(fill=tk.X, pady=(0, 6))

        label = tk.Label(
            panel,
            text="🌡️ Temperatura Corporal",
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            fg="#34495e"
        )
        label.pack(anchor="w")

        self.etiqueta_temp = tk.Label(
            panel,
            text="37.0°C",
            font=("Helvetica", 24, "bold"),
            bg="#ffffff",
            fg="#27ae60"
        )
        self.etiqueta_temp.pack(anchor="w", pady=(3, 3))

        #Barra de progreso personalizada.
        barra_frame = tk.Frame(panel, bg="#ecf0f1", height=6)
        barra_frame.pack(fill=tk.X, pady=4)

        self.barra_temp_fill = tk.Frame(barra_frame, bg="#27ae60", height=6)
        self.barra_temp_fill.place(x=0, y=0, relwidth=0.88, relheight=1)

        rango = tk.Label(
            panel,
            text="Normal: 36-38°C",
            font=("Helvetica", 8),
            bg="#ffffff",
            fg="#95a5a6"
        )
        rango.pack(anchor="w", pady=(2, 0))

    def crear_metrica_infeccion(self, parent):
        panel = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT)
        panel.pack(fill=tk.X, padx=15, pady=5)

        tk.Frame(panel, bg="#ecf0f1", height=1).pack(fill=tk.X, pady=(0, 6))

        label = tk.Label(
            panel,
            text="🦠 Nivel de Infección",
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            fg="#34495e"
        )
        label.pack(anchor="w")

        self.etiqueta_infeccion = tk.Label(
            panel,
            text="0.0%",
            font=("Helvetica", 24, "bold"),
            bg="#ffffff",
            fg="#95a5a6"
        )
        self.etiqueta_infeccion.pack(anchor="w", pady=(3, 3))

        barra_frame = tk.Frame(panel, bg="#ecf0f1", height=6)
        barra_frame.pack(fill=tk.X, pady=4)

        self.barra_infeccion_fill = tk.Frame(barra_frame, bg="#95a5a6", height=6)
        self.barra_infeccion_fill.place(x=0, y=0, relwidth=0, relheight=1)

    def crear_metrica_zombificacion(self, parent):
        panel = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT)
        panel.pack(fill=tk.X, padx=15, pady=5)

        tk.Frame(panel, bg="#ecf0f1", height=1).pack(fill=tk.X, pady=(0, 6))

        label = tk.Label(
            panel,
            text="🧟 Estado de Zombificación",
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            fg="#34495e"
        )
        label.pack(anchor="w")

        self.etiqueta_estado_zombie = tk.Label(
            panel,
            text="✓ Saludable",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#27ae60"
        )
        self.etiqueta_estado_zombie.pack(anchor="w", pady=(3, 2))

        self.etiqueta_etapa = tk.Label(
            panel,
            text="Etapa: Normal",
            font=("Helvetica", 9),
            bg="#ffffff",
            fg="#95a5a6"
        )
        self.etiqueta_etapa.pack(anchor="w")

    def crear_metrica_inmune(self, parent):
        """Crea la métrica del sistema inmune."""
        panel = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT)
        panel.pack(fill=tk.X, padx=15, pady=5)

        tk.Frame(panel, bg="#ecf0f1", height=1).pack(fill=tk.X, pady=(0, 6))

        label = tk.Label(
            panel,
            text="🛡️ Sistema Inmune",
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            fg="#34495e"
        )
        label.pack(anchor="w")

        barra_frame = tk.Frame(panel, bg="#ecf0f1", height=6)
        barra_frame.pack(fill=tk.X, pady=6)

        self.barra_inmune_fill = tk.Frame(barra_frame, bg="#3498db", height=6)
        self.barra_inmune_fill.place(x=0, y=0, relwidth=0, relheight=1)

        self.etiqueta_inmune = tk.Label(
            panel,
            text="Eficiencia: 0%",
            font=("Helvetica", 9),
            bg="#ffffff",
            fg="#3498db"
        )
        self.etiqueta_inmune.pack(anchor="w")

    def crear_metrica_conteo(self, parent):
        """Crea la métrica de conteo celular."""
        panel = tk.Frame(parent, bg="#ffffff", relief=tk.FLAT)
        panel.pack(fill=tk.X, padx=15, pady=5)

        tk.Frame(panel, bg="#ecf0f1", height=1).pack(fill=tk.X, pady=(0, 6))

        label = tk.Label(
            panel,
            text="🔬 Análisis Celular",
            font=("Helvetica", 10, "bold"),
            bg="#ffffff",
            fg="#34495e"
        )
        label.pack(anchor="w", pady=(0, 6))

        #Contadores para sección.
        self.etiqueta_globulos_rojos = self.crear_contador(panel, "●", "#dc143c", "Eritrocitos: 0")
        self.etiqueta_globulos_blancos = self.crear_contador(panel, "●", "#6495ed", "Leucocitos: 0")
        self.etiqueta_celulas_infectadas = self.crear_contador(panel, "●", "#ff8c00", "Infectadas: 0")
        self.etiqueta_virus = self.crear_contador(panel, "●", "#ffeb3b", "Virus: 0")
        self.etiqueta_zombie = self.crear_contador(panel, "●", "#8b0000", "Zombie: 0")

    def crear_contador(self, parent, simbolo, color, texto_inicial):
        frame = tk.Frame(parent, bg="#ffffff")
        frame.pack(fill=tk.X, pady=2)

        circulo = tk.Label(
            frame,
            text=simbolo,
            font=("Helvetica", 10),
            fg=color,
            bg="#ffffff"
        )
        circulo.pack(side=tk.LEFT, padx=(0, 6))

        label = tk.Label(
            frame,
            text=texto_inicial,
            font=("Helvetica", 9),
            bg="#ffffff",
            fg="#34495e",
            anchor="w"
        )
        label.pack(side=tk.LEFT, fill=tk.X)

        return label

    def rgb_a_hex(self, rgb_tuple):
        return f'#{rgb_tuple[0]:02x}{rgb_tuple[1]:02x}{rgb_tuple[2]:02x}'

    def dibujar_sangre(self):
        self.canvas.delete("all")

        for fila in range(self.torrente_sanguineo.obtenerAlto()):
            for col in range(self.torrente_sanguineo.obtenerAncho()):
                estado = self.torrente_sanguineo.obtenerEstadoCelula(fila, col)
                color = self.rgb_a_hex(estado.obtenerColor())

                x1 = col * self.TAMANO_CELULA
                y1 = fila * self.TAMANO_CELULA
                x2 = x1 + self.TAMANO_CELULA - 1
                y2 = y1 + self.TAMANO_CELULA - 1

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def actualizar_visualizacion(self):
        self.dibujar_sangre()

        #Actualización Temperatura.
        temp = self.torrente_sanguineo.obtenerTemperaturaCorporal()
        self.etiqueta_temp.config(text=f"{temp:.1f}°C")

        #Actualizar barra y color de temperatura.
        temp_percent = min(1.0, max(0.0, (temp - 36) / 6))
        self.barra_temp_fill.place(relwidth=temp_percent)

        if temp > 39.5:
            color_temp = "#e74c3c"
        elif temp > 38.0:
            color_temp = "#f39c12"
        elif temp < 36.0:
            color_temp = "#3498db"
        else:
            color_temp = "#27ae60"

        self.etiqueta_temp.config(fg=color_temp)
        self.barra_temp_fill.config(bg=color_temp)

        #Infección.
        tasa_infeccion = self.torrente_sanguineo.obtenerTasaInfeccion()
        self.etiqueta_infeccion.config(text=f"{tasa_infeccion:.1f}%")
        self.barra_infeccion_fill.place(relwidth=min(1.0, max(0.0, tasa_infeccion / 100.0)))

        if tasa_infeccion > 70:
            color_inf = "#c0392b"
        elif tasa_infeccion > 40:
            color_inf = "#e74c3c"
        elif tasa_infeccion > 10:
            color_inf = "#f39c12"
        else:
            color_inf = "#95a5a6"

        self.etiqueta_infeccion.config(fg=color_inf)
        self.barra_infeccion_fill.config(bg=color_inf)

        #Actualización Zombificación.
        if self.torrente_sanguineo.obtenerEstaZombificado():
            self.etiqueta_estado_zombie.config(text="☠ Zombificado", fg="#c0392b")
        else:
            self.etiqueta_estado_zombie.config(text="✓ Saludable", fg="#27ae60")

        self.etiqueta_etapa.config(text=f"Etapa: {self.torrente_sanguineo.obtenerEtapaInfeccion()}")

        #Actualización Sistema Inmune.
        eficiencia = self.torrente_sanguineo.obtenerEficienciaInmune()
        self.barra_inmune_fill.place(relwidth=min(1.0, max(0.0, eficiencia / 100.0)))
        self.etiqueta_inmune.config(text=f"Eficiencia: {eficiencia:.0f}%")

        #Actualización del conteo celular.
        self.etiqueta_globulos_rojos.config(
            text=f"Eritrocitos: {self.torrente_sanguineo.obtenerGlobulosRojos()}"
        )
        self.etiqueta_globulos_blancos.config(
            text=f"Leucocitos: {self.torrente_sanguineo.obtenerGlobulosBlancos()} "
                 f"(Activos: {self.torrente_sanguineo.obtenerCelulasInmunesActivas()})"
        )
        self.etiqueta_celulas_infectadas.config(
            text=f"Infectadas: {self.torrente_sanguineo.obtenerCelulasInfectadas()}"
        )
        self.etiqueta_virus.config(
            text=f"Virus: {self.torrente_sanguineo.obtenerParticulasVirus()}"
        )
        self.etiqueta_zombie.config(
            text=f"Zombie: {self.torrente_sanguineo.obtenerCelulasZombie()}"
        )

    def loop_simulacion(self):
        while self.ejecutando:
            self.torrente_sanguineo.paso()
            #actualizar GUI desde thread con after 
            self.root.after(0, self.actualizar_visualizacion)
            self.root.after(0, self.verificar_zombificacion)
            time.sleep(0.2)

    #Iniciación de la simmulación.
    def iniciar(self):
        if not self.ejecutando:
            self.ejecutando = True
            self.hilo_simulacion = threading.Thread(target=self.loop_simulacion, daemon=True)
            self.hilo_simulacion.start()

    def pausar(self):
        self.ejecutando = False

    def paso(self):
        self.torrente_sanguineo.paso()
        self.actualizar_visualizacion()
        self.verificar_zombificacion()

    def reiniciar(self):
        self.ejecutando = False
        time.sleep(0.3)
        self.torrente_sanguineo = GrillaTorrenteSanguineo(self.ANCHO_SANGRE, self.ALTO_SANGRE)
        self.actualizar_visualizacion()

    def inyectar_virus(self):
        radio = 3 + int(random.random() * 5)
        margen = radio + 5
        fila = margen + int(random.random() * (self.ALTO_SANGRE - 2 * margen))
        col = margen + int(random.random() * (self.ANCHO_SANGRE - 2 * margen))

        self.torrente_sanguineo.introducirVirus(fila, col, radio)

        messagebox.showinfo(
            "Virus Inyectado",
            f"💉 Virus zombie introducido en el sistema\n\n"
            f"Posición: Fila {fila}, Columna {col}\n"
            f"Radio de infección: {radio} células\n\n"
            f"Observe la propagación de la infección."
        )

        self.actualizar_visualizacion()

    def verificar_zombificacion(self):
        if self.torrente_sanguineo.obtenerEstaZombificado() and self.ejecutando:
            self.ejecutando = False

            messagebox.showerror(
                "Zombificación Completa",
                f"☠ CONVERSIÓN A ZOMBIE COMPLETA ☠\n\n"
                f"Infección: {self.torrente_sanguineo.obtenerTasaInfeccion():.1f}%\n"
                f"Temperatura: {self.torrente_sanguineo.obtenerTemperaturaCorporal():.1f}°C\n"
                f"Generación: {self.torrente_sanguineo.obtenerGeneracion()}\n\n"
                f"El sujeto ha sido completamente zombificado."
            )

    def cerrar(self):
        self.ejecutando = False
        time.sleep(0.3)
        self.root.destroy()

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    simulador = Simulador()
    simulador.ejecutar()
