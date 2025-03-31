const portBack = 5000;
new Vue({
    el: "#app",
    data() {
        return {
            datos: [],
            equipo1: null,
            equipo2: null,
            jugadores_con_experiencia: null,
            jugadores_con_suerte: null,
            mejores_arqueros: null,
            puntaje_global: null,
            total_generos: null,
            victorias_juegos_femenino: null,
            victorias_juegos_masculino: null,
            victorias_por_genero_juego: null,
            victorias_rondas_femenino: null,
            victorias_rondas_masculino: null,
            victorias_totales: null,
            puntajesPorJuego: {} // Almacena los puntajes de los arqueros por juego
        };
    },
    methods: {
        // Este método se encarga de recibir los datos del back
        async getAllData() {
            try {
                const response = await fetch(`http://localhost:${portBack}/datos`);
                if (response.ok) {
                    const result = await response.json();
                    if (result.length > 0) {
                        const data = result[0];

                        this.datos = result;
                        this.equipo1 = data.equipo_1;
                        this.equipo2 = data.equipo_2;
                        this.jugadores_con_experiencia = data.jugadores_con_experiencia;
                        this.jugadores_con_suerte = data.jugadores_con_suerte;
                        this.mejores_arqueros = data.mejores_arqueros;
                        this.puntaje_global = data.puntaje_global;
                        this.total_generos = data.total_generos;
                        this.victorias_juegos_femenino = data.victorias_juegos_femenino;
                        this.victorias_juegos_masculino = data.victorias_juegos_masculino;
                        this.victorias_por_genero_juego = data.victorias_por_genero_juego;
                        this.victorias_rondas_femenino = data.victorias_rondas_femenino;
                        this.victorias_rondas_masculino = data.victorias_rondas_masculino;
                        this.victorias_totales = data.victorias_totales;

                        // Extraer puntajes por juego y generar la gráfica
                        this.puntajesPorJuego = this.obtenerPuntajesPorJuego([...this.equipo1, ...this.equipo2]);
                        this.dibujarGrafico();

                        console.log("Datos actualizados correctamente", this.$data);
                    }
                } else {
                    console.error("Error en la solicitud:", response.status);
                }
            } catch (error) {
                console.error("Error de conexión:", error);
            }
        },

        obtenerPuntajesPorJuego(arqueros) {
            let puntajes = {};
            arqueros.forEach(arquero => {
                puntajes[arquero.nombre] = arquero.puntajes_por_juego;
            });
            return puntajes;
        },

        dibujarGrafico() {
            const ctx = document.getElementById("graficoPuntajes").getContext("2d");

            // Si ya existe una instancia de gráfico, la destruimos para evitar duplicados
            if (this.chartInstance) {
                this.chartInstance.destroy();
            }

            const datasets = Object.keys(this.puntajesPorJuego).map(nombre => {
                return {
                    label: `Arquero ${nombre}`,
                    data: Object.values(this.puntajesPorJuego[nombre]), // Puntos obtenidos
                    borderColor: this.getRandomColor(),
                    fill: false,
                    tension: 0.1
                };
            });

            this.chartInstance = new Chart(ctx, {
                type: "line",
                data: {
                    labels: Object.keys(this.puntajesPorJuego[Object.keys(this.puntajesPorJuego)[0]]), // Juegos
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: "top"
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Juego"
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: "Puntaje"
                            },
                            beginAtZero: true
                        }
                    }
                }
            });
        },

        getRandomColor() {
            return `rgb(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)})`;
        }
    },
    mounted() {
        this.getAllData();
    }
});
