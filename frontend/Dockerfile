FROM node:20-alpine AS builder

RUN npm install -g pnpm

WORKDIR /app

COPY package*.json ./
RUN pnpm i

COPY . .

RUN pnpm run build


FROM caddy:2-alpine

COPY --from=builder /app/dist /usr/share/caddy

COPY Caddyfile /etc/caddy/Caddyfile

EXPOSE 3000
