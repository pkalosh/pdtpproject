PHD_DEGREE='PHD DEGREE'
MASTERS_DEGREE='MASTERS DEGREE'
BACHELORS_DEGREE='BACHELORS DEGREE'
HIGHER_DIPLOMA='HIGHER DIPLOMA'
DIPLOMA='DIPLOMA'
CERTIFICATE='CERTIFICATE'
OTHERS='OTHERS'

ACADEMIC_QUALIFICATIONS=(
	(PHD_DEGREE,"PHD DEGREE"),
	(MASTERS_DEGREE,"MASTERS DEGREE"),
	(BACHELORS_DEGREE,"BACHELORS DEGREE"),
(HIGHER_DIPLOMA,"HIGHER DIPLOMA"),(DIPLOMA,"DIPLOMA"),
(CERTIFICATE,"CERTIFICATE"),
(OTHERS,"OTHERS"))


MALE='MALE'
FEMALE='FEMALE'
GENDER=((MALE,"MALE"),(FEMALE,"FEMALE"))

SINGLE='SINGLE'
MARRIED='MARRIED'
MARITAL_STATUS=((SINGLE,"SINGLE"),(MARRIED,'MARRIED'))


SECTOR_CHOICES = ((True, 'Private'), (False, 'Public'))

PDTPS='PDTPS'
MENTORS='MENTORS'
SUPERVISORS='SUPERVISORS'
CONTACT_PERSONS='CONTACT PERSONS'
ALL='ALL'
ATTENDEES = ((PDTPS,'PDTPS'), (MENTORS,'MENTORS'),(SUPERVISORS,'SUPERVISORS'),(CONTACT_PERSONS,'CONTACT PERSONS'),
	(ALL,'ALL'
))
RECIEVED='RECIEVED'
ESCALATE='ESCALATE'
SOLVED='SOLVED'
ISSUE_STATUS = ((RECIEVED,'RECIEVED'),(ESCALATE,'ESCALATE'), (SOLVED,'SOLVED'))

Development_Database = 'Development-Database'
Development_Java = 'Development-Java'
Development_Design = 'Development-Design'
Networking_Dialup = 'Networking-Dialup'
Networking_WAN = 'Networking-WAN'
Networking_LAN = 'Networking-LAN'
Server_Backup_storage_service = 'Server-Backup and storage service'
Server_Network_Management = 'Server-Network Management'
Servers_Application = 'Servers-Application'
SKILLS = (
	(Development_Database,'Development-Database'),(Development_Java,'Development-Java'),
	(Development_Design,'Development-Design'),(Networking_Dialup,'Networking-Dialup'),
	(Networking_WAN,'Networking-WAN'),(Networking_LAN,'Networking-LAN'),
	(Server_Backup_storage_service,'Server-Backup and storage service'),(Server_Network_Management,'Server-Network Management'),
	(Servers_Application,'Server-Application'))


Advanced = 'Advanced'
Intermediate = 'Intermediate'
Basic = 'Basic'
SKILL_LEVEL = (
	(Advanced,'Advanced'),(Intermediate,'Intermediate'),(Basic,'Basic')
	)