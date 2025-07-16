# frontend/Dockerfile

# Stap 1: Bouw de applicatie
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build

# Stap 2: Draai de applicatie
FROM node:18-alpine
WORKDIR /app

# Kopieer de output van de build en de benodigde bestanden
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY package.json .

# De poort die de SvelteKit Node server gebruikt
EXPOSE 3000

# Het commando om de server te starten
CMD ["node", "build"]