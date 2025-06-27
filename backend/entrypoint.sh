#!/bin/sh
# Este es un script de punto de entrada personalizado. Su único propósito
# es asegurar que el contenedor se mantenga en ejecución para que podamos
# depurarlo, incluso si hay problemas con los comandos de Docker Compose.

echo "Entrypoint script iniciado. El contenedor permanecerá activo."
echo "Puedes conectarte ahora con 'docker-compose exec rag_backend bash'."

# Este comando mantiene el script (y por lo tanto el contenedor)
# corriendo indefinidamente.
tail -f /dev/null
