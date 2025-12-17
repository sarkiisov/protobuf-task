import grpc
from concurrent import futures
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import glossary_pb2
import glossary_pb2_grpc
from app.database import SessionLocal, engine
from app import models, crud
from grpc_reflection.v1alpha import reflection

models.Base.metadata.create_all(bind=engine)

class GlossaryServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    
    def GetTerm(self, request, context):
        db = SessionLocal()
        try:
            term = crud.get_term_by_keyword(db, request.keyword)
            if not term:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Term not found")
                return glossary_pb2.Term()
            return glossary_pb2.Term(
                id=term.id,
                keyword=term.keyword,
                description=term.description
            )
        finally:
            db.close()
    
    def GetAllTerms(self, request, context):
        db = SessionLocal()
        try:
            terms = crud.get_terms(db)
            for term in terms:
                yield glossary_pb2.Term(
                    id=term.id,
                    keyword=term.keyword,
                    description=term.description
                )
        finally:
            db.close()
    
    def CreateTerm(self, request, context):
        db = SessionLocal()
        try:
            existing = crud.get_term_by_keyword(db, request.keyword)
            if existing:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("Term already exists")
                return glossary_pb2.Term()
            
            term = crud.create_term(db, request.keyword, request.description)
            return glossary_pb2.Term(
                id=term.id,
                keyword=term.keyword,
                description=term.description
            )
        finally:
            db.close()
    
    def UpdateTerm(self, request, context):
        db = SessionLocal()
        try:
            term = crud.update_term(db, request.keyword, request.description)
            if not term:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Term not found")
                return glossary_pb2.Term()
            
            return glossary_pb2.Term(
                id=term.id,
                keyword=term.keyword,
                description=term.description
            )
        finally:
            db.close()
    
    def DeleteTerm(self, request, context):
        db = SessionLocal()
        try:
            term = crud.delete_term(db, request.keyword)
            if not term:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Term not found")
                return glossary_pb2.DeleteTermResponse(message="")
            
            return glossary_pb2.DeleteTermResponse(
                message=f"Term '{request.keyword}' deleted successfully"
            )
        finally:
            db.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    glossary_pb2_grpc.add_GlossaryServiceServicer_to_server(
        GlossaryServicer(), server
    )
    
    SERVICE_NAMES = (
        glossary_pb2.DESCRIPTOR.services_by_name['GlossaryService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    
    server.add_insecure_port('[::]:50051')
    print("gRPC server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()