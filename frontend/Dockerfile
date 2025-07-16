# /frontend/Dockerfile

### STAP 1: Bouw de Svelte App ###
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . .
RUN npm run build

### STAP 2: Serveer de gebouwde app met Nginx ###
FROM nginx:stable-alpine
# Kopieer de gebouwde bestanden uit de 'builder' stap
COPY --from=builder /app/build /usr/share/nginx/html
# Optioneel: kopieer een eigen Nginx-config als je routing hebt
# COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]