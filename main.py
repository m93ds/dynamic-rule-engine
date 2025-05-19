from datetime import datetime, timedelta
from typing import List, Dict, Any, Callable
import json
import os

# Definición de una cita médica estandarizada
class Appointment:
    def __init__(self, data: Dict[str, Any]):
        # Campos estándar definidos por el sistema
        self.id = data.get("id")
        self.date = data.get("date")
        self.specialty = data.get("specialty")
        self.doctor_id = data.get("doctor_id")
        self.patient_type = data.get("patient_type")
        self.status = data.get("status")
        self.patient_age = data.get("patient_age", 0)
        self.unit = data.get("unit")
        self.data = data  # Datos completos originales

    def __repr__(self):
        return f"Cita {self.id} | Especialidad: {self.specialty} | Doctor: {self.doctor_id}"

# Clase principal del motor de reglas
class RuleEngine:
    def __init__(self, rules_config: List[Dict]):
        """Inicializa el motor de reglas con configuración dinámica"""
        self.rules = []
        for rule in rules_config:
            self.add_rule(
                name=rule["name"],
                condition=self._create_condition(rule["condition"]),
                priority=rule.get("priority", 0)
            )
        # Ordena las reglas por prioridad (opcional)
        self.rules.sort(key=lambda r: r["priority"], reverse=True)

    def _create_condition(self, condition_dict: Dict) -> Callable[[Appointment], bool]:
        """Convierte un diccionario de condiciones en una función ejecutable"""
        def condition(appointment: Appointment) -> bool:
            for field, value in condition_dict.items():
                if isinstance(value, dict):
                    # Manejo de condiciones complejas (ej: rangos de edad)
                    if field == "age_range":
                        min_age = value.get("min", 0)
                        max_age = value.get("max", float('inf'))
                        if not (min_age <= appointment.patient_age <= max_age):
                            return False
                elif getattr(appointment, field, None) != value:
                    return False
            return True
        return condition

    def add_rule(self, name: str, condition: Callable[[Appointment], bool], priority: int = 0):
        """Agrega una nueva regla al motor"""
        self.rules.append({
            "name": name,
            "condition": condition,
            "priority": priority
        })

    def filter_appointments(self, appointments: List[Appointment]) -> List[Appointment]:
        """Aplica todas las reglas activas sobre las citas"""
        filtered = []
        for appt in appointments:
            # Verifica si cumple TODAS las condiciones
            if all(rule["condition"](appt) for rule in self.rules):
                filtered.append(appt)
        return filtered

def load_json_file(file_path: str) -> Dict:
    """Carga datos desde un archivo JSON"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    # Cargar configuración
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cargar reglas desde archivo de configuración
    rules_config = load_json_file(os.path.join(current_dir, "rules_config.json"))
    
    # Cargar datos de ejemplo
    raw_data = load_json_file(os.path.join(current_dir, "data", "samples.json"))
    
    # Convertir datos crudos a objetos Appointment
    appointments = [Appointment(data) for data in raw_data]

    # Inicializar el motor de reglas
    engine = RuleEngine(rules_config)

    # Filtrar citas según las reglas
    filtered = engine.filter_appointments(appointments)

    print("Citas filtradas:")
    for appt in filtered:
        print(appt)
