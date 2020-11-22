# build stage
FROM node:lts-alpine as build-stage
WORKDIR .
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# production stage
FROM nginx:stable-alpine as production-stage
COPY ./.nginx/nginx.conf /etc/nginx/nginx.conf

COPY --from=build-stage ./dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]