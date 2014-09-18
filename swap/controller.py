def mk_query(query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor

def fetch_all(query):
    cursor = mk_query(query)
    return cursor.fetchall()

def fetch_one(query):
    cursor = mk_query(query)
    return cursor.fetchone()

def mk_insert(relation, *values):
    insert = 'INSERT INTO %s VALUES(' % relation
    for value in values:
        insert += '%s, ' % value
    insert = '%s);\n' % query[:-2]
    return insert

def mk_transaction(*queries):
    transaction = 'START TRANSACTION;\n'
    for query in queries:
        transaction += query
    transaction += 'COMMIT;\n'
    return transaction

def mk_read(*queries):
    transaction = 'SET TRANSACTION READ ONLY;\n'
    return transaction + mk_transaction(*queries)

def mk_write(*queries):
    transaction = 'SET TRANSACTION READ WRITE;\n'
    return transaction + mk_transaction(*queries)

def add_professional(user_login, resume_pdf,
                    current_job, current_org):
    values = [user_login, resume_pdf,
             current_job, current_org]
    return mk_insert('professionals', *values)

def add_password(user_login, password, question, answer):
    values = [user_login, password, question, answer]
    return mk_insert('passwords', *values)

def add_user(login, pk_id, name, email, phone):
    values = [login, pk_id, name, email, phone]
    return mk_insert('users', *values)

def add_investor(user_login, is_enterprise):
    values = [user_login, is_enterprise]
    return mk_insert('investors', *values)

def add_legals(pk_id, name, user_login):
    values = [pk_id, name, user_login]
    return mk_insert('legals', *values)

def add_contact(user_login, link, name):
    values = [user_login, link, name]
    return mk_insert('contacts', *values)

def add_follow(follower_login, following_login):
    values = [follower_login, following_login]
    return mk_insert('follows', *values)

def add_transaction(pk_id, created_at, passive_login,
                   active_login, solved_request, sold_request):
    values = [pk_id, created_at, passive_login,
             active_login, solved_request, sold_request]
    return mk_insert('transactions', *values)

def add_typeval(pk_id, name, description, offerant_login):
    values = [pk_id, name, description, offerant_login]
    return mk_insert('passwords', *values)

def add_location(user_login, country, city, department,
                gmt, address, zip_code):
    values = [user_login, country, city, department,
             gmt, address, zip_code]
    return mk_insert('locations', *values)

def add_comment(pk_id, content, created_at, news_title,
                news_taken_from, user_login):
    values = [pk_id, content, created_at, news_title,
             news_taken_from, user_login]
    return mk_insert('comments', *values)

def add_payment(user_login, money):
    values = [user_login, money]
    return mk_insert('payments', *values)

def add_typerent(pk_id, name, description, function,
                 length, rent_type, offerant_login):
    values = [pk_id, name, description, function,
             length, rent_type, offerant_login]
    return mk_insert('typerents', *values)

def add_active(user_login, passive_register):
    values = [user_login, passive_register]
    return mk_insert('actives', *values)

def add_val(pk_id, typeval, amount, price,
           active_login, typerent):
    values = [pk_id, typeval, amount, price,
             active_login, typerent]
    return mk_insert('vals', *values)

def add_new(title, content, media, taken_from, created_at):
    values = [title, content, media, taken_from, created_at]
    return mk_insert('news', *values)

def add_solicitude(pk_id, solicitude_type, amount,
                  created_at, total, min_price, bought,
                  value, active_login, passive_login):
    values = [pk_id, solicitude_type, amount,
             created_at, total, min_price, bought,
             value, active_login, passive_login]
    return mk_insert('solicitudes', *values)

def add_offerants(user_login, offerant_type):
    values = [user_login, offerant_type]
    return mk_insert('offerants', *values)

def add_passive(register, user_login):
    values = [register, user_login]
    return mk_insert('passives', *values)

def add_profile(user_login, status, biography, avatar,
               currency, age, last_active):
    values = [user_login, status, biography, avatar,
             currency, age, last_active]
    return mk_insert('profiles', *values)
