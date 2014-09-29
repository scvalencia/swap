import os

def is_valid_class(vals):
    if len(vals) > 1:
        return vals[0] == 'class' and vals[1] != 'Meta:'
    else:
        return False

def add_class(classes, class_block):
    name_start = class_block.find(' ')
    name_end = class_block.find('(')
    class_name = class_block[name_start:name_end].split()[0].lower()
    classes[class_name] = class_block[:-2]

def fix_inspect_db():
    old_path = os.path.join(os.getcwd(), 'old_models.py')
    new_path = os.path.join(os.getcwd(), 'models.py')
    old_models = open(old_path, 'r')
    new_models = open(new_path, 'w')
    class_name = ''
    for line in old_models:
        if line.find('class') != -1:
            end_name = line.find(')')
            class_name = line.split()[1][:end_name].lower()
        if line.find('ForeignKey') != -1:
            line = fix_foreign(line, class_name)
        new_models.write(line)
    new_models.write('\n')
    old_models.close()
    new_models.close()

def fix_foreign(line, class_name):
    start_model = line.find('(') + 1
    end_line = line.find(',', start_model)
    if end_line == -1: end_line = line.find(')', start_model)
    model_name = line[start_model:end_line]
    if model_name.find('\'') != -1: model_name = model_name[1:-1]
    first_part_line = line[:start_model]
    change_part_line = '\'%s.%s\'' % (model_name.lower(), model_name)
    second_part_line = line[end_line:]
    line = first_part_line + change_part_line + second_part_line
    related_name = line.split('=')[0].split()[0]
    end_line = line.find(')')
    first_part_line = line[:end_line]
    change_part_line = ', related_name=\'%s_%s\'' % (class_name, related_name)
    second_part_line = line[end_line:]
    return first_part_line + change_part_line + second_part_line

def get_classes_and_header():
    classes = {}
    path = os.path.join(os.getcwd(), 'models.py')
    in_file = open(path, 'r')
    class_block = ''
    got_header = False
    header = ''
    for line in in_file:
        vals = line.split()
        if is_valid_class(vals):
            if got_header is False:
                header = class_block
                got_header = True
            else:
                add_class(classes, class_block)
            class_block = ''
        class_block += line
    add_class(classes, class_block)
    in_file.close()
    return header, classes

def make_models(header, classes):
    for name in classes:
        os.system('python manage.py startapp %s' % name)
        try:
            output = header + classes[name]
            path = os.path.join(os.getcwd(), '%s/models.py' % name)
            model_file = open(path, 'w')
            model_file.write(output)
            model_file.close()
        except:
            print 'ERROR CREATING MODEL %s' % name
            continue
    print 'DONE MAKE MODELS!'

def make_admins(classes):
    import_admin = 'from django.contrib import admin\n'
    for name in classes:
        try:
            model_name = name.capitalize()
            import_model = 'from models import %s\n\n' % model_name
            register = 'admin.site.register(%s)' % model_name
            output = import_admin + import_model + register
            path = os.path.join(os.getcwd(), '%s/admin.py' % name)
            model_file = open(path, 'w')
            model_file.write(output)
            model_file.close()
        except:
            print 'ERROR CREATING ADMIN %s' % name
            continue
    print 'DONE MAKE ADMINS!'

def make_inspect_db():
    os.system('python manage.py inspectdb > old_models.py')
    print 'DONE INSPECTDB!'

def make_sync_db():
    os.system('python manage.py syncdb')
    print 'DONE SYNCDB'

make_inspect_db()
fix_inspect_db()
header, classes = get_classes_and_header()
make_models(header, classes)
make_admins(classes)
make_sync_db()
