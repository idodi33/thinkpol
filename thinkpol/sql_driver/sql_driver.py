from sqlalchemy import *


class DataBase:
	def __init__(self, url):
		print("Initializing database")
		self.engine = create_engine(url,pool_size=10,
                                      max_overflow=2,
                                      pool_recycle=300,
                                      pool_pre_ping=True)
		self.metadata = MetaData()
		self.users = Table('users', self.metadata,
			Column('user_id', Integer, primary_key=True),
			Column('username', String(255), nullable=False),
			Column('birthday', Float, nullable=False),
			Column('gender', String(1), nullable=False)
			)
		self.snapshots = Table('snapshots', self.metadata,
			Column('id', Integer, primary_key=True),
			Column('parent_user_id', None, ForeignKey('users.user_id'), nullable=False),
			Column('datetime', Float(64)),
			Column('color_image', String(255)),
			Column('depth_image', String(255)),
			Column('translation_x', Float(64)),
			Column('translation_y', Float(64)),
			Column('translation_z', Float(64)),
			Column('rotation_x', Float(64)),
			Column('rotation_y', Float(64)),
			Column('rotation_z', Float(64)),
			Column('rotation_w', Float(64)),
			Column('happiness', Float),
			Column('exhaustion', Float),
			Column('hunger', Float),
			Column('thirst', Float)
			)
		self.metadata.create_all(self.engine)
		print("Created tables")
		self.connection = self.engine.connect()
		print("Connected engine")


	def save(self, field, data):
		'''
		Gets a json with data from parser and saves it into the database.
		'''
		insert = self.users.insert(user_id=data['user_id'],
			username=data['username'],
			birthday=data['birthday'],
			gender=data['gender']
			)
		self.connection.execute(insert)
		if field == "color_image":
			insert = self.snapshots.insert(
				datetime=data['datetime'],
				color_image=data['color_image']
				)
		elif field == "depth_image":
			insert = self.snapshots.insert(
				datetime=data['datetime'],
				depth_image=data['depth_image']
				)
		elif field == "pose":
			insert = self.snapshots.insert(
				datetime=data['datetime'],
				translation_x=data['translation_x'],
				translation_y=data['translation_y'],
				translation_z=data['translation_z'],
				rotation_x=data['rotation_x'],
				rotation_y=data['rotation_y'],
				rotation_z=data['rotation_z'],
				rotation_w=data['rotation_w']
				)
		elif field == "feelings":
			insert = self.snapshots.insert(
				datetime=data['datetime'],
				happiness=data['happiness'],
				exhaustion=data['exhaustion'],
				hunger=data['hunger'],
				thirst=data['thirst']
				)
		else:
			raise ValueError("Error in postgresql_driver: Invalid field")
		self.connection.execute(insert)


