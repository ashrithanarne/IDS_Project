The SQLite database (humanitarian.db) is generated locally and is not stored in the repository. This approach ensures that all collaborators can reproduce the database from raw data rather than relying on a static file.

To generate the database:

- Clone the repository.

- Ensure all required CSV files are located in data/raw/.

- Execute the data loading notebook or script.

The database file will be created automatically in the project directory.

The database schema is defined in sql/schema.sql and executed programmatically during setup. Because both the schema and loading logic are version-controlled, the database can be recreated consistently across environments.

To connect manually:

import sqlite3
conn = sqlite3.connect("humanitarian.db")