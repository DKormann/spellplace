import readline
import sys
import time
import pickle


last_time = time.time()
timestep = 1

def update():
    new_time = time.time()
    global last_time
    delta = new_time - last_time
    if delta > timestep:
        steps = int(delta/timestep)
        last_time += steps*timestep
        forward(steps)

def forward(steps):
    for p in world.players.values():
        p.update(steps)

class Player:
    def __init__(self, name, key,  node, world):
        self.key = key
        self.world = world
        self.name = name
        world.players[self.name] = self
        self.energy = 0
        self.max_energy = 1000
        self.energy_regen = 20
        self.max_hp = 1000
        self.hp = self.max_hp
        self.position = node
        node.players[self.name] = self

    def update(self,steps):
        self.energy = min(self.max_energy, self.energy +  self.energy_regen* steps)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.position.players.pop(self.name)
            self.position = None
            self.energy = 0
            self.energy_regen = 0
            self.max_energy = 0

    def status(self):
        Nhp = self.hp/self.max_hp 

        segments = 20
        hp_bar = "["+"="*int(Nhp*segments)+"_"*int(segments-Nhp*segments+0.99)+"]"

        Nen = self.energy/self.max_energy
        energy_bar = "["+"="*int(Nen*segments)+"_"*int(segments-Nen*segments+0.99)+"]"
        return "\nstatus of player: "+self.name+"\n\nhp:\t" + hp_bar + "\nenergy:\t"  + energy_bar

    def __str__(self):
        return "[p] "+self.name

def execute(self,words):

    ret = ""

    try:
        func = command_table[words[0]]

        ret = func(self,words[1:])

    except Exception as e:
        return str(e)

        try:
            n = int(words[0])
            for i in range(n):
                ret += execute(self, words[1:])
        except Exception as e :
            return str(e)
    return ret


class Node:
    
    def __init__(self, name, parent = None, master = None):
        self.master = master

        self.name = name
        self.neighbors = dict()
        if parent!=None:
            self.neighbors [parent.name] = parent
        self.players = {}

    def get_name(self):
        return self.name
    
    def __str__(self):
        return '[n] '+self.name

def cast_hit(self,args):
    if args == []:
        return 
    for target in args:
        target_player = self.position.players[target]
        if self.energy > 20:
            self.energy -=20
            target_player.take_damage(5)
                

def rename_node(self,args):
    if args == []:
        print('error need name')
        return
    new_name = args [0]
    if self.position.name == "~":
        print('cant name root')
        return 
    if self.position.master == self:
        for neighbor in self.position.neighbors.values():
            neighbor.neighbors.pop(self.position.name)
            neighbor.neighbors[new_name] = self.position
        self.position.name = new_name

def make_nodes(self, names):
    for name in names:
        if name == "~":
            print("cant make root name node")
            return 
        if name == self.position.name:
            return 
        new_node = Node(name,parent = self.position, master = self)
        self.position.neighbors[name] = new_node

def link_node(self, path):
    node = get_node_from_path(self, path)
    if node.name == self.position.name:
        return 'cant link nodes of same name'
    node.neighbors[self.position.name] = self.position
    self.position.neighbors[node.name] = node
    
def remove_link(self, path):
    if self.position.master == self:
        for name in path:
            node = self.position.neighbors[name]
            node.neighbors.pop(self.position.name)
            self.position.neighbors.pop(name)
    

def list_node(self, path):
    ret =""
    node = get_node_from_path(self,path)
    print()

    for el in node.neighbors:
        ret += (str(node.neighbors[el]))
    ret +='\n'
    for el in node.players:
        ret += str(node.players[el])
    ret+='\n'
    return ret

def get_node_from_path(self,path):
    node = self.position
    for name in path:
        try:
            node = node.neighbors[name]
        except:
            print(node,'has no neighbor',name)
            return None
    return node

def go_to_node(self, path):

    node = get_node_from_path(self, path)

    self.position.players.pop(self.name)
    self.position = node
    node.players[self.name] = self

command_table = {
        'p': lambda self, args: self.position.get_name(),
        'mk': make_nodes,
        'l': list_node,
        'go': go_to_node,
        'status': lambda self, args: print_status(self,args),
        'hit': cast_hit,
        'rename': rename_node,
        'link': link_node,
        'cut': remove_link,
        }


def print_status(self,args):
    if args == []:
        return  self.status()
    ret = ''
    for target in args:
        try:
            player = self.position.players[target]
            ret += player.status()+'\n'
        except:
            pass
    return ret
            

class World():
    def __init__(self):
        self.players = {}
        self.root = Node('~')
        kuro = Player("kuro", 'wasabi',  self.root, self)
        shino = Player("shino", 'wasabi',  self.root, self)

    def load(filepath = 'file'):
        try:
            file = open(filepath,"rb")
            new_world = pickle.load(file)
            file.close()
        except Exception as e:
            print('cant load world from memory')
            print(e)
            new_world = World()
        return new_world

    def save(self,filepath = 'file'):
        file = open (filepath, "wb")

        pickle.dump(self,file)

        file.close()

def complete(self, text, state):
    if state == 0:
        words = text.split()
        if len(words) == 1:
            for command in command_table.keys():
                if command.startswith(words[0]):
                    return command
    node = get_node_from_path(self,words[1:-1])
    for neighbor in node.neighbors:
        if neighbor.name.startswith(words[-1]):
            res = ""
            for word in words [:-1]:
                res += word
            res += neighbor.name
            return res


def play(self):

    readline.set_completer(lambda text, state: complete(self,text,state))
    readline.parse_and_bind('tab: complete')
    commands = input('\t'+self.position.name+ ' ').split(';')

    while(commands != ['\\c']):
        update()

        for command in commands:

            if command == '\\c':
                return
            
            words = command.split()

            execute(self, words)

            if self.hp <= 0:
                print('you died')
                return
        commands = input('\t'+self.position.name+ ' ').split(';')
    world.save()


def parse_remote_input(msg):
    response = ""
    words = msg.split()
    flag = words[0]
    name = words[1]
    if flag == "enter":
        if name in world.players :
            return "exists"
        else :
            return "newplayer"
    if flag == "authenticate":
        player = world.players[name]
        key = words[2]
        if player.key == key:
            return "authenticated"
        else:
            return "denied"
    if flag == "create":
        key = words [2]
        player = Player(name, key, world.root, world)
        return "created"
    if flag == "command":
        key = words[2]
        command = words[3:]
        player = world.players[name]
        if player.key == key:
            response = execute(player, command)
    return response



world = World.load()
if __name__ == "__main__":
    name = input("what is your name? ")
    try:
        player = world.players[name]
    except:
        res = input('player',name,'doesnt exist. create new?')
        if res in ['y','yes'] :
            player = Player(name,world.root, world)
    play(player)


def __getattr__(name):
    return world.players[name]

