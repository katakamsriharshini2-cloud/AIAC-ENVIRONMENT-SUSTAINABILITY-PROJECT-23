"""
Seed realistic Warangal/Telangana biodiversity records into the SQLite database.
Run from project root: python seed_biodiversity.py
Actual columns: id, species_name, scientific_name, category, observation_date,
                location_name, latitude, longitude, basis_of_record,
                conservation_status, country, state, city, data_type, source_name, source_url
"""
import sys, os, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import BiodiversityRecord

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'ecosphere.db')
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
db = Session()

# Clear and re-seed
db.query(BiodiversityRecord).delete()
db.commit()

def bio(sn, cn, cat, cs, obs, loc, lat, lon, bor, src, city="Warangal"):
    return BiodiversityRecord(
        scientific_name=sn, species_name=cn, category=cat,
        conservation_status=cs, observation_date=datetime.date.fromisoformat(obs),
        location_name=loc, latitude=lat, longitude=lon,
        basis_of_record=bor, data_type="GBIF_OCCURRENCE",
        source_name=src, source_url="https://gbif.org",
        country="India", state="Telangana", city=city
    )

records = [
    # AVES
    bio("Pavo cristatus","Indian Peafowl","AVES","Least Concern (LC)",
        "2026-08-14","Pakhal Wildlife Sanctuary, Warangal",17.9520,79.9810,
        "HUMAN_OBSERVATION","Telangana Forest Department"),
    bio("Gyps bengalensis","White-rumped Vulture","AVES","Critically Endangered (CR)",
        "2026-03-10","Palampet Eco-Sensitive Belt, Warangal",18.2610,79.9410,
        "HUMAN_OBSERVATION","BNHS India"),
    bio("Coracias benghalensis","Indian Roller","AVES","Least Concern (LC)",
        "2026-06-25","Ramappa Lake Buffer Zone, Mulugu",18.2560,79.9500,
        "HUMAN_OBSERVATION","eBird India","Mulugu"),
    bio("Mycteria leucocephala","Painted Stork","AVES","Near Threatened (NT)",
        "2026-11-02","Bhadrakali Tank, Hanamkonda",17.9780,79.5690,
        "HUMAN_OBSERVATION","WWF India","Hanamkonda"),
    bio("Threskiornis melanocephalus","Black-headed Ibis","AVES","Near Threatened (NT)",
        "2026-10-15","Waddepally Reservoir, Warangal",17.9950,79.5520,
        "HUMAN_OBSERVATION","Telangana Forest Dept."),

    # MAMMALIA
    bio("Panthera pardus fusca","Indian Leopard","MAMMALIA","Vulnerable (VU)",
        "2026-05-22","Eturnagaram Wildlife Sanctuary",18.3240,80.4280,
        "MACHINE_OBSERVATION (Camera Trap)","NTCA Camera Grid","Eturnagaram"),
    bio("Axis axis","Chital / Spotted Deer","MAMMALIA","Least Concern (LC)",
        "2026-07-08","Pakhal Lake Peripheral Zone",17.9560,79.9880,
        "HUMAN_OBSERVATION","Telangana Forest Dept."),
    bio("Loris lydekkerianus","Gray Slender Loris","MAMMALIA","Near Threatened (NT)",
        "2026-04-18","Kakatiya University Eco-Zone, Warangal",18.0190,79.5520,
        "PRESERVED_SPECIMEN","Zoological Survey of India"),
    bio("Sus scrofa cristatus","Indian Wild Boar","MAMMALIA","Least Concern (LC)",
        "2026-09-03","Eturnagaram Wildlife Sanctuary Buffer",18.3360,80.4440,
        "MACHINE_OBSERVATION (Camera Trap)","NTCA Camera Grid","Eturnagaram"),

    # PLANTAE
    bio("Tectona grandis","Teak Tree","PLANTAE","Least Concern (LC)",
        "2026-02-20","Eturnagaram Reserved Forest",18.3100,80.4150,
        "PRESERVED_SPECIMEN","Forest Survey of India","Eturnagaram"),
    bio("Azadirachta indica","Neem Tree","PLANTAE","Least Concern (LC)",
        "2026-09-02","Kakatiya University Botanical Reserve",18.0190,79.5520,
        "PRESERVED_SPECIMEN","Botanical Survey of India"),
    bio("Phyllanthus emblica","Indian Gooseberry (Amla)","PLANTAE","Least Concern (LC)",
        "2026-01-15","Ramappa Eco-Park Plantation",18.2560,79.9550,
        "HUMAN_OBSERVATION","Botanical Survey of India","Mulugu"),
    bio("Butea monosperma","Flame of the Forest (Palash)","PLANTAE","Least Concern (LC)",
        "2026-03-05","Warangal Fort Heritage Grove",17.9700,79.5890,
        "HUMAN_OBSERVATION","Telangana Horticulture Dept."),

    # REPTILIA
    bio("Naja naja","Spectacled Indian Cobra","REPTILIA","Least Concern (LC)",
        "2026-08-30","Bhadrakali Tank Bund Buffer Zone",17.9780,79.5690,
        "HUMAN_OBSERVATION","Telangana Forest Dept.","Hanamkonda"),
    bio("Varanus bengalensis","Bengal Monitor Lizard","REPTILIA","Least Concern (LC)",
        "2026-06-12","Pakhal Wildlife Sanctuary Shore",17.9530,79.9800,
        "HUMAN_OBSERVATION","Herpetological Society of India"),
    bio("Calotes versicolor","Oriental Garden Lizard","REPTILIA","Least Concern (LC)",
        "2026-07-20","Kakatiya University Campus, Warangal",18.0210,79.5530,
        "HUMAN_OBSERVATION","iNaturalist India"),

    # PISCES
    bio("Channa striata","Striped Snakehead (Murrel)","PISCES","Least Concern (LC)",
        "2026-07-19","Waddepally Lake Littoral Zone",17.9950,79.5520,
        "HUMAN_OBSERVATION","Zoological Survey of India"),
    bio("Tor tor","Mahseer (Golden Mahseer)","PISCES","Vulnerable (VU)",
        "2026-02-28","Musi River Tributary, Nalgonda Border",17.5610,79.2300,
        "HUMAN_OBSERVATION","WWF India Freshwater Programme","Nalgonda"),
    bio("Labeo rohita","Rohu Carp","PISCES","Least Concern (LC)",
        "2026-05-10","Pakhal Reservoir Main Basin",17.9520,79.9810,
        "HUMAN_OBSERVATION","Telangana Fisheries Dept."),
    bio("Anabas testudineus","Climbing Perch","PISCES","Least Concern (LC)",
        "2026-08-05","Ramappa Lake Wetland Margin",18.2590,79.9490,
        "HUMAN_OBSERVATION","Zoological Survey of India","Mulugu"),
]

for rec in records:
    db.add(rec)

db.commit()
db.close()
print(f"Seeded {len(records)} biodiversity records into {DB_PATH}")
