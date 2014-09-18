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
        except:
            print 'ERROR CREATING %s' % name
            continue
    print 'DONE :D'

header, classes = get_classes_and_header()
make_models(header, classes)
