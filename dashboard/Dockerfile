# Production Dockerfile (Dockerfile)

#
# ---- Build ----
FROM node:8-alpine AS builder

WORKDIR /usr/src/app

COPY package.json package-lock.json ./

RUN npm install --quiet

COPY . ./

CMD [ "npm", "run", "build" ]

#
# ---- Serve with Nginx ---
FROM nginx:1.15

COPY --from=builder /usr/src/app/dist /usr/share/nginx/html

EXPOSE 80
RUN chown nginx.nginx /usr/share/nginx/html/ -R
