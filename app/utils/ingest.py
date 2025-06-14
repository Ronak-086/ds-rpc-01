from app.services.ingestion_service import IngestionService

if __name__ == "__main__":
    service = IngestionService()
    service.run_ingestion()
