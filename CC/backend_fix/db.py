from select import select
from tabnanny import check
from sqlmodel import SQLModel, Session, create_engine, select
import dbmod
import xlrd

#Jika ingin menginisialisasi/connect ke SQLite local, uncomment 4 baris dibawah
sqlite_file_name = "testqc.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

#Jika ingin connect ke Cloud SQL, uncomment 2 baris dibawah
#sqlite_url = "mysql+pymysql://hariyangcerah:hoshikara@34.101.221.48/qtdb"
#engine = create_engine(sqlite_url, echo=True)

loc = ("quotes.xlsx")
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)

#Fungsi inisialisasi table dan data
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_tags():
    with Session(engine) as session:
        check = session.exec(select(dbmod.Tag)).first()
        if check != None:
            return
        friends = dbmod.Tag(tag="friends")
        family = dbmod.Tag(tag="family")
        works = dbmod.Tag(tag="works")
        school = dbmod.Tag(tag="school")
        someone = dbmod.Tag(tag="someone gone")
        lonely = dbmod.Tag(tag="lonely")
        failure = dbmod.Tag(tag="failure")
        hollow = dbmod.Tag(tag="hollow")
        session.add(friends)
        session.add(family)
        session.add(works)
        session.add(family)
        session.add(school)
        session.add(someone)
        session.add(lonely)
        session.add(failure)
        session.add(hollow)
        session.commit()
        session.refresh(friends)
        session.refresh(family)
        session.refresh(works)
        session.refresh(family)
        session.refresh(school)
        session.refresh(someone)
        session.refresh(lonely)
        session.refresh(failure)
        session.refresh(hollow)

def make_quotes():
    with Session(engine) as session:
        check = session.exec(select(dbmod.Quote)).first()
        if check != None:
            return
        for i in range(sheet.nrows):
            q = sheet.cell_value(i, 0)
            c = sheet.cell_value(i, 1)
            qm = dbmod.Quote(quote_text=q, category=c)
            taglist = []
            qt = [int(sheet.cell_value(i, 2))]
            for i, q in enumerate(qt):
                taglist.append(session.get(dbmod.Tag, q))
                qm.tags.append(taglist[i])
            session.add(qm)
            session.commit()
            session.refresh(qm)

def create_activities():
    with Session(engine) as session:
        check = session.exec(select(dbmod.Activity)).first()
        if check != None:
            return
        acs = ['read books', 'hangout', 'meditate', 'sports', 'listen to music']
        for ac in acs:
            activ = dbmod.Activity(activity=ac)
            session.add(activ)
            session.commit()
            session.refresh(activ)