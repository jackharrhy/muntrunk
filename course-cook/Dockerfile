FROM node:13-alpine as build

WORKDIR /app

COPY package.json /app/package.json
RUN npm install --silent
COPY . /app
COPY .env.dist /app/.env
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
