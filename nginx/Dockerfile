FROM nginx:1.27-alpine

# Копируем свой конфиг виртуального хоста.
COPY nginx.conf /etc/nginx/nginx.conf

# Открываем стандартный HTTP-порт внутри контейнера.
EXPOSE 80

# Запускаем nginx в foreground-режиме,
CMD ["nginx", "-g", "daemon off;"]
