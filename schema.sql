CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);

CREATE TABLE actions (
	id SERIAL PRIMARY KEY,
	name TEXT UNIQUE,
	category TEXT, 
	free BOOLEAN, 
	lowcost BOOLEAN,
	highcost BOOLEAN
);

CREATE TABLE effects (
	id SERIAL PRIMARY KEY,
        action_name TEXT,
	creator_id INT REFERENCES users(id),	
	low BOOLEAN,
	neutral BOOLEAN, 
	high BOOLEAN,	
	sent_at TIMESTAMP
);

CREATE TABLE private_actions (
	id SERIAL PRIMARY KEY,
        creator_id INT REFERENCES users(id),
	name TEXT,
	category TEXT,
	free BOOLEAN,
	lowcost BOOLEAN,
	highcost BOOLEAN 
);

CREATE TABLE supervisors (
	id SERIAL PRIMARY KEY,
	username TEXT UNIQUE,
	password TEXT
);
	
CREATE TABLE moods (
	id SERIAL PRIMARY KEY,
	feeling INT,
	user_id INT,
	sent_at TIMESTAMP
);
