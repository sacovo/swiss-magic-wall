FROM node:lts AS app

WORKDIR /app

COPY package.json /app/
RUN npm install -g @angular/cli
RUN npm install 

COPY ./ /app/

CMD ["npm", "start", "--", "--host", "0.0.0.0", "--poll", "50"]

FROM app as builder

RUN ng build app --configuration=production

FROM nginx:alpine

COPY --from=builder /app/dist/app/* /usr/share/nginx/html/

COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.conf /usr/local/nginx/conf/nginx.conf
