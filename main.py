import logging
import time
from datetime import datetime

from logic.pipeline import AlturasPipelineExecutor

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    logger = logging.getLogger(__name__)
    inicio_ts = time.time()
    inicio_humano = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        executor = AlturasPipelineExecutor()
        executor.run()
    finally:
        fin_ts = time.time()
        fin_humano = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duracion = fin_ts - inicio_ts

        minutos = int(duracion // 60)
        segundos = int(duracion % 60)

        logger.info(f"Duración total: {minutos} min {segundos} seg")
