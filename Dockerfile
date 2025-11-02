# Використовуємо базовий образ Apache
FROM httpd:2.4

# Копіюємо наш HTML файл в папку Apache
COPY index.html /usr/local/apache2/htdocs/

# Відкриваємо порт 80
EXPOSE 80

# Запускаємо Apache
CMD ["httpd-foreground"]