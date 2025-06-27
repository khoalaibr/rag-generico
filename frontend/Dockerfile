# frontend/Dockerfile

# Usar una imagen oficial de Node.js como imagen base.
FROM node:20-alpine

# Establecer el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Copiar los archivos de definición de dependencias.
COPY package.json ./

# --- CORRECCIÓN FINAL ---
# Al haber resuelto el conflicto de TypeScript directamente en package.json,
# ya no necesitamos flags especiales. Un 'npm install' limpio y estándar
# funcionará de forma robusta.
RUN npm install

# Copiar el resto del código de la aplicación.
COPY . .

# Exponer el puerto y definir el comando de inicio.
EXPOSE 3000
CMD ["npm", "start"]
