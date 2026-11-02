from app.database import Base, SessionLocal, engine
from app.models import Task

Base.metadata.create_all(bind=engine)

with SessionLocal() as session:
    task1 = Task(
        title="Learn FastAPI",
        completed = False,
    )

    task2 = Task(
        title="Practice SQL",
        completed = True,
    )
    session.add_all([task1, task2])
    session.commit()
