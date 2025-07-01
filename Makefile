.PHONY: all comuna tipo fecha visualizar limpiar

all: limpiar comuna tipo fecha visualizar

comuna:
	@echo "➤ Ejecutando análisis por comuna..."
	docker-compose run --rm pig /opt/pig/bin/pig -x local /data/comuna.pig

tipo:
	@echo "➤ Ejecutando análisis por tipo..."
	docker-compose run --rm pig /opt/pig/bin/pig -x local /data/tipo.pig

fecha:
	@echo "➤ Ejecutando análisis por fecha..."
	docker-compose run --rm pig /opt/pig/bin/pig -x local /data/fecha.pig

visualizar:
	@echo "➤ Iniciando visualizador..."
	docker-compose up -d visualizador

limpiar:
	@echo "➤ Limpiando archivos y carpetas anteriores"
	sudo rm -rf salida/comuna salida/tipo salida/fecha
	sudo rm -f salida/*.log
	sudo rm -f salida/*.pig
