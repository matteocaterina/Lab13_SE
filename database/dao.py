from database.DB_connect import DBConnect
from model.gene import Gene


class DAO:

    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_geni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM gene """

        cursor.execute(query)

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_cromosomi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT cromosoma FROM gene WHERE cromosoma > 0 """

        cursor.execute(query)

        for row in cursor:
            result.append(row['cromosoma'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_geni_connessi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT g1.id as gene1, g2.id as gene2, i.correlazione
                    FROM gene g1, gene g2, interazione i
                    WHERE g1.id = i.id_gene1 AND g2.id = i.id_gene2 
                            AND g1.cromosoma != g2.cromosoma
                            AND g1.cromosoma > 0 
                            and g2.cromosoma > 0
                    GROUP BY g1.id, g2.id"""

        cursor.execute(query)

        for row in cursor:
            result.append((row['gene1'], row['gene2'], row['correlazione']))

        cursor.close()
        conn.close()
        return result

