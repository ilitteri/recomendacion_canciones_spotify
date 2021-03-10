class Queue:
    def __init__(self):
        self.data = []
        self.count = 0
        
    def enqueue(self, dato):
        self.data.append(dato)
        self.count += 1

    def dequeue(self):
        self.count -= 1
        dato = self.data.pop(0)
        return dato

    def esta_vacia(self):
        return self.count == 0