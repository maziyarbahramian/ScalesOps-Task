import psycopg2


def create_connection():
    connection = psycopg2.connect(dbname='scalesops',
                                  user='postgres',
                                  password='postgres',
                                  host='localhost',
                                  port='5432')
    cursor = connection.cursor()
    return connection, cursor


def create_images_table():
    try:
        connection, cursor = create_connection()
        try:
            cursor.execute("create table if not exists images( \
                            id    serial primary key, \
                            image bytea)")
        except(Exception, psycopg2.Error) as error:
            print("Error while creating image table", error)
        finally:
            connection.commit()
            connection.close()
    finally:
        pass


def insert_image(image):
    try:
        connection, cursor = create_connection()
        try:
            query = f'INSERT INTO images (image) VALUES({psycopg2.Binary(image)})'
            cursor.execute(query)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while inserting data in image table", error)
        finally:
            cursor.close()
            connection.close()
    finally:
        pass


create_images_table()
