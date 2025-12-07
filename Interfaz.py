# interface.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ProcesoDatos import cargar_limpiar_datos
from AnalisisRegresion import calcular_BOD5, stepwise_regression, calculate_correlation_matrix, stepwise_regression_od
import io
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
matplotlib.use('TkAgg')
import mplcursors

# Nombres de meses en español
MESES_ESP = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
             7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}

# Paleta de colores profesional
COLOR_DARK_TEAL = "#1a3a3a"
COLOR_TEAL = "#2d5a5a"
COLOR_GREEN = "#3d8b6e"
COLOR_LIGHT_GREEN = "#5cb88a"
COLOR_ACCENT = "#7ed3a4"
COLOR_LIGHT_TEAL = "#e8f4f0"
COLOR_WHITE = "#FFFFFF"
COLOR_LIGHT_GRAY = "#f8f9fa"
COLOR_BORDER = "#e0e0e0"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Regresión para DBO5")
        self.root.geometry("1400x850")
        self.root.configure(bg=COLOR_LIGHT_GRAY)
        self.root.minsize(1200, 700)
        
        # Variable para almacenar el archivo cargado
        self.file_path = None
        self.data = None
        self.current_figure = None
        self.current_canvas = None
        
        # Crear la pantalla inicial
        self.create_initial_screen()

    def create_initial_screen(self):
        """Crea la pantalla inicial con el botón para cargar archivo"""
        # Frame principal
        self.initial_frame = tk.Frame(self.root, bg=COLOR_LIGHT_GRAY)
        self.initial_frame.pack(fill="both", expand=True)
        
        # Contenedor central
        center_container = tk.Frame(self.initial_frame, bg=COLOR_LIGHT_GRAY)
        center_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        title_label = tk.Label(
            center_container,
            text="Análisis de Regresión\npara DBO5",
            font=("Segoe UI", 36, "bold"),
            bg=COLOR_LIGHT_GRAY,
            fg=COLOR_DARK_TEAL
        )
        title_label.pack(pady=(0, 15))
        
        # Línea decorativa
        line_frame = tk.Frame(center_container, bg=COLOR_GREEN, height=3, width=200)
        line_frame.pack(pady=(0, 20))
        
        # Subtítulo
        subtitle_label = tk.Label(
            center_container,
            text="Sistema de análisis de datos del Río Atoyac",
            font=("Segoe UI", 14),
            bg=COLOR_LIGHT_GRAY,
            fg=COLOR_TEAL
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Descripción del proyecto
        description_text = (
            "Este sistema analiza la calidad del agua del Río Atoyac\n"
            "mediante modelos de regresión para predecir la Demanda Bioquímica\n"
            "de Oxígeno (DBO5) utilizando parámetros como Oxígeno Disuelto (OD),\n"
            "Demanda Química de Oxígeno (DQO), pH, Sólidos Suspendidos Totales\n"
            "(SST) y temperatura."
        )
        
        description_label = tk.Label(
            center_container,
            text=description_text,
            font=("Segoe UI", 11),
            bg=COLOR_LIGHT_GRAY,
            fg=COLOR_TEAL,
            justify="center",
            wraplength=500
        )
        description_label.pack(pady=(0, 40))
        
        # Botón de cargar archivo
        load_button = tk.Button(
            center_container,
            text="📁  Cargar Datos (Excel)",
            font=("Segoe UI", 14, "bold"),
            bg=COLOR_GREEN,
            fg=COLOR_WHITE,
            activebackground=COLOR_LIGHT_GREEN,
            activeforeground=COLOR_WHITE,
            relief="flat",
            padx=35,
            pady=15,
            cursor="hand2",
            command=self.load_file,
            borderwidth=0
        )
        load_button.pack()
        
        # Hover effect
        load_button.bind("<Enter>", lambda e: load_button.config(bg=COLOR_LIGHT_GREEN))
        load_button.bind("<Leave>", lambda e: load_button.config(bg=COLOR_GREEN))

    def create_main_interface(self):
        """Crea la interfaz principal con barra lateral y área de resultados"""
        # Destruir la pantalla inicial
        self.initial_frame.destroy()
        
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg=COLOR_LIGHT_GRAY)
        self.main_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(self.main_frame, bg=COLOR_DARK_TEAL, height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="📊  Análisis de Regresión DBO5",
            font=("Segoe UI", 18, "bold"),
            bg=COLOR_DARK_TEAL,
            fg=COLOR_WHITE
        )
        header_label.pack(side="left", padx=25, pady=12)
        
        # Botón para recargar archivo
        reload_button = tk.Button(
            header_frame,
            text="🔄  Cambiar Archivo",
            font=("Segoe UI", 10),
            bg=COLOR_TEAL,
            fg=COLOR_WHITE,
            activebackground=COLOR_GREEN,
            activeforeground=COLOR_WHITE,
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.reload_file,
            borderwidth=0
        )
        reload_button.pack(side="right", padx=(10, 25), pady=12)
        reload_button.bind("<Enter>", lambda e: reload_button.config(bg=COLOR_GREEN))
        reload_button.bind("<Leave>", lambda e: reload_button.config(bg=COLOR_TEAL))
        
        # Botón para salir
        exit_button = tk.Button(
            header_frame,
            text="🚪  Salir",
            font=("Segoe UI", 10),
            bg="#8b3a3a",
            fg=COLOR_WHITE,
            activebackground="#a04545",
            activeforeground=COLOR_WHITE,
            relief="flat",
            padx=15,
            pady=6,
            cursor="hand2",
            command=self.confirm_exit,
            borderwidth=0
        )
        exit_button.pack(side="right", padx=10, pady=12)
        exit_button.bind("<Enter>", lambda e: exit_button.config(bg="#a04545"))
        exit_button.bind("<Leave>", lambda e: exit_button.config(bg="#8b3a3a"))
        
        # Contenedor para sidebar y área de contenido
        self.content_container = tk.Frame(self.main_frame, bg=COLOR_LIGHT_GRAY)
        self.content_container.pack(fill="both", expand=True)
        
        # Crear sidebar fija
        self.create_sidebar()
        self.sidebar.pack(side="left", fill="y")
        
        # Área de contenido principal (donde se mostrarán las gráficas)
        self.content_area = tk.Frame(self.content_container, bg=COLOR_WHITE)
        self.content_area.pack(side="right", fill="both", expand=True, padx=(0, 0))
        
        # Frame interior con padding
        self.display_frame = tk.Frame(self.content_area, bg=COLOR_WHITE)
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Mostrar mensaje de bienvenida
        self.show_welcome()

    def show_welcome(self):
        """Muestra el mensaje de bienvenida en el área de contenido"""
        self.clear_display()
        
        welcome_container = tk.Frame(self.display_frame, bg=COLOR_WHITE)
        welcome_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Icono grande
        icon_label = tk.Label(
            welcome_container,
            text="📈",
            font=("Segoe UI", 64),
            bg=COLOR_WHITE
        )
        icon_label.pack(pady=(0, 20))
        
        welcome_label = tk.Label(
            welcome_container,
            text="Bienvenido al Sistema de Análisis",
            font=("Segoe UI", 20, "bold"),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        welcome_label.pack(pady=(0, 10))
        
        instruction_label = tk.Label(
            welcome_container,
            text="Seleccione una opción del menú lateral para comenzar\nel análisis de los datos cargados.",
            font=("Segoe UI", 12),
            bg=COLOR_WHITE,
            fg=COLOR_TEAL,
            justify="center"
        )
        instruction_label.pack()

    def clear_display(self):
        """Limpia el área de visualización"""
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        if self.current_canvas:
            self.current_canvas = None
        if self.current_figure:
            plt.close(self.current_figure)
            self.current_figure = None

    def get_available_years(self):
        """Obtiene los años disponibles en los datos"""
        if self.data is not None and 'AÑO' in self.data.columns:
            years = sorted(self.data['AÑO'].dropna().unique().astype(int).tolist())
            return years
        return []

    def embed_figure_with_filter(self, plot_function, title="", column_name="", y_label="", color="#3d8b6e", log_scale=False):
        """Embebe una figura con filtro por año"""
        self.clear_display()
        
        # Frame superior para título y filtro
        header_frame = tk.Frame(self.display_frame, bg=COLOR_WHITE)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Título
        title_label = tk.Label(
            header_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        title_label.pack(side="left")
        
        # Frame para el filtro (a la derecha)
        filter_frame = tk.Frame(header_frame, bg=COLOR_WHITE)
        filter_frame.pack(side="right")
        
        # Label del filtro
        filter_label = tk.Label(
            filter_frame,
            text="📅 Filtrar por año:",
            font=("Segoe UI", 10),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        filter_label.pack(side="left", padx=(0, 10))
        
        # Combobox para seleccionar año
        years = self.get_available_years()
        year_options = ["Todos los años"] + [str(y) for y in years]
        
        self.year_var = tk.StringVar(value="Todos los años")
        year_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.year_var,
            values=year_options,
            state="readonly",
            width=15,
            font=("Segoe UI", 10)
        )
        year_combo.pack(side="left")
        
        # Estilo del combobox
        style = ttk.Style()
        style.configure("TCombobox", padding=5)
        
        # Frame para la figura
        self.fig_container = tk.Frame(self.display_frame, bg=COLOR_WHITE, relief="solid", borderwidth=1)
        self.fig_container.pack(fill="both", expand=True)
        
        # Guardar parámetros para actualizar
        self.current_plot_params = {
            'column_name': column_name,
            'y_label': y_label,
            'color': color,
            'log_scale': log_scale,
            'title': title
        }
        
        # Función para actualizar gráfica
        def update_plot(*args):
            self.update_visualization_plot()
        
        year_combo.bind("<<ComboboxSelected>>", update_plot)
        
        # Dibujar gráfica inicial
        self.update_visualization_plot()

    def update_visualization_plot(self):
        """Actualiza la gráfica de visualización según el filtro"""
        # Limpiar contenedor de figura
        for widget in self.fig_container.winfo_children():
            widget.destroy()
        
        if self.current_figure:
            plt.close(self.current_figure)
        
        # Obtener datos filtrados
        selected_year = self.year_var.get()
        if selected_year == "Todos los años":
            filtered_data = self.data.copy()
        else:
            filtered_data = self.data[self.data['AÑO'] == int(selected_year)].copy()
        
        params = self.current_plot_params
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if len(filtered_data) > 0:
            # Ordenar por fecha si existe
            if 'FECHA_DT' in filtered_data.columns:
                filtered_data = filtered_data.sort_values('FECHA_DT')
            
            valores = filtered_data[params['column_name']].values
            x_pos = range(len(filtered_data))
            
            # Graficar
            line, = ax.plot(x_pos, valores, 'o-', color=params['color'], markersize=6, linewidth=1.5)
            
            # Configurar eje X según el filtro seleccionado
            if selected_year == "Todos los años":
                # Mostrar observaciones cuando se selecciona "Todos los años"
                ax.set_xlabel("Observaciones", fontsize=10)
            elif 'MES' in filtered_data.columns and 'AÑO' in filtered_data.columns:
                # Mostrar meses cuando se filtra por un año específico
                meses = filtered_data['MES'].values
                años = filtered_data['AÑO'].values
                x_labels = [f"{MESES_ESP.get(int(m), m)}" for m, a in zip(meses, años)]
                
                # Configurar etiquetas del eje X (mostrar cada N etiquetas para evitar saturación)
                n_labels = len(x_labels)
                if n_labels > 20:
                    step = n_labels // 15
                else:
                    step = 1
                
                ax.set_xticks(range(0, n_labels, step))
                ax.set_xticklabels([x_labels[i] for i in range(0, n_labels, step)], rotation=45, ha='right')
                ax.set_xlabel("Mes", fontsize=10)
            else:
                ax.set_xlabel("Observaciones", fontsize=10)
            
            # Agregar estadísticas
            mean_val = filtered_data[params['column_name']].mean()
            ax.axhline(y=mean_val, color='red', linestyle='--', alpha=0.7, 
                      label=f'Media: {mean_val:.2f}')
            ax.legend(loc='upper right')
            
            # Agregar interactividad con mplcursors
            cursor = mplcursors.cursor(line, hover=True)
            
            # Guardar datos para el cursor
            self._cursor_data = {
                'valores': valores,
                'meses': filtered_data['MES'].values if 'MES' in filtered_data.columns else None,
                'años': filtered_data['AÑO'].values if 'AÑO' in filtered_data.columns else None,
                'y_label': params['y_label']
            }
            
            @cursor.connect("add")
            def on_add(sel):
                idx = int(sel.index)
                valor = self._cursor_data['valores'][idx]
                if self._cursor_data['meses'] is not None:
                    mes = MESES_ESP.get(int(self._cursor_data['meses'][idx]), self._cursor_data['meses'][idx])
                    año = int(self._cursor_data['años'][idx])
                    sel.annotation.set_text(f"{mes} {año}\n{self._cursor_data['y_label']}: {valor:.2f}")
                else:
                    sel.annotation.set_text(f"Obs {idx+1}\n{self._cursor_data['y_label']}: {valor:.2f}")
                sel.annotation.get_bbox_patch().set(fc="white", alpha=0.9)
        else:
            ax.text(0.5, 0.5, 'No hay datos para el año seleccionado', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=12)
        
        ax.set_ylabel(params['y_label'], fontsize=10)
        
        # Título con año si está filtrado
        title_base = params['title'].replace('🌡️', '').replace('💧', '').replace('🧪', '').replace('🔬', '').replace('⚗️', '').strip()
        if selected_year != "Todos los años":
            ax.set_title(f"{title_base} - Año {selected_year}", fontsize=12, fontweight='bold')
        else:
            ax.set_title(title_base, fontsize=12, fontweight='bold')
        
        ax.grid(True, alpha=0.3)
        
        if params['log_scale']:
            ax.set_yscale("log")
            ax.grid(True, alpha=0.3, which="both")
        
        fig.tight_layout()
        
        # Canvas de matplotlib
        self.current_figure = fig
        self.current_canvas = FigureCanvasTkAgg(fig, master=self.fig_container)
        self.current_canvas.draw()
        
        # Toolbar de navegación
        toolbar_frame = tk.Frame(self.fig_container, bg=COLOR_LIGHT_GRAY)
        toolbar_frame.pack(side="bottom", fill="x")
        toolbar = NavigationToolbar2Tk(self.current_canvas, toolbar_frame)
        toolbar.update()
        
        # Widget del canvas
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def create_sidebar(self):
        """Crea la barra lateral con todos los botones centrados y scroll"""
        self.sidebar = tk.Frame(self.content_container, bg=COLOR_DARK_TEAL, width=280)
        self.sidebar.pack_propagate(False)
        
        # Canvas para scroll
        sidebar_canvas = tk.Canvas(self.sidebar, bg=COLOR_DARK_TEAL, highlightthickness=0, width=265)
        scrollbar = tk.Scrollbar(self.sidebar, orient="vertical", command=sidebar_canvas.yview)
        
        # Frame scrollable dentro del canvas
        sidebar_inner = tk.Frame(sidebar_canvas, bg=COLOR_DARK_TEAL)
        
        # Configurar scroll
        sidebar_inner.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )
        
        sidebar_canvas.create_window((0, 0), window=sidebar_inner, anchor="nw", width=265)
        sidebar_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas y scrollbar
        scrollbar.pack(side="right", fill="y")
        sidebar_canvas.pack(side="left", fill="both", expand=True)
        
        # Guardar referencia del canvas para el scroll
        self.sidebar_canvas = sidebar_canvas
        
        # Título de la sidebar
        sidebar_title = tk.Label(
            sidebar_inner,
            text="MENÚ DE ANÁLISIS",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_DARK_TEAL,
            fg=COLOR_WHITE
        )
        sidebar_title.pack(fill="x", pady=(15, 20), padx=15)
        
        # Separador
        sep = tk.Frame(sidebar_inner, bg=COLOR_TEAL, height=1)
        sep.pack(fill="x", pady=(0, 15), padx=15)
        
        # Definir botones con iconos y texto separados
        button_groups = [
            {
                "title": "📊 Análisis Estadístico",
                "buttons": [
                    ("📋", "Matriz de Correlación", self.show_correlation),
                    ("📐", "Regresión Paso a Paso", self.run_regression)
                ]
            },
            {
                "title": "📉 Visualización",
                "buttons": [
                    ("🌡️", "Temperatura", self.vista_temp),
                    ("💧", "Oxígeno Disuelto (OD)", self.vista_od),
                    ("🧪", "pH", self.vista_ph),
                    ("🔬", "Demanda Química de Oxígeno (DQO)", self.vista_dqo),
                    ("🧪", "Demanda Bioquímica de Oxígeno (DBO5)", self.vista_dbo5),
                    ("⚗️", "Sólidos Suspendidos Totales (SST)", self.vista_sst)
                ]
            },
            {
                "title": "🎯 Predicción",
                "buttons": [
                    ("📈", "Comparación DBO5", self.vista_dbo5_mes_vs_pred),
                    ("📉", "DBO5 vs Predicción", self.vista_dbo5_vs_pred),
                    ("⚠️", "Residuales", self.vista_residuals),
                    ("🎯", "Predicción OD", self.vista_tss_bod5),
                    ("🎯", "Predicción DQO", self.run_regression_dqo)
                ]
            },
            {
                "title": "🔮 Herramientas Avanzadas",
                "buttons": [
                    ("📅", "Tendencia Temporal", self.vista_tendencia_temporal),
                    ("🖩", "Simulador DBO5", self.vista_simulador)
                ]
            }
        ]
        
        # Crear grupos de botones
        for group in button_groups:
            # Título del grupo
            group_label = tk.Label(
                sidebar_inner,
                text=group["title"],
                font=("Segoe UI", 10, "bold"),
                bg=COLOR_DARK_TEAL,
                fg=COLOR_ACCENT,
                anchor="center"
            )
            group_label.pack(fill="x", pady=(15, 8), padx=10)
            
            # Botones del grupo
            for btn_icon, btn_text, btn_command in group["buttons"]:
                self.create_menu_button(sidebar_inner, btn_icon, btn_text, btn_command)
        
        # Espacio al final para mejor scroll
        spacer = tk.Frame(sidebar_inner, bg=COLOR_DARK_TEAL, height=20)
        spacer.pack(fill="x")

    def create_menu_button(self, parent, icon, text, command):
        """Crea un botón de menú estilizado"""
        btn_frame = tk.Frame(parent, bg=COLOR_TEAL, cursor="hand2")
        btn_frame.pack(fill="x", pady=2, padx=10)
        
        # Contenedor interior para centrar
        inner_frame = tk.Frame(btn_frame, bg=COLOR_TEAL)
        inner_frame.pack(fill="x", padx=10, pady=8)
        
        # Label para el icono
        icon_label = tk.Label(
            inner_frame,
            text=icon,
            font=("Segoe UI", 11),
            bg=COLOR_TEAL,
            fg=COLOR_WHITE,
            width=2
        )
        icon_label.pack(side="left", padx=(5, 8))
        
        # Label para el texto
        text_label = tk.Label(
            inner_frame,
            text=text,
            font=("Segoe UI", 10),
            bg=COLOR_TEAL,
            fg=COLOR_WHITE,
            anchor="w"
        )
        text_label.pack(side="left", fill="x", expand=True)
        
        # Hover effects
        def on_enter(e):
            btn_frame.config(bg=COLOR_LIGHT_GREEN)
            inner_frame.config(bg=COLOR_LIGHT_GREEN)
            icon_label.config(bg=COLOR_LIGHT_GREEN)
            text_label.config(bg=COLOR_LIGHT_GREEN)
        
        def on_leave(e):
            btn_frame.config(bg=COLOR_TEAL)
            inner_frame.config(bg=COLOR_TEAL)
            icon_label.config(bg=COLOR_TEAL)
            text_label.config(bg=COLOR_TEAL)
        
        # Función para scroll con mousewheel
        def on_mousewheel(event):
            if hasattr(self, 'sidebar_canvas'):
                self.sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind eventos hover, click y scroll
        for widget in [btn_frame, inner_frame, icon_label, text_label]:
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e, cmd=command: cmd())
            widget.bind("<MouseWheel>", on_mousewheel)

    def embed_figure(self, fig, title=""):
        """Embebe una figura de matplotlib en el área de contenido"""
        self.clear_display()
        
        # Título de la sección
        if title:
            title_frame = tk.Frame(self.display_frame, bg=COLOR_WHITE)
            title_frame.pack(fill="x", pady=(0, 10))
            
            title_label = tk.Label(
                title_frame,
                text=title,
                font=("Segoe UI", 16, "bold"),
                bg=COLOR_WHITE,
                fg=COLOR_DARK_TEAL
            )
            title_label.pack(side="left")
        
        # Frame para la figura
        fig_frame = tk.Frame(self.display_frame, bg=COLOR_WHITE, relief="solid", borderwidth=1)
        fig_frame.pack(fill="both", expand=True)
        
        # Ajustar el tamaño de la figura
        fig.set_size_inches(10, 6)
        fig.tight_layout()
        
        # Canvas de matplotlib
        self.current_figure = fig
        self.current_canvas = FigureCanvasTkAgg(fig, master=fig_frame)
        self.current_canvas.draw()
        
        # Toolbar de navegación
        toolbar_frame = tk.Frame(fig_frame, bg=COLOR_LIGHT_GRAY)
        toolbar_frame.pack(side="bottom", fill="x")
        toolbar = NavigationToolbar2Tk(self.current_canvas, toolbar_frame)
        toolbar.update()
        
        # Widget del canvas
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

    def show_text_result(self, title, content, description=""):
        """Muestra resultados de texto en el área de contenido"""
        self.clear_display()
        
        # Título
        title_label = tk.Label(
            self.display_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        title_label.pack(anchor="w", pady=(0, 8))
        
        # Descripción
        if description:
            desc_frame = tk.Frame(self.display_frame, bg="#e3f2fd", relief="flat")
            desc_frame.pack(fill="x", pady=(0, 15))
            
            desc_label = tk.Label(
                desc_frame,
                text=f"💡 {description}",
                font=("Segoe UI", 9),
                bg="#e3f2fd",
                fg="#1565c0",
                justify="left",
                wraplength=800,
                pady=8,
                padx=10
            )
            desc_label.pack(anchor="w")
        
        # Frame con borde para el contenido
        content_frame = tk.Frame(self.display_frame, bg=COLOR_LIGHT_GRAY, relief="solid", borderwidth=1)
        content_frame.pack(fill="both", expand=True)
        
        # Text widget con scroll
        text_scroll = tk.Scrollbar(content_frame)
        text_scroll.pack(side="right", fill="y")
        
        text_widget = tk.Text(
            content_frame,
            wrap="word",
            font=("Consolas", 10),
            bg=COLOR_LIGHT_GRAY,
            fg=COLOR_DARK_TEAL,
            relief="flat",
            padx=15,
            pady=15,
            yscrollcommand=text_scroll.set
        )
        text_widget.pack(side="left", fill="both", expand=True)
        text_scroll.config(command=text_widget.yview)
        
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")

    def load_file(self):
        """Dialogo para cargar archivo"""
        file_path = filedialog.askopenfilename(
            title="Selecciona un archivo de Excel",
            filetypes=[("Archivos de Excel", "*.xlsx")]
        )
        if not file_path:
            return

        self.file_path = file_path
        try:
            self.data = cargar_limpiar_datos(self.file_path)
            messagebox.showinfo("✅ Éxito", "Datos cargados y limpiados exitosamente.")
            self.create_main_interface()
        except Exception as e:
            messagebox.showerror("❌ Error", f"No se pudo cargar el archivo:\n{e}")

    def reload_file(self):
        """Recargar archivo y volver a la pantalla inicial"""
        self.data = None
        self.file_path = None
        if self.current_figure:
            plt.close(self.current_figure)
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_initial_screen()

    def confirm_exit(self):
        """Muestra diálogo de confirmación para salir"""
        result = messagebox.askyesno(
            "Confirmar Salida",
            "¿Está seguro que desea salir del programa?",
            icon="question"
        )
        if result:
            if self.current_figure:
                plt.close(self.current_figure)
            self.root.quit()
            self.root.destroy()

    def show_correlation(self):
        """Muestra la matriz de correlación"""
        if self.data is not None:
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            correlation_matrix = calculate_correlation_matrix(self.data, target_column='DBO5')
            
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            description = ("La matriz de correlación muestra qué tan relacionadas están las variables entre sí. "
                          "Valores cercanos a 1 o -1 indican fuerte relación (positiva o negativa), mientras que "
                          "valores cercanos a 0 indican poca o ninguna relación lineal. Esto ayuda a identificar "
                          "qué variables son mejores predictores de la DBO5.")
            
            self.show_text_result("📊 Matriz de Correlación", output, description)
        else:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            
    def run_regression(self):
        """Ejecuta la regresión paso a paso"""
        if self.data is not None:
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            X = self.data[['pH_CAMPO', 'DQO_TOT', 'OD_mg/L', 'SST', 'TEMP_AGUA']]
            y = self.data['DBO5']
            self.model = stepwise_regression(X, y)
            
            sys.stdout = old_stdout
            output = captured_output.getvalue()
            
            description = ("La regresión paso a paso (stepwise) construye un modelo predictivo seleccionando automáticamente "
                          "las variables más significativas. Comienza sin variables y añade una a una las que más mejoran "
                          "el modelo, evaluando en cada paso si alguna variable debe eliminarse. El resultado es un modelo "
                          "optimizado que predice la DBO5 usando solo las variables más relevantes.")
            
            self.show_text_result("📐 Regresión Paso a Paso", output, description)
        else:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")

    def vista_temp(self):
        """Gráfica de Temperatura con filtro por año"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        
        self.embed_figure_with_filter(
            plot_function=None,
            title="🌡️ Temperatura del Agua",
            column_name='TEMP_AGUA',
            y_label="Temperatura (°C)",
            color="#3d8b6e"
        )
    
    def vista_od(self):
        """Gráfica de Oxígeno Disuelto (OD) con filtro por año"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        
        self.embed_figure_with_filter(
            plot_function=None,
            title="💧 Oxígeno Disuelto (OD)",
            column_name='OD_mg/L',
            y_label="Oxígeno Disuelto (mg/L)",
            color="#3d8b6e"
        )
    
    def vista_ph(self):
        """Gráfica de pH con filtro por año"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        
        self.embed_figure_with_filter(
            plot_function=None,
            title="🧪 Potencial de Hidrógeno (pH)",
            column_name='pH_CAMPO',
            y_label="pH",
            color="#9b59b6"
        )
    
    def vista_dqo(self):
        """Gráfica de DQO con filtro por año"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        
        self.embed_figure_with_filter(
            plot_function=None,
            title="🔬 Demanda Química de Oxígeno (DQO)",
            column_name='DQO_TOT',
            y_label="Demanda Química de Oxígeno (mg/L)",
            color="#e67e22"
        )

    def vista_sst(self):
        """Gráfica de SST con filtro por año"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        
        self.embed_figure_with_filter(
            plot_function=None,
            title="⚗️ Sólidos Suspendidos Totales (SST)",
            column_name='SST',
            y_label="Sólidos Suspendidos Totales (mg/L)",
            color="#9b59b6",
            log_scale=True
        )

    def vista_dbo5(self):
        """Gráfica de DBO5 con filtro por año"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        
        self.embed_figure_with_filter(
            plot_function=None,
            title="🧪 Demanda Bioquímica de Oxígeno (DBO5)",
            column_name='DBO5',
            y_label="Demanda Bioquímica de Oxígeno (mg/L)",
            color="#3498db"
        )

    def embed_prediction_figure(self, fig, title="", stats_info="", description=""):
        """Embebe una figura de predicción con panel de estadísticas y descripción"""
        self.clear_display()
        
        # Frame superior para título y descripción
        header_frame = tk.Frame(self.display_frame, bg=COLOR_WHITE)
        header_frame.pack(fill="x", pady=(0, 10))
        
        title_label = tk.Label(
            header_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        title_label.pack(anchor="w")
        
        # Descripción de la gráfica
        if description:
            desc_frame = tk.Frame(header_frame, bg="#e3f2fd", relief="flat")
            desc_frame.pack(fill="x", pady=(8, 0))
            
            desc_label = tk.Label(
                desc_frame,
                text=f"💡 {description}",
                font=("Segoe UI", 9),
                bg="#e3f2fd",
                fg="#1565c0",
                justify="left",
                wraplength=800,
                pady=8,
                padx=10
            )
            desc_label.pack(anchor="w")
        
        # Contenedor principal horizontal
        main_container = tk.Frame(self.display_frame, bg=COLOR_WHITE)
        main_container.pack(fill="both", expand=True)
        
        # Frame para la figura (lado izquierdo)
        fig_frame = tk.Frame(main_container, bg=COLOR_WHITE, relief="solid", borderwidth=1)
        fig_frame.pack(side="left", fill="both", expand=True)
        
        # Ajustar el tamaño de la figura
        fig.set_size_inches(9, 5.5)
        fig.tight_layout()
        
        # Canvas de matplotlib
        self.current_figure = fig
        self.current_canvas = FigureCanvasTkAgg(fig, master=fig_frame)
        self.current_canvas.draw()
        
        # Toolbar de navegación
        toolbar_frame = tk.Frame(fig_frame, bg=COLOR_LIGHT_GRAY)
        toolbar_frame.pack(side="bottom", fill="x")
        toolbar = NavigationToolbar2Tk(self.current_canvas, toolbar_frame)
        toolbar.update()
        
        # Widget del canvas
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Panel de estadísticas (lado derecho)
        if stats_info:
            stats_frame = tk.Frame(main_container, bg=COLOR_LIGHT_TEAL, width=220)
            stats_frame.pack(side="right", fill="y", padx=(10, 0))
            stats_frame.pack_propagate(False)
            
            # Título del panel
            stats_title = tk.Label(
                stats_frame,
                text="📊 Estadísticas",
                font=("Segoe UI", 12, "bold"),
                bg=COLOR_LIGHT_TEAL,
                fg=COLOR_DARK_TEAL
            )
            stats_title.pack(pady=(15, 10), padx=10)
            
            # Separador
            sep = tk.Frame(stats_frame, bg=COLOR_GREEN, height=2)
            sep.pack(fill="x", padx=15, pady=(0, 10))
            
            # Contenido de estadísticas
            stats_label = tk.Label(
                stats_frame,
                text=stats_info,
                font=("Segoe UI", 9),
                bg=COLOR_LIGHT_TEAL,
                fg=COLOR_DARK_TEAL,
                justify="left",
                wraplength=190
            )
            stats_label.pack(padx=10, pady=5, anchor="w")
            
            # Tip para el usuario
            tip_frame = tk.Frame(stats_frame, bg="#d4edda", relief="solid", borderwidth=1)
            tip_frame.pack(fill="x", padx=10, pady=(15, 10), side="bottom")
            
            tip_label = tk.Label(
                tip_frame,
                text="💡 Tip: Pase el cursor sobre\nlos puntos para ver detalles",
                font=("Segoe UI", 8),
                bg="#d4edda",
                fg="#155724",
                justify="center"
            )
            tip_label.pack(pady=8, padx=5)

    def vista_dbo5_vs_pred(self):
        """Gráfica DBO5 vs Predicción con tooltips interactivos"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
            
        OD_values = self.data['OD_mg/L'].values
        DQO_values = self.data['DQO_TOT'].values
        BOD5_values = self.data['DBO5'].values
        BOD5_predichos = calcular_BOD5(self.data['OD_mg/L'], self.data['DQO_TOT'])
        
        # Calcular métricas de error
        errores = BOD5_values - BOD5_predichos
        mae = np.mean(np.abs(errores))
        rmse = np.sqrt(np.mean(errores**2))
        r2 = 1 - (np.sum(errores**2) / np.sum((BOD5_values - np.mean(BOD5_values))**2))
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Scatter con colores según el error
        scatter = ax.scatter(BOD5_values, BOD5_predichos, c=np.abs(errores), 
                            cmap='RdYlGn_r', alpha=0.7, edgecolors='white', s=60)
        
        # Barra de colores
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Error Absoluto (mg/L)', fontsize=9)
        
        # Línea de referencia
        min_val = min(BOD5_values.min(), BOD5_predichos.min())
        max_val = max(BOD5_values.max(), BOD5_predichos.max())
        ax.plot([min_val, max_val], [min_val, max_val], 'b--', linewidth=2, 
                label='Predicción perfecta', alpha=0.8)
        
        ax.set_xlabel("DBO5 Medida (mg/L)", fontsize=10)
        ax.set_ylabel("DBO5 Predicha (mg/L)", fontsize=10)
        ax.set_title("Validación del Modelo: DBO5 Medida vs Predicha", fontsize=12, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Agregar tooltips interactivos
        cursor = mplcursors.cursor(scatter, hover=True)
        
        @cursor.connect("add")
        def on_add(sel):
            idx = int(sel.index)
            medido = BOD5_values[idx]
            predicho = BOD5_predichos[idx]
            error = errores[idx]
            od = OD_values[idx]
            dqo = DQO_values[idx]
            sel.annotation.set_text(
                f"📍 Observación {idx+1}\n"
                f"─────────────\n"
                f"DBO5 Medida: {medido:.2f} mg/L\n"
                f"DBO5 Predicha: {predicho:.2f} mg/L\n"
                f"Error: {error:+.2f} mg/L\n"
                f"─────────────\n"
                f"OD: {od:.2f} mg/L\n"
                f"DQO: {dqo:.2f} mg/L"
            )
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.95)
            sel.annotation.set_fontsize(9)
        
        # Panel de estadísticas
        stats_info = (
            f"📈 Métricas del Modelo:\n\n"
            f"• R² (Coef. Determinación):\n  {r2:.4f}\n\n"
            f"• MAE (Error Absoluto Medio):\n  {mae:.2f} mg/L\n\n"
            f"• RMSE (Raíz Error Cuadrático):\n  {rmse:.2f} mg/L\n\n"
            f"• N° Observaciones:\n  {len(BOD5_values)}\n\n"
            f"─────────────────\n"
            f"🎯 Interpretación:\n"
            f"Puntos verdes = bajo error\n"
            f"Puntos rojos = alto error"
        )
        
        description = ("Esta gráfica compara los valores de DBO5 medidos en laboratorio contra los predichos por el modelo. "
                      "Los puntos cercanos a la línea diagonal indican predicciones precisas. El color representa el error: "
                      "verde significa que el modelo predijo bien, rojo indica mayor desviación.")
        
        self.embed_prediction_figure(fig, "📉 DBO5: Medida vs Predicha", stats_info, description)

    def vista_dbo5_mes_vs_pred(self):
        """Comparación DBO5 medido vs predicho con filtro por año"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        
        self.clear_display()
        
        # Frame superior para título, descripción y filtro
        header_frame = tk.Frame(self.display_frame, bg=COLOR_WHITE)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="📈 Comparación Temporal DBO5",
            font=("Segoe UI", 16, "bold"),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        title_label.pack(anchor="w")
        
        # Descripción
        desc_frame = tk.Frame(header_frame, bg="#e3f2fd", relief="flat")
        desc_frame.pack(fill="x", pady=(8, 0))
        
        desc_label = tk.Label(
            desc_frame,
            text="💡 Visualización temporal que muestra la evolución de la DBO5 medida (azul) y predicha (rojo). "
                 "El área sombreada representa la diferencia entre ambos valores. Use el filtro para ver datos por año.",
            font=("Segoe UI", 9),
            bg="#e3f2fd",
            fg="#1565c0",
            justify="left",
            wraplength=800,
            pady=8,
            padx=10
        )
        desc_label.pack(anchor="w")
        
        # Frame para el filtro
        filter_frame = tk.Frame(header_frame, bg=COLOR_WHITE)
        filter_frame.pack(fill="x", pady=(10, 0))
        
        filter_label = tk.Label(
            filter_frame,
            text="📅 Filtrar por año:",
            font=("Segoe UI", 10),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        filter_label.pack(side="left", padx=(0, 10))
        
        # Combobox para seleccionar año
        years = self.get_available_years()
        year_options = ["Todos los años"] + [str(y) for y in years]
        
        self.comp_year_var = tk.StringVar(value="Todos los años")
        year_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.comp_year_var,
            values=year_options,
            state="readonly",
            width=15,
            font=("Segoe UI", 10)
        )
        year_combo.pack(side="left")
        
        # Contenedor principal horizontal
        main_container = tk.Frame(self.display_frame, bg=COLOR_WHITE)
        main_container.pack(fill="both", expand=True)
        
        # Frame para la figura
        self.comp_fig_container = tk.Frame(main_container, bg=COLOR_WHITE, relief="solid", borderwidth=1)
        self.comp_fig_container.pack(side="left", fill="both", expand=True)
        
        # Frame para estadísticas
        self.comp_stats_frame = tk.Frame(main_container, bg=COLOR_LIGHT_TEAL, width=220)
        self.comp_stats_frame.pack(side="right", fill="y", padx=(10, 0))
        self.comp_stats_frame.pack_propagate(False)
        
        # Bindear el combobox
        year_combo.bind("<<ComboboxSelected>>", lambda e: self.update_comp_plot())
        
        # Dibujar gráfica inicial
        self.update_comp_plot()
    
    def update_comp_plot(self):
        """Actualiza la gráfica de comparación temporal según el filtro"""
        # Limpiar contenedores
        for widget in self.comp_fig_container.winfo_children():
            widget.destroy()
        for widget in self.comp_stats_frame.winfo_children():
            widget.destroy()
        
        if self.current_figure:
            plt.close(self.current_figure)
        
        # Obtener datos filtrados
        selected_year = self.comp_year_var.get()
        if selected_year == "Todos los años":
            filtered_data = self.data.copy()
        else:
            filtered_data = self.data[self.data['AÑO'] == int(selected_year)].copy()
        
        if len(filtered_data) == 0:
            # Mostrar mensaje si no hay datos
            no_data_label = tk.Label(
                self.comp_fig_container,
                text="No hay datos para el año seleccionado",
                font=("Segoe UI", 12),
                bg=COLOR_WHITE,
                fg=COLOR_TEAL
            )
            no_data_label.pack(expand=True)
            return
        
        # Ordenar por fecha si existe
        if 'FECHA_DT' in filtered_data.columns:
            filtered_data = filtered_data.sort_values('FECHA_DT')
        
        # Obtener valores
        OD_values = filtered_data['OD_mg/L'].values
        DQO_values = filtered_data['DQO_TOT'].values
        BOD5_values = filtered_data['DBO5'].values
        BOD5_predichos = calcular_BOD5(filtered_data['OD_mg/L'], filtered_data['DQO_TOT'])
        
        # Calcular métricas
        errores = BOD5_values - BOD5_predichos
        correlacion = np.corrcoef(BOD5_values, BOD5_predichos)[0, 1]
        
        fig, ax = plt.subplots(figsize=(9, 5.5))
        
        x_pos = np.arange(len(filtered_data))
        
        # Área sombreada entre las dos líneas
        ax.fill_between(x_pos, BOD5_values, BOD5_predichos, 
                       alpha=0.2, color='gray', label='Diferencia')
        
        # Líneas con marcadores
        line1, = ax.plot(x_pos, BOD5_values, 'o-', label="DBO5 Medido", 
                        color="#3498db", markersize=5, linewidth=1.5)
        line2, = ax.plot(x_pos, BOD5_predichos, 's-', label="DBO5 Predicho", 
                        color="#e74c3c", markersize=5, linewidth=1.5)
        
        # Configurar eje X según el filtro
        if selected_year == "Todos los años":
            ax.set_xlabel("Observaciones", fontsize=10)
        elif 'MES' in filtered_data.columns:
            meses = filtered_data['MES'].values
            x_labels = [f"{MESES_ESP.get(int(m), m)}" for m in meses]
            
            n_labels = len(x_labels)
            if n_labels > 15:
                step = n_labels // 12
            else:
                step = 1
            
            ax.set_xticks(range(0, n_labels, step))
            ax.set_xticklabels([x_labels[i] for i in range(0, n_labels, step)], rotation=45, ha='right')
            ax.set_xlabel("Mes", fontsize=10)
        else:
            ax.set_xlabel("Observaciones", fontsize=10)
        
        ax.set_ylabel("Demanda Bioquímica de Oxígeno (mg/L)", fontsize=10)
        
        # Título con año si está filtrado
        if selected_year != "Todos los años":
            ax.set_title(f"Serie Temporal: DBO5 Medida vs Predicha - {selected_year}", fontsize=12, fontweight='bold')
        else:
            ax.set_title("Serie Temporal: DBO5 Medida vs Predicha", fontsize=12, fontweight='bold')
        
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Tooltips para ambas líneas
        cursor1 = mplcursors.cursor(line1, hover=True)
        cursor2 = mplcursors.cursor(line2, hover=True)
        
        # Guardar datos para tooltips
        self._comp_data = {
            'BOD5_values': BOD5_values,
            'BOD5_predichos': BOD5_predichos,
            'errores': errores,
            'OD_values': OD_values,
            'DQO_values': DQO_values,
            'meses': filtered_data['MES'].values if 'MES' in filtered_data.columns else None,
            'años': filtered_data['AÑO'].values if 'AÑO' in filtered_data.columns else None
        }
        
        @cursor1.connect("add")
        def on_add1(sel):
            idx = int(sel.index)
            texto = f"📊 DBO5 Medida: {self._comp_data['BOD5_values'][idx]:.2f} mg/L\n"
            texto += f"Error: {self._comp_data['errores'][idx]:+.2f} mg/L"
            if self._comp_data['meses'] is not None:
                mes = MESES_ESP.get(int(self._comp_data['meses'][idx]), self._comp_data['meses'][idx])
                año = int(self._comp_data['años'][idx])
                texto = f"📅 {mes} {año}\n" + texto
            sel.annotation.set_text(texto)
            sel.annotation.get_bbox_patch().set(fc="#e3f2fd", alpha=0.95)
        
        @cursor2.connect("add")
        def on_add2(sel):
            idx = int(sel.index)
            texto = f"🎯 DBO5 Predicha: {self._comp_data['BOD5_predichos'][idx]:.2f} mg/L\n"
            texto += f"OD: {self._comp_data['OD_values'][idx]:.2f} | DQO: {self._comp_data['DQO_values'][idx]:.2f}"
            if self._comp_data['meses'] is not None:
                mes = MESES_ESP.get(int(self._comp_data['meses'][idx]), self._comp_data['meses'][idx])
                año = int(self._comp_data['años'][idx])
                texto = f"📅 {mes} {año}\n" + texto
            sel.annotation.set_text(texto)
            sel.annotation.get_bbox_patch().set(fc="#ffebee", alpha=0.95)
        
        fig.tight_layout()
        
        # Canvas de matplotlib
        self.current_figure = fig
        self.current_canvas = FigureCanvasTkAgg(fig, master=self.comp_fig_container)
        self.current_canvas.draw()
        
        # Toolbar
        toolbar_frame = tk.Frame(self.comp_fig_container, bg=COLOR_LIGHT_GRAY)
        toolbar_frame.pack(side="bottom", fill="x")
        toolbar = NavigationToolbar2Tk(self.current_canvas, toolbar_frame)
        toolbar.update()
        
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Panel de estadísticas
        stats_title = tk.Label(
            self.comp_stats_frame,
            text="📊 Estadísticas",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_LIGHT_TEAL,
            fg=COLOR_DARK_TEAL
        )
        stats_title.pack(pady=(15, 10), padx=10)
        
        sep = tk.Frame(self.comp_stats_frame, bg=COLOR_GREEN, height=2)
        sep.pack(fill="x", padx=15, pady=(0, 10))
        
        # Estadísticas
        stats_info = (
            f"📊 Resumen Comparativo:\n\n"
            f"• Correlación:\n  {correlacion:.4f}\n\n"
            f"• DBO5 Medida:\n"
            f"  Promedio: {np.mean(BOD5_values):.2f} mg/L\n"
            f"  Máx: {np.max(BOD5_values):.2f} mg/L\n"
            f"  Mín: {np.min(BOD5_values):.2f} mg/L\n\n"
            f"• DBO5 Predicha:\n"
            f"  Promedio: {np.mean(BOD5_predichos):.2f} mg/L\n"
            f"  Máx: {np.max(BOD5_predichos):.2f} mg/L\n"
            f"  Mín: {np.min(BOD5_predichos):.2f} mg/L\n\n"
            f"• N° Observaciones:\n  {len(BOD5_values)}\n\n"
            f"─────────────────\n"
            f"🔵 Azul = Medido\n"
            f"🔴 Rojo = Predicho"
        )
        
        stats_label = tk.Label(
            self.comp_stats_frame,
            text=stats_info,
            font=("Segoe UI", 9),
            bg=COLOR_LIGHT_TEAL,
            fg=COLOR_DARK_TEAL,
            justify="left",
            wraplength=190
        )
        stats_label.pack(padx=10, pady=5, anchor="w")
        
        # Tip
        tip_frame = tk.Frame(self.comp_stats_frame, bg="#d4edda", relief="solid", borderwidth=1)
        tip_frame.pack(fill="x", padx=10, pady=(15, 10), side="bottom")
        
        tip_label = tk.Label(
            tip_frame,
            text="💡 Tip: Pase el cursor sobre\nlos puntos para ver detalles",
            font=("Segoe UI", 8),
            bg="#d4edda",
            fg="#155724",
            justify="center"
        )
        tip_label.pack(pady=8, padx=5)

    def vista_residuals(self):
        """Gráfica de residuales (errores) con tooltips"""
        if not hasattr(self, 'model'):
            messagebox.showerror("Error", "Por favor, ejecute primero la 'Regresión Paso a Paso'\nen la sección de Análisis Estadístico.")
            return
            
        y_pred = self.model.predict()
        y_real = self.data['DBO5'].values
        residuos = y_real - y_pred
        
        # Calcular estadísticas de residuos
        media_res = np.mean(residuos)
        std_res = np.std(residuos)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico de residuos vs. valores observados
        scatter1 = ax1.scatter(y_real, residuos, c=residuos, cmap='coolwarm', 
                              alpha=0.7, edgecolors='white', s=50)
        ax1.axhline(0, color='black', linestyle='--', linewidth=1.5)
        ax1.axhline(2*std_res, color='red', linestyle=':', alpha=0.5, label=f'±2σ ({2*std_res:.2f})')
        ax1.axhline(-2*std_res, color='red', linestyle=':', alpha=0.5)
        ax1.set_xlabel("DBO5 Observada (mg/L)", fontsize=10)
        ax1.set_ylabel("Residuos (mg/L)", fontsize=10)
        ax1.set_title("Residuos vs DBO5 Observada", fontsize=11, fontweight='bold')
        ax1.legend(loc='upper right', fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # Gráfico de residuos vs. valores predichos
        scatter2 = ax2.scatter(y_pred, residuos, c=residuos, cmap='coolwarm', 
                              alpha=0.7, edgecolors='white', s=50)
        ax2.axhline(0, color='black', linestyle='--', linewidth=1.5)
        ax2.axhline(2*std_res, color='red', linestyle=':', alpha=0.5, label=f'±2σ ({2*std_res:.2f})')
        ax2.axhline(-2*std_res, color='red', linestyle=':', alpha=0.5)
        ax2.set_xlabel("DBO5 Predicha (mg/L)", fontsize=10)
        ax2.set_ylabel("Residuos (mg/L)", fontsize=10)
        ax2.set_title("Residuos vs DBO5 Predicha", fontsize=11, fontweight='bold')
        ax2.legend(loc='upper right', fontsize=8)
        ax2.grid(True, alpha=0.3)
        
        # Tooltips
        cursor1 = mplcursors.cursor(scatter1, hover=True)
        cursor2 = mplcursors.cursor(scatter2, hover=True)
        
        @cursor1.connect("add")
        def on_add1(sel):
            idx = int(sel.index)
            sel.annotation.set_text(
                f"Obs {idx+1}\n"
                f"DBO5 Real: {y_real[idx]:.2f}\n"
                f"Residuo: {residuos[idx]:+.2f}"
            )
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.9)
        
        @cursor2.connect("add")
        def on_add2(sel):
            idx = int(sel.index)
            sel.annotation.set_text(
                f"Obs {idx+1}\n"
                f"DBO5 Pred: {y_pred[idx]:.2f}\n"
                f"Residuo: {residuos[idx]:+.2f}"
            )
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.9)
        
        plt.tight_layout()
        
        # Contar outliers
        outliers = np.sum(np.abs(residuos) > 2*std_res)
        
        stats_info = (
            f"📉 Análisis de Residuos:\n\n"
            f"• Media de Residuos:\n  {media_res:.4f} mg/L\n\n"
            f"• Desv. Estándar (σ):\n  {std_res:.2f} mg/L\n\n"
            f"• Outliers (>2σ):\n  {outliers} de {len(residuos)}\n\n"
            f"─────────────────\n"
            f"🎯 Interpretación:\n\n"
            f"• Residuos cercanos a 0\n  indican buen ajuste\n\n"
            f"• Patrón aleatorio =\n  modelo adecuado\n\n"
            f"• Azul = sobreestima\n"
            f"• Rojo = subestima"
        )
        
        description = ("Los residuos son las diferencias entre valores reales y predichos. Un buen modelo muestra residuos "
                      "distribuidos aleatoriamente alrededor de cero. Las líneas punteadas rojas (±2σ) marcan los límites "
                      "para detectar valores atípicos. Patrones sistemáticos sugieren que el modelo podría mejorarse.")
        
        self.embed_prediction_figure(fig, "⚠️ Análisis de Errores (Residuales)", stats_info, description)
    
    def vista_tss_bod5(self):
        """Relación DQO-DBO5 con tooltips"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
            
        sorted_data = self.data.sort_values(by='DQO_TOT', ascending=True)
        cod_sorted = sorted_data['DQO_TOT'].values
        dbo5_sorted = sorted_data['DBO5'].values
        
        # Calcular correlación y regresión
        correlacion = np.corrcoef(cod_sorted, dbo5_sorted)[0, 1]
        z = np.polyfit(cod_sorted, dbo5_sorted, 1)
        p = np.poly1d(z)
        
        # Ratio DQO/DBO5
        ratio = cod_sorted / np.where(dbo5_sorted > 0, dbo5_sorted, 0.1)
        ratio_medio = np.mean(ratio)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Scatter con colores según el ratio
        scatter = ax.scatter(cod_sorted, dbo5_sorted, c=ratio, cmap='viridis', 
                            alpha=0.7, edgecolors='white', s=60)
        
        # Barra de colores
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Ratio DQO/DBO5', fontsize=9)
        
        # Línea de tendencia
        x_line = np.linspace(cod_sorted.min(), cod_sorted.max(), 100)
        ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, 
                label=f'Tendencia: y = {z[0]:.4f}x + {z[1]:.2f}')
        
        ax.set_xlabel("Demanda Química de Oxígeno (mg/L)", fontsize=10)
        ax.set_ylabel("Demanda Bioquímica de Oxígeno (mg/L)", fontsize=10)
        ax.set_title("Relación: DQO vs DBO5", fontsize=12, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Tooltips
        cursor = mplcursors.cursor(scatter, hover=True)
        
        @cursor.connect("add")
        def on_add(sel):
            idx = int(sel.index)
            sel.annotation.set_text(
                f"📍 Punto de Medición\n"
                f"─────────────\n"
                f"DQO: {cod_sorted[idx]:.2f} mg/L\n"
                f"DBO5: {dbo5_sorted[idx]:.2f} mg/L\n"
                f"Ratio: {ratio[idx]:.2f}\n"
                f"─────────────\n"
                f"{'🟢 Biodegradable' if ratio[idx] < 2.5 else '🟡 Moderado' if ratio[idx] < 4 else '🔴 Poco biodegradable'}"
            )
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.95)
        
        # Panel de estadísticas
        stats_info = (
            f"🔬 Análisis DQO/DBO5:\n\n"
            f"• Correlación:\n  {correlacion:.4f}\n\n"
            f"• Pendiente:\n  {z[0]:.4f}\n\n"
            f"• Ratio medio DQO/DBO5:\n  {ratio_medio:.2f}\n\n"
            f"─────────────────\n"
            f"📖 Interpretación Ratio:\n\n"
            f"• < 2.5: Muy biodegradable\n"
            f"  (tratamiento biológico)\n\n"
            f"• 2.5-4: Moderadamente\n"
            f"  biodegradable\n\n"
            f"• > 4: Poco biodegradable\n"
            f"  (tratamiento químico)"
        )
        
        description = ("Muestra la relación entre la Demanda Química (DQO) y Bioquímica (DBO5) de Oxígeno. El ratio DQO/DBO5 "
                      "indica la biodegradabilidad del agua: valores bajos significan contaminación orgánica tratable biológicamente, "
                      "mientras que valores altos indican contaminantes que requieren tratamiento químico.")
        
        self.embed_prediction_figure(fig, "🎯 Relación DQO vs DBO5", stats_info, description)
    
    def run_regression_dqo(self):
        """Regresión DQO con tooltips y estadísticas"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
            
        X = self.data['DQO_TOT'].values
        y = self.data['DBO5'].values
        
        # Calcular regresión
        z = np.polyfit(X, y, 1)
        p = np.poly1d(z)
        y_pred = p(X)
        
        # Métricas
        r2 = 1 - (np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2))
        correlacion = np.corrcoef(X, y)[0, 1]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Scatter con gradiente de color
        scatter = ax.scatter(X, y, c=y, cmap='plasma', alpha=0.7, 
                            edgecolors='white', s=60, label='Datos observados')
        
        # Línea de regresión
        x_line = np.linspace(X.min(), X.max(), 100)
        ax.plot(x_line, p(x_line), "r-", alpha=0.9, linewidth=2.5, 
                label=f'Regresión: DBO5 = {z[0]:.4f}×DQO + {z[1]:.2f}')
        
        # Intervalo de confianza aproximado
        se = np.sqrt(np.sum((y - y_pred)**2) / (len(y) - 2))
        ax.fill_between(x_line, p(x_line) - 2*se, p(x_line) + 2*se, 
                       alpha=0.15, color='red', label='Intervalo ±2σ')
        
        ax.set_xlabel("Demanda Química de Oxígeno (mg/L)", fontsize=10)
        ax.set_ylabel("Demanda Bioquímica de Oxígeno (mg/L)", fontsize=10)
        ax.set_title("Regresión Lineal: DQO → DBO5", fontsize=12, fontweight='bold')
        ax.legend(loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('DBO5 (mg/L)', fontsize=9)
        
        # Tooltips
        cursor = mplcursors.cursor(scatter, hover=True)
        
        @cursor.connect("add")
        def on_add(sel):
            idx = int(sel.index)
            dqo_val = X[idx]
            dbo5_real = y[idx]
            dbo5_pred = p(dqo_val)
            error = dbo5_real - dbo5_pred
            sel.annotation.set_text(
                f"📊 Observación {idx+1}\n"
                f"─────────────\n"
                f"DQO: {dqo_val:.2f} mg/L\n"
                f"DBO5 Real: {dbo5_real:.2f} mg/L\n"
                f"DBO5 Estimado: {dbo5_pred:.2f} mg/L\n"
                f"Error: {error:+.2f} mg/L"
            )
            sel.annotation.get_bbox_patch().set(fc="white", alpha=0.95)
        
        # Panel de estadísticas
        stats_info = (
            f"📈 Modelo de Regresión:\n\n"
            f"• Ecuación:\n  DBO5 = {z[0]:.4f}×DQO\n  + {z[1]:.2f}\n\n"
            f"• R² (Determinación):\n  {r2:.4f}\n\n"
            f"• Correlación:\n  {correlacion:.4f}\n\n"
            f"• Error Estándar:\n  {se:.2f} mg/L\n\n"
            f"─────────────────\n"
            f"🎯 Uso del Modelo:\n\n"
            f"Para estimar DBO5,\n"
            f"multiplique DQO por\n"
            f"{z[0]:.4f} y sume {z[1]:.2f}"
        )
        
        description = ("Modelo de regresión lineal que permite estimar la DBO5 a partir de la DQO. La línea roja representa "
                      "la ecuación del modelo, y el área sombreada indica el intervalo de confianza (±2σ). Este modelo es útil "
                      "cuando solo se dispone de mediciones de DQO y se necesita estimar rápidamente la DBO5.")
        
        self.embed_prediction_figure(fig, "🎯 Regresión DQO → DBO5", stats_info, description)
    
    def vista_tendencia_temporal(self):
        """Análisis de tendencia temporal con proyecciones - ComboBox selector"""
        if self.data is None:
            messagebox.showerror("Error", "Por favor, cargue un archivo primero.")
            return
        
        self.clear_display()
        
        # Frame superior para título, descripción y selector
        header_frame = tk.Frame(self.display_frame, bg=COLOR_WHITE)
        header_frame.pack(fill="x", pady=(0, 5))
        
        # Título
        title_label = tk.Label(
            header_frame,
            text="📅 Análisis de Tendencia Temporal con Proyecciones",
            font=("Segoe UI", 16, "bold"),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        title_label.pack(anchor="w")
        
        # Frame para los selectores (parámetro y años de proyección)
        selector_frame = tk.Frame(header_frame, bg=COLOR_WHITE)
        selector_frame.pack(fill="x", pady=(10, 0))
        
        # Selector de parámetro
        selector_label = tk.Label(
            selector_frame,
            text="📊 Parámetro:",
            font=("Segoe UI", 10),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        selector_label.pack(side="left", padx=(0, 5))
        
        # Opciones del ComboBox de parámetros
        param_options = [
            "💧 Oxígeno Disuelto (OD)",
            "🔬 Demanda Química de Oxígeno (DQO)",
            "🧪 Demanda Bioquímica de Oxígeno (DBO5)"
        ]
        
        self.tendencia_param_var = tk.StringVar(value=param_options[0])
        param_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.tendencia_param_var,
            values=param_options,
            state="readonly",
            width=35,
            font=("Segoe UI", 10)
        )
        param_combo.pack(side="left", padx=(0, 20))
        
        # Selector de años de proyección (máximo 4 años)
        proyeccion_label = tk.Label(
            selector_frame,
            text="🔮 Años a proyectar:",
            font=("Segoe UI", 10),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        proyeccion_label.pack(side="left", padx=(0, 5))
        
        # Opciones de años de proyección (máximo 4)
        proyeccion_options = ["1 año", "2 años", "3 años", "4 años"]
        
        self.tendencia_proyeccion_var = tk.StringVar(value="2 años")
        proyeccion_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.tendencia_proyeccion_var,
            values=proyeccion_options,
            state="readonly",
            width=10,
            font=("Segoe UI", 10)
        )
        proyeccion_combo.pack(side="left")
        
        # Frame para la descripción (cambiará según el parámetro)
        self.tendencia_desc_frame = tk.Frame(header_frame, bg="#e3f2fd", relief="flat")
        self.tendencia_desc_frame.pack(fill="x", pady=(10, 0))
        
        self.tendencia_desc_label = tk.Label(
            self.tendencia_desc_frame,
            text="",
            font=("Segoe UI", 9),
            bg="#e3f2fd",
            fg="#1565c0",
            justify="left",
            wraplength=900,
            pady=8,
            padx=10
        )
        self.tendencia_desc_label.pack(anchor="w")
        
        # Contenedor principal con scroll para las gráficas y panel de estadísticas
        main_container = tk.Frame(self.display_frame, bg=COLOR_WHITE)
        main_container.pack(fill="both", expand=True)
        
        # Frame izquierdo para las gráficas
        graph_container = tk.Frame(main_container, bg=COLOR_WHITE)
        graph_container.pack(side="left", fill="both", expand=True)
        
        # Canvas con scroll para las gráficas
        self.tendencia_canvas = tk.Canvas(graph_container, bg=COLOR_WHITE, highlightthickness=0)
        scrollbar_v = tk.Scrollbar(graph_container, orient="vertical", command=self.tendencia_canvas.yview)
        
        self.tendencia_scrollable_frame = tk.Frame(self.tendencia_canvas, bg=COLOR_WHITE)
        
        self.tendencia_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.tendencia_canvas.configure(scrollregion=self.tendencia_canvas.bbox("all"))
        )
        
        self.tendencia_canvas.create_window((0, 0), window=self.tendencia_scrollable_frame, anchor="nw")
        self.tendencia_canvas.configure(yscrollcommand=scrollbar_v.set)
        
        scrollbar_v.pack(side="right", fill="y")
        self.tendencia_canvas.pack(side="left", fill="both", expand=True)
        
        # ===== PANEL DE ESTADÍSTICAS (derecha) =====
        self.tendencia_stats_frame = tk.Frame(main_container, bg="#f8f9fa", width=280, relief="flat")
        self.tendencia_stats_frame.pack(side="right", fill="y", padx=(5, 0))
        self.tendencia_stats_frame.pack_propagate(False)
        
        # Título del panel
        stats_title = tk.Label(
            self.tendencia_stats_frame,
            text="📊 Panel de Estadísticas",
            font=("Segoe UI", 11, "bold"),
            bg="#f8f9fa",
            fg=COLOR_DARK_TEAL
        )
        stats_title.pack(pady=(10, 5), padx=10, anchor="w")
        
        # Separador
        sep = tk.Frame(self.tendencia_stats_frame, height=2, bg=COLOR_DARK_TEAL)
        sep.pack(fill="x", padx=10, pady=(0, 10))
        
        # Canvas con scroll para las estadísticas
        stats_canvas = tk.Canvas(self.tendencia_stats_frame, bg="#f8f9fa", highlightthickness=0)
        stats_scrollbar = tk.Scrollbar(self.tendencia_stats_frame, orient="vertical", command=stats_canvas.yview)
        
        self.tendencia_stats_content = tk.Frame(stats_canvas, bg="#f8f9fa")
        
        self.tendencia_stats_content.bind(
            "<Configure>",
            lambda e: stats_canvas.configure(scrollregion=stats_canvas.bbox("all"))
        )
        
        stats_canvas.create_window((0, 0), window=self.tendencia_stats_content, anchor="nw", width=260)
        stats_canvas.configure(yscrollcommand=stats_scrollbar.set)
        
        stats_scrollbar.pack(side="right", fill="y")
        stats_canvas.pack(side="left", fill="both", expand=True)
        
        # Bind mousewheel para scroll
        def on_mousewheel(event):
            self.tendencia_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.tendencia_canvas.bind_all("<MouseWheel>", on_mousewheel)
        
        # Bindear los combobox
        param_combo.bind("<<ComboboxSelected>>", lambda e: self.update_tendencia_plot())
        proyeccion_combo.bind("<<ComboboxSelected>>", lambda e: self.update_tendencia_plot())
        
        # Dibujar gráficas iniciales
        self.update_tendencia_plot()
    
    def update_tendencia_plot(self):
        """Actualiza las gráficas de tendencia temporal - una por cada año proyectado"""
        # Limpiar contenedor scrollable
        for widget in self.tendencia_scrollable_frame.winfo_children():
            widget.destroy()
        
        if self.current_figure:
            plt.close(self.current_figure)
        
        # Obtener años de proyección seleccionados (máximo 4)
        proyeccion_str = self.tendencia_proyeccion_var.get()
        años_proyeccion = min(int(proyeccion_str.split()[0]), 4)  # Máximo 4 años
        
        # Obtener datos
        n_puntos = len(self.data)
        tiempo = np.arange(n_puntos)
        
        # Determinar qué parámetro graficar
        selected = self.tendencia_param_var.get()
        
        # Obtener último año de los datos
        ultimo_año = int(self.data['AÑO'].max()) if 'AÑO' in self.data.columns else 2024
        
        # Configuración según parámetro
        if "OD" in selected:
            valores = self.data['OD_mg/L'].values
            color_datos = "#3d8b6e"
            color_linea = "#2980b9"
            y_label = "Oxígeno Disuelto (mg/L)"
            titulo_base = "Oxígeno Disuelto (OD)"
            emoji = "💧"
            unidad = "mg/L"
            descripcion = (f"💡 Proyección del Oxígeno Disuelto para los próximos {años_proyeccion} año(s). "
                          f"Cada gráfica muestra los valores mensuales predichos. Valores >6 mg/L indican buena calidad del agua.")
        elif "DQO" in selected:
            valores = self.data['DQO_TOT'].values
            color_datos = "#e67e22"
            color_linea = "#d35400"
            y_label = "Demanda Química de Oxígeno (mg/L)"
            titulo_base = "Demanda Química de Oxígeno (DQO)"
            emoji = "🔬"
            unidad = "mg/L"
            descripcion = (f"💡 Proyección de la DQO para los próximos {años_proyeccion} año(s). "
                          f"Valores altos indican mayor contaminación. La tendencia ayuda a planificar acciones de control.")
        else:  # DBO5
            valores = self.data['DBO5'].values
            color_datos = "#9b59b6"
            color_linea = "#8e44ad"
            y_label = "Demanda Bioquímica de Oxígeno (mg/L)"
            titulo_base = "Demanda Bioquímica de Oxígeno (DBO5)"
            emoji = "🧪"
            unidad = "mg/L"
            descripcion = (f"💡 Proyección de la DBO5 para los próximos {años_proyeccion} año(s). "
                          f"Valores <3 mg/L = agua limpia, 3-6 = aceptable, >30 = contaminación significativa.")
        
        # Actualizar descripción
        self.tendencia_desc_label.config(text=descripcion)
        
        # Calcular tendencia lineal
        z = np.polyfit(tiempo, valores, 1)
        p = np.poly1d(z)
        tendencia = z[0]  # Pendiente por período
        
        # Calcular R² de la tendencia
        y_pred_tendencia = p(tiempo)
        ss_res = np.sum((valores - y_pred_tendencia)**2)
        ss_tot = np.sum((valores - np.mean(valores))**2)
        r2_tendencia = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        # Determinar si la tendencia es buena o mala
        if "OD" in selected:
            tendencia_buena = tendencia > 0
        else:
            tendencia_buena = tendencia < 0
        
        # Colores para cada año
        colores_años = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6']
        
        # Crear figura con subplots (1 fila por año + 1 para resumen)
        n_graficas = años_proyeccion + 1  # +1 para gráfica de resumen/histórico
        fig, axes = plt.subplots(n_graficas, 1, figsize=(12, 3.5 * n_graficas))
        
        if n_graficas == 1:
            axes = [axes]
        
        # --- Primera gráfica: Datos históricos y tendencia general ---
        ax0 = axes[0]
        
        # Datos históricos
        scatter = ax0.scatter(tiempo, valores, alpha=0.6, color=color_datos, s=40, 
                             edgecolors='white', linewidth=0.5, label='Datos históricos', zorder=3)
        
        # Línea de tendencia
        ax0.plot(tiempo, p(tiempo), color=color_linea, linewidth=2.5, label='Tendencia lineal', zorder=2)
        
        # Proyección completa
        tiempo_futuro_total = np.arange(n_puntos, n_puntos + años_proyeccion * 12)
        ax0.plot(tiempo_futuro_total, p(tiempo_futuro_total), color=color_linea, linestyle='--', 
                linewidth=2, alpha=0.7, label=f'Proyección ({años_proyeccion} años)', zorder=2)
        
        # Línea del presente
        ax0.axvline(x=n_puntos-1, color='#e74c3c', linestyle=':', linewidth=2, alpha=0.8, label='Presente')
        
        # Intervalo de incertidumbre
        incertidumbre = np.linspace(0.1, 0.2, len(tiempo_futuro_total))
        valores_proy = p(tiempo_futuro_total)
        ax0.fill_between(tiempo_futuro_total, valores_proy * (1-incertidumbre), valores_proy * (1+incertidumbre),
                        alpha=0.15, color=color_linea)
        
        ax0.set_xlabel('Período de muestreo', fontsize=10)
        ax0.set_ylabel(y_label, fontsize=10)
        ax0.set_title(f'{emoji} {titulo_base} - Visión General y Tendencia', fontsize=12, fontweight='bold')
        ax0.legend(loc='upper right', fontsize=8)
        ax0.grid(True, alpha=0.3)
        
        # Anotación de tendencia
        tendencia_texto = "📈 Ascendente" if tendencia > 0 else "📉 Descendente"
        tendencia_color_txt = "#e74c3c" if not tendencia_buena else "#27ae60"
        ax0.annotate(f'{tendencia_texto} ({tendencia:+.4f}/mes)\nR² = {r2_tendencia:.4f}', 
                    xy=(0.02, 0.95), xycoords='axes fraction',
                    fontsize=9, fontweight='bold', color=tendencia_color_txt,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=tendencia_color_txt, alpha=0.9))
        
        # --- Gráficas por año proyectado (valores mensuales) ---
        meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        for año_idx in range(años_proyeccion):
            ax = axes[año_idx + 1]
            año_futuro = ultimo_año + año_idx + 1
            color_año = colores_años[año_idx % len(colores_años)]
            
            # Calcular valores mensuales para este año
            inicio_mes = n_puntos + (año_idx * 12)
            valores_mensuales = []
            
            for mes in range(12):
                pos = inicio_mes + mes
                valor_pred = p(pos)
                valores_mensuales.append(valor_pred)
            
            valores_mensuales = np.array(valores_mensuales)
            
            # Gráfica de barras para los valores mensuales
            x_meses = np.arange(12)
            bars = ax.bar(x_meses, valores_mensuales, color=color_año, alpha=0.7, edgecolor='white', linewidth=1.5)
            
            # Línea conectando los valores
            ax.plot(x_meses, valores_mensuales, 'o-', color=color_año, linewidth=2, markersize=8, 
                   markerfacecolor='white', markeredgecolor=color_año, markeredgewidth=2, zorder=5)
            
            # Añadir valores encima de las barras
            for i, (bar, valor) in enumerate(zip(bars, valores_mensuales)):
                ax.annotate(f'{valor:.1f}', 
                           xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                           xytext=(0, 5), textcoords='offset points',
                           ha='center', va='bottom', fontsize=8, fontweight='bold', color=color_año)
            
            # Línea de referencia del valor promedio histórico
            promedio_hist = np.mean(valores)
            ax.axhline(y=promedio_hist, color='gray', linestyle='--', linewidth=1.5, alpha=0.7,
                      label=f'Promedio histórico: {promedio_hist:.2f}')
            
            # Configurar eje X con nombres de meses
            ax.set_xticks(x_meses)
            ax.set_xticklabels(meses_nombres, fontsize=9)
            ax.set_xlabel('Mes', fontsize=10)
            ax.set_ylabel(unidad, fontsize=10)
            ax.set_title(f'📅 Proyección Año {año_futuro} (+{año_idx + 1} año{"s" if año_idx > 0 else ""})', 
                        fontsize=11, fontweight='bold', color=color_año)
            ax.legend(loc='upper right', fontsize=8)
            ax.grid(True, alpha=0.3, axis='y')
            
            # Estadísticas del año
            stats_text = (f'Promedio: {np.mean(valores_mensuales):.2f} | '
                         f'Máx: {np.max(valores_mensuales):.2f} | '
                         f'Mín: {np.min(valores_mensuales):.2f}')
            ax.annotate(stats_text, xy=(0.5, 0.02), xycoords='axes fraction',
                       fontsize=9, ha='center', va='bottom',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='#f0f0f0', edgecolor='gray', alpha=0.9))
            
            # Indicador de calidad según el parámetro
            valor_medio_año = np.mean(valores_mensuales)
            if "OD" in selected:
                if valor_medio_año > 6:
                    calidad = "🟢 Buena"
                elif valor_medio_año > 4:
                    calidad = "🟡 Aceptable"
                else:
                    calidad = "🔴 Deficiente"
            elif "DQO" in selected:
                if valor_medio_año < 40:
                    calidad = "🟢 Buena"
                elif valor_medio_año < 100:
                    calidad = "🟡 Moderada"
                else:
                    calidad = "🔴 Alta"
            else:  # DBO5
                if valor_medio_año < 3:
                    calidad = "🟢 Excelente"
                elif valor_medio_año < 6:
                    calidad = "🟡 Buena"
                elif valor_medio_año < 30:
                    calidad = "🟠 Aceptable"
                else:
                    calidad = "🔴 Contaminada"
            
            ax.annotate(f'Calidad esperada: {calidad}', xy=(0.98, 0.95), xycoords='axes fraction',
                       fontsize=9, ha='right', va='top', fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color_año, alpha=0.9))
        
        plt.tight_layout()
        
        # Embeber la figura en el frame scrollable
        self.current_figure = fig
        canvas = FigureCanvasTkAgg(fig, master=self.tendencia_scrollable_frame)
        canvas.draw()
        
        # Toolbar
        toolbar_frame = tk.Frame(self.tendencia_scrollable_frame, bg=COLOR_LIGHT_GRAY)
        toolbar_frame.pack(fill="x", pady=(5, 0))
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        toolbar.update()
        
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Actualizar el scroll region
        self.tendencia_scrollable_frame.update_idletasks()
        self.tendencia_canvas.configure(scrollregion=self.tendencia_canvas.bbox("all"))
        
        # ===== ACTUALIZAR PANEL DE ESTADÍSTICAS =====
        self._update_tendencia_stats(selected, valores, tiempo, años_proyeccion, ultimo_año, unidad)
    
    def _update_tendencia_stats(self, selected, valores, tiempo, años_proyeccion, ultimo_año, unidad):
        """Actualiza el panel de estadísticas de tendencia temporal"""
        # Limpiar contenido anterior
        for widget in self.tendencia_stats_content.winfo_children():
            widget.destroy()
        
        # Realizar regresión polinomial para las estadísticas
        z = np.polyfit(tiempo, valores, 2)
        p = np.poly1d(z)
        
        # Calcular R²
        valores_predichos = p(tiempo)
        ss_res = np.sum((valores - valores_predichos) ** 2)
        ss_tot = np.sum((valores - np.mean(valores)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        # ===== SECCIÓN: Datos Históricos =====
        self._create_stats_section("📈 Datos Históricos", self.tendencia_stats_content, "#2196F3")
        
        historico_frame = tk.Frame(self.tendencia_stats_content, bg="#f8f9fa")
        historico_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        stats_historicos = [
            ("N° Observaciones", f"{len(valores)}"),
            ("Promedio", f"{np.mean(valores):.2f} {unidad}"),
            ("Desv. Estándar", f"{np.std(valores):.2f} {unidad}"),
            ("Valor Máximo", f"{np.max(valores):.2f} {unidad}"),
            ("Valor Mínimo", f"{np.min(valores):.2f} {unidad}"),
            ("Mediana", f"{np.median(valores):.2f} {unidad}"),
            ("Rango", f"{np.max(valores) - np.min(valores):.2f} {unidad}")
        ]
        
        for label, value in stats_historicos:
            row = tk.Frame(historico_frame, bg="#f8f9fa")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label + ":", font=("Segoe UI", 9), bg="#f8f9fa", fg="#555", anchor="w").pack(side="left")
            tk.Label(row, text=value, font=("Segoe UI", 9, "bold"), bg="#f8f9fa", fg="#333", anchor="e").pack(side="right")
        
        # ===== SECCIÓN: Análisis de Tendencia =====
        self._create_stats_section("📊 Análisis de Tendencia", self.tendencia_stats_content, "#9C27B0")
        
        tendencia_frame = tk.Frame(self.tendencia_stats_content, bg="#f8f9fa")
        tendencia_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Calcular pendiente de tendencia lineal
        z_lin = np.polyfit(tiempo, valores, 1)
        pendiente = z_lin[0]
        
        if pendiente > 0.1:
            tendencia_dir = "↗️ Ascendente"
            tendencia_color = "#e74c3c" if "OD" not in selected else "#27ae60"
        elif pendiente < -0.1:
            tendencia_dir = "↘️ Descendente"
            tendencia_color = "#27ae60" if "OD" not in selected else "#e74c3c"
        else:
            tendencia_dir = "➡️ Estable"
            tendencia_color = "#3498db"
        
        stats_tendencia = [
            ("R² del modelo", f"{r_squared:.4f}"),
            ("Pendiente", f"{pendiente:.4f}"),
            ("Dirección", tendencia_dir)
        ]
        
        for label, value in stats_tendencia:
            row = tk.Frame(tendencia_frame, bg="#f8f9fa")
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label + ":", font=("Segoe UI", 9), bg="#f8f9fa", fg="#555", anchor="w").pack(side="left")
            if label == "Dirección":
                tk.Label(row, text=value, font=("Segoe UI", 9, "bold"), bg="#f8f9fa", fg=tendencia_color, anchor="e").pack(side="right")
            else:
                tk.Label(row, text=value, font=("Segoe UI", 9, "bold"), bg="#f8f9fa", fg="#333", anchor="e").pack(side="right")
        
        # Interpretación de R²
        if r_squared > 0.8:
            r2_interpretacion = "Excelente ajuste del modelo"
        elif r_squared > 0.6:
            r2_interpretacion = "Buen ajuste del modelo"
        elif r_squared > 0.4:
            r2_interpretacion = "Ajuste moderado"
        else:
            r2_interpretacion = "Ajuste débil"
        
        tk.Label(tendencia_frame, text=f"💡 {r2_interpretacion}", font=("Segoe UI", 8, "italic"), 
                bg="#f8f9fa", fg="#666").pack(anchor="w", pady=(5, 0))
        
        # ===== SECCIÓN: Proyecciones por Año =====
        self._create_stats_section("🔮 Proyecciones por Año", self.tendencia_stats_content, "#FF9800")
        
        proyecciones_frame = tk.Frame(self.tendencia_stats_content, bg="#f8f9fa")
        proyecciones_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Generar estadísticas por año proyectado
        n_puntos = len(tiempo)
        meses_por_año = n_puntos // max(1, (int(self.data['AÑO'].max()) - int(self.data['AÑO'].min()) + 1))
        if meses_por_año == 0:
            meses_por_año = 12
        
        for año_idx in range(años_proyeccion):
            año_futuro = ultimo_año + año_idx + 1
            
            # Calcular valores proyectados para este año
            inicio_mes = n_puntos + (año_idx * 12)
            valores_año = [p(inicio_mes + mes) for mes in range(12)]
            promedio_año = np.mean(valores_año)
            
            # Frame para cada año
            año_frame = tk.Frame(proyecciones_frame, bg="#fff", relief="solid", bd=1)
            año_frame.pack(fill="x", pady=3)
            
            # Color según calidad esperada
            if "OD" in selected:
                if promedio_año > 6:
                    color_calidad = "#27ae60"
                elif promedio_año > 4:
                    color_calidad = "#f39c12"
                else:
                    color_calidad = "#e74c3c"
            elif "DQO" in selected:
                if promedio_año < 40:
                    color_calidad = "#27ae60"
                elif promedio_año < 100:
                    color_calidad = "#f39c12"
                else:
                    color_calidad = "#e74c3c"
            else:  # DBO5
                if promedio_año < 6:
                    color_calidad = "#27ae60"
                elif promedio_año < 30:
                    color_calidad = "#f39c12"
                else:
                    color_calidad = "#e74c3c"
            
            # Barra de color indicador
            indicator = tk.Frame(año_frame, width=4, bg=color_calidad)
            indicator.pack(side="left", fill="y")
            
            # Contenido del año
            content = tk.Frame(año_frame, bg="#fff")
            content.pack(side="left", fill="x", expand=True, padx=5, pady=5)
            
            tk.Label(content, text=f"Año {año_futuro}", font=("Segoe UI", 9, "bold"), 
                    bg="#fff", fg="#333").pack(anchor="w")
            tk.Label(content, text=f"Promedio: {promedio_año:.2f} {unidad}", font=("Segoe UI", 8), 
                    bg="#fff", fg="#666").pack(anchor="w")
            tk.Label(content, text=f"Rango: {min(valores_año):.1f} - {max(valores_año):.1f}", font=("Segoe UI", 8), 
                    bg="#fff", fg="#666").pack(anchor="w")
        
        # ===== SECCIÓN: Evaluación General =====
        self._create_stats_section("🎯 Evaluación General", self.tendencia_stats_content, "#4CAF50")
        
        evaluacion_frame = tk.Frame(self.tendencia_stats_content, bg="#f8f9fa")
        evaluacion_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Calcular tendencia general para los años proyectados
        valores_todos_años = []
        for año_idx in range(años_proyeccion):
            inicio_mes = n_puntos + (año_idx * 12)
            for mes in range(12):
                valores_todos_años.append(p(inicio_mes + mes))
        
        promedio_futuro = np.mean(valores_todos_años)
        promedio_historico = np.mean(valores)
        cambio_porcentual = ((promedio_futuro - promedio_historico) / promedio_historico) * 100
        
        # Determinar evaluación general
        if "OD" in selected:
            if promedio_futuro > 6:
                evaluacion = "✅ FAVORABLE"
                eval_color = "#27ae60"
                eval_msg = "Se proyectan niveles saludables de oxígeno"
            elif promedio_futuro > 4:
                evaluacion = "⚠️ PRECAUCIÓN"
                eval_color = "#f39c12"
                eval_msg = "Niveles de oxígeno en rango aceptable"
            else:
                evaluacion = "❌ CRÍTICO"
                eval_color = "#e74c3c"
                eval_msg = "Se proyectan niveles bajos de oxígeno"
        elif "DQO" in selected:
            if promedio_futuro < 40:
                evaluacion = "✅ FAVORABLE"
                eval_color = "#27ae60"
                eval_msg = "Baja demanda química de oxígeno"
            elif promedio_futuro < 100:
                evaluacion = "⚠️ PRECAUCIÓN"
                eval_color = "#f39c12"
                eval_msg = "DQO en niveles moderados"
            else:
                evaluacion = "❌ CRÍTICO"
                eval_color = "#e74c3c"
                eval_msg = "Alta demanda química de oxígeno"
        else:  # DBO5
            if promedio_futuro < 6:
                evaluacion = "✅ FAVORABLE"
                eval_color = "#27ae60"
                eval_msg = "Agua con buena calidad biológica"
            elif promedio_futuro < 30:
                evaluacion = "⚠️ PRECAUCIÓN"
                eval_color = "#f39c12"
                eval_msg = "DBO5 en niveles aceptables"
            else:
                evaluacion = "❌ CRÍTICO"
                eval_color = "#e74c3c"
                eval_msg = "Alta demanda biológica de oxígeno"
        
        # Mostrar evaluación
        eval_box = tk.Frame(evaluacion_frame, bg=eval_color, relief="flat")
        eval_box.pack(fill="x", pady=5)
        
        tk.Label(eval_box, text=evaluacion, font=("Segoe UI", 12, "bold"), 
                bg=eval_color, fg="white").pack(pady=5)
        
        tk.Label(evaluacion_frame, text=eval_msg, font=("Segoe UI", 9), 
                bg="#f8f9fa", fg="#555", wraplength=240).pack(anchor="w", pady=(5, 0))
        
        # Cambio respecto al histórico
        cambio_text = f"{'📈' if cambio_porcentual > 0 else '📉'} Cambio vs histórico: {cambio_porcentual:+.1f}%"
        tk.Label(evaluacion_frame, text=cambio_text, font=("Segoe UI", 9, "bold"), 
                bg="#f8f9fa", fg="#333").pack(anchor="w", pady=(5, 0))
    
    def _create_stats_section(self, title, parent, color):
        """Crea un encabezado de sección para el panel de estadísticas"""
        section_frame = tk.Frame(parent, bg="#f8f9fa")
        section_frame.pack(fill="x", padx=5, pady=(10, 5))
        
        # Barra de color
        color_bar = tk.Frame(section_frame, width=4, height=18, bg=color)
        color_bar.pack(side="left", padx=(0, 8))
        
        # Título
        tk.Label(section_frame, text=title, font=("Segoe UI", 10, "bold"), 
                bg="#f8f9fa", fg="#333").pack(side="left")
    
    def embed_figure_with_description(self, fig, title="", description=""):
        """Embebe una figura con descripción"""
        self.clear_display()
        
        # Título
        title_label = tk.Label(
            self.display_frame,
            text=title,
            font=("Segoe UI", 16, "bold"),
            bg=COLOR_WHITE,
            fg=COLOR_DARK_TEAL
        )
        title_label.pack(anchor="w", pady=(0, 8))
        
        # Descripción
        if description:
            desc_frame = tk.Frame(self.display_frame, bg="#e3f2fd", relief="flat")
            desc_frame.pack(fill="x", pady=(0, 10))
            
            desc_label = tk.Label(
                desc_frame,
                text=f"💡 {description}",
                font=("Segoe UI", 9),
                bg="#e3f2fd",
                fg="#1565c0",
                justify="left",
                wraplength=900,
                pady=8,
                padx=10
            )
            desc_label.pack(anchor="w")
        
        # Frame para la figura
        fig_frame = tk.Frame(self.display_frame, bg=COLOR_WHITE, relief="solid", borderwidth=1)
        fig_frame.pack(fill="both", expand=True)
        
        fig.tight_layout()
        
        # Canvas de matplotlib
        self.current_figure = fig
        self.current_canvas = FigureCanvasTkAgg(fig, master=fig_frame)
        self.current_canvas.draw()
        
        # Toolbar
        toolbar_frame = tk.Frame(fig_frame, bg=COLOR_LIGHT_GRAY)
        toolbar_frame.pack(side="bottom", fill="x")
        toolbar = NavigationToolbar2Tk(self.current_canvas, toolbar_frame)
        toolbar.update()
        
        self.current_canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
    
    def vista_simulador(self):
        """Simulador interactivo para predecir DBO5"""
        # Limpiar área de contenido usando el método estándar
        self.clear_display()
        
        # Frame principal del simulador dentro de display_frame
        main_frame = tk.Frame(self.display_frame, bg=COLOR_LIGHT_TEAL)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🖩 Simulador de Predicción DBO5",
            font=("Segoe UI", 18, "bold"),
            bg=COLOR_LIGHT_TEAL,
            fg=COLOR_DARK_TEAL
        )
        title_label.pack(pady=(10, 10))
        
        # Recuadro azul con descripción
        desc_frame = tk.Frame(main_frame, bg="#e3f2fd", relief="flat")
        desc_frame.pack(fill="x", padx=30, pady=(0, 15))
        
        desc_info = tk.Label(
            desc_frame,
            text="💡 Este simulador permite predecir la DBO5 ingresando valores de Oxígeno Disuelto (OD) y Demanda Química "
                 "de Oxígeno (DQO). Utiliza el modelo de regresión calibrado con los datos del Río Atoyac. Es útil para "
                 "estimar rápidamente la calidad del agua sin necesidad de esperar los 5 días que toma el análisis de DBO5.",
            font=("Segoe UI", 9),
            bg="#e3f2fd",
            fg="#1565c0",
            justify="left",
            wraplength=700,
            pady=10,
            padx=10
        )
        desc_info.pack(anchor="w")
        
        # Ecuación del modelo
        eq_label = tk.Label(
            main_frame,
            text="Modelo: DBO5 = -6.6283 × OD + 0.3407 × DQO + 21.3075",
            font=("Segoe UI", 10, "italic"),
            bg=COLOR_LIGHT_TEAL,
            fg="#555555",
            justify="center"
        )
        eq_label.pack(pady=(0, 20))
        
        # Frame para inputs
        input_frame = tk.Frame(main_frame, bg=COLOR_LIGHT_TEAL)
        input_frame.pack(pady=10)
        
        # Variables para entries
        self.od_var = tk.StringVar(value="5.0")
        self.dqo_var = tk.StringVar(value="100.0")
        
        # Input OD
        od_frame = tk.Frame(input_frame, bg=COLOR_LIGHT_TEAL)
        od_frame.pack(pady=10)
        
        tk.Label(
            od_frame,
            text="💧 Oxígeno Disuelto (OD) [mg/L]:",
            font=("Segoe UI", 12),
            bg=COLOR_LIGHT_TEAL,
            fg=COLOR_DARK_TEAL
        ).pack(side="left", padx=(0, 10))
        
        od_entry = tk.Entry(
            od_frame,
            textvariable=self.od_var,
            font=("Segoe UI", 12),
            width=15,
            justify="center",
            relief="solid",
            bd=1
        )
        od_entry.pack(side="left")
        
        # Input DQO
        dqo_frame = tk.Frame(input_frame, bg=COLOR_LIGHT_TEAL)
        dqo_frame.pack(pady=10)
        
        tk.Label(
            dqo_frame,
            text="🔬 Demanda Química de Oxígeno (DQO) [mg/L]:",
            font=("Segoe UI", 12),
            bg=COLOR_LIGHT_TEAL,
            fg=COLOR_DARK_TEAL
        ).pack(side="left", padx=(0, 10))
        
        dqo_entry = tk.Entry(
            dqo_frame,
            textvariable=self.dqo_var,
            font=("Segoe UI", 12),
            width=15,
            justify="center",
            relief="solid",
            bd=1
        )
        dqo_entry.pack(side="left")
        
        # Botón calcular
        calc_button = tk.Button(
            main_frame,
            text="🧮 Calcular DBO5",
            font=("Segoe UI", 12, "bold"),
            bg=COLOR_GREEN,
            fg="white",
            activebackground=COLOR_LIGHT_GREEN,
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2",
            command=self.calcular_dbo5_simulador
        )
        calc_button.pack(pady=30)
        
        # Frame para resultado
        self.result_frame = tk.Frame(main_frame, bg="white", relief="solid", bd=2)
        self.result_frame.pack(fill="x", padx=50, pady=10)
        
        self.result_label = tk.Label(
            self.result_frame,
            text="Ingrese valores y presione 'Calcular DBO5'",
            font=("Segoe UI", 14),
            bg="white",
            fg="#888888",
            pady=20
        )
        self.result_label.pack()
        
        # Información adicional
        info_frame = tk.Frame(main_frame, bg=COLOR_LIGHT_TEAL)
        info_frame.pack(fill="x", pady=30)
        
        info_text = """
Información del Modelo:
• Coeficiente de determinación (R²): El modelo explica una porción significativa de la variabilidad
• Rango típico de OD: 2.0 - 10.0 mg/L
• Rango típico de DQO: 50 - 500 mg/L
• La predicción es más precisa dentro de los rangos de datos de entrenamiento
        """
        
        tk.Label(
            info_frame,
            text=info_text,
            font=("Segoe UI", 10),
            bg=COLOR_LIGHT_TEAL,
            fg="#666666",
            justify="left"
        ).pack(anchor="w", padx=50)
    
    def calcular_dbo5_simulador(self):
        """Calcula DBO5 con los valores ingresados en el simulador"""
        try:
            od = float(self.od_var.get())
            dqo = float(self.dqo_var.get())
            
            # Aplicar modelo de regresión
            # DBO5 = -6.6283 × OD + 0.3407 × DQO + 21.3075
            dbo5_pred = -6.6283 * od + 0.3407 * dqo + 21.3075
            
            # Determinar calidad del agua según DBO5
            if dbo5_pred < 3:
                calidad = "🟢 Excelente (Agua muy limpia)"
                color = "#27ae60"
            elif dbo5_pred < 6:
                calidad = "🟡 Buena (Agua limpia)"
                color = "#f39c12"
            elif dbo5_pred < 30:
                calidad = "🟠 Aceptable (Algo contaminada)"
                color = "#e67e22"
            elif dbo5_pred < 100:
                calidad = "🔴 Contaminada"
                color = "#e74c3c"
            else:
                calidad = "⚫ Muy contaminada"
                color = "#2c3e50"
            
            # Actualizar resultado
            self.result_label.config(
                text=f"DBO5 Predicho: {dbo5_pred:.2f} mg/L\n\nCalidad del agua: {calidad}",
                fg=color,
                font=("Segoe UI", 16, "bold")
            )
            
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para OD y DQO.")
