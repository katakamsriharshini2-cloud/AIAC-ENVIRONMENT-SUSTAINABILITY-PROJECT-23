import sys
sys.path.insert(0, 'backend')
from app.database import SessionLocal
from app.models import User
from app.auth import verify_password

db = SessionLocal()
accounts = [
    ('admin@ecosphere.org',   'Admin@123456'),
    ('officer@ecosphere.org', 'Officer@123456'),
    ('citizen@ecosphere.org', 'Citizen@123456'),
]
print('=== DATABASE USER VERIFICATION ===')
all_ok = True
for email, pw in accounts:
    u = db.query(User).filter(User.email == email).first()
    if u:
        ok = verify_password(pw, u.hashed_password)
        status = 'CORRECT' if ok else 'WRONG'
        if not ok:
            all_ok = False
        print(f'  {email}')
        print(f'    Role     : {u.role}')
        print(f'    Active   : {u.is_active}')
        print(f'    Password : {status}')
    else:
        all_ok = False
        print(f'  {email}: NOT FOUND IN DB')
db.close()
print('')
if all_ok:
    print('RESULT: All 3 users verified - logins will work once backend is running.')
else:
    print('RESULT: Issues found above - need fixing.')
