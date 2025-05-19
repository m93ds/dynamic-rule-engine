# Motor de Reglas Dinámicas - Cero.ai

## Descripción
Sistema para filtrar citas médicas según políticas específicas de hospitales y clínicas, con capacidad de adaptarse a diferentes sistemas hospitalarios.

## Características
- ✅ Reglas configurables sin modificar código
- ✅ Soporte para múltiples condiciones complejas
- ✅ Adaptabilidad a diferentes esquemas de datos hospitalarios
- ✅ Priorización de reglas

## Requisitos
- Python 3.11+
- Librerías: `typing`, `datetime`

## Instalación
```bash
git clone https://github.com/tu-usuario/cero-rule-engine.git 
cd cero-rule-engine
pip install -r requirements.txt

##Uso
python main.py

#Ejemplo Salida
Citas filtradas:
Cita A123 | Especialidad: cardiología | Doctor: DR123

#Estructura de archivos
main.py: Implementación de motor de reglas
rules_config.json: Definición de reglas
data_samples.json: Datos de ejemplo 
