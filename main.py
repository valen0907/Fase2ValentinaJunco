import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from abc import ABC, abstractmethod

class Persona(ABC):
    """
    Clase abstracta base que define el contrato para todas
    las clases relacionadas con personas en el sistema.
    """
    @abstractmethod
    def obtener_resumen(self):
        pass

class Gestion_Empleados(Persona):
    """
    Clase pública que almacena los datos del empleado
    y calcula el total a pagar por nómina.
    Hereda de Persona (ABC).
    """

    CARGOS = {
        "Servicios Generales": 40000,
        "Administrativo":      50000,
        "Electricista":        60000,
        "Mecánico":            80000,
        "Soldador":            90000,
    }

    def __init__(self):
        self.id               = ""
        self.nombre           = ""
        self.genero           = ""
        self.cargo            = ""
        self.salario_dia      = 0
        self.dias_laborados   = 0
        self.fecha_registro   = ""

    def calcular_pago_total(self):
        """
        Método de cálculo principal.
        Fórmula: total = salario_dia × dias_laborados
        Retorna un entero con el total a pagar.
        """
        return self.salario_dia * self.dias_laborados

    def obtener_resumen(self):
        """
        Implementa el método abstracto heredado de Persona.
        Llama a calcular_pago_total() y construye el reporte.
        """
        total = self.calcular_pago_total()
        return (
            f"Nombre:              {self.nombre}\n"
            f"ID:                  {self.id}\n"
            f"Género:              {self.genero}\n"
            f"Cargo:               {self.cargo}\n"
            f"Días Laborados:      {self.dias_laborados}\n"
            f"Fecha de Registro:   {self.fecha_registro}\n"
            f"Valor día trabajo:   ${self.salario_dia:,}\n"
            f"Total a Pagar:       ${total:,}"
        )

class AplicacionNomina:
    """
    Clase que gestiona toda la interfaz gráfica de la aplicación.
    Navega entre pantallas: Login → Registro → Reporte.
    """

    def __init__(self, root):
        self.root    = root
        self.empleado = Gestion_Empleados()
        self.mostrar_login()

    def limpiar_pantalla(self):
        """Destruye todos los widgets actuales de la ventana."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_login(self):
        """
        Construye la interfaz inicial de acceso.
        Muestra nombre de la app y campo de contraseña enmascarada.
        """
        self.root.title("Login - Constructora Mejor")
        self.root.geometry("350x260")
        self.root.resizable(False, False)
        self.limpiar_pantalla()

        frame = ttk.Frame(self.root, padding="20")
        frame.pack(expand=True)

        ttk.Label(frame, text="Aplicación: Gestión de Empleados",
                  font=("Arial", 10, "bold")).pack()
        ttk.Label(frame, text="Autor: Maria Valentina Monroy Junco").pack(pady=2)
        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(frame, text="Contraseña:").pack()

        self.ent_pass = ttk.Entry(frame, show="*", width=20)
        self.ent_pass.pack(pady=5)
        self.ent_pass.bind("<Return>", lambda e: self.validar_acceso())

        ttk.Button(frame, text="Ingresar",
                   command=self.validar_acceso).pack(pady=10)
        self.ent_pass.focus()

    def validar_acceso(self):
        """
        Valida la contraseña ingresada contra el código de acceso.
        Contraseña correcta → mostrar_registro()
        Contraseña incorrecta → mensaje de error
        """
        PASSWORD = "4682"
        if self.ent_pass.get() == PASSWORD:
            self.mostrar_registro()
        else:
            messagebox.showerror("Acceso denegado", "Contraseña incorrecta.\nIntente nuevamente.")
            self.ent_pass.delete(0, tk.END)
            self.ent_pass.focus()

    def mostrar_registro(self):
        """
        Construye la interfaz de registro de datos del empleado.
        Campos: ID, nombre, género (radio), cargo (combo),
                salario día (deshabilitado), días laborados.
        Botones: Guardar Registro | Calcular Nómina / Reporte | Salir
        """
        self.root.title("Registro de Empleados - Constructora Mejor")
        self.root.geometry("460x420")
        self.root.resizable(False, False)
        self.limpiar_pantalla()

        frame = ttk.Frame(self.root, padding="15")
        frame.pack(fill="both")

        campos = [
            ("Identificación:",  0),
            ("Nombre Completo:", 1),
        ]
        for label, row in campos:
            ttk.Label(frame, text=label).grid(row=row, column=0, sticky="w", pady=4)

        self.ent_id  = ttk.Entry(frame, width=28)
        self.ent_id.grid(row=0, column=1, pady=4)

        self.ent_nom = ttk.Entry(frame, width=28)
        self.ent_nom.grid(row=1, column=1, pady=4)

        ttk.Label(frame, text="Género:").grid(row=2, column=0, sticky="w", pady=4)
        self.var_gen = tk.StringVar(value="Masculino")
        gen_frame = ttk.Frame(frame)
        gen_frame.grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(gen_frame, text="Masculino", variable=self.var_gen,
                        value="Masculino").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(gen_frame, text="Femenino",  variable=self.var_gen,
                        value="Femenino").pack(side="left")

        ttk.Label(frame, text="Cargo Laboral:").grid(row=3, column=0, sticky="w", pady=4)
        self.cb_cargo = ttk.Combobox(
            frame,
            values=list(Gestion_Empleados.CARGOS.keys()),
            state="readonly",
            width=26
        )
        self.cb_cargo.grid(row=3, column=1, pady=4)
        self.cb_cargo.bind("<<ComboboxSelected>>", self.actualizar_salario)

        ttk.Label(frame, text="Salario día:").grid(row=4, column=0, sticky="w", pady=4)
        self.ent_sal = ttk.Entry(frame, state="disabled", width=28)
        self.ent_sal.grid(row=4, column=1, pady=4)

        ttk.Label(frame, text="Días laborados:").grid(row=5, column=0, sticky="w", pady=4)
        self.ent_dias = ttk.Entry(frame, width=28)
        self.ent_dias.grid(row=5, column=1, pady=4)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=12)

        ttk.Button(btn_frame, text="Guardar Registro",
                   command=self.guardar_datos).grid(row=0, column=0, padx=6)
        ttk.Button(btn_frame, text="Calcular Nómina / Reporte",
                   command=self.mostrar_reporte).grid(row=0, column=1, padx=6)
        ttk.Button(self.root, text="Salir",
                   command=self.confirmar_salida).pack()

    def actualizar_salario(self, event):
        """
        Disparado por el evento <<ComboboxSelected>>.
        Habilita temporalmente el campo salario, inserta el valor
        correspondiente al cargo seleccionado y lo deshabilita.
        Garantiza que el usuario no pueda editar el salario manualmente.
        """
        cargo = self.cb_cargo.get()
        valor = Gestion_Empleados.CARGOS.get(cargo, 0)

        self.ent_sal.config(state="normal")
        self.ent_sal.delete(0, tk.END)
        self.ent_sal.insert(0, str(valor))
        self.ent_sal.config(state="disabled")

    def guardar_datos(self):
        """
        Lee los valores del formulario y los asigna al objeto empleado.
        Validaciones:
          - Todos los campos obligatorios deben estar completos.
          - Se debe haber seleccionado un cargo.
          - Días laborados debe ser un número entero positivo.
        La fecha de registro se genera en este momento (no al instanciar).
        """
        if not self.ent_id.get().strip():
            messagebox.showwarning("Campo requerido", "Ingrese la identificación del empleado.")
            return
        if not self.ent_nom.get().strip():
            messagebox.showwarning("Campo requerido", "Ingrese el nombre completo del empleado.")
            return
        if not self.cb_cargo.get():
            messagebox.showwarning("Campo requerido", "Seleccione un cargo laboral.")
            return
        if not self.ent_dias.get().strip():
            messagebox.showwarning("Campo requerido", "Ingrese los días laborados.")
            return

        try:
            dias = int(self.ent_dias.get())
            if dias <= 0:
                raise ValueError("Debe ser positivo")
        except ValueError:
            messagebox.showerror("Dato inválido",
                                 "Días laborados debe ser un número entero mayor a cero.")
            self.ent_dias.focus()
            return

        try:
            self.empleado.id             = self.ent_id.get().strip()
            self.empleado.nombre         = self.ent_nom.get().strip()
            self.empleado.genero         = self.var_gen.get()
            self.empleado.cargo          = self.cb_cargo.get()
            self.empleado.salario_dia    = int(self.ent_sal.get())
            self.empleado.dias_laborados = dias
            self.empleado.fecha_registro = datetime.now().strftime("%Y-%m-%d")

            messagebox.showinfo("✔ Guardado",
                                f"Datos de '{self.empleado.nombre}' guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"No se pudo guardar: {e}")

    def mostrar_reporte(self):
        """
        Verifica que exista un registro guardado y muestra la pantalla
        de reporte con todos los datos del empleado y el total a pagar.
        Llama a empleado.obtener_resumen() para obtener el texto formateado.
        """
        if not self.empleado.id:
            messagebox.showwarning("Sin registro",
                                   "Primero debe guardar un registro de empleado.")
            return

        self.root.title("Reporte de Nómina - Constructora Mejor")
        self.root.geometry("400x360")
        self.limpiar_pantalla()

        frame = ttk.Frame(self.root, padding="25")
        frame.pack(expand=True)

        ttk.Label(frame, text="── REPORTE DE PAGO ──",
                  font=("Arial", 13, "bold")).pack(pady=(0, 12))

        ttk.Label(frame,
                  text=self.empleado.obtener_resumen(),
                  justify="left",
                  font=("Courier", 10)).pack()

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=12)
        ttk.Button(frame, text="← Regresar",
                   command=self.mostrar_registro).pack()

    def confirmar_salida(self):
        """
        Solicita confirmación antes de cerrar la aplicación.
        """
        if messagebox.askyesno("Salir", "¿Realmente desea salir de la aplicación?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app  = AplicacionNomina(root)
    root.mainloop()
