# 📘 Glossary API

## 🔧 Генерация gRPC кода

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. glossary.proto

## 🐳 Запуск с помощью Docker Compose

```
docker compose up -d
# http://localhost:50051
```

## 🧪 Тестовые сценарии

1. Проверка сервера и методов:

   ```
   C:\Users\Nikita>grpcurl -plaintext localhost:50051 list
   glossary.GlossaryService
   grpc.reflection.v1alpha.ServerReflection
   ```

   ```
   C:\Users\Nikita>grpcurl -plaintext localhost:50051 describe glossary.GlossaryService
   glossary.GlossaryService is a service:
   service GlossaryService {
   rpc CreateTerm ( .glossary.CreateTermRequest ) returns ( .glossary.Term );
   rpc DeleteTerm ( .glossary.DeleteTermRequest ) returns ( .glossary.DeleteTermResponse );
   rpc GetAllTerms ( .glossary.GetAllTermsRequest ) returns ( stream .glossary.Term );
   rpc GetTerm ( .glossary.GetTermRequest ) returns ( .glossary.Term );
   rpc UpdateTerm ( .glossary.UpdateTermRequest ) returns ( .glossary.Term );
   }
   ```

2. Создание терминов:

   ```
   C:\Users\Nikita>grpcurl -d "{\"keyword\":\"API\",\"description\":\"Application Programming Interface\"}" -plaintext localhost:50051 glossary.GlossaryService/CreateTerm
   {
   "id": 1,
   "keyword": "API",
   "description": "Application Programming Interface"
   }
   ```

   ```
   C:\Users\Nikita>grpcurl -d "{\"keyword\":\"API\",\"description\":\"Application Programming Interface\"}" -plaintext localhost:50051 glossary.GlossaryService/CreateTerm
   ERROR:
   Code: AlreadyExists
   Message: Term already exists
   ```

3. Получение терминов:

   ```
   C:\Users\Nikita>grpcurl -plaintext localhost:50051 glossary.GlossaryService/GetAllTerms
   {
   "id": 1,
   "keyword": "API",
   "description": "Application Programming Interface"
   }
   ```

   ```
   C:\Users\Nikita>grpcurl -d "{\"keyword\":\"API\"}" -plaintext localhost:50051 glossary.GlossaryService/GetTerm
   {
   "id": 1,
   "keyword": "API",
   "description": "Application Programming Interface"
   }
   ```

4. Обновление терминов:

   ```
   C:\Users\Nikita>grpcurl -d "{\"keyword\":\"API\",\"description\":\"UPDATED: Application Programming Interface\"}" -plaintext localhost:50051 glossary.GlossaryService/UpdateTerm
   {
   "id": 1,
   "keyword": "API",
   "description": "UPDATED: Application Programming Interface"
   }
   ```

5. Удаление терминов:

   ```
   C:\Users\Nikita>grpcurl -d "{\"keyword\":\"API\"}" -plaintext localhost:50051 glossary.GlossaryService/DeleteTerm
   {
   "message": "Term 'API' deleted successfully"
   }
   ```

   ```
   C:\Users\Nikita>grpcurl -d "{\"keyword\":\"NonExistent\"}" -plaintext localhost:50051 glossary.GlossaryService/DeleteTerm
   ERROR:
   Code: NotFound
   Message: Term not found
   ```
