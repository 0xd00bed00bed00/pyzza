class ModelType:
    CONTAINER = 'CONTAINER'
    IMAGE = 'IMAGE'
    VOLUME = 'VOLUME'
    NETWORK = 'NETWORK'

class FileInfo:
    name=None
    owner=None
    group=None
    size=None
    created=None
    permissions=None
    
    def __init__(self, line: str=None, name=None, owner=None, group=None, size=None, created=None, permissions=None):
        self.name=name
        self.owner=owner
        self.group=group
        self.size=size
        self.created=created
        self.permissions=permissions
        if line is not None:
            props=line.split(' ')
            if len(props)==9:
                self.name = props[8]
                self.owner = props[2]
                self.group = props[3]
                self.size = props[4]
                self.created = ' '.join(props[5:7])
                self.permissions = props[8]

    def to_list(self):
        return [
            self.name,
            '',
            self.size,
            self.created,
            self.owner,
            self.group,
            self.permissions,
        ]